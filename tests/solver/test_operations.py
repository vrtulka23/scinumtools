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
