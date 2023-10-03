import numpy as np
import pytest
import os
import sys
from decimal import Decimal
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.units import *

def test_decimal():
    
    assert str(Quantity(Decimal(3.3239840203948394e-3), 'cm')) == "Quantity(3.324e-3 cm)"
    
    a = Quantity(Decimal(3.3239840203948394e-3), 'cm')
    b = Quantity(Decimal(9.9239000409020932894e6), 'cm')
    c = Quantity(9.9239000409020932894e6, 'cm')

    # basic arithmetics
    assert str(a+b)      == "Quantity(9.924e+6 cm)"
    assert (a+b).value() == Decimal('9923900.044226077073258914050')
    assert str(a+c)      == "Quantity(9.924e+6 cm)"
    assert str(c+a)      == "Quantity(9.924e+6 cm)"

    assert str(a-b)      == "Quantity(-9.924e+6 cm)"
    assert (a-b).value() == Decimal('-9923900.037578109032469235364')

    assert str(a*b)      == "Quantity(3.299e+4 cm2)"
    assert (a*b).value() == Decimal('32986.88515595424986253677220')

    assert str(a/b)      == "Quantity(3.349e-10)"
    assert (a/b).value() == Decimal('3.349473500030020118277236552E-10')

    assert str(a**2)      == "Quantity(1.105e-5 cm2)"
    assert (a**2).value() == Decimal('0.00001104886976784023973209249265')

    # NumPy functions
    assert str(np.sqrt(a*a))    == "Quantity(3.324e-3 cm)"
    assert np.sqrt(a*a).value() == Decimal('0.003323984020394839342810167081')

    # unit conversion
    assert str(a.to('nm')) == "Quantity(3.324e+4 nm)"
    assert a.value()       == Decimal('33239.84020394839204981469679')
