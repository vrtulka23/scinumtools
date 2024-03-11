import numpy as np
import re
from typing import Union

from . import Norm
from .compound import Compound
from .substance import Substance
from .material_solver import MaterialSolver
from ..units import Quantity, Unit

class Material(Compound):
    item_class = Substance
    
    natural: bool
    rho: Quantity = None
    columns_substances: dict = {
        'fraction': None,
        "mass": "Da",
        'Z': None,
        'N': None,
        'e': None,
    }
    columns_material: dict = {
        "x": "%", 
        "X": "%",
    }

    def atom(self, expr:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expr):
            return float(expr)
        else:
            return Material({expr: 1.0}, natural=self.natural, norm=self.norm)

    def __init__(self, expr:Union[str,dict]=None, natural:bool=True, norm:Norm=Norm.NUMBER_FRACTION):
        self.natural   = natural
        self.norm  = norm
        self.items = {}
        if isinstance(expr, str) and expr:
            self.expr = expr
            with MaterialSolver(self.atom) as ms:
                material = ms.solve(expr)
            for expr, mol in material.items.items():
                mol.natural = self.natural
                self.items[expr] = mol
        elif isinstance(expr, dict) and expr:
            for expr, frac in expr.items():
                self.add(expr, frac)
        self._norm()

    def __str__(self):
        substances = []
        for expr, mol in self.items.items():
            substances.append(f"{mol.count} {expr}")
        substances = "; ".join(substances)
        return f"Material({substances})"
        
    def __rmul__(self, other:float):
        return self._multiply(Material(natural=self.natural, norm=self.norm), other)

    def __add__(self, other):
        return self._add(Material(natural=self.natural, norm=self.norm), other)

    def data_substances(self, quantity:bool=True):
        def fn_row(s,m):
            subs = m.data_substance()
            return {
                'fraction': m.count,
                'mass':     m.total_mass,
                'Z':        subs.sum.Z,
                'N':        subs.sum.N,
                'e':        subs.sum.e,
            }
        return self._data(self.columns_substances, fn_row, quantity=quantity)

    def data_material(self, quantity:bool=True):
        def fn_row(s,m):
            row = {}
            if self.norm==Norm.NUMBER_FRACTION:
                row['x'] = 100*m.count/self.total_count
                row['X'] = m.total_mass*m.count/self.total_mass
            elif self.norm==Norm.MASS_FRACTION:
                row['x'] = m.count/m.total_mass/self.total_count
                row['X'] = 100*m.count/self.total_mass
            return row
        return self._data(self.columns_material, fn_row, stats=True, quantity=quantity)
            
    def print_substances(self):
        self._print(self.columns_substances, self.data_substances)
        
    def print_material(self):
        self._print(self.columns_material, self.data_material)