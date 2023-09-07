import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import *
from scinumtools.units.settings import *
    
def test_unit_list():
    
    assert str(Unit())
    assert str(Constant())

    #print(Constant())
    #exit(1)
    
def test_unique_names():
    
    units = list(UNIT_STANDARD.keys())
    for symbol, unit in UNIT_STANDARD.items():
        if isinstance(unit.prefixes, list):
            for prefix in unit.prefixes:
                assert prefix in UNIT_PREFIXES
                units.append(f"{prefix}{symbol}")
        elif unit.prefixes is True:
            for prefix in UNIT_PREFIXES.keys():
                units.append(f"{prefix}{symbol}")
    #print(units)
    #exit(1)
    units.sort()
    seen = set()
    dupes = [x for x in units if x in seen or seen.add(x)]    
    assert len(dupes)==0
    
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
        base = q.baseunits.base()
        magnitude = q.magnitude*base.magnitude
        if base.dimensions.value(dtype=list) != unit.dimensions or not isclose(magnitude,  unit.magnitude, rel_tol=MAGNITUDE_PRECISION):
            print(q, symbol, unit.definition, unit.magnitude)
        assert isclose(magnitude,  unit.magnitude, rel_tol=MAGNITUDE_PRECISION)
        assert base.dimensions.value(dtype=list) == unit.dimensions
        
    for symbol, unit in UNIT_PREFIXES.items():
        if not isinstance(unit.definition,str):
            continue
        q = Quantity(1, unit.definition)
        base = q.baseunits.base()
        assert isclose(q.magnitude,  unit.magnitude, rel_tol=MAGNITUDE_PRECISION)
        assert base.dimensions.value(dtype=list) == unit.dimensions
        