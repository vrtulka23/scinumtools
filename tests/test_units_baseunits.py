import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *

def test_base_units():

    # Test simplification
    bu = BaseUnits({'g':(3,2), 'km': 3, '[m_p]': (3,1)})
    assert str(bu) == "BaseUnits(g=3:2 km=3 [m_p]=3)"

    # Test arithmetics
    bu1 = BaseUnits({'km':3,'g':(3,2)})
    bu2 = BaseUnits({'km':2,'g':(4,7)})
    assert not bu1 == bu2
    assert str(bu1+bu2)  == "BaseUnits(km=5 g=29:14)"
    assert str(bu1-bu2)  == "BaseUnits(km=1 g=13:14)"
    assert str(bu1*2)    == "BaseUnits(km=6 g=3)"
    assert str(bu2*0.5)  == "BaseUnits(km=1 g=2:7)"

    # Test values
    value = {"km": 2, "K": (3,2)}
    bu = BaseUnits(dict(value))
    assert str(bu) == "BaseUnits(km=2 K=3:2)"
    assert bu.value() == value
    
    
def test_rebase():
    
    # simple prefix rebasing 
    assert str(Quantity(1, 'cm*m*dm').rebase())  == "Quantity(1.000e+03 cm3)"
    
    # rebasing prefixes with exponents
    assert str(Quantity(1, 'C3*cm*m2').rebase()) == "Quantity(1.000e+04 C3*cm3)"
    assert str(Quantity(1, 'cm*m3:2').rebase())  == "Quantity(1.000e+03 cm5:2)"
    
    # rebasing different units
    assert str(Quantity(1, 'erg*J').rebase())    == "Quantity(1.000e+07 erg2)"
