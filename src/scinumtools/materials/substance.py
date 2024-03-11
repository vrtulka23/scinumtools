import numpy as np
import re
from math import isclose
import copy
from typing import Union

from . import Norm
from .compound import Compound, Item
from .element import Element
from .substance_solver import SubstanceSolver
from .. import ParameterTable, RowCollector
from ..units import Quantity, Unit

class Substance(Compound, Item):
    norm = Norm.ITEM_COUNT
    item_class = Element
    
    natural: bool
    rho: Quantity = None
    V: Quantity = None
    n: Quantity = None
    columns_elements:dict = {
        'element': None,
        'isotope': None,
        'ionisation': None,
        'mass': 'Da',
        'Z': None,
        'N': None,
        'e': None,
    }
    columns_substance:dict = {
        'count': None,
        "mass": "Da", 
        'Z': None,
        'N': None,
        'e': None,
        "x": "%", 
        "X": "%",
        "n": "cm-3", 
        "rho": "g/cm3",
        "n_V": None,
        "M_V": "g",
    }
    
    def atom(self, expr:str):
        if m:=re.match("[0-9]+(\.[0-9]+|)([eE]{1}[+-]?[0-9]{0,3}|)",expr):
            return float(expr)
        else:
            return Substance({expr: 1}, natural=self.natural)
            
    def __init__(self, expr:Union[str,dict]=None, natural:bool=True, count:float=1.0, rho:Quantity=None, V:Quantity=None):
        self.expr = ''
        self.natural = natural
        self.count = count
        self.items = {}
        if isinstance(expr,str) and expr:
            self.expr = expr
            with SubstanceSolver(self.atom) as ms:
                substance = ms.solve(expr)
            for expr, el in substance.items.items():
                self.items[expr] = el
        elif isinstance(expr, dict) and expr:
            for expr, frac in expr.items():
                self.add(expr, frac)
        self.rho = rho
        self.V = V
        self._norm()

    def __str__(self):
        elements = []
        for expr, el in self.items.items():
            element = f"{expr}" 
            if el.count>1:
                element += f"{int(el.count):d}"
            elements.append(element)
        elements = " ".join(elements)
        data = self.data_substance(quantity=False)
        p = int(round(data['sum']['Z']))
        n = data['sum']['N']
        e = int(round(data['sum']['e']))
        M = data['sum']['mass']
        return f"Substance(mass={M:.03f} Z={p:d} N={n:.03f} e={e:d})"
        
    def __mul__(self, other:float):
        return self._multiply(Substance(natural=self.natural), other)

    def __add__(self, other):
        return self._add(Substance(natural=self.natural), other)
    
    def _norm(self):
        super()._norm()
        self.mass = self.total_mass
        if self.rho:
            self.n = (self.rho/self.total_mass).rebase()
    
    def add(self, expr:str, count:float=1.0):
        self.expr += expr
        super().add(expr, count)

    def data_elements(self, quantity:bool=True):
        def fn_row(s,e):
            return {
                'element':    e.element, 
                'isotope':    e.isotope, 
                'ionisation': e.ionisation, 
                'mass':       e.mass, 
                'Z':          e.Z, 
                'N':          e.N, 
                'e':          e.e, 
            }
        return self._data(self.columns_elements, fn_row, quantity=quantity)
            
    def data_substance(self, items:list=None, quantity:bool=True):
        def fn_row(s,e):
            row = {
                'count': e.count, 
                'x':     100*e.count/self.total_count,
                'X':     e.count*e.mass/self.total_mass,
                'mass':  e.count*e.mass,
                'Z':     e.count*e.Z, 
                'N':     e.count*e.N, 
                'e':     e.count*e.e, 
            }
            if self.rho:
                row['n']   = e.count*self.n
                row['rho'] = e.count*e.mass*self.n
            if self.V:
                row['n_V'] = e.count*self.n*self.V
                row['M_V'] = e.count*e.mass*self.n*self.V
            return row
        if self.rho:
            if self.V:
                columns = self.columns_substance
            else:
                columns = {k:v for k,v in self.columns_substance.items() if k in ['count','mass','Z','N','e','x','X','n','rho']}
        else:
            columns = {k:v for k,v in self.columns_substance.items() if k in ['count','mass','Z','N','e','x','X']}
        return self._data(columns, fn_row, stats=True, weight='count', items=items, quantity=quantity)
    
    def print_elements(self):
        self._print(self.columns_elements, self.data_elements)

    def print_substance(self, items:list=None):
        self._print(self.columns_substance, self.data_substance)
        
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
        self._print(self.columns_elements, self.data_elements)
        print("")
        print("Substance:")
        print("")
        self._print(self.columns_substance, self.data_substance)