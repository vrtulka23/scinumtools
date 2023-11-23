from typing import Union, List
import numpy as np

from .type import Type
from .type_boolean import BooleanType

class StringType(Type):    
    value: Union[str,list]
    dtype = str

    def __str__(self):
        return f"StringType({self.value})"
    
    def __repr__(self):
        return f"StringType({self.value})"
        
    def __eq__(self, other):
        return self.value == other.value
        
    def __init__(self, value, **kwargs):
        kwargs['value'] = value
        if isinstance(kwargs['value'], np.ndarray):
            kwargs['value'] = kwargs['value'].tolist()
        super().__init__(**kwargs)
