import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
    
def test_fractions():

    # Test initialization
    assert str(Fraction(2))   == "2"
    assert str(Fraction(0,3)) == "0"
    assert str(Fraction(1,3)) == "1:3"

    # Test arithmetics
    assert str(Fraction(1,3)+3)             == "10:3"
    assert str(Fraction(1,3)+(3,2))         == "11:6"
    assert str(Fraction(1,3)+Fraction(3,2)) == "11:6"
    assert str(Fraction(1,3)-3)             == "-8:3"
    assert str(Fraction(1,3)-(3,2))         == "-7:6"
    assert str(Fraction(1,3)-Fraction(3,2)) == "-7:6"
    assert str(Fraction(1,3)*3)             == "1"
    assert str(Fraction(1,3)*(3,2))         == "1:2"
    assert str(Fraction(1,3)*Fraction(3,2)) == "1:2"
    assert str(Fraction(1,3)/3)             == "1:9"
    assert str(Fraction(1,3)/(3,2))         == "2:9"
    assert str(Fraction(1,3)/Fraction(3,2)) == "2:9"