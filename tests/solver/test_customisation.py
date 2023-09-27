import numpy as np
import os
import pytest
import sys
sys.path.insert(0, 'src')

from scinumtools.solver import *

def test_custom_atom1():

    # test with external variables
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
        
def test_custom_atom2():
    
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
    # test simpple functions
    with ExpressionSolver(AtomCustom, operators) as es:
        result = es.solve('foo + bar')
        assert result.value == 'foobar'
        
    steps = [
        dict(operators=['add'],  otype=Otype.BINARY),
        dict(operators=['gt'],   otype=Otype.BINARY),
    ]
    # test multiple functions
    with ExpressionSolver(AtomCustom, operators, steps) as es:
        result = es.solve("limit + 100 km/s > limit + 50000000000 km/s")
        assert result.value == 'False' # AtomCustom returns strings
    
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
    steps = [
        dict(operators=['square','cube'], otype=Otype.UNARY),
        dict(operators=['add'],           otype=Otype.BINARY),
    ]
    with ExpressionSolver(AtomBase, operators, steps) as es:
        result = es.solve('~3 + 2^')
        assert result.value == 17
        
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
    steps = [
        dict(operators=['par'],  otype=Otype.ARGS),
        dict(operators=['add'],  otype=Otype.BINARY),
        dict(operators=['gt'],   otype=Otype.BINARY),
    ]
    with ExpressionSolver(AtomCustom, operators, steps) as es:
        # test multiple functions
        result = es.solve("(limit + 100 km/s) > (limit + 50000000000 km/s)")
        assert result.value == 'False' # AtomCustom returns strings