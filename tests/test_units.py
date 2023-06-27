import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.structs import ParameterDict
from scinumtools.phys.units.UnitList import UnitStandard, UnitPrefixes
from scinumtools.phys.units import *

def test_definitions():
    
    unitlist = ParameterDict(['magnitude','dimensions','definition','name'], UnitStandard)
    for symbol, unit in unitlist.items():
        if not isinstance(unit['definition'],str):
            continue
        q = Quantity(1, unit['definition'])
        assert isclose(q.magnitude,  unit['magnitude'], rel_tol=1e-07)
        assert q.dimensions == unit['dimensions']
    prefixes = ParameterDict(['magnitude','dimensions','definition','name'], UnitPrefixes)

def test_temperatures():
    
    # Temperature conversions
    assert str(Quantity(23,'K').to('Cel'))        == "Quantity(-2.501e+02 Cel)"
    assert str(Quantity(23,'K').to('degF'))       == "Quantity(-4.183e+02 degF)"
    assert str(Quantity(23,'K').to('degR'))       == "Quantity(4.140e+01 degR)"
    assert str(Quantity(23,'Cel').to('K'))        == "Quantity(2.961e+02 K)"
    assert str(Quantity(23,'Cel').to('degF'))     == "Quantity(7.340e+01 degF)"
    assert str(Quantity(23,'Cel').to('degR'))     == "Quantity(5.331e+02 degR)"
    assert str(Quantity(23,'degF').to('K'))       == "Quantity(2.681e+02 K)"
    assert str(Quantity(23,'degF').to('Cel'))     == "Quantity(-5.000e+00 Cel)"
    assert str(Quantity(23,'degF').to('degR'))    == "Quantity(4.827e+02 degR)"
    assert str(Quantity(23,'degR').to('K'))       == "Quantity(1.278e+01 K)"
    assert str(Quantity(23,'degR').to('Cel'))     == "Quantity(-2.604e+02 Cel)"
    assert str(Quantity(23,'degR').to('degF'))    == "Quantity(-4.367e+02 degF)"
    assert str(Quantity(2300,'Cel').to('kK'))     == "Quantity(2.573e+00 kK)"
    
def test_inversion():

    assert str(Quantity(23, 'Hz').to('s'))     == "Quantity(4.348e-02 s)"
    assert str(Quantity(34, 'Ohm').to('S'))    == "Quantity(2.941e-02 S)"
    assert str(Quantity(102, 'J').to('erg-1')) == "Quantity(9.804e-10 erg-1)"

def test_scalar_arithmetics():
    
    q = Quantity(123e2, [3,3,0,0,1,0,0,0])
    assert str(q) == "Quantity(1.230e+04 m3*g3*C)"    
    q /= Quantity(123, 'C')
    assert str(q) == "Quantity(1.000e+02 m3*g3)"
    q *= Quantity(2, 's2')
    assert str(q) == "Quantity(2.000e+02 m3*g3*s2)"
    q = Quantity(123, "kg3*cm-2*s")
    assert str(q) == "Quantity(1.230e+02 kg3*cm-2*s)"
    q = Quantity(123e34, "J")
    assert str(q) == "Quantity(1.230e+36 J)"
    q /= Quantity(123, 's')
    assert str(q) == "Quantity(1.000e+34 J*s-1)"
    q = q ** 2
    assert str(q) == "Quantity(1.000e+68 J2*s-2)"
    q = q.to('kg2*m4/s6')
    assert str(q) == "Quantity(1.000e+68 kg2*m4*s-6)"
    q = Quantity(123, "kg3*s/(cm2*m)")
    assert str(q) == "Quantity(1.230e+02 kg3*s*cm-2*m-1)"
    q = q.to("kg3*s/cm3")
    assert str(q) == "Quantity(1.230e+00 kg3*s*cm-3)"
    q = Quantity(134e-34)
    assert str(q) == "Quantity(1.340e-32)"
    
    with pytest.raises(Exception) as excinfo:
        q = q.to("kg3*s/cm3")
    assert excinfo.value.args[0]=="Converting units with different dimensions:"
    assert excinfo.value.args[1]==[0, 0, 0, 0, 0, 0, 0, 0]
    assert excinfo.value.args[2]==[-3, 3, 1, 0, 0, 0, 0, 0]

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

    # Test unit conversion on arrays
    assert str(Quantity([1,2,3], 'm').to('km')) == "Quantity([0.001 0.002 0.003] km)"

def test_numpy():
    
    # Test numpy functions
    assert str(np.sqrt(Quantity([4, 9, 16], 'm2'))) == "Quantity([2. 3. 4.] m2)"

def test_operation_sides():
    
    p = Quantity([2,3,4], 'm')
    q = Quantity([5,6,7], 'm')
    assert p+q == q+p
    assert p-q == -(q-p)
    assert q*2 == 2*q
    assert p/2 == 1/(2/p)

def test_units():

    assert str(Unit('m'))         == "Quantity(1.000e+00 m)"
    assert str(Unit('kg*m2*s-2')) == "Quantity(1.000e+00 kg*m2*s-2)"
    
    unit = Unit()
    assert str(unit.m)      == "Quantity(1.000e+00 m)"
    assert str(2*unit.kJ)   == "Quantity(2.000e+00 kJ)"
    assert str(unit.kg*unit.m**2/unit.s**2) == "Quantity(1.000e+00 kg*m2*s-2)"
    assert str(unit.J.to('erg')) == "Quantity(1.000e+07 erg)"

def test_constants():

    assert str(Constant('c')) == "Quantity(1.000e+00 [c])"

    const = Constant()
    assert str(const.c)   == "Quantity(1.000e+00 [c])"
    assert str(const.m_e) == "Quantity(1.000e+00 [m_e])"
    
def test_unique_names():

    units = list(UnitStandard.keys())
    for unit in UnitStandard.keys():
        for prefix in UnitPrefixes.keys():
            units.append(f"{prefix}{unit}")
    units.sort()
    seen = set()
    dupes = [x for x in units if x in seen or seen.add(x)]    
    assert len(dupes)==0

def test_dimensions():
    
    dims = Dimensions(m=(5,-2), g=3, s=1, cd=(-0,3), K=(34,1), rad=(18,12))
    assert str(dims) == "Dimensions(m=Ratio(-5,2), g=3, s=1, K=34, rad=Ratio(3,2))"

    dims1 = Dimensions(m=3, g=(3,2))
    dims2 = Dimensions(m=2, g=(4,7))
    assert not dims1==dims2
    assert str(dims1+dims1) == "Dimensions(m=3, g=Ratio(3,2))"
    assert str(dims2-dims2) == "Dimensions(m=2, g=Ratio(4,7))"
    assert str(dims1*dims2) == "Dimensions(m=5, g=Ratio(29,14))"
    assert str(dims1/dims2) == "Dimensions(m=1, g=Ratio(13,14))"
    assert str(dims1**2)    == "Dimensions(m=6, g=3)"
    assert str(dims2**0.5)  == "Dimensions(m=1, g=Ratio(2,7))"
