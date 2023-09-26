import numpy as np
from enum import Enum

from .expression import Expression

class Otype(Enum):
    
    ARGS = 0
    UNARY = 1
    BINARY = 2
    TERNARY = 3
    
class OperatorBase:
    
    symbol: str       # Operator symbol
    args: list = None # Arguments of a parenthesis operator
    
    def __init__(self, expr:str=None):
        if expr:
            expr.remove(self.symbol)
            
    def __repr__(self):
        return f"Oper({self.symbol})"
    
class OperatorAdd(OperatorBase):
    
    symbol: str = '+'
    
    def operate_unary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if left is None and isinstance(right, tokens.atom):
            tokens.put_left(right)        
        elif isinstance(right, OperatorAdd):
            tokens.put_left(left)
            tokens.put_right(right)
        elif isinstance(right, OperatorSub):
            tokens.put_left(left)
            tokens.put_right(right)
        elif not isinstance(left, tokens.atom) and isinstance(right, tokens.atom):
            tokens.put_left(left)
            tokens.put_right(right)
        else:
            tokens.put_left(left)
            tokens.put_left(OperatorAdd())
            tokens.put_right(right)
            
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left + right)

class OperatorSub(OperatorBase):
    
    symbol: str = '-'
    
    def operate_unary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        if left is None and isinstance(right, tokens.atom):
            tokens.put_left(-right)
        elif isinstance(right, OperatorAdd):
            tokens.put_left(left)
            tokens.put_right(OperatorSub())
        elif isinstance(right, OperatorSub):
            tokens.put_left(left)
            tokens.put_right(OperatorAdd())
        elif not isinstance(left, tokens.atom) and isinstance(right, tokens.atom):
            tokens.put_left(left)
            tokens.put_right(-right)
        else:
            tokens.put_left(left)
            tokens.put_left(OperatorSub())
            tokens.put_right(right)
            
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left - right)

class OperatorMul(OperatorBase):
    
    symbol: str = '*'
    
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left * right)

class OperatorTruediv(OperatorBase):
    
    symbol: str = '/'
    
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left / right)

class OperatorPow(OperatorBase):

    symbol: str = '**'

    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left ** right)
        
class OperatorPar(OperatorBase):
    
    symbol: str = '('            # operator specifc opening symbol
    symbol_open: str = '('       # general opening symbol
    symbol_separator: str = ','  # argument separator
    symbol_close: str = ')'      # general closing symbol 
    narg: int = 1
    
    def __init__(self, expr:str):
        super().__init__(expr)
        depth=1
        self.args = []
        while depth>0:
            if len(expr.right)==0:
                raise Exception("Unclosed parenthesis in", expr.expr)
            elif expr.right.startswith(self.symbol) or expr.right.startswith(self.symbol_open):
                depth += 1
            elif expr.right.startswith(self.symbol_separator) and depth==1:
                expr.remove(self.symbol_separator)
                self.args.append(Expression(expr.pop_left()))                
            elif expr.right.startswith(self.symbol_close):
                depth -= 1
                if depth==0:
                    expr.remove(self.symbol_close)
                    self.args.append(Expression(expr.pop_left()))
                    break
            expr.shift()
        if len(self.args)!=self.narg:
            raise Exception("Wrong number of arguments:", expr.expr, len(self.args), self.narg)
        
    def operate_args(self, tokens):
        tokens.put_left(self.args[0])

class OperatorExp(OperatorPar):

    symbol: str = 'exp('

    def operate_args(self, tokens):
        tokens.put_left(tokens.atom(np.e)**self.args[0])        
            
class OperatorLog(OperatorPar):

    symbol: str = 'log('

    def operate_args(self, tokens):
        tokens.put_left(self.args[0].log())        

class OperatorLog10(OperatorPar):

    symbol: str = 'log10('

    def operate_args(self, tokens):
        tokens.put_left(self.args[0].log10())        

class OperatorSqrt(OperatorPar):

    symbol: str = 'sqrt('

    def operate_args(self, tokens):
        tokens.put_left(self.args[0].sqrt())        

class OperatorSin(OperatorPar):

    symbol: str = 'sin('

    def operate_args(self, tokens):
        tokens.put_left(self.args[0].sin())        

class OperatorCos(OperatorPar):

    symbol: str = 'cos('

    def operate_args(self, tokens):
        tokens.put_left(self.args[0].cos())        

class OperatorTan(OperatorPar):

    symbol: str = 'tan('

    def operate_args(self, tokens):
        tokens.put_left(self.args[0].tan())        

class OperatorLogb(OperatorPar):

    symbol: str = 'logb('
    narg: int = 2

    def operate_args(self, tokens):
        tokens.put_left(self.args[0].log()/self.args[1].log())        

class OperatorPowb(OperatorPar):

    symbol: str = 'pow('
    narg: int = 2

    def operate_args(self, tokens):
        tokens.put_left(self.args[0]**self.args[1])     
        
class OperatorAnd(OperatorBase):
    
    symbol: str = '&&'
    
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left.logical_and(right))

class OperatorOr(OperatorBase):
    
    symbol: str = '||'
    
    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left.logical_or(right))

class OperatorNot(OperatorBase):
    
    symbol: str = '!'
    
    def operate_unary(self, tokens):
        right = tokens.get_right()
        tokens.put_right(right.logical_not())
        
class OperatorEq(OperatorBase):

    symbol: str = '=='

    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left == right)

class OperatorNe(OperatorBase):

    symbol: str = '!='

    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left != right)

class OperatorLe(OperatorBase):

    symbol: str = '<='

    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left <= right)

class OperatorGe(OperatorBase):

    symbol: str = '>='

    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left >= right)

class OperatorLt(OperatorBase):

    symbol: str = '<'

    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left < right)

class OperatorGt(OperatorBase):

    symbol: str = '>'

    def operate_binary(self, tokens):
        left, right = tokens.get_left(), tokens.get_right()
        tokens.put_left(left > right)
