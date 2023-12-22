import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
    
def test_initialization():

    # Test initialization
    assert str(Fraction(2))     == "2"
    assert str(Fraction(0,3))   == "0"
    assert str(Fraction(1,3))   == "1:3"
    assert str(Fraction.from_tuple((1,2))) == "1:2"

def test_arithmetics():
    f1 = Fraction(1,3)
    f2 = Fraction(3,2)
    # with scalars
    assert str(f1+3)        == "10:3"
    assert str(f1-3)        == "-8:3"
    assert str(f1*3)        == "1"
    assert str(f1/3)        == "1:9"
    # with tuples
    assert str(f1+(3,2))    == "11:6"
    assert str(f1-(3,2))    == "-7:6"
    assert str(f1*(3,2))    == "1:2"
    assert str(f1/(3,2))    == "2:9"
    # with fractions
    assert str(f1+f2)       == "11:6"
    assert str(f1-f2)       == "-7:6"
    assert str(f1*f2)       == "1:2"
    assert str(f1/f2)       == "2:9"
    
def test_equality():
    
    fract1 = Fraction(4,4)
    fract2 = Fraction(1,1)
    assert fract1 == fract2