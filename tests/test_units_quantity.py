import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools import ParameterTable
from scinumtools.units import *

def test_quantity():
    
    assert str(Quantity(123e2))          == "Quantity(1.230e+04)"
    q = Quantity(123e2, 'km/s')
    assert str(q) == "Quantity(1.230e+04 km*s-1)"
    assert str(q.value())                == "12300.0"
    assert str(q.value('m/s'))           == "12300000.0"
    assert str(q.value('m/s',dtype=int)) == "12300000"
    assert str(q.value({'m':1,'s':-1}))  == "12300000.0"
    assert str(q.units())                == "km*s-1"
    
    result = "Quantity(1.230e+04 m*s2:3)"
    assert str(Quantity(123e2, [1,0,(2,3),0,0,0,0,0] ))    == result
    assert str(Quantity(123e2, Dimensions(m=1, s=(2,3)) )) == result

    result = "Quantity(1.230e+04 J2*kg2:3)"
    assert str(Quantity(123e2, {'J': 2, 'k:g':(2,3)} )) == result
    assert str(Quantity(123e2, BaseUnits({'J': 2, 'k:g':(2,3)}) )) == result

    result = "Quantity(2.460e+04 m)"
    assert str(Quantity(123e2, Quantity(2, 'm'))) == result
    assert str(Quantity(123e2, 2*Unit('m'))) == result
    
def test_units():

    assert str(Unit('m'))                   == "Quantity(1.000e+00 m)"
    assert str(Unit('kg*m2*s-2'))           == "Quantity(1.000e+00 kg*m2*s-2)"
                                            
    unit = Unit()                           
    assert str(unit.m)                      == "Quantity(1.000e+00 m)"
    assert str(2*unit.kJ)                   == "Quantity(2.000e+00 kJ)"
    assert str(unit.kg*unit.m**2/unit.s**2) == "Quantity(1.000e+00 kg*m2*s-2)"
    assert str(unit.J.to('erg'))            == "Quantity(1.000e+07 erg)"
    assert str(unit.m**(2,3))               == "Quantity(1.000e+00 m2:3)"
    assert str(unit.m**Fraction(2,3))       == "Quantity(1.000e+00 m2:3)"
    assert str((9*unit.m)**(1,2))           == "Quantity(3.000e+00 m1:2)"

    with Unit() as unit:
        assert str(unit.m)                  == "Quantity(1.000e+00 m)"

def test_constants():

    assert str(Constant('c')) == "Quantity(1.000e+00 [c])"

    const = Constant()
    assert str(const.c)       == "Quantity(1.000e+00 [c])"
    assert str(const.m_e)     == "Quantity(1.000e+00 [m_e])"

    with Constant() as const:
        assert str(const.c)   == "Quantity(1.000e+00 [c])"
    
def test_aliases():
    assert str(quant(23, 'km'))   == "Quantity(2.300e+01 km)"
    assert str(unit('m'))         == "Quantity(1.000e+00 m)"
    assert str(const('c'))        == "Quantity(1.000e+00 [c])"    

def test_scalar_arithmetics():

    # addition and substtraction
    assert str(Quantity(1.1, 'km')-Quantity(100, 'm')) == "Quantity(1.000e+00 km)"
    assert str(Quantity(1.0, 'km')+Quantity(100, 'm')) == "Quantity(1.100e+00 km)"

    # multiplication, division and power
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
    
    # arithmetics of dimensionless quantities
    q = Quantity(34)
    assert str(q-1) == "Quantity(3.300e+01)"

def test_scalar_unit_conversion():
    
    # error if converting different units
    q = Quantity(134e-34)
    with pytest.raises(Exception) as excinfo:
        q = q.to("kg3*s/cm3")
    assert excinfo.value.args[0]=="Converting units with different dimensions:"
    assert excinfo.value.args[1].value()==[0, 0, 0, 0, 0, 0, 0, 0]
    assert excinfo.value.args[2].value()==[-3, 3, 1, 0, 0, 0, 0, 0]

    # test unit conversion on scalars
    result = "Quantity(3.000e+03 m)"
    assert str(Quantity(3, 'km').to('m'))                 == result
    assert str(Quantity(3, 'km').to([1,0,0,0,0,0,0,0]))   == result
    assert str(Quantity(3, 'km').to(Dimensions(m=1)))     == result
    assert str(Quantity(3, 'km').to({'m':1}))             == result
    assert str(Quantity(3, 'km').to(BaseUnits({'m':1})))  == result
    assert str(Quantity(3, 'km').to(Unit().m))            == result

    # reset base units if dimensions are all zero
    assert str(Quantity(3, 'kg*m2/s2')/Quantity(2, 'J')) == "Quantity(1.500e+00)"

