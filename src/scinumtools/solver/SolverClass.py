from typing import Union

from .OperatorClass import *
from .ExpressionClass import Expression
from .TokensClass import Tokens

class ExpressionSolver:

    tokens: list
    operators: dict
    expr: Expression
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass
    
    def __init__(self, atom, operators:dict = None):
        self.tokens = Tokens(atom)
        self.operators = operators if operators else {
            'log':OperatorLog, 'log10':OperatorLog10, 'logb':OperatorLogb,
            'exp':OperatorExp, 'sqrt':OperatorSqrt,   'powb':OperatorPowb,
            'sin':OperatorSin, 'cos':OperatorCos,     'tan':OperatorTan,
            'par':OperatorPar,  # should be the last of parenthesis operators
            'pow':OperatorPow,
            'mul':OperatorMul, 'truediv':OperatorTruediv,
            'add':OperatorAdd, 'sub':OperatorSub,
            'eq':OperatorEq,   'ne':OperatorNe,
            'not':OperatorNot,  # needs to be after OperatorNe
            'le':OperatorLe,   'ge':OperatorGe,
            'lt':OperatorLt,   'gt':OperatorGt,
            'and':OperatorAnd, 'or':OperatorOr, 
        }

    def solve(self, expr:Union[str,Expression], osteps:list = None):
        self.expr = Expression(expr) if isinstance(expr, str) else expr
        
        # Tokenize expression
        while self.expr.right:
            for operator in self.operators.values():
                if self.expr.right.startswith(operator.symbol):
                    # Create atom from the left side and append it to tokens
                    if left:=self.expr.pop_left():
                        self.tokens.append(self.tokens.atom(left))
                    # Initialize an operator
                    op = operator(self.expr)
                    if op.args:
                        # Solve operator arguments
                        with ExpressionSolver(self.tokens.atom) as es:
                            for a in range(len(op.args)):
                                op.args[a] = es.solve(op.args[a])
                    # Append operator to tokens
                    self.tokens.append(op)
                    break
            else:
                self.expr.shift()
        # Create atom from the remaining left side
        if left:=self.expr.pop_left():
            self.tokens.append(self.tokens.atom(left))

        # Perform operation steps
        osteps = osteps if osteps else [
            dict(operators=['log', 'log10', 'logb', 'exp', 'sqrt', 'powb', 'sin', 'cos', 'tan', 'par'], otype=Otype.ARGS),
            dict(operators=['add', 'sub'],     otype=Otype.UNARY),
            dict(operators=['pow'],            otype=Otype.BINARY),
            dict(operators=['mul', 'truediv'], otype=Otype.BINARY),
            dict(operators=['add', 'sub'],     otype=Otype.BINARY),
            dict(operators=['eq', 'ne', 'le', 'ge', 'lt', 'gt'], otype=Otype.BINARY),
            dict(operators=['not'],            otype=Otype.UNARY),
            dict(operators=['and'],            otype=Otype.BINARY),
            dict(operators=['or'],             otype=Otype.BINARY),
        ]
        for o,ostep in enumerate(osteps):
            ostep['operators'] = tuple([self.operators[o] for o in ostep['operators'] if o in self.operators.keys()])
            if ostep['operators']:
                self.tokens.operate(**ostep)

        # Return the final atom
        if len(self.tokens.left)>0 or len(self.tokens.right)>1:
            raise Exception("Cannot solve expression due to unprocessed tokens:", self.tokens.left, self.tokens.right)
        atom = self.tokens.get_right()
        #print(self.expr.expr, atom)
        return atom
