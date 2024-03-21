import numpy as np
import re
from typing import Union

from . import Norm
from .compound import Compound, Units
from .substance import Substance
from .material_solver import MaterialSolver
from ..units import Quantity, Unit

class Material(Compound):
    
    def atom(self, expr:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expr):
            return float(expr)
        else:
            return Material({expr: 1.0}, natural=self.natural, norm_type=self.norm_type)

    def __init__(self, expr:Union[str,dict]=None, natural:bool=True, norm_type:Norm=Norm.NUMBER_FRACTION, **kwargs):
        Compound.__init__( self,
            MaterialSolver, Substance, expr, {  
                'fraction': None,       
                "mass": Units.ATOMIC_MASS,
                'Z': None,
                'N': None,
                'e': None,
            }, {}, natural=natural, norm_type=norm_type, **kwargs
        )

    def __str__(self):
        substances = []
        for expr, mol in self.components.items():
            substances.append(f"{mol.count} {expr}")
        substances = "; ".join(substances)
        return f"Material({substances})"
        
    def __rmul__(self, other:float):
        return self._multiply(Material(natural=self.natural, norm_type=self.norm_type), other)

    def __add__(self, other):
        return self._add(Material(natural=self.natural, norm_type=self.norm_type), other)

    def _add_expr(self, expr:str, count:int):
        self.expr += f"{count} <{expr}>"
        
    def data_components(self, quantity:bool=True):
        def fn_row(s,m):
            subs = m.data_compound()
            return {
                'fraction': m.count,
                'mass':     m.mass,
                'Z':        subs.sum.Z,
                'N':        subs.sum.N,
                'e':        subs.sum.e,
            }
        return self._data(self.cols_components, fn_row, quantity=quantity)

    def data_compound(self, components:list=None, quantity:bool=True):
        def fn_row(s,m):
            return {}
        return self._data(self.cols_compound, fn_row, stats=True, weight=False, components=components, quantity=quantity)
            