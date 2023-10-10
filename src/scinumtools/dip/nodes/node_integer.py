from typing import List
import numpy as np

from ...units import Unit, UnitEnvironment
from .node_base import BaseNode
from .node_select import SelectNode
from ..datatypes import IntegerType,FloatType
from ..solvers import NumericalSolver, FunctionSolver

class IntegerNode(BaseNode, SelectNode):
    keyword: str = 'int'
    value: int = None
    options: List = None
    value_expr: str = False
    tags: list = None
    description: str = None
    dtype = int
    bits = 32

    def __init__(self, *args, **kwargs):
        self.options = []
        super().__init__(*args, **kwargs)
        
    @staticmethod
    def is_node(parser):
        if parser.keyword=='int':
             parser.part_dimension()
             parser.part_equal()
             if parser.is_parsed('part_equal'): # definition
                 parser.part_value()  
             else:
                 parser.defined = True  # declaration
             parser.part_units()    
             parser.part_comment()
             return IntegerNode(parser)
         
    def set_value(self, value=None):
        """ Set value using value_raw or arbitrary value
        """
        unsigned, precision = self.dtype_prop
        unsigned = True if unsigned else IntegerType.unsigned
        precision = precision if precision else IntegerType.precision
        if value is None and self.value_raw:
            self.value = IntegerType(self.cast_value(), self.units_raw, precision=precision, unsigned=unsigned)
        elif value:
            self.value = IntegerType(value, self.units_raw, precision=precision, unsigned=unsigned)
        else:
            self.value = None
            
    def parse(self, env):
        if self.value_fn: # Process function
            with FunctionSolver(env) as s:
                self.value_raw = s.solve(self.value_fn, self.units_raw)
        if self.value_expr: # Process expression
            with NumericalSolver(env) as s:
                self.value_raw = np.round(s.solve(self.value_expr, self.units_raw))
        # Testing validity of units
        if self.units_raw:
            with UnitEnvironment(env.units):
                Unit(self.units_raw)
        return None    