def test_operation_sides():
    
    p = Quantity(2, 'm')
    q = Quantity(3, 'm')
    assert p+q == q+p
    assert p-q == -(q-p)
    assert q*2 == 2*q
    assert p/2 == 1/(2/p)
    
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

    assert str(Quantity(23, 'Hz').to('s'))        == "Quantity(4.348e-02 s)"
    assert str(Quantity(34, 'Ohm').to('S'))       == "Quantity(2.941e-02 S)"
    assert str(Quantity(102, 'J').to('erg-1'))    == "Quantity(9.804e-10 erg-1)"

def test_logarithmic():

    # Bels, Nepers and Amplitude/Power Ratios
    assert str(Quantity(1, 'B').to('dB'))     == "Quantity(1.000e+01 dB)"
    assert str(Quantity(1, 'dB').to('B'))     == "Quantity(1.000e-01 B)"
    assert str(Quantity(1, 'B').to('Np'))     == "Quantity(1.151e+00 Np)"
    assert str(Quantity(1, 'Np').to('B'))     == "Quantity(8.686e-01 B)"
    assert str(Quantity(1, 'dB').to('cNp'))   == "Quantity(1.151e+01 cNp)"
    assert str(Quantity(1000, 'AR').to('dB')) == "Quantity(6.000e+01 dB)"
    assert str(Quantity(30, 'dB').to('AR'))   == "Quantity(3.162e+01 AR)"
    assert str(Quantity(1000, 'PR').to('dB')) == "Quantity(3.000e+01 dB)"
    assert str(Quantity(6, 'dB').to('PR'))    == "Quantity(3.981e+00 PR)"
    
    # Decibel-milliwatts (dBm)
    assert str(Quantity(1, 'mW').to('W'))     == "Quantity(1.000e-03 W)"
    assert str(Quantity(1, 'mW').to('dBm'))   == "Quantity(0.000e+00 dBm)"
    assert str(Quantity(10, 'W').to('dBm'))   == "Quantity(4.000e+01 dBm)"
    assert str(Quantity(10, 'pW').to('dBm'))  == "Quantity(-8.000e+01 dBm)"
    assert str(Quantity(-3, 'dBm').to('uW'))  == "Quantity(5.012e+02 uW)"
    assert str(Quantity(22, 'dBm').to('mW'))  == "Quantity(1.585e+02 mW)"
    
    # Decibel-milliwatts (dBmW)
    assert str(Quantity(10, 'W').to('dBmW'))   == "Quantity(4.000e+01 dBmW)"
    assert str(Quantity(-3, 'dBmW').to('uW'))  == "Quantity(5.012e+02 uW)"
    
    # Decibel-watts (dBW)
    
    assert str(Quantity(1, 'W').to('dBW'))     == "Quantity(0.000e+00 dBW)"
    assert str(Quantity(20,'dBW').to('W'))     == "Quantity(1.000e+02 W)"
    
    # Decibel-Volt (dBV)
    assert str(Quantity(100, 'mV').to('dBV'))  == "Quantity(-2.000e+01 dBV)"
    assert str(Quantity(1, 'V').to('dBV'))     == "Quantity(0.000e+00 dBV)"
    assert str(Quantity(10, 'V').to('dBV'))    == "Quantity(2.000e+01 dBV)"
    assert str(Quantity(-60, 'dBV').to('mV'))  == "Quantity(1.000e+00 mV)"
    assert str(Quantity(0, 'dBV').to('V'))     == "Quantity(1.000e+00 V)"
    assert str(Quantity(40, 'dBV').to('V'))    == "Quantity(1.000e+02 V)"

    # Decibel-microvolt (dBuV)
    assert str(Quantity(42, 'dBuV').to('uV'))   == "Quantity(1.259e+02 uV)"
    assert str(Quantity(1000, 'uV').to('dBuV')) == "Quantity(6.000e+01 dBuV)"
    