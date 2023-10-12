from .node_base import BaseNode
from .node_select import SelectNode
from ..solvers import TemplateSolver, FunctionSolver
from ..datatypes import StringType

class StringNode(BaseNode, SelectNode):
    keyword: str = 'str'
    format: str = None
    tags: list = None
    options: list = None
    description: str = None
    dtype = str

    def __init__(self, *args, **kwargs):
        self.options = []
        super().__init__(*args, **kwargs)
        
    @staticmethod
    def is_node(parser):
        if parser.keyword=='str':
             parser.part_dimension()
             parser.part_equal()
             if parser.is_parsed('part_equal'): # definition
                 parser.part_value()  
             else:
                 parser.defined = True  # declaration
             parser.part_units()    
             parser.part_comment()
             return StringNode(parser)
         
    def set_value(self, value=None):
        """ Set value using value_raw or arbitrary value
        """
        if value is None and self.value_raw:
            self.value = StringType(self.cast_value())
        elif value:
            self.value = StringType(value)
        else:
            self.value = None
            
    def parse(self, env):
        if self.value_fn: # Process function
            with FunctionSolver(env) as s:
                self.value_raw = s.solve(self.value_fn)
        if self.value_expr: # Process function
            with TemplateSolver(env, source=self.source) as s:
                self.value_raw = s.solve(self.value_expr)
        if self.units_raw:
            raise Exception('String datatype does not support units:', self.code)
        return None    
