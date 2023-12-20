import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.solvers import LogicalSolver
from scinumtools.dip.datatypes import BooleanType

def test_or_and():
    with LogicalSolver() as p:
        assert p.solve('true || true || true')    == BooleanType(True)
        assert p.solve('false || true || false')  == BooleanType(True)
        assert p.solve('false || false || false') == BooleanType(False)
        assert p.solve('true && true && true')    == BooleanType(True)
        assert p.solve('true && false && true')   == BooleanType(False)
        assert p.solve('false && false && false') == BooleanType(False)
        assert p.solve('true && true && true || false || false') == BooleanType(True)
        assert p.solve('false || true && false && true || true') == BooleanType(True)
        assert p.solve('false || false || true && false && true') == BooleanType(False)

def test_parenthesis():
    with LogicalSolver() as p:
        assert p.solve('(true || false) && true && true') == BooleanType(True)
        assert p.solve('true && (true && false) && true') == BooleanType(False)
        assert p.solve('false || false || (true || false)') == BooleanType(True)
        assert p.solve('false || (true || false) && true') == BooleanType(True)
        assert p.solve('false || true && (false || false)') == BooleanType(False)
        assert p.solve('false || ((false||true) || false) && (true||false)') == BooleanType(True)

def test_compare_nodes():
    with DIP() as dip:
        dip.add_string("""
        dogs int = 23
        cats int = 44
        birds int = 23
        fish int = 12
        animal bool = true
        """)
        env = dip.parse()
    with LogicalSolver(env) as p:
        # node pair comparison
        assert p.solve('{?dogs} == {?cats}') == BooleanType(False)
        assert p.solve('{?dogs} == {?birds}') == BooleanType(True)
        assert p.solve('{?dogs} != {?cats}') == BooleanType(True)
        assert p.solve('{?dogs} != {?birds}') == BooleanType(False)
        assert p.solve('{?dogs} <= {?cats}') == BooleanType(True)
        assert p.solve('{?dogs} <= {?birds}') == BooleanType(True)
        assert p.solve('{?dogs} <= {?fish}') == BooleanType(False)
        assert p.solve('{?dogs} >= {?cats}') == BooleanType(False)
        assert p.solve('{?dogs} >= {?birds}') == BooleanType(True)
        assert p.solve('{?dogs} >= {?fish}') == BooleanType(True)
        assert p.solve('{?dogs} <  {?cats}') == BooleanType(True)
        assert p.solve('{?dogs} <  {?fish}') == BooleanType(False)
        assert p.solve('{?dogs} >  {?fish}') == BooleanType(True)
        assert p.solve('{?dogs} >  {?cats}') == BooleanType(False)
        # single bool node
        assert p.solve('{?animal}') == BooleanType(True)
        assert p.solve('~{?animal}') == BooleanType(False)   # negated value
        # is node defined
        assert p.solve('!{?dogs}') == BooleanType(True)
        assert p.solve('!{?elefant}') == BooleanType(False)
        assert p.solve('!{?elefant} == false') == BooleanType(True)
        assert p.solve('~!{?elefant}') == BooleanType(True)  # negated value

def test_compare_values():
    with DIP() as dip:
        dip.add_string("""
    weight float = 57.3 kg
        """)
        env = dip.parse()
    with LogicalSolver(env) as p:
        # comparison with the same units
        assert p.solve('{?weight} == 57.30 kg') == BooleanType(True)
        assert p.solve('{?weight} == 57.31 kg') == BooleanType(False)
        assert p.solve('{?weight} != 57.30 kg') == BooleanType(False)
        assert p.solve('{?weight} != 57.31 kg') == BooleanType(True)
        assert p.solve('{?weight} <= 57.30 kg') == BooleanType(True)
        assert p.solve('{?weight} <= 60 kg') == BooleanType(True)
        assert p.solve('{?weight} <= 50 kg') == BooleanType(False)
        # comparison with different units
        assert p.solve('{?weight} >= 57300 g') == BooleanType(True)
        assert p.solve('{?weight} >= 50000 g') == BooleanType(True)
        assert p.solve('{?weight} >= 60000 g') == BooleanType(False)
        assert p.solve('{?weight} > 50000 g') == BooleanType(True)
        assert p.solve('{?weight} > 60000 g') == BooleanType(False)
        # comparison without specifying units
        assert p.solve('{?weight} < 50') == BooleanType(False)
        assert p.solve('{?weight} < 60') == BooleanType(True)

def test_combination():
    with DIP() as dip:
        dip.add_string("""
    size float = 34 cm
    geometry int = 2
      = 1 # line
      = 2 # square
      = 3 # cube
    filled bool = true
    dimension int = 2
        """)
        env = dip.parse()
    with LogicalSolver(env) as p:
        assert p.solve("""
        {?size} > 30 cm 
        || ({?size} < 0.4 m || {?size} >= 34) 
        && ({?geometry} == 1 && {?geometry}<={?dimension})
        && {?filled}
        || ~!{?color}
        """) == BooleanType(True)
        
if __name__ == "__main__":
    # Specify wich test to run
    test = sys.argv[1] if len(sys.argv)>1 else True

    # Loop through all tests
    for fn in dir(sys.modules[__name__]):
        if fn[:5]=='test_' and (test is True or test==fn[5:]):
            print(f"\nTesting: {fn}\n")
            locals()[fn]()
