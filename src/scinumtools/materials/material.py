import numpy as np
import re
from typing import Union

from . import Norm, Units
from .matter import Matter
from .composite import Composite
from .substance import Substance
from .material_solver import MaterialSolver
from ..units import Quantity, Unit

class Material(Composite, Matter):
    
    def atom(self, expr:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expr):
            return float(expr)
        else:
            return Material({expr: 1.0}, natural=self.natural, norm_type=self.norm_type)

    def __init__(self, expr:Union[str,dict]=None, natural:bool=True, norm_type:Norm=Norm.NUMBER_FRACTION, **kwargs):
        Matter.__init__(self, **kwargs)
        Composite.__init__( self,
            MaterialSolver, Substance, expr, {  
                'fraction': None,       
                "mass": Units.ATOMIC_MASS,
                'Z': None,
                'N': None,
                'e': None,
            }, {}, natural=natural, norm_type=norm_type
        )

    def __str__(self):
        substances = []
        for expr, mol in self.components.items():
            substances.append(f"{mol.proportion} {expr}")
        substances = "; ".join(substances)
        return f"Material({substances})"
        
    def __rmul__(self, other:float):
        return self._multiply(Material(natural=self.natural, norm_type=self.norm_type), other)

    def __add__(self, other):
        return self._add(Material(natural=self.natural, norm_type=self.norm_type), other)

    def _add_expr(self, expr:str, proportion:int):
        self.expr += f"{proportion} <{expr}>"
        
    def data_components(self, quantity:bool=True):
        def fn_row(s,m):
            subs = m.data_composite()
            return {
                'fraction': m.proportion,
                'mass':     m.component_mass,
                'Z':        subs.sum.Z,
                'N':        subs.sum.N,
                'e':        subs.sum.e,
            }
        return self._data(self.cols_components, fn_row, quantity=quantity)

    def data_composite(self, components:list=None, quantity:bool=True):
        def fn_row(s,m):
            return {}
        return self._data(self.cols_composite, fn_row, stats=True, weight=False, components=components, quantity=quantity)
            