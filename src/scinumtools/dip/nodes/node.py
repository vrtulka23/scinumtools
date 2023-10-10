from typing import List
import copy

from ..source import Source

class Node:
    code: str 
    source: Source = None
    keyword: str = None
    dtype = str                     # datatype
    dtype_prop = list               # datatype properties (e.g.: unsigned, precision)
    indent: int = 0
    name: str = None
    value_raw: str = None           # Raw value
    value_ref: str = None           # Reference
    value_fn: str = None            # Function
    value_expr: str = None          # Expression
    value_slice: List[tuple] = None # Slice
    units_raw: str = None           # Ras units
    defined: bool = False
    dimension: List[tuple] = None

    def __init__(self, code, **kwargs):
        self.code = code
        self.dtype_prop = []
        for key,val in kwargs.items():
            setattr(self, key, val)

    def copy(self):
        return copy.deepcopy(self)