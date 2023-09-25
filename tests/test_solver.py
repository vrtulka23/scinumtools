import numpy as np
import os
import pytest
import sys
sys.path.insert(0, 'src')

from scinumtools.solver import *

def test_solver_basic():

    expressions = {
        '1+2':           1+2,
        '1-2':           1-2,
        '1*2':           1*2,
        '1/2':           1/2,
        '((2+3) /(3) )': ((2+3) / 3 ),
        "1 * ((2+3) / +3 - -10 ) + (-23 *++2) + 23**2":
        1 * ((2+3) / +3 - -10 ) + (-23 *++2) + 23**2
    }
    with ExpressionSolver(AtomBase) as es:
        for expr, value in expressions.items():
            result = es.solve(expr).value
            assert np.isclose(result, value)
        
def test_solver_math():

    expressions = {
        'exp(23+3)':          np.exp(23+3),
        'log(23+3)':          np.log(23+3),
        'log10(23+3)':        np.log10(23+3),
        'sqrt(23+3)':         np.sqrt(23+3),
        'sin(23+3)':          np.sin(23+3),
        'cos(23+3)':          np.cos(23+3),
        'tan(23+3)':          np.tan(23+3),
        'logb(23+3, 10)':     np.log(23+3)/np.log(10),
        'pow(23+3, 2)':       np.power(23+3, 2),
        '3*1+6/4*sin(34)':    3*1+6/4*np.sin(34),
        'sin(cos(23))':       np.sin(np.cos(23)),
        'pow((23+3), (2*4))': np.power((23+3), (2*4)),
    }
    with ExpressionSolver(AtomBase) as es:
        for expr, value in expressions.items():
            result = es.solve(expr).value
            assert np.isclose(result, value)
            
def test_solver_logical():

    expressions = {
        '1 && 1':    1 and 1,
        '1 && 0':    1 and 0,
        '0 && 0':    0 and 0,
        '1 || 1':    1 or 1,
        '1 || 0':    1 or 0,
        '0 || 0':    0 or 0,
        '!1':        not 1,
        '!0':        not 0,
        '1 && 0 || 1 && !0 && 1 || 0': 1 and 0 or 1 and not 0 and 1 or 0,
        '1-1 && (1*32)/2 || sin(3)':   1-1 and (1*32)/2 or np.sin(3),
    }
    with ExpressionSolver(AtomBase) as es:
        for expr, value in expressions.items():
            result = es.solve(expr)
            assert np.isclose(result.value, value)
            
def test_solver_logical():

    expressions = {
        '1 == 1':    1 == 1,
        '1 == 0':    1 == 0,
        '1 != 1':    1 != 1,
        '1 != 0':    1 != 0,
        '23 <= 45':  23 <= 45,
        '45 <= 45':  45 <= 45,
        '81 <= 45':  81 <= 45,
        '23 >= 45':  23 >= 45,
        '45 >= 45':  45 >= 45,
        '81 >= 45':  81 >= 45,
        '23 < 45':   23 < 45,
        '45 < 45':   45 < 45,
        '81 < 45':   81 < 45,
        '23 > 45':   23 > 45,
        '45 > 45':   45 > 45,
        '81 > 45':   81 > 45,
        'sin(23) < 1 && 3*2 == 6 || !(23 > 43) && cos(0) == 1':
        np.sin(23) < 1 and 3*2 == 6 or not (23 > 43) and np.cos(0) == 1
    }
    with ExpressionSolver(AtomBase) as es:
        for expr, value in expressions.items():
            result = es.solve(expr)
            assert result.value == value

def test_solver_atom():

    foo = 3
    bar = 4
    
    class Atom(AtomBase):
        
        def __init__(self, value:str):
            if value=='foo':
                self.value = foo
            elif value=='bar':
                self.value = bar
            else:
                self.value = float(value)
                
    expressions = {
        'foo < bar && foo * bar == 12':    foo < bar and foo*bar==12,
        'foo*bar**(2-233)':                foo*bar**(2-233),
        'sin(foo)':                        np.sin(foo),
    }
    with ExpressionSolver(Atom) as es:
        for expr, value in expressions.items():
            result = es.solve(expr)
            assert result.value == value
    
