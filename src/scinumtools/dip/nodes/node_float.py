from typing import List

from ...units import Unit, UnitEnvironment
from .node_base import BaseNode
from .node_select import SelectNode
from ..solvers import NumericalSolver, FunctionSolver
from ..datatypes import FloatType, IntegerType

class FloatNode(BaseNode, SelectNode):
    keyword: str = 'float'
    value: float = None
    options: List = None
    value_expr: str = False
    tags: list = None
    description: str = None
    dtype = float
    precision: int

    def __init__(self, *args, **kwargs):
        self.options = []
        super().__init__(*args, **kwargs)
        self.precision = self.dtype_prop[0] if self.dtype_prop[0] else FloatType.precision
        
    @staticmethod
    def is_node(parser):
        if parser.keyword=='float':
             parser.part_dimension()
             parser.part_equal()
             if parser.is_parsed('part_equal'): # definition
                 parser.part_value()  
             else:
                 parser.defined = True  # declaration
             parser.part_units()    
             parser.part_comment()
             return FloatNode(parser)
         
    def set_value(self, value=None):
        """ Set value using value_raw or arbitrary value
        """
        if value is None and self.value_raw:
            self.value = FloatType(self.cast_value(), self.units_raw, precision=self.precision)
        elif value:
            self.value = FloatType(value, self.units_raw, precision=self.precision)
        else:
            self.value = None
            
    def parse(self, env):
        if self.value_fn: # Process function
            with FunctionSolver(env) as s:
                self.value_raw = s.solve(self.value_fn, self.units_raw)
        if self.value_expr: # Process expression
            with NumericalSolver(env) as s:
                self.value_raw = s.solve(self.value_expr, self.units_raw)
        # Testing validity of units
        if self.units_raw:
            with UnitEnvironment(env.units):
                Unit(self.units_raw)
        return None    
