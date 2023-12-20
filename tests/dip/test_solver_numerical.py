import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.solvers import NumericalSolver

def test_plus_minus():
    with NumericalSolver() as p:
        assert p.equal('2 + 4 - 3',                '3')           # numbers only
        assert p.equal('1 - -3 + -4',              '0')           # negative values and zeros
        assert p.equal('34 cm + 4 mm',             '34.4 cm')     # addition
        assert p.equal('10 m + 4 cm + 3 m + 1 mm', '13.041 m')    # multiple additions
        assert p.equal('3 m - 5 cm',               '295 cm')      # substraction
        assert p.equal('10 m - 1 m + 3 cm - 3 mm', '9.027 m')     # multiple substractions
        assert p.equal('23 kg*m*s-2',              '23 kg*m*s-2') # complex units with -
    with pytest.raises(Exception) as e_info:
        p.solve('10 m + 1 J')
    assert e_info.value.args[0] == "Unsupported conversion between units:"
    with pytest.raises(Exception) as e_info:
        p.solve('10 m - 1 J')
    assert e_info.value.args[0] == "Unsupported conversion between units:"

def test_times_divide():
    with NumericalSolver() as p:
        assert p.equal('8 / 4 * 3',                    '6')          # numbers only
        assert p.equal('2 * 3 * 4',                    '24')         # multiple *
        assert p.equal('8 / 2 / 4',                    '1')          # multiple /
        assert p.equal('-8 / 2 * -4',                  '16')         # negative values
        assert p.equal('10 m * 2 cm',                  '0.2 m2')     # * with dimensional values
        assert p.equal('4 cm2 + 10 m * 2 cm - 0.2 m2', '0.0004 m2')  # * within + -
        assert p.equal('10 m2 / 200 cm',               '50 dm')      # / with dimensional values
        assert p.equal('4 m2 + 10 m3 / 2 m - 3 m2',    '6 m2')       # / within + -
        assert p.equal('3 kg * 4 m2 / 2 s2 + 1e7 erg', '7 J')        # combination of * /
        assert p.equal('23 kg*m2/s2 * 2',              '46 J')       # complex units with *
        assert p.equal('23 kg*m2/s2 / 2 J',            '11.5')       # complex units with /
        
def test_parenthesis():
    with NumericalSolver() as p:
        assert p.equal('(10 m - 1 m) + 3 cm - 3 mm',       '9.027 m')  # at the begining
        assert p.equal('10 m - (1 m + 3 cm) - 3 mm',       '8.967 m')  # in the middle
        assert p.equal('10 m - (1 m + 3 cm - 3 mm)',       '8.973 m')  # at the end
        assert p.equal('4 m2 + 10000 mm * (300 cm - 1 m)', '24 m2')    # after *
        assert p.equal('36 m2 / (20 dm * 300 cm) - 1',     '5')        # after \
        assert p.equal('(2 + (3 - 4))',                    '1')        # nested

def test_functions():
    with NumericalSolver() as p:
        # unary operations
        assert p.equal('exp(10 m / 5 cm)',    '7.22597376e86')   
        assert p.equal('log(10 m / 5 cm)',     '5.298317')   
        assert p.equal('log10(10 m / 5 cm)',  '2.301029995')   
        assert p.equal('sin(10 m / 5 cm)',    '-0.873297297')   
        assert p.equal('cos(10 m / 5 cm)',    '0.4871876750')   
        # binary operations
        assert p.equal('pow(10 m, 2)',        '100 m2')   

def test_references():
    with DIP() as dip:
        dip.add_string("""
a float = 10 m
b float = 300 cm
        """)
        env = dip.parse()
    with NumericalSolver(env) as p:
        assert p.equal('3 m * log10({?a} / (7 cm - 20 mm)) + {?b}', '9.9030899 m')
        
if __name__ == "__main__":
    # Specify wich test to run
    test = sys.argv[1] if len(sys.argv)>1 else True

    # Loop through all tests
    for fn in dir(sys.modules[__name__]):
        if fn[:5]=='test_' and (test is True or test==fn[5:]):
            print(f"\nTesting: {fn}\n")
            locals()[fn]()