def test_operator_selection():

    expressions = {
        '23 > 4':    23 > 4,
        '20 == 20':  20. == 20.,
    }
    
    # specify operators
    operators = {'gt':OperatorGt,'eq':OperatorEq}
    with ExpressionSolver(AtomBase, operators) as es:
        for expr, value in expressions.items():
            result = es.solve(expr)
            assert result.value == value

    # throw error if operator is not specified
    operators = {'log':OperatorLog}
    with ExpressionSolver(AtomBase, operators) as es:
        for expr, value in expressions.items():
            with pytest.raises(ValueError) as excinfo:
                result = es.solve(expr)
            assert str(excinfo.value)==f"could not convert string to float: '{expr}'"

def test_operator_modification():

    # modify existing operators
    class CustomOperatorNot(OperatorNot):
        symbol: str = 'not'
    operators = {'not':CustomOperatorNot}
    with ExpressionSolver(AtomBase, operators) as es:
        result = es.solve('not 1')
        assert result.value == False
    
def test_custom_operator():
    
    # create a new operator
    class OperatorSquare(OperatorBase):   # operate from left side
        symbol: str = '~'
        def operate_unary(self, tokens):
            right = tokens.get_right()
            tokens.put_left(right*right)
    class OperatorCube(OperatorBase):     # operate from right side
        symbol: str = '^'
        def operate_unary(self, tokens):
            left = tokens.get_left()
            tokens.put_left(left*left*left)
    operators = {'square':OperatorSquare,'cube':OperatorCube,'add':OperatorAdd}
    with ExpressionSolver(AtomBase, operators) as es:
        osteps = [
            dict(operators=['square','cube'], otype=Otype.UNARY),
            dict(operators=['add'],           otype=Otype.BINARY),
        ]
        result = es.solve('~3 + 2^', osteps)
        assert result.value == 17
        
def test_custom_atom():
    
    # modify atom to operate with strings
    class AtomCustom(AtomBase):
        value: str
        def __init__(self, value:str):
            self.value = str(value)
        def __add__(self, other):
            return AtomCustom(self.value + other.value)
        def __gt__(self, other):
            return AtomCustom(len(self.value) > len(other.value))
    operators = {'add':OperatorAdd,'gt':OperatorGt}
    with ExpressionSolver(AtomCustom, operators) as es:
        # test simpple functions
        result = es.solve('foo + bar')
        assert result.value == 'foobar'
        
        # test multiple functions
        osteps = [
            dict(operators=['add'],  otype=Otype.BINARY),
            dict(operators=['gt'],   otype=Otype.BINARY),
        ]
        result = es.solve("limit + 100 km/s > limit + 50000000000 km/s", osteps)
        assert result.value == 'False' # AtomCustom returns strings
        
def test_customisation_in_parentheses():
    
    # modify atom to operate with strings
    class AtomCustom(AtomBase):
        value: str
        def __init__(self, value:str):
            self.value = str(value)
        def __add__(self, other):
            return AtomCustom(self.value + other.value)
        def __gt__(self, other):
            return AtomCustom(len(self.value) > len(other.value))
    operators = {'add':OperatorAdd,'gt':OperatorGt,'par':OperatorPar}
    with ExpressionSolver(AtomCustom, operators) as es:
        # test multiple functions
        osteps = [
            dict(operators=['par'],  otype=Otype.ARGS),
            dict(operators=['add'],  otype=Otype.BINARY),
            dict(operators=['gt'],   otype=Otype.BINARY),
        ]
        result = es.solve("(limit + 100 km/s) > (limit + 50000000000 km/s)", osteps)
        assert result.value == 'False' # AtomCustom returns strings