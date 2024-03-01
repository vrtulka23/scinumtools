import numpy as np
import re
from typing import Union

from . import FracType
from .molecule import Molecule
from .mixture_solver import MixtureSolver
from ..units import Quantity, Unit
from .. import ParameterTable, RowCollector

class Mixture:
    
    natural: bool
    molecules: dict
    total_mass: Quantity
    total_count: float
    expression: str = ''
    rho: Quantity = None
    fractype: FracType = None

    def atom(self, expression:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expression):
            return float(expression)
        else:
            return Mixture({
                expression: 1.0
            }, natural=self.natural, fractype=self.fractype)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
            
    def __init__(self, expression:Union[str,dict]=None, natural:bool=True, fractype:FracType=FracType.NUMBER):
        self.natural   = natural
        self.fractype  = fractype
        self.molecules = {}
        if isinstance(expression, str) and expression:
            self.expression = expression
            with MixtureSolver(self.atom) as ms:
                mixture = ms.solve(expression)
            for expr, mol in mixture.molecules.items():
                mol.natural = self.natural
                self.molecules[expr] = mol
        elif isinstance(expression, dict) and expression:
            for expr, frac in expression.items():
                self.add_molecule(expr, frac)
        self._set_norms()

    def __str__(self):
        molecules = []
        for expr, mol in self.molecules.items():
            molecules.append(f"{mol.count} {expr}")
        molecules = "; ".join(molecules)
        return f"Mixture({molecules})"
        
    def __rmul__(self, other:float):
        mixture = Mixture(natural=self.natural, fractype=self.fractype)
        mixture.molecules = {}
        for expression, molecule in self.molecules.items():
            mixture.add_molecule(expression, molecule.count*other)
        return mixture
        
    def __add__(self, other):
        mixture = Mixture(natural=self.natural, fractype=self.fractype)
        mixture.molecules = {}
        for expression, molecule in self.molecules.items():
            mixture.add_molecule(expression, molecule.count)
        for expression, molecule in other.molecules.items():
            mixture.add_molecule(expression, molecule.count)
        return mixture

    def _set_norms(self):
        if self.fractype==FracType.NUMBER:
            self.total_count = np.sum([m.count for m in self.molecules.values()])
            self.total_mass  = np.sum([m.count*m.total_mass for m in self.molecules.values()])
        elif self.fractype==FracType.MASS:
            self.total_count = np.sum([m.count/m.total_mass for m in self.molecules.values()])
            self.total_mass  = np.sum([m.count for m in self.molecules.values()])
        else:
            raise Exception("Invalid fraction type:", self.fractype)
            
    def add_molecule(self, expression:str, count:float=1.0):
        if expression in self.molecules:
            self.molecules[expression].count += count
        else:
            self.molecules[expression] = Molecule(expression, natural=self.natural, count=count)
        self._set_norms()

    def data_molecules(self, quantity=True):
        if not self.molecules:
            return None
        columns = ['count','M']
        with ParameterTable(columns, keys=True, keyname='expression') as pt:
            rc = RowCollector(columns)
            for s,m in self.molecules.items():
                row = [
                    m.count,
                    m.total_mass.to('Da') if quantity else m.total_mass.value('Da'), 
                ]
                pt[s] = row
                rc.append(row)
            pt['avg'] = [np.average(rc[p]) for p in columns]
            pt['sum'] = [np.sum(rc[p]) for p in columns]
            return pt
            
    def data_mixture(self, quantity=True):
        if not self.molecules:
            return None
        columns = ['x','X']
        with ParameterTable(columns, keys=True, keyname='expression') as pt:
            rc = RowCollector(columns)
            for s,m in self.molecules.items():
                row = []
                if self.fractype==FracType.NUMBER:
                    row = row + [
                        m.count/self.total_count,
                        (m.total_mass*m.count/self.total_mass).value(None),
                    ]
                elif self.fractype==FracType.MASS:
                    row = row + [
                        (m.count/m.total_mass/self.total_count).value(None),
                        m.count/self.total_mass,
                    ]
                pt[s] = row
                rc.append(row)
            pt['avg'] = [np.average(rc[p]) for p in columns]
            pt['sum'] = [np.sum(rc[p]) for p in columns]
            return pt
            
    def print_molecules(self):
        df = self.data_molecules(quantity=False).to_dataframe()
        columns = {"M": "M[Da]"}
        df = df.rename(columns=columns)
        print( df.to_string(index=False) )
        
    def print_mixture(self):
        df = self.data_mixture(quantity=False).to_dataframe()
        columns = {}
        df = df.rename(columns=columns)
        print( df.to_string(index=False) )