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
    norm: dict
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
                self.molecules[expr] = mol
        elif isinstance(expression, dict) and expression:
            for expr, frac in expression.items():
                self.add_molecule(expr, frac)
        self._calculate_norm()
   
    def __str__(self):
        molecules = []
        for expr, mol in self.molecules.items():
            molecules.append(f"{mol.fraction} {expr}")
        molecules = "; ".join(molecules)
        return f"Mixture({molecules})"
        
    def __rmul__(self, other:float):
        mixture = Mixture(natural=self.natural, fractype=self.fractype)
        mixture.molecules = {}
        for expression in self.molecules.keys():
            fraction = self.molecules[expression].fraction*other
            mixture.add_molecule(expression, fraction)
        return mixture
        
    def __add__(self, other):
        mixture = Mixture(natural=self.natural, fractype=self.fractype)
        mixture.molecules = {}
        for expression in self.molecules.keys():
            fraction = self.molecules[expression].fraction
            mixture.add_molecule(expression, fraction)
        for expression in other.molecules.keys():
            fraction = other.molecules[expression].fraction
            mixture.add_molecule(expression, fraction)
        return mixture

    def _calculate_norm(self):
        fractions = [m.fraction for m in self.molecules.values()]
        self.norm = np.sum(fractions)
        if self.norm>1:
            raise Exception("Sum of all molecule ratios is more than one", self.norm , fractions)
    
    def add_molecule(self, expression:str, fraction:float=1.0):
        if expression in self.molecules:
            self.molecules[expression].fraction += fraction
        else:
            self.molecules[expression] = Molecule(expression, natural=self.natural, fraction=fraction)
        self._calculate_norm()
        
    def data_molecules(self, quantity=True):
        if not self.molecules:
            return None
        FRACSIGN = 'X_N' if self.fractype==FracType.NUMBER else 'X_M'
        columns = ['M']
        with ParameterTable([FRACSIGN]+columns, keys=True, keyname='expression') as pt:
            rc = RowCollector([FRACSIGN]+columns)
            for s,m in self.molecules.items():
                row = [
                    m.fraction,
                    m.M.to('Da') if quantity else m.M.value('Da'), 
                ]
                pt[s] = row
                rc.append(row)
            avg = [np.average(rc[FRACSIGN])]
            sum = [np.sum(rc[FRACSIGN])]
            for p in columns:
                sum.append(np.sum(rc[p]))
                avg.append(np.average(rc[p]))
            pt['avg'] = avg
            pt['sum'] = sum
            return pt
            
    def data_mixture(self, quantity=True):
        pass
            
    def print_molecules(self):
        df = self.data_molecules(quantity=False).to_dataframe()
        columns = {"M": "M[Da]"}
        df = df.rename(columns=columns)
        print( df.to_string(index=False) )