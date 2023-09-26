import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
from scinumtools.units.unit_solver import AtomParser, Atom

def test_atom():
    
    a = Atom(3e2, {'k:g':Fraction(2),'m':Fraction(3,2)})
    assert str(a)    == "Atom(3.000e+02 kg=2 m=3:2)"
    assert str(a*a)  == "Atom(9.000e+04 kg=4 m=3)"
    assert str(a/a)  == "Atom(1.000e+00)"

def test_atom_parser():
    
    assert str(AtomParser("kg2"))    == "Atom(1.000e+00 kg=2)"

def test_quantity():
    
    assert str(UnitSolver("kg*m2/s2"))         == "Atom(1.000e+00 kg=1 m=2 s=-2)"
    assert str(UnitSolver("12/4*kg/(m2*s2)"))  == "Atom(3.000e+00 kg=1 m=-2 s=-2)"
