import numpy as np
import re
from math import isclose
import copy
from typing import Union

from .element import Element
from .molecule_solver import MoleculeSolver
from .. import ParameterTable, RowCollector
from ..units import Quantity, Unit

class Molecule:
    natural: bool
    elements: dict
    total_mass: Quantity   # total molecule mass
    total_count: float     # total number of atoms
    rho: Quantity = None
    V: Quantity = None
    n: Quantity = None
    count: float = None
    expression: str = ''
    
    def atom(self, expression:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expression):
            return float(expression)
        else:
            return Molecule({
                expression: 1,
            }, natural=self.natural)
            
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
            
    def __init__(self, expression:Union[str,dict]=None, natural:bool=True, count:float=1.0):
        self.natural = natural
        self.count = count
        self.elements = {}
        if isinstance(expression,str) and expression:
            self.expression = expression
            with MoleculeSolver(self.atom) as ms:
                molecule = ms.solve(expression)
            for expr, el in molecule.elements.items():
                self.elements[expr] = el
        elif isinstance(expression, dict) and expression:
            for expr, frac in expression.items():
                self.add_element(expr, frac)
        self._set_norms()

    def __str__(self):
        elements = []
        for expr, el in self.elements.items():
            element = f"{expr}" 
            if el.count>1:
                element += f"{int(el.count):d}"
            elements.append(element)
        elements = " ".join(elements)
        data = self.data_molecule(quantity=False)
        p = int(round(data['sum']['Z']))
        n = data['sum']['N']
        e = int(round(data['sum']['e']))
        A = data['sum']['A']
        return f"Molecule(A={A:.03f} Z={p:d} N={n:.03f} e={e:d})"
        
    def __mul__(self, other:float):
        molecule = Molecule(natural=self.natural)
        for expr, element in self.elements.items():
            molecule.add_element(expr, element.count*other)
        return molecule
    
    def __add__(self, other):
        molecule = Molecule(natural=self.natural)
        for expr, element in self.elements.items():
            molecule.add_element(expr, element.count)
        if isinstance(other, Molecule):
            for expr, element in other.elements.items():
                molecule.add_element(expr, element.count)
        elif isinstance(other, Element):
            molecule.add_element(other.expression, other.count)
        return molecule
    
    def _set_norms(self):
        self.total_mass = np.sum([e.A for e in self.elements.values()])
        self.total_count = np.sum([e.count for e in self.elements.values()])
    
    def add_element(self, expression:str, count:float=1.0):
        print(expression)
        self.expression += expression
        if expression in self.elements:
            self.elements[expression].count += count
        else:
            self.elements[expression] = Element(expression, natural=self.natural, count=count)
            if self.rho:
                self.elements[expression].set_density(self.n)
        self._set_norms()

    def set_amount(self, rho:Quantity, V:Quantity=None):
        self.rho = rho
        self.n = (rho/self.total_mass).rebase()
        for s in self.elements.keys():
            self.elements[s].set_density(self.n)
        self.V = V
            
    def data_elements(self, quantity=True):
        with ParameterTable(['element','isotope','ionisation','A','Z','N','e'], #,'A_nuc','E_bin'], 
                keys=True, keyname='expression') as pt:
            for s,e in self.elements.items():
                el = Element(s, natural=self.natural)
                pt[s] = [
                    el.element, 
                    el.isotope, 
                    el.ionisation, 
                    el.A.to('Da') if quantity else el.A.value('Da'), 
                    el.Z, 
                    el.N, 
                    el.e, 
                ]
            return pt
            
    def data_molecule(self, part:list=None, quantity=True):
        if not self.elements:
            return None
        columns = ['A','Z','N','e','x','X']
        if self.rho:
            columns += ['n','rho']
        if self.V:
            columns += ['n_V','M_V']
        with ParameterTable(['count']+columns, keys=True, keyname='expression') as pt:
            rc = RowCollector(['count']+columns)
            for s,e in self.elements.items():
                if part and s not in part:
                    continue
                row = [
                    e.count, 
                    e.A.to('Da') if quantity else e.A.value('Da'), 
                    e.Z, 
                    e.N, 
                    e.e, 
                    Quantity(100*e.count/self.total_count, '%') if quantity else 100*e.count/self.total_count,
                    (e.A/self.total_mass).to('%') if quantity else (e.A/self.total_mass).value('%'),
                ]
                if self.rho:
                    row += [
                        e.n.to('cm-3') if quantity else e.n.value('cm-3'), 
                        e.rho.to('g/cm3') if quantity else e.rho.value('g/cm3'),
                    ]
                if self.V:
                    row += [
                        (e.n*self.V).value(),
                        (e.rho*self.V).to('g') if quantity else (e.rho*self.V).value('g'),
                    ]
                pt[s] = row
                rc.append(row)
            avg = [np.average(rc['count'])]
            sum = [np.sum(rc['count'])]
            for p in columns:
                sum.append(np.sum(rc[p]))
                avg.append(np.average(np.divide(rc[p],rc['count']), weights=rc['count']))
            pt['avg'] = avg
            pt['sum'] = sum
            return pt
    
    def print_elements(self):
        df = self.data_elements(quantity=False).to_dataframe()
        df = df.rename(columns={"A": "A[Da]", "A_nuc": "A_nuc[Da]", "E_bin": "E_bin[MeV]"})
        print( df.to_string(index=False) )

    def print_molecule(self, part:list=None):
        df = self.data_molecule(part=part, quantity=False).to_dataframe()
        columns = {"A": "A[Da]", "x": "x[%]", "X": "X[%]"}
        if self.rho:
            columns.update({"n": "n[cm-3]", "rho": "rho[g/cm3]"})
        if self.V:
            columns.update({"M_V": "M_V[g]"})
        df = df.rename(columns=columns)
        print( df.to_string(index=False) )
        
    def print(self):
        print("Properties:")
        print()
        print(f"Molecular mass: {self.total_mass}")
        if self.rho:
            print(f"Mass density: {self.rho}")
            print(f"Molecular density: {self.n}")
        if self.V:
            print(f"Volume: {self.V}")
        print("")
        print("Elements:")
        print("")
        self.print_elements()
        print("")
        print("Molecule:")
        print("")
        self.print_molecule()