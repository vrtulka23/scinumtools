from typing import Union, List
import numpy as np

from .DIP_Type_Number import NumberType

class IntegerType(NumberType):
    value: Union[int,list]
    dtype = int

    def __str__(self):
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
        super().__init__(**kwargs)
