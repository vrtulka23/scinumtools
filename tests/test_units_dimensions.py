import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
    
def test_dimensions():

    # Test simplification
    dims = Dimensions(m=(5,-2), g=3, s=1, cd=(-0,3), K=(34,1), rad=(18,12))
    assert str(dims) == "Dimensions(m=-5:2 g=3 s=1 K=34 rad=3:2)"

def test_arithmetics():
    
    dims1 = Dimensions(m=3, g=(3,2))
    dims2 = Dimensions(m=2, g=(4,7))
    assert not dims1==dims2
    assert str(dims1+dims2) == "Dimensions(m=5 g=29:14)"
    assert str(dims1-dims2) == "Dimensions(m=1 g=13:14)"
    assert str(dims1*2)     == "Dimensions(m=6 g=3)"
    assert str(dims2*0.5)   == "Dimensions(m=1 g=2:7)"

def test_values():
    
    value = [3, (3,2), 0, 0, 0, 0, 0, 0]
    dims = Dimensions(*value)
    assert str(dims) == "Dimensions(m=3 g=3:2)" 
    assert dims.value() == value
    assert dims.value(dtype=dict) == {'m': 3, 'g':(3,2)}
