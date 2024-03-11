import numpy as np
import re

from .substance import Substance
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
        PATTERN_NUMBER = "([0-9]+(\.([0-9]+([eE]{1}[+-]?[0-9]{0,3}|)|)|))"
        PATTERN_MOLECULE = "(\<[^\<\>]+\>)"
        def repl1(m):
            return m.group(1)+CustomOperatorMul.symbol+m.group(5)
        expr = re.sub(PATTERN_NUMBER+"\s*"+PATTERN_MOLECULE, repl1, expr)
        def repl1(m):
            return m.group(1)+CustomOperatorAdd.symbol+m.group(2)
        expr = re.sub(PATTERN_MOLECULE+"\s*"+PATTERN_NUMBER, repl1, expr)
        def repl1(m):
            return m.group(1)+CustomOperatorAdd.symbol+m.group(2)
        expr = re.sub(PATTERN_MOLECULE+"\s*"+PATTERN_MOLECULE, repl1, expr)
        return expr

    def solve(self, expr):
        expr_bak = expr

        # preprocess expression
        expr = self.preprocess(expr)
        # solve expression
        operators = {
            'par':CustomOperatorPar,  # should be the last of parenthesis operators
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

class CustomOperatorPar(OperatorPar):
    symbol: str = '<'            # operator specifc opening symbol
    symbol_open: str = '<'       # general opening symbol
    symbol_separator: str = ','  # argument separator
    symbol_close: str = '>'      # general closing symbol 

class CustomOperatorAdd(OperatorAdd):
    symbol: str = ' + '

class CustomOperatorMul(OperatorMul):
    symbol: str = ' * '