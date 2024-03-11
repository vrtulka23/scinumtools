import numpy as np
from typing import Union, Dict

from . import Norm
from .. import ParameterTable, RowCollector
from ..units import Quantity

class Item:
    expr: str
    count: Union[float,int]
    mass: Quantity

class Compound:
    items: Dict[str,Item]
    item_class: callable
    norm: Norm
    total_count: Union[float,int]
    total_mass: Quantity
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def _norm(self):
        items = self.items.values()
        if self.norm==Norm.MASS_FRACTION:
            self.total_count = np.sum([i.count/i.mass for i in items])
            self.total_mass  = np.sum([i.count for i in items])
        else:
            self.total_count = np.sum([i.count for i in items])
            self.total_mass  = np.sum([i.count*i.mass for i in items])

    def _data(self, columns:dict, fn_row:callable, stats:bool=False, weight:str=False, items:list=None, quantity:bool=True):
        if not self.items: 
            return None   # no items
        column_names = list(columns.keys())
        pt = ParameterTable(column_names, keys=True, keyname='expr')
        rc = RowCollector(column_names)
        for s,m in self.items.items():
            if items and s not in items:
                continue  # item is not selected
            row, values = [], fn_row(s,m)
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
            pt[s] = row
            rc.append(row)
        if stats: # add statistics
            if weight: # use weighted average
                pt['avg'] = [np.average(rc[weight])] + [
                    np.average(np.divide(rc[p],rc[weight]), weights=rc[weight]) for p in column_names if p!=weight
                ]
            else:
                pt['avg'] = [np.average(rc[p]) for p in column_names]
            pt['sum'] = [np.sum(rc[p]) for p in column_names]
        return pt

    def _print(self, columns:dict, fn_data:callable, **kwargs):
        df = fn_data(quantity=False, **kwargs).to_dataframe()
        df = df.rename(columns={k:f"{k}[{v}]" for k,v in columns.items() if v})
        print( df.to_string(index=False) )

    def _multiply(self, compound, other):
        for expr, item in self.items.items():
            compound.add(expr, item.count*other)
        return compound
    
    def _add(self, compound, other):
        for expr, item in self.items.items():
            compound.add(expr, item.count)
        if isinstance(other, self.item_class):
            compound.add(other.expr, other.count)
        else:
            for expr, item in other.items.items():
                compound.add(expr, item.count)
        return compound
    
    def add(self, expr:str, count:int=1):
        if expr in self.items:
            self.items[expr].count += count
        else:
            self.items[expr] = self.item_class(expr, natural=self.natural, count=count)
        self._norm()
