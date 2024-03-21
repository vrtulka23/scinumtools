import numpy as np
from typing import Union, Dict

from . import Norm
from .. import ParameterTable, RowCollector
from ..units import Quantity

class Units:
    ATOMIC_MASS    = "Da"
    MATERIAL_MASS  = "g"
    NUMBER_DENSITY = "cm-3"
    MASS_DENSITY   = "g/cm3"
    FRACTION       = "%"

class Component:
    expr: str                       # expression
    count: Union[float,int]         # number of components
    mass: Quantity                  # component mass

    def __init__(self, count:int=1):
        self.count = count

class Compound:
    components: Dict[str,Component] # list of compound components
    component_class: callable       # name of the class that inherits Compound
    
    cols_components: dict           # settings of component columns
    cols_compound: dict             # settings of compound columns
    
    natural: bool                   # natural ements
    norm_type: Norm                 # type of compound norm
    norm_count: Union[float,int]    # total number of components
    norm_mass: Quantity             # total mass of components
    
    mass_density: Quantity = None   # compound mass density
    number_density: Quantity = None # compound number density
    volume: Quantity = None         # compound volume

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def __init__(self, 
        solver:callable, component_class:callable, expr:Union[str,dict], 
        cols_components: dict, cols_compound: dict,
        natural:bool, norm_type:Norm, 
        number_density:Quantity=None, mass_density:Quantity=None, volume:Quantity=None
    ):
        self.expr = ''
        self.norm_type = norm_type
        self.natural = natural
        self.cols_components = cols_components
        self.cols_compound = cols_compound | {
            "x":     Units.FRACTION, 
            "X":     Units.FRACTION,
        }
        self.cols_matter = {
            "n":     Units.NUMBER_DENSITY, 
            "rho":   Units.MASS_DENSITY,
            "N":     None,
            "M":     Units.MATERIAL_MASS,
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
        self.number_density = number_density
        self.mass_density = mass_density
        self.volume = volume
        self._norm()
    
    def _norm(self):
        # calculate total coutn and mass of all components
        components = self.components.values()
        if self.norm_type==Norm.MASS_FRACTION:
            self.norm_count = np.sum([i.count/i.mass for i in components])
            self.norm_mass  = np.sum([i.count for i in components])
        else:
            self.norm_count = np.sum([i.count for i in components])
            self.norm_mass  = np.sum([i.count*i.mass for i in components])
        # if compound is an component as well, register its component mass
        if type(self) in Component.__subclasses__(): 
            self.mass = self.norm_mass
        # setup densities of the compound
        if self.mass_density:
            self.mass_density.to(Units.MASS_DENSITY)
            self.number_density = (self.mass_density/self.norm_mass).to(Units.NUMBER_DENSITY)
        elif self.number_density: # !! number density of a compound, not sum of all its components
            self.mass_density = (self.number_density*self.norm_mass).to(Units.MASS_DENSITY)
            self.number_density.to(Units.NUMBER_DENSITY)

    def _data(self, columns:dict, fn_row:callable, stats:bool=False, weight:bool=False, components:list=None, quantity:bool=True):
        if not self.components: 
            return None   # no components
            
        # create a new copy of the column list and remove unused columns
        columns = dict(columns) 
        if not self.mass_density:
            if 'n' in columns: del columns['n']
            if 'rho' in columns: del columns['rho']
        if not self.volume:
            if 'N' in columns and 'M' in columns: del columns['N']
            if 'M' in columns: del columns['M']

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
                values['x'] = Quantity(m.count/self.norm_count)
                values['X'] = m.count*m.mass/self.norm_mass
                weights.append(m.count)
            elif self.norm_type==Norm.MASS_FRACTION:
                values['x'] = m.count/m.mass/self.norm_count
                values['X'] = Quantity(m.count/self.norm_mass)
                weights.append(m.count/m.mass)
            if self.number_density:
                values['n']   = m.count*self.number_density
                values['rho'] = m.count*m.mass*self.number_density
            if self.volume and 'M' in columns:
                values['N'] = values['n']*self.volume
                values['M'] = values['rho']*self.volume
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

    def data_matter(self, components:list=None, quantity:bool=True):
        def fn_row(s,m):
            values = {
                'count': m.count
            }
            if self.number_density:
                values['n']   = m.count*self.number_density
                values['rho'] = m.count*m.mass*self.number_density
            if self.volume:
                values['N'] = values['n']*self.volume
                values['M'] = values['rho']*self.volume
            return values
        return self._data(self.cols_matter, fn_row, stats=True, weight=True, components=components, quantity=quantity)

    def _multiply(self, compound, other):
        for expr, component in self.components.items():
            compound.add(expr, component.count*other)
        return compound
    
    def _add(self, compound, other):
        for expr, component in self.components.items():
            compound.add(expr, component.count)
        if isinstance(other, self.component_class):
            compound.add(other.expr, other.count)
        else:
            for expr, component in other.components.items():
                compound.add(expr, component.count)
        return compound
    
    def _add_expr(self, expr:str, count:int):
        pass
    
    def add(self, expr:str, count:int=1):
        self._add_expr(expr, count)
        if expr in self.components:
            self.components[expr].count += count
        else:
            self.components[expr] = self.component_class(expr, natural=self.natural, count=count)
        self._norm()

    def _print_table(self, columns:dict, fn_data:callable, **kwargs):
        df = fn_data(quantity=False, **kwargs).to_dataframe()
        df = df.rename(columns={k:f"{k}[{v}]" for k,v in columns.items() if v})
        print( df.to_string(index=False) )
        
    def print_components(self):
        self._print_table(self.cols_components, self.data_components)
        
    def print_compound(self, components:list=None):
        self._print_table(self.cols_compound, self.data_compound, components=components)
        
    def print_matter(self, components:list=None):
        self._print_table(self.cols_matter, self.data_matter, components=components)
        
    def print(self):
        print("Components:")
        print("")
        self._print_table(self.cols_components, self.data_components)
        print("")
        print("Compound:")
        if self.norm_type == Norm.NUMBER:
            print("")
            print(f"Total mass:     {self.norm_mass}")
            print(f"Total number:   {self.norm_count}")
        print("")
        self._print_table(self.cols_compound, self.data_compound)
        if self.mass_density:
            print("")
            print("Matter:")
            print("")
            if self.mass_density:
                print(f"Mass density:   {self.mass_density}")
                print(f"Number density: {self.number_density}")
                if self.volume:
                    print(f"Volume:         {self.volume}")
            print("")
            self._print_table(self.cols_matter, self.data_matter)
