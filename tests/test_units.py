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
    assert str(Quantity(123e2, {'J': 2, 'kg':(2,3)} )) == result
    assert str(Quantity(123e2, BaseUnits({'J': 2, 'kg':(2,3)}) )) == result

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
    
def test_dimensions():

    # Test simplification
    dims = Dimensions(m=(5,-2), g=3, s=1, cd=(-0,3), K=(34,1), rad=(18,12))
    assert str(dims) == "Dimensions(m=-5:2 g=3 s=1 K=34 rad=3:2)"

    # Test arithmetics
    dims1 = Dimensions(m=3, g=(3,2))
    dims2 = Dimensions(m=2, g=(4,7))
    assert not dims1==dims2
    assert str(dims1+dims2) == "Dimensions(m=5 g=29:14)"
    assert str(dims1-dims2) == "Dimensions(m=1 g=13:14)"
    assert str(dims1*2)     == "Dimensions(m=6 g=3)"
    assert str(dims2*0.5)   == "Dimensions(m=1 g=2:7)"

    # Test values
    value = [3, (3,2), 0, 0, 0, 0, 0, 0]
    dims = Dimensions(*value)
    assert str(dims) == "Dimensions(m=3 g=3:2)" 
    assert dims.value() == value
    assert dims.value(dtype=dict) == {'m': 3, 'g':(3,2)}

def test_fractions():

    # Test initialization
    assert str(Fraction(2))   == "2"
    assert str(Fraction(0,3)) == "0"
    assert str(Fraction(1,3)) == "1:3"

    # Test arithmetics
    assert str(Fraction(1,3)+3)             == "10:3"
    assert str(Fraction(1,3)+(3,2))         == "11:6"
    assert str(Fraction(1,3)+Fraction(3,2)) == "11:6"
    assert str(Fraction(1,3)-3)             == "-8:3"
    assert str(Fraction(1,3)-(3,2))         == "-7:6"
    assert str(Fraction(1,3)-Fraction(3,2)) == "-7:6"
    assert str(Fraction(1,3)*3)             == "1"
    assert str(Fraction(1,3)*(3,2))         == "1:2"
    assert str(Fraction(1,3)*Fraction(3,2)) == "1:2"
    assert str(Fraction(1,3)/3)             == "1:9"
    assert str(Fraction(1,3)/(3,2))         == "2:9"
    assert str(Fraction(1,3)/Fraction(3,2)) == "2:9"
    
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
    
def test_definitions():
    
    unitlist = ParameterTable(['magnitude','dimensions','definition','name'], UnitStandard, keys=True)
    for symbol, unit in unitlist.items():
        if not isinstance(unit['definition'],str):
            continue
        q = Quantity(1, unit['definition'])
        if q.dimensions.value() != unit['dimensions'] or not isclose(q.magnitude,  unit['magnitude'], rel_tol=1e-07):
            print(q, symbol, unit['definition'], unit['magnitude'])
        assert isclose(q.magnitude,  unit['magnitude'], rel_tol=1e-07)
        assert q.dimensions.value() == unit['dimensions']
        
    prefixes = ParameterTable(['magnitude','dimensions','definition','name'], UnitPrefixes, keys=True)
    for symbol, unit in prefixes.items():
        if not isinstance(unit['definition'],str):
            continue
        q = Quantity(1, unit['definition'])
        assert isclose(q.magnitude,  unit['magnitude'], rel_tol=1e-07)
        assert q.dimensions.value() == unit['dimensions']
        
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

    # error if converting different units
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

    # arithmetics of dimensionless quantities
    q = Quantity(34)
    assert str(q-1) == "Quantity(3.300e+01)"
    
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

    # Array slicing
    q = Quantity([1,2,3], 'm')
    assert str(q[:2])              == "Quantity([1. 2.] m)"
    assert str(q.value(dtype=int)) == "[1 2 3]"
    
def test_numpy():
    
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
    
def test_operation_sides():
    
    p = Quantity([2,3,4], 'm')
    q = Quantity([5,6,7], 'm')
    assert p+q == q+p
    assert p-q == -(q-p)
    assert q*2 == 2*q
    assert p/2 == 1/(2/p)
    
def test_unique_names():
    
    unitlist = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], UnitStandard, keys=True)
    prefixes = UnitPrefixes.keys()
    
    units = list(unitlist.keys())
    for symbol, unit in unitlist.items():
        if isinstance(unit.prefixes, list):
            for prefix in unit.prefixes:
                assert prefix in prefixes
                units.append(f"{prefix}{symbol}")
        elif unit.prefixes is True:
            for prefix in prefixes:
                units.append(f"{prefix}{symbol}")
    #print(units)
    #exit(1)
    units.sort()
    seen = set()
    dupes = [x for x in units if x in seen or seen.add(x)]    
    assert len(dupes)==0

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

def test_nan():

    assert str(NaN()) == "Quantity(nan)"
    assert str(NaN('cm')) == "Quantity(nan cm)"

def test_unit_list():
    
    assert str(Unit())
    assert str(Constant())

    #print(Constant())
    #exit(1)
    
def test_prefixes():
    
    # unit can have any prefix
    assert str(Quantity(1, 'km'))    == "Quantity(1.000e+00 km)"
    
    # unit cannot have prefixes
    with pytest.raises(Exception) as excinfo:
        Quantity(1, 'kCel')
    assert excinfo.value.args[0]=="Unit cannot have any prefixes:"
    assert excinfo.value.args[1]=="Cel"
    
    # unit can have only selected prefixes
    with pytest.raises(Exception) as excinfo:
        Quantity(1, 'mpc')
    assert excinfo.value.args[0]=="Unit can have only following prefixes:"
    assert excinfo.value.args[1]==['k', 'M', 'G', 'T']
    
def test_rebase():
    
    # simple prefix rebasing 
    assert str(Quantity(1, 'cm*m*dm').rebase())  == "Quantity(1.000e+03 cm3)"
    
    # rebasing prefixes with exponents
    assert str(Quantity(1, 'C3*cm*m2').rebase()) == "Quantity(1.000e+04 C3*cm3)"
    assert str(Quantity(1, 'cm*m3:2').rebase())  == "Quantity(1.000e+03 cm5:2)"
    
    # rebasing different units
    assert str(Quantity(1, 'erg*J').rebase())    == "Quantity(1.000e+07 erg2)"