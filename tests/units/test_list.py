import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
from scinumtools.units.settings import SI
from scinumtools.units.unit_environment import *
    
def test_unit_list():
    
    assert str(Unit())
    assert str(Constant())

    #print(Constant())
    #print(Unit())
    #exit(1)
    
def test_unique_unique():
    
    assert check_unique_symbols()

def test_custom_units():
    
    # register custom unit
    units = {
        'x': {'magnitude':3, 'dimensions':[3,2,-1,0,0,1,0,0]},   # defined as a dictionary
        'y': Quantity(2, 'cm/g2')                                # defined as a quantity
    }
    with UnitEnvironment(units):
    
        q = Quantity(1, 'x')
        assert str(q) == "Quantity(1.000e+00 x)"
        assert q.baseunits.magnitude          == 3.0
        assert q.baseunits.dimensions.value() == [3,2,-1,0,0,1,0,0]
        
        q = Quantity(1, 'y')
        assert str(q) == "Quantity(1.000e+00 y)"
        assert q.baseunits.magnitude          == 0.02
        assert q.baseunits.dimensions.value() == [1,-2,0,0,0,0,0,0]

        with pytest.raises(Exception) as excinfo:
            Quantity(1, 'kx')
        assert excinfo.value.args[0]=="Unit cannot have any prefixes:"
        assert excinfo.value.args[1]=="x"

        # try to register new unit with already existing symbol
        with pytest.raises(Exception) as excinfo:
            with UnitEnvironment(units):
                pass
        assert excinfo.value.args[0]=="Unit with this symbol already exists:"
        assert excinfo.value.args[1]=="x"
    
    # make sure that units does not exist outside of the environment
    assert 'x' not in UNIT_STANDARD
    
    # register new unit with a custom converter 
    class CustomUnitType(UnitType):
        def _istype(self):
            return False
    units = {'x': {'magnitude':3, 'dimensions':[3,2,-1,0,0,1,0,0], 'definition':CustomUnitType}}
    env = UnitEnvironment(units)
    assert 'x' in UNIT_STANDARD
    assert CustomUnitType in UNIT_TYPES
    env.close()
    
    # make sure that units and types does not exist aftr environment is closed
    assert 'x' not in UNIT_STANDARD
    assert CustomUnitType not in UNIT_TYPES
    

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
    

def test_definitions():
    
    for symbol, unit in UNIT_STANDARD.items():
        if not isinstance(unit.definition,str):
            continue
        q = Quantity(1, unit.definition)
        base = q.baseunits
        magnitude = q.magnitude.value*base.magnitude
        if base.dimensions.value(dtype=list) != unit.dimensions or not isclose(magnitude,  unit.magnitude, rel_tol=MAGNITUDE_PRECISION):
            print(q, symbol, unit.definition, unit.magnitude)
        assert isclose(magnitude,  unit.magnitude, rel_tol=MAGNITUDE_PRECISION)
        assert base.dimensions.value(dtype=list) == unit.dimensions
        
    for symbol, unit in UNIT_PREFIXES.items():
        if not isinstance(unit.definition,str):
            continue
        q = Quantity(1, unit.definition)
        base = q.baseunits
        assert isclose(q.magnitude.value,  unit.magnitude, rel_tol=MAGNITUDE_PRECISION)
        assert base.dimensions.value(dtype=list) == unit.dimensions
        
def test_quantities():
    
    assert SI.Pressure.value       == '#SPRE'
    assert CGS.Energy.value        == '#CENE'
    assert AU.ElectricCharge.value == '#AECH'
    assert type(SI.Pressure)       == SI

    text = [
        "#############################################",
        "# Do not modify this file!                  #",
        "# It is generated automatically in:         #",
        "# tests/units/test_list.py::test_quantities #",
        "#############################################",
        ""
        "QUANTITY_UNITS = {",
    ]
    symbols = []
    for q in range(len(QUANTITY_LIST)):
        name = QUANTITY_LIST.name[q]
        text.append(f"  # {name}")
        for system in ['SI','CGS','AU']:
            definition = getattr(QUANTITY_LIST,system)[q]
            if definition is None:
                continue
            else:
                symbol = QUANTITY_LIST.symbol[q]
                unitid = f"#{system[0]}{symbol}"
                atom = UnitSolver(definition)
                base = BaseUnits(atom.baseunits)
                c1 = f"{atom.magnitude*base.magnitude},"
                c2 = f"{base.dimensions.value()}"
                symbols.append(unitid)
                text.append(f"  '{unitid}': ({c1:25s}{c2:27s}), # {definition}") 
    text.append("}")
    text = "\n".join(text)
    
    # test if new symbols are unique
    assert len(np.unique(symbols)) == len(symbols)
    
    # test if we produced a valid Python code
    exec(text)
    assert QUANTITY_UNITS

    # test if quantity lists work
    assert str(Quantity(23, SI.Pressure))          == 'Quantity(2.300e+01 #SPRE)'
    assert str(Quantity(23, 'Pa').to(SI.Pressure)) == 'Quantity(2.300e+01 #SPRE)'
    assert str(Quantity(23, SI.Pressure).to('Pa')) == 'Quantity(2.300e+01 Pa)'
    assert str(Quantity(1, '[a_0]').to(AU.Length)) == 'Quantity(1.000e+00 #ALEN)'
    assert str(Unit(AU.Length))                    == "Quantity(1.000e+00 #ALEN)"
    assert str(Unit('[a_0]')/Unit(AU.Length))      == 'Quantity(1.000e+00)'
    assert str(Unit(AU.Length)*Unit('s'))          == 'Quantity(1.000e+00 #ALEN*s)'
    assert str(Quantity(1, '#ALEN/s').to('m/s'))   == 'Quantity(5.292e-11 m*s-1)'
    
    # save the new version of the code
    path_units = "src/scinumtools/units"
    assert os.path.isdir(path_units)
    with open(f'{path_units}/unit_list.py','w') as f:
        f.write(text)
