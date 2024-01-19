import numpy as np
import re
from math import isclose

from .element import Element
from .material_solver import MaterialSolver
from .. import RowCollector
from ..units import Quantity, Unit

class Compound:
    elements: dict = None
    rho: Quantity = None
    V: Quantity = None
    M: Quantity = None
    n: Quantity = None
    
    @staticmethod
    def from_elements(elements:list):
        compound = Compound()
        for el in elements:
            compound.add_element(el)
        return compound
        
    @staticmethod
    def from_atom(expression:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expression):
            return float(expression)
        else:
            return Compound.from_elements([
                Element(expression),
            ])
            
    def __init__(self, expression:str=None):
        self.elements = {}
        if expression and expression!='':
            with MaterialSolver(Compound.from_atom) as ms:
                compound = ms.solve(expression)
            for expr, el in compound.elements.items():
                self.elements[expr] = el
        self.M = np.sum([e.A for e in self.elements.values()])
        
    def __str__(self):
        elements = []
        for expr, el in self.elements.items():
            element = f"{expr}" 
            if el.count>1:
                element += f"{int(el.count):d}"
            elements.append(element)
        elements = " ".join(elements)
        data = self.data_compound()
        p = int(round(data['Z'][-1]))
        n = data['N'][-1]
        e = int(round(data['e'][-1]))
        A = data['A[Da]'][-1]
        return f"Compound(p={p:d} n={n:.03f} e={e:d} A={A:.03f})"
        
    def __mul__(self, other:float):
        compound = Compound()
        compound.rho = self.rho
        compound.M = self.M
        compound.V = self.V
        compound.n = self.n
        for expr in self.elements.keys():
            el = self.elements[expr] * other
            compound.add_element(el)
        return compound
    
    def __add__(self, other):
        compound = Compound()
        compound.rho = self.rho
        compound.M = self.M
        compound.V = self.V
        compound.n = self.n
        for expr,el in self.elements.items():
            compound.add_element(el)
        if isinstance(other, Compound):
            for expr,el in other.elements.items():
                compound.add_element(el)
        elif isinstance(other, Element):
            compound.add_element(other)
        return compound
    
    def add_element(self, element:Element):
        expr = element.expression
        if self.rho:
            element.set_density(self.n)
        if expr in self.elements:
            self.elements[expr] += element
        else:
            self.elements[expr] = element
        self.M = np.sum([e.A for e in self.elements.values()])
    
    def set_amount(self, rho:Quantity, volume:Quantity=None):
        self.rho = rho
        self.V = volume
        self.n = (rho/self.M).rebase()
        for s in self.elements.keys():
            self.elements[s].set_density(self.n)
            
    def data_elements(self):
        with RowCollector(['expression','element','isotope','ionisation','A[Da]','Z','N','e','A_nuc[Da]','E_bin[MeV]']) as rc:
            for s,e in self.elements.items():
                element    = e.element
                NA, A, Z, N, e, isotope, ionisation = Element.get_isotope(e.element, e.isotope, e.ionisation)
                A_nuc = Quantity(Z, '[m_p]') + Quantity(N, '[m_n]') + Quantity(e, '[m_e]')
                E_bin = ((A_nuc-A)*Unit('[c]')**2)/(Z+N)
                rc.append([
                    s, 
                    element, 
                    f"{isotope:d}", 
                    f"{ionisation:d}", 
                    A.value('Da'), 
                    Z, 
                    N, 
                    e, 
                    A_nuc.value('Da'), 
                    E_bin.value('MeV'),
                ])
            return rc
            
    def data_compound(self, part:list=None):
        if not self.elements:
            return None
        columns = ['A[Da]','Z','N','e']
        if self.rho:
            columns += ['n[cm-3]','rho[g/cm3]','X[%]']
        if self.V:
            columns += ['n_V','M_V[g]']
        with RowCollector(['expression','count']+columns) as rc:
            for s,e in self.elements.items():
                if part and s not in part:
                    continue
                row = [
                    s, 
                    e.count, 
                    e.A.value('Da'), 
                    e.Z, 
                    e.N, 
                    e.e, 
                ]
                if self.rho:
                    row += [
                        e.n.value('cm-3'), 
                        e.rho.value('g/cm3'),
                        (e.rho/self.rho).value('%'),
                    ]
                if self.V:
                    row += [
                        (e.n*self.V).value(),
                        (e.rho*self.V).value('g'),
                    ]
                rc.append(row)
            avg = ['avg', np.average(rc['count'])]
            sum = ['sum', np.sum(rc['count'])]
            for p in columns:
                sum.append(np.sum(rc[p]))
                avg.append(np.average(np.divide(rc[p],rc['count']), weights=rc['count']))
            rc.append(avg)
            rc.append(sum)
            return rc
            
    def print(self):
        print("Properties:\n")
        print("Mass density:", self.rho)
        print("Molecular mass:", self.M)
        print("Molecular density:", self.n)
        print("")
        print("Elements:\n")
        print(self.data_elements().to_dataframe().to_string(index=False))
        print("")
        print("Compound:\n")
        print(self.data_compound().to_dataframe().to_string(index=False))