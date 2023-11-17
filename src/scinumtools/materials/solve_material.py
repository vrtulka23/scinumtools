import numpy as np
import re

from ..solver import *
from .material_part import MaterialPart
from .list_elements import *

class MaterialSolver:
    
    def __init__(self):
        pass

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass

    def _parse_atom(self, expr):
        # Match numbers
        if m := re.match('[0-9]+', expr):
            return int(expr.strip())
            
        # Match elements
        pattern = "([A-Z]+[a-z]?)(\{([0-9]*)([+-]?[0-9]*)\}|)"
        if m := re.match(pattern, expr):
            exceptions = {
                'H': ('H',1,1),
                'D': ('H',1,2),
                'T': ('H',1,3),
            }
            # parse atom and mass numbers
            if not m.group(3) and m.group(1) in exceptions:
                S, Z, A = exceptions[m.group(1)]
            elif m.group(1) in ELEMENTS:
                S = m.group(1)
                Z = ELEMENTS[S][0]
                A = int(m.group(3)) if m.group(3) else Z*2
            else:
                raise Exception("Unknown element:", m.group(1))
            # parse ionization state
            if m.group(4) in ['-','+']:
                I = int(m.group(4)+'1')
            elif m.group(4):
                I = int(m.group(4))
            else:
                I = 0
            # parse mass
            M = ELEMENTS[S][2][str(A)][0] + I * NUCLEONS['[e]'][3]
            return MaterialPart(Z, M, A-Z, Z+I)
        elif expr in NUCLEONS:
            Z, N, E, M, name = NUCLEONS[expr]
            return MaterialPart(Z, M, N, E)
        else:
            raise Exception("Atom canot be parsed from given string:", expr)

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
        with ExpressionSolver(self._parse_atom, operators, steps) as es:
            material = es.solve(expr)
            
        return material

class CustomOperatorAdd(OperatorAdd):
    symbol: str = ' + '

class CustomOperatorMul(OperatorMul):
    symbol: str = ' * '