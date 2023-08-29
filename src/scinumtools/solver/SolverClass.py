from typing import Union

from .OperatorClass import *
from .ExpressionClass import Expression
from .TokensClass import Tokens

class ExpressionSolver:

    tokens: list
    operators: list
    expr: Expression
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass
    
    def __init__(self, atom, operators:list = None):
        self.tokens = Tokens(atom)
        self.operators = operators if operators else [
            OperatorLog, OperatorLog10, OperatorLogb,
            OperatorExp, OperatorSqrt, OperatorPowb,
            OperatorSin, OperatorCos, OperatorTan,
            OperatorPar,  # should be the last of parenthesis operators
            OperatorPow,
            OperatorMul, OperatorTruediv,
            OperatorAdd, OperatorSub,
            OperatorEq, OperatorNe,
            OperatorNot,  # needs to be after OperatorNe
            OperatorLe, OperatorGe,
            OperatorLt, OperatorGt,
            OperatorAnd, OperatorOr, 
        ]

    def solve(self, expr:Union[str,Expression]):
        self.expr = Expression(expr) if isinstance(expr, str) else expr
        
        # Tokenize expression
        while self.expr.right:
            for operator in self.operators:
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
        osteps = [
            dict(operators=[
                OperatorLog, OperatorLog10, OperatorLogb,
                OperatorExp, OperatorSqrt, OperatorPowb,
                OperatorSin, OperatorCos, OperatorTan,
                OperatorPar
            ], otype=Otype.ARGS),
            dict(operators=[OperatorAdd, OperatorSub],     otype=Otype.UNARY),
            dict(operators=[OperatorPow],                  otype=Otype.BINARY),
            dict(operators=[OperatorMul, OperatorTruediv], otype=Otype.BINARY),
            dict(operators=[OperatorAdd, OperatorSub],     otype=Otype.BINARY),
            dict(operators=[
                OperatorEq, OperatorNe,
                OperatorLe, OperatorGe,
                OperatorLt, OperatorGt,
            ], otype=Otype.BINARY),
            dict(operators=[OperatorNot],                  otype=Otype.UNARY),
            dict(operators=[OperatorAnd],                  otype=Otype.BINARY),
            dict(operators=[OperatorOr],                   otype=Otype.BINARY),
        ]
        for o,ostep in enumerate(osteps):
            ostep['operators'] = tuple([o for o in ostep['operators'] if o in self.operators])
            if ostep['operators']:
                self.tokens.operate(**ostep)

        # Return the final atom
        if len(self.tokens.left)>0 or len(self.tokens.right)>1:
            raise Exception("Cannot solve expression due to unprocessed tokens:", self.tokens.left, self.tokens.right)
        atom = self.tokens.get_right()
        #print(self.expr.expr, atom)
        return atom
