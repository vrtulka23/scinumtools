import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *

def test_quantity():
    
    assert str(UnitSolver("kg*m2/s2"))   == "Atom(1.0 kg=1 m=2 s=-2)"
