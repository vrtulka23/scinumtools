import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
    
def test_array_arithmetics():

    # Test basic arithmetics
    q = Quantity([2,3,4], 'm')
    assert str(q) == "Quantity([2. 3. 4.] m)"
    q += Quantity(2, 'm')
    assert str(q) == "Quantity([4. 5. 6.] m)"
    q -= Quantity(2, 'm')
    assert str(q) == "Quantity([2. 3. 4.] m)"
    q /= Quantity(2)
    assert str(q) == "Quantity([1.  1.5 2. ] m)"
    q *= Quantity(2)
    assert str(q) == "Quantity([2. 3. 4.] m)"
    q /= 2
    assert str(q) == "Quantity([1.  1.5 2. ] m)"
    q *= 2
    assert str(q) == "Quantity([2. 3. 4.] m)"
    q /= [1, 1.5, 2]
    assert str(q) == "Quantity([2. 2. 2.] m)"
    q *= [1, 1.5, 2]
    assert str(q) == "Quantity([2. 3. 4.] m)"
    q = q ** 10
    assert str(q) == "Quantity([1.024e+03 5.905e+04 1.049e+06] m10)"

def test_array_slicing():

    # Array slicing
    q = Quantity([1,2,3], 'm')
    assert str(q[:2])              == "Quantity([1. 2.] m)"
    assert str(q.value(dtype=int)) == "[1 2 3]"

def test_array_unit_conversion():

    # Test unit conversion on arrays
    assert str(Quantity([1,2,3], 'm').to('km')) == "Quantity([0.001 0.002 0.003] km)"
    
def test_numpy_functions():
    
    # Test numpy functions
    assert str(np.sqrt(Quantity(4, 'm2')))             == "Quantity(2.000e+00 m)"
    assert str(np.sqrt(Quantity([4, 9, 16], 'm2')))    == "Quantity([2. 3. 4.] m)"
    assert str(np.sqrt(Quantity([4, 9, 16], 'm3')))    == "Quantity([2. 3. 4.] m3:2)"
    assert str(np.sqrt(Quantity([4, 9, 16], 'm-3')))   == "Quantity([2. 3. 4.] m-3:2)"
    assert str(np.sqrt(Quantity([4, 9, 16], 'm2:3')))  == "Quantity([2. 3. 4.] m1:3)"
    assert str(np.sqrt(Quantity([4, 9, 16], 'm2:3*g3:5*s5')))  == "Quantity([2. 3. 4.] m1:3*g3:10*s5:2)"
    assert str(np.cbrt(Quantity([8, 27, 64], 'm3')))   == "Quantity([2. 3. 4.] m)"
    assert str(np.power(Quantity([2, 3, 4], 'm'),3))   == "Quantity([ 8. 27. 64.] m3)"
    assert str(np.sin(Quantity([45, 60], "deg")))      == "Quantity([0.707 0.866])"
    assert str(np.cos(Quantity([45, 60], "deg")))      == "Quantity([0.707 0.5  ])"
    assert str(np.tan(Quantity([45, 60], "deg")))      == "Quantity([1.    1.732])"
    assert str(np.arcsin(Quantity([0.3, -0.7])))       == "Quantity([ 0.305 -0.775] rad)"
    assert str(np.arccos(Quantity([0.3, -0.7])))       == "Quantity([1.266 2.346] rad)"
    assert str(np.arctan(Quantity([0.3, -0.7])))       == "Quantity([ 0.291 -0.611] rad)"
    assert str(np.linspace(0,Quantity(20,'m'),3))      == "Quantity([ 0. 10. 20.] m)"
    assert str(np.linspace(Quantity(10,'m'),Quantity(0.03,'km'),3))  == "Quantity([10. 20. 30.] m)"
    assert str(np.absolute(Quantity(-3,'m')))          == "Quantity(3.000e+00 m)"
    assert str(np.linspace(0,Quantity(23,'km'),3))     == "Quantity([ 0.  11.5 23. ] km)"
    assert str(np.logspace(1,Quantity(3,'m'),3))       == "Quantity([  10.  100. 1000.] m)"
    assert str(np.absolute(Quantity(-3,'m')))          == "Quantity(3.000e+00 m)"
    assert str(np.abs(Quantity(-3,'m')))               == "Quantity(3.000e+00 m)"
    assert str(np.round(Quantity(2.3,'m')))            == "Quantity(2.000e+00 m)"
    assert str(np.floor(Quantity(2.3,'m')))            == "Quantity(2.000e+00 m)"
    assert str(np.ceil(Quantity(2.3,'m')))             == "Quantity(3.000e+00 m)"

def test_numpy_nan():

    assert str(NaN()) == "Quantity(nan)"
    assert str(NaN('cm')) == "Quantity(nan cm)"

def test_array_operation_sides():
    
    p = Quantity([2,3,4], 'm')
    q = Quantity([5,6,7], 'm')
    assert p+q == q+p
    assert p-q == -(q-p)
    assert q*2 == 2*q
    assert p/2 == 1/(2/p)