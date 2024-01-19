import numpy as np
import re

from .element import Element
from ..solver import *

class MaterialSolver:
    
    atom
    
    def __init__(self, atom:callable):
        self.atom = atom

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass

    def preprocess(self, expr):
        pattern = "(([A-Z]+[a-z]?|\[p\]|\[n\]|\[e\])(\{[0-9+-]+\}|)([0-9]*))"
        # insert implicit additions
        while True:
            expr_new = re.sub(pattern+"\s*"+pattern,"\g<1> + \g<5>",expr,count=1)
            if expr_new == expr:
                break
            else:
                expr = expr_new
        # insert implicit multiplications
        def repl1(m):
            if m.group(4):
                return m.group(2)+m.group(3)+CustomOperatorMul.symbol+m.group(4)
            else:
                return m.group(2)+m.group(3)
        expr = re.sub(pattern, repl1, expr)
        # insert implicit operation around parentheses
        def repl2(m):
            if m.group(1):
                return m.group(1) + CustomOperatorAdd.symbol + "("
            else:
                return m.group(2) + "("
        expr = re.sub("([^*+(\s]*)(\s*)\(", repl2, expr)
        def repl3(m):
            if m.group(1) and m.group(3):
                return ")" + CustomOperatorMul.symbol + m.group(1) + CustomOperatorAdd.symbol + m.group(3)
            elif m.group(1):
                return ")" + CustomOperatorMul.symbol + m.group(1)
            elif m.group(3):
                return ")" + CustomOperatorAdd.symbol + m.group(3)
            else:
                return ")"+m.group(2)
        expr = re.sub("\)([0-9]*)(\s*)([^+*)\s]*)", repl3, expr)
        return expr

    def solve(self, expr):
        expr_bak = expr

        # preprocess expression
        expr = self.preprocess(expr)
        # solve expression
        operators = {
            'par':OperatorPar,  # should be the last of parenthesis operators
            'mul':CustomOperatorMul,
            'add':CustomOperatorAdd, 
        }
        steps = [
            dict(operators=['par'],  otype=Otype.ARGS),
            dict(operators=['mul'],  otype=Otype.BINARY),
            dict(operators=['add'],  otype=Otype.BINARY),
        ]
        with ExpressionSolver(self.atom, operators, steps) as es:
            material = es.solve(expr)
            
        return material

class CustomOperatorAdd(OperatorAdd):
    symbol: str = ' + '

class CustomOperatorMul(OperatorMul):
    symbol: str = ' * '