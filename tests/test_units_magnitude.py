import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
    
def test_initialization():
    assert str(Magnitude(1))           == "1.000e+00"           # no error
    assert str(Magnitude(32, 0.3))     == "3.200(30)e+01"       # absolute error
    assert str(Magnitude(32, 3e-6))    == "3.20000000(30)e+01"    
    assert str(Magnitude(32, rele=10)) == "3.20(32)e+01"        # relative error
    
def test_arithmetics():
    a = Magnitude(4, 0.01)
    b = Magnitude(1, 0.005)
    
    assert str(a+b)    == "5.000(15)e+00"
    assert str(b+a)    == "5.000(15)e+00"
    assert str(a+3)    == "7.000(10)e+00"
    assert str(3+a)    == "7.000(10)e+00"
    
    assert str(a-b)    == "3.000(15)e+00"
    assert str(b-a)    == "-3.000(15)e+00"
    assert str(a-3)    == "1.000(10)e+00"
    assert str(3-a)    == "-1.000(10)e+00"
    
    a = Magnitude(4, 0.05)
    b = Magnitude(7, 0.1)
    
    assert str(a*b)    == "2.800(76)e+01"
    assert str(b*a)    == "2.800(76)e+01"
    assert str(a*5)    == "2.000(25)e+01"
    assert str(5*a)    == "2.000(25)e+01"
    
    a = Magnitude(12, 0.2)
    b = Magnitude(4, 0.1)

    assert str(a/b)    == "3.00(13)e+00"
    assert str(b/a)    == "3.33(14)e-01"
    assert str(a/6)    == "2.000(33)e+00"
    assert str(6/a)    == "5.000(85)e-01"
