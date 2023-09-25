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
    
def test_values():
    
    m = Magnitude(30, 0.3)
    assert m.abse()  == 0.3
    assert m.rele()  == 1.0
    assert str(m.abse(0.5)) == "3.000(50)e+01"
    assert str(m.rele(30))  == "3.00(90)e+01"

def test_arithmetics():
    a = Magnitude(4, 0.01)
    b = Magnitude(1, 0.005)
    # addition
    assert str(a+b)    == "5.000(15)e+00"
    assert str(b+a)    == "5.000(15)e+00"
    assert str(a+3)    == "7.000(10)e+00"
    assert str(3+a)    == "7.000(10)e+00"
    # substraction
    assert str(a-b)    == "3.000(15)e+00"
    assert str(b-a)    == "-3.000(15)e+00"
    assert str(a-3)    == "1.000(10)e+00"
    assert str(3-a)    == "-1.000(10)e+00"
    assert str(-a)     == "-4.000(10)e+00"
    
    a = Magnitude(4, 0.05)
    b = Magnitude(7, 0.1)
    # multiplication
    assert str(a*b)    == "2.800(76)e+01"
    assert str(b*a)    == "2.800(76)e+01"
    assert str(a*5)    == "2.000(25)e+01"
    assert str(5*a)    == "2.000(25)e+01"
    
    a = Magnitude(12, 0.2)
    b = Magnitude(4, 0.1)
    # division
    assert str(a/b)    == "3.00(13)e+00"
    assert str(b/a)    == "3.33(14)e-01"
    assert str(a/6)    == "2.000(33)e+00"
    assert str(6/a)    == "5.000(85)e-01"
    # power
    assert str(a**2)   == "1.4400(40)e+02"
    
def test_numpy():
    
    a = Magnitude([12, 3], 0.2)
    b = Magnitude([2, 4], 0.1)
    assert str(a.value)  == "[12.  3.]"
    assert str(a.error)  == "[0.2 0.2]"
    assert str(a)        == "[1.200(20)e+01 3.00(20)e+00]"
    assert str(b)        == "[2.00(10)e+00 4.00(10)e+00]"
    assert str(a+b)      == "[1.400(30)e+01 7.00(30)e+00]"
    assert str(a*b)      == "[2.40(16)e+01 1.20(16)e+01]"
    assert str(a**2)     == "[1.4400(40)e+02 9.00(40)e+00]"

def test_quantities():
    
    m1 = Magnitude(12, 0.2)

    q1 = Quantity(m1, 'cm')
    q2 = Quantity(4, 'cm', abse=0.1)
    q3 = Quantity(4, 'cm', rele=10)
    q4 = Quantity(4, 'cm')
    q5 = Quantity([2, 4], 'cm', abse=0.1)
    
    assert str(q1)               == "Quantity(1.200(20)e+01 cm)"
    assert str(q2)               == "Quantity(4.00(10)e+00 cm)"
    assert str(q3)               == "Quantity(4.00(40)e+00 cm)"
    assert str(q4.abse(0.1))     == "Quantity(4.00(10)e+00 cm)"  # setting new Magnitude
    assert str(q4.rele(10))      == "Quantity(4.00(40)e+00 cm)"
    assert str(q4.abse(0.2))     == "Quantity(4.00(20)e+00 cm)"  # changing existing Mangitude error
    assert str(q4.rele(20))      == "Quantity(4.00(80)e+00 cm)"
    assert str(q5)               == "Quantity([2.00(10)e+00 4.00(10)e+00] cm)"
    
    assert str(q1+q2)  == "Quantity(1.600(30)e+01 cm)"
    assert str(q1*2)   == "Quantity(2.400(40)e+01 cm)"
    assert str(q1*q2)  == "Quantity(4.80(20)e+01 cm2)"
    assert str(q1**2)  == "Quantity(1.4400(40)e+02 cm2)"
    
    q = Quantity(30, 'cm', abse=0.3)
    assert q.abse()  == 0.3
    assert q.rele()  == 1.0
    assert str(q.abse(0.5)) == "Quantity(3.000(50)e+01 cm)"
    assert str(q.rele(30))  == "Quantity(3.00(90)e+01 cm)"