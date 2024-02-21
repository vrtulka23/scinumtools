import numpy as np
import re
import copy

from .molecule import Molecule
from .mixture_solver import MixtureSolver
from ..units import Quantity, Unit
from .. import ParameterTable, RowCollector

class Mixture:
    
    natural: bool
    molecules: dict
    norm: dict
    rho: Quantity = None
    expression: str = ''

    @staticmethod
    def from_molecules(molecules:list, natural:bool=True):
        mixture = Mixture(natural=natural)
        for mol in molecules:
            mixture.add_molecule(mol)
        return mixture
        
    def atom(self, expression:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expression):
            return float(expression)
        else:
            return Mixture.from_molecules([
                Molecule(expression, natural=self.natural),
            ], natural=self.natural)
            
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
            
    def __init__(self, expression:str=None, natural:bool=True):
        self.natural = natural
        self.molecules = {}
        if expression and expression!='':
            self.expression = expression
            with MixtureSolver(self.atom) as ms:
                mixture = ms.solve(expression)
            for expr, mol in mixture.molecules.items():
                self.molecules[expr] = mol
        self._calculate_norm()
   
    def __str__(self):
        molecules = []
        for expr, mol in self.molecules.items():
            molecules.append(f"{mol.fraction} {expr}")
        molecules = "; ".join(molecules)
        return f"Mixture({molecules})"
        
    def __rmul__(self, other:float):
        mixture = copy.deepcopy(self)
        mixture.molecules = {}
        for expr in self.molecules.keys():
            el = self.molecules[expr]
            el.fraction *= other
            mixture.add_molecule(el)
        return mixture
        
    def __add__(self, other):
        mixture = copy.deepcopy(self)
        mixture.molecules = {}
        for expr,el in self.molecules.items():
            mixture.add_molecule(el)
        for expr,el in other.molecules.items():
            mixture.add_molecule(el)
        return mixture

    def _calculate_norm(self):
        fractions = [m.fraction for m in self.molecules.values()]
        self.norm = np.sum(fractions)
        if self.norm>1:
            raise Exception("Sum of all molecule ratios is more than one", self.norm , fractions)
    
    def add_molecule(self, molecule:Molecule, fraction:float=None):
        expression = molecule.expression
        if fraction is not None:
            molecule.fraction = fraction
        if expression in self.molecules:
            self.molecules[expression].fraction += molecule.fraction
        else:
            self.molecules[expression] = molecule
        self._calculate_norm()
        
    def data_molecules(self, quantity=True):
        if not self.molecules:
            return None
        columns = ['M']
        with ParameterTable(['X']+columns, keys=True, keyname='expression') as pt:
            rc = RowCollector(['X']+columns)
            for s,m in self.molecules.items():
                row = [
                    m.fraction,
                    m.M.to('Da') if quantity else m.M.value('Da'), 
                ]
                pt[s] = row
                rc.append(row)
            avg = [np.average(rc['X'])]
            sum = [np.sum(rc['X'])]
            for p in columns:
                sum.append(np.sum(rc[p]))
                avg.append(np.average(rc[p]))
            pt['avg'] = avg
            pt['sum'] = sum
            return pt
            
    def print_molecules(self):
        df = self.data_molecules(quantity=False).to_dataframe()
        columns = {"M": "M[Da]"}
        df = df.rename(columns=columns)
        print( df.to_string(index=False) )