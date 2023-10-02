import numpy as np
import pytest
import os
import sys
from decimal import Decimal
sys.path.insert(0, 'src')

from scinumtools.units import *

def test_decimal():
    
    assert str(Quantity(Decimal(3.3239840203948394e-3), 'cm')) == "Quantity(3.324e-3 cm)"
    
    a = Quantity(Decimal(3.3239840203948394e-3), 'cm')
    b = Quantity(Decimal(9.9239000409020932894e6), 'cm')
    assert str(a+b)      == "Quantity(9.924e+6 cm)"
    assert (a+b).value() == Decimal('9923900.044226077073258914050')
    
    assert str(a*b)      == "Quantity(3.299e+4 cm2)"
    assert (a*b).value() == Decimal('32986.88515595424986253677220')