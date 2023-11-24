import numpy as np

from ...units import Quantity, UnitEnvironment
from ...solver import *
from ..nodes.parser import Parser
from ..environment import Environment

class NumericalSolver:

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

    def _parse_atom(self, expr):
        expr = expr.lstrip()
        kwargs = {'code': expr, 'source':None}
        p = Parser(keyword='node',**kwargs)
        p.part_value()
        if p.value_ref:   # import existing node
            nodes = self.env.request(p.value_ref, count=[0,1])
            if len(nodes)==1:
                node = nodes[0]
                value, units = node.value.value, node.value.unit
            else:
                raise Exception('Reference does not return any nodes:', p.value_ref)
        else:             # create anonymous node
            p.part_units()
            value, units = p.value_raw, p.units_raw
        with UnitEnvironment(self.env.units):                
            unit = Quantity(float(value), units)
        unit.symbol = expr
        return unit
        
    def solve(self, expr, in_units=None):
        expr_bak = expr
        # immediately return boolean values
        if isinstance(expr,(int,float)):
            return expr
            
        # solve expression
        with UnitEnvironment(self.env.units):
            operators = {
                'log':CustomOperatorLog, 'log10':CustomOperatorLog10, 'logb':CustomOperatorLogb,
                'exp':CustomOperatorExp, 'sqrt':CustomOperatorSqrt,   'powb':CustomOperatorPowb,
                'sin':CustomOperatorSin, 'cos':CustomOperatorCos,     'tan':CustomOperatorTan,
                'par':OperatorPar,  # should be the last of parenthesis operators
                'pow':OperatorPow,
                'mul':CustomOperatorMul, 'truediv':CustomOperatorTruediv,
                'add':CustomOperatorAdd, 'sub':CustomOperatorSub,
            }
            with ExpressionSolver(self._parse_atom, operators) as es:
                result = es.solve(expr)
            if in_units:
                return result.value(in_units)
            else:
                return result
            
    def equal(self, expr1, expr2):
        unit1 = self.solve(expr1)
        unit2 = self.solve(expr2)
        if not unit1.baseunits.nodim:
            unit2.to(unit1.baseunits)
        if unit1 == unit2:
            return True
        else: 
            return False

class CustomOperatorAdd(OperatorAdd):
    symbol: str = ' + '
    def operate_unary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if left is None and isinstance(right, Quantity):
            tokens.put_left(right)        
        elif isinstance(right, CustomOperatorAdd):
            tokens.put_left(left)
            tokens.put_right(right)
        elif isinstance(right, CustomOperatorSub):
            tokens.put_left(left)
            tokens.put_right(right)
        elif not isinstance(left, Quantity) and isinstance(right, Quantity):
            tokens.put_left(left)
            tokens.put_right(right)
        else:
            tokens.put_left(left)
            tokens.put_left(CustomOperatorAdd())
            tokens.put_right(right)
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if not left.baseunits.nodim:
            right.to(left.baseunits)
        tokens.put_left(left + right)

class CustomOperatorSub(OperatorSub):
    symbol: str = ' - '
    def operate_unary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if left is None and isinstance(right, Quantity):
            tokens.put_left(-right)
        elif isinstance(right, CustomOperatorAdd):
            tokens.put_left(left)
            tokens.put_right(CustomOperatorSub())
        elif isinstance(right, CustomOperatorSub):
            tokens.put_left(left)
            tokens.put_right(CustomOperatorAdd())
        elif not isinstance(left, Quantity) and isinstance(right, Quantity):
            tokens.put_left(left)
            tokens.put_right(-right)
        else:
            tokens.put_left(left)
            tokens.put_left(CustomOperatorSub())
            tokens.put_right(right)
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if not left.baseunits.nodim:
            right.to(left.baseunits)
        tokens.put_left(left - right)

class CustomOperatorMul(OperatorMul):
    symbol: str = ' * '

class CustomOperatorTruediv(OperatorTruediv):
    symbol: str = ' / '

class CustomOperatorExp(OperatorExp):
    def operate_args(self, tokens):
        tokens.put_left(Quantity(np.e)**self.args[0].value())        
            
class CustomOperatorLog(OperatorLog):
    def operate_args(self, tokens):
        tokens.put_left(np.log(self.args[0]))     

class CustomOperatorLog10(OperatorLog10):
    def operate_args(self, tokens):
        tokens.put_left(np.log10(self.args[0]))        

class CustomOperatorSqrt(OperatorSqrt):
    def operate_args(self, tokens):
        tokens.put_left(np.sqrt(self.args[0]))      

class CustomOperatorSin(OperatorSin):
    def operate_args(self, tokens):
        tokens.put_left(np.sin(self.args[0]))      

class CustomOperatorCos(OperatorCos):
    def operate_args(self, tokens):
        tokens.put_left(np.cos(self.args[0]))       

class CustomOperatorTan(OperatorTan):
    def operate_args(self, tokens):
        tokens.put_left(np.tan(self.args[0]))       

class CustomOperatorLogb(OperatorLogb):
    def operate_args(self, tokens):
        tokens.put_left(np.log(self.args[0])/np.log(self.args[1]))

class CustomOperatorPowb(OperatorPowb):
    def operate_args(self, tokens):
        tokens.put_left(np.power(self.args[0],self.args[1].value()))     

