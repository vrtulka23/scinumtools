import numpy as np
import re
from math import isclose
import copy
from typing import Union

from . import Norm
from .compound import Compound, Component, Units
from .element import Element
from .substance_solver import SubstanceSolver
from .. import ParameterTable, RowCollector
from ..units import Quantity, Unit

class Substance(Compound, Component):
    
    def atom(self, expr:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expr):
            return float(expr)
        else:
            return Substance({expr: 1}, natural=self.natural)
            
    def __init__(self, expr:Union[str,dict]=None, count:float=1.0, natural:bool=True, **kwargs):
        Component.__init__(self, count)
        Compound.__init__(self, 
            SubstanceSolver, Element, expr, {
                'element':    None,
                'isotope':    None,
                'ionisation': None,
                'mass':       Units.ATOMIC_MASS,
                'count':      None,
                'Z':          None,
                'N':          None,
                'e':          None,
            }, {
                "mass":  Units.ATOMIC_MASS, 
                'Z':     None,
                'N':     None,
                'e':     None,
            }, natural=natural, norm_type=Norm.NUMBER, **kwargs
        )

    def __str__(self):
        elements = []
        for expr, el in self.components.items():
            element = f"{expr}" 
            if el.count>1:
                element += f"{int(el.count):d}"
            elements.append(element)
        elements = " ".join(elements)
        data = self.data_compound(quantity=False)
        p = int(round(data['sum']['Z']))
        n = data['sum']['N']
        e = int(round(data['sum']['e']))
        M = data['sum']['mass']
        return f"Substance(mass={M:.03f} Z={p:d} N={n:.03f} e={e:d})"
        
    def __mul__(self, other:float):
        return self._multiply(Substance(natural=self.natural), other)

    def __add__(self, other):
        return self._add(Substance(natural=self.natural), other)
    
    def _add_expr(self, expr:str, count:int):
        self.expr += f"{expr}{count}" if count>1 else expr
    
    def data_components(self, quantity:bool=True):
        def fn_row(s,m):
            return {
                'element':    m.element, 
                'isotope':    m.isotope, 
                'ionisation': m.ionisation, 
                'mass':       m.mass, 
                'count':      m.count, 
                'Z':          m.Z, 
                'N':          m.N, 
                'e':          m.e, 
            }
        return self._data(self.cols_components, fn_row, quantity=quantity)
        
    def data_compound(self, components:list=None, quantity:bool=True):
        def fn_row(s,m):
            return {
                'mass':  m.count*m.mass,
                'Z':     m.count*m.Z, 
                'N':     m.count*m.N, 
                'e':     m.count*m.e, 
            }
        return self._data(self.cols_compound, fn_row, stats=True, weight=True, components=components, quantity=quantity)