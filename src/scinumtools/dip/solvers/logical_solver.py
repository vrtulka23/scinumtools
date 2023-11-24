import numpy as np

from ...solver import *
from ...units import UnitEnvironment
from ..environment import Environment
from ..nodes.parser import Parser
from ..datatypes import NumberType, BooleanType
from ..settings import Keyword, Sign

class LogicalSolver:

    env: Environment
    
    def __init__(self, env:Environment=None, **kwargs):
        if env:
            self.env = env
        else:
            self.env = Environment()
            
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def _eval_node(self, expr):
        expr = expr.strip()
        if expr=='':
            return None
        flags = []
        if expr[0]==Sign.DEFINED:
            flags.append('defined')
            expr = expr[1:]
        # parse node from the code
        kwargs = {'code': expr, 'source':None}
        p = Parser(keyword='node',**kwargs)
        p.part_value()
        if p.value_ref:   # import existing node
            nodes = self.env.request(p.value_ref, count=[0,1])
            if len(nodes)==1:
                if 'defined' in flags:
                    node = BooleanType(True)
                else:
                    node = nodes[0].value
            elif len(nodes)==0:
                if 'defined' in flags:
                    node = BooleanType(False)
                else:
                    raise Exception('Missing reference:', expr)
        elif p.value_raw==Keyword.TRUE:
            node = BooleanType(True)
        elif p.value_raw==Keyword.FALSE:
            node = BooleanType(False)
        else:            # create anonymous node
            p.part_units()
            node = NumberType(p.value_raw, p.units_raw)
        return node

    def solve(self, expr):
        with UnitEnvironment(self.env.units):
            operators = {
                'par': OperatorPar,        # should be the last of parenthesis operators
                'eq': OperatorEq, 'ne': OperatorNe,
                'not': CustomNot,          # needs to be after OperatorNe
                'le': OperatorLe, 'ge': OperatorGe,
                'lt': OperatorLt, 'gt': OperatorGt,
                'and': CustomAnd, 'or': CustomOr, 
            }
            with ExpressionSolver(self._eval_node, operators) as es:
                return es.solve(expr)
                

class CustomNot(OperatorNot):
    symbol: str = Sign.NEGATE

class CustomAnd(OperatorAnd):
    
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if isinstance(left, (bool, np.bool_)):
            left = BooleanType(left)
        if isinstance(right, (bool, np.bool_)):
            right = BooleanType(right)
        tokens.put_left(left.logical_and(right))
        
class CustomOr(OperatorOr):
    
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if isinstance(left, (bool, np.bool_)):
            left = BooleanType(left)
        if isinstance(right, (bool, np.bool_)):
            right = BooleanType(right)
        tokens.put_left(left.logical_or(right))