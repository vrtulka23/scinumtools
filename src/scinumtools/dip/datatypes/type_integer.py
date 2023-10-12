from typing import Union, List
import numpy as np

from .type_number import NumberType
from .type_boolean import BooleanType

class IntegerType(NumberType):
    value: Union[int,list]
    unsigned: bool = False
    precision: int = 32
    dtype = int
        
    def __str__(self):
        if self.unit:
            return f"IntegerType({self.value} {self.unit})"
        else:
            return f"IntegerType({self.value})"
            
    def __repr__(self):
        if self.unit:
            return f"IntegerType({self.value} {self.unit})"
        else:
            return f"IntegerType({self.value})"
            
    def __init__(self, value, unit=None, **kwargs):
        if isinstance(value, IntegerType):
            kwargs['value'] = value.value
            kwargs['unit'] = value.unit
        else:
            kwargs['value'] = value
            kwargs['unit'] = unit
        if isinstance(kwargs['value'], np.ndarray):
            kwargs['value'] = kwargs['value'].tolist()
        if 'unsigned' in kwargs:
            self.unsigned = kwargs['unsigned']
            del kwargs['unsigned']
        if 'precision' in kwargs:
            self.precision = int(kwargs['precision'])
            del kwargs['precision']
        super().__init__(**kwargs)
