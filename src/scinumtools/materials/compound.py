import numpy as np
from typing import Union, Dict

from . import Norm, Units
from .matter import Matter
from .. import ParameterTable, RowCollector
from ..units import Quantity

class Component:
    expr: str                       # expression
    proportion: Union[float,int]    # proportion 
    component_mass: Quantity        # mass of a component

    def __init__(self, proportion:int=1):
        self.proportion = proportion

class Compound:
    components: Dict[str,Component] # list of compound components
    component_class: callable       # name of the class that inherits Compound
    
    cols_components: dict           # settings of component columns
    cols_compound: dict             # settings of compound columns
    
    natural: bool                   # natural ements
    norm_type: Norm                 # type of compound norm
    proportion_norm: Union[float,int] # sum of all comonent proportions
    compound_mass: Quantity         # sum of all component masses
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def __init__(self, 
        solver:callable, component_class:callable, expr:Union[str,dict], 
        cols_components: dict, cols_compound: dict,
        natural:bool, norm_type:Norm,
    ):
        self.expr = ''
        self.norm_type = norm_type
        self.natural = natural
        self.cols_components = cols_components
        self.cols_compound = cols_compound | {
            "x":     Units.FRACTION, 
            "X":     Units.FRACTION,
        }
        self.component_class = component_class
        self.components = {}
        if isinstance(expr,str) and expr:
            self.expr = expr
            with solver(self.atom) as ms:
                for expr, component in ms.solve(expr).components.items():
                    self.components[expr] = component
        elif isinstance(expr, dict) and expr:
            for expr, frac in expr.items():
                self.add(expr, frac)
        self._norm()
    
    def _norm(self):
        # calculate total coutn and mass of all components
        components = self.components.values()
        if self.norm_type==Norm.MASS_FRACTION:
            self.proportion_norm = np.sum([i.proportion/i.component_mass for i in components])
            self.compound_mass  = np.sum([i.proportion for i in components])
        else:
            self.proportion_norm = np.sum([i.proportion for i in components])
            self.compound_mass  = np.sum([i.proportion*i.component_mass for i in components])
        if type(self) in Component.__subclasses__():
            self.component_mass = self.compound_mass
        Matter._norm(self)

    def _data(self, columns:dict, fn_row:callable, stats:bool=False, weight:bool=False, components:list=None, quantity:bool=True):
        if not self.components: 
            return None   # no components
            
        # populate columns with values
        weights = []
        column_names = list(columns.keys())
        pt = ParameterTable(column_names, keys=True, keyname='expr')
        rc = RowCollector(column_names)
        for s,m in self.components.items():
            # component is not selected
            if components and s not in components:
                continue  
            # calculate matter properties
            row, values = [], fn_row(s,m)
            if self.norm_type in [Norm.NUMBER_FRACTION, Norm.NUMBER]:
                values['x'] = Quantity(m.proportion/self.proportion_norm)
                values['X'] = m.proportion*m.component_mass/self.compound_mass
                weights.append(m.proportion)
            elif self.norm_type==Norm.MASS_FRACTION:
                values['x'] = m.proportion/m.component_mass/self.proportion_norm
                values['X'] = Quantity(m.proportion/self.compound_mass)
                weights.append(m.proportion/m.component_mass)
            # convert to proper units
            for col in column_names:
                value, unit = values[col], columns[col]
                if quantity and unit: # returning quantities
                    if isinstance(value, Quantity):
                        row.append(value.to(unit))
                    else:
                        row.append(Quantity(value, unit))
                elif isinstance(value, Quantity): # returning scalar
                        row.append(value.value(unit) if unit else value.value())
                else: # returning scalar
                    row.append(value)
            # insert row
            pt[s] = row
            rc.append(row)
        
        # add rows with averages and sums
        if stats:
            if weight: # use weighted average
                if self.norm_type == Norm.NUMBER:
                    pt['avg'] = [np.average(np.divide(rc[p],weights), weights=weights) for p in column_names]
                else:
                    pt['avg'] = [np.average(rc[p]) for p in column_names]
            else:
                pt['avg'] = [np.average(rc[p]) for p in column_names]
            pt['sum'] = [np.sum(rc[p]) for p in column_names]
            
        return pt

    def _multiply(self, compound, other):
        for expr, component in self.components.items():
            compound.add(expr, component.proportion*other)
        return compound
    
    def _add(self, compound, other):
        for expr, component in self.components.items():
            compound.add(expr, component.proportion)
        if isinstance(other, self.component_class):
            compound.add(other.expr, other.proportion)
        else:
            for expr, component in other.components.items():
                compound.add(expr, component.proportion)
        return compound
    
    def _add_expr(self, expr:str, proportion:int):
        pass
    
    def add(self, expr:str, proportion:int=1):
        self._add_expr(expr, proportion)
        if expr in self.components:
            self.components[expr].proportion += proportion
        else:
            self.components[expr] = self.component_class(expr, natural=self.natural, proportion=proportion)
        self._norm()

    def _print_table(self, columns:dict, fn_data:callable, **kwargs):
        df = fn_data(quantity=False, **kwargs).to_dataframe()
        df = df.rename(columns={k:f"{k}[{v}]" for k,v in columns.items() if v})
        print( df.to_string(index=False) )
        
    def print_components(self):
        self._print_table(self.cols_components, self.data_components)
        
    def print_compound(self, components:list=None):
        self._print_table(self.cols_compound, self.data_compound, components=components)
        
    def print(self):
        print("Components:")
        print("")
        self._print_table(self.cols_components, self.data_components)
        print("")
        print("Compound:")
        if self.norm_type == Norm.NUMBER:
            print("")
            print(f"Total mass:     {self.compound_mass}")
            print(f"Total number:   {self.proportion_norm}")
        print("")
        self._print_table(self.cols_compound, self.data_compound)
        if self.mass_density:
            print("")
            Matter.print(self)