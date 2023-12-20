import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.settings import Format
from scinumtools.dip.datatypes import FloatType, IntegerType

def parse(code):
    with DIP() as p:
        p.add_string(code)
        return p.parse().data(verbose=True,format=Format.TYPE)

def test_hierarchy():
    data = parse('''
general.colonel int = 1  # namespace notation
  captain                # group nodes
     soldier int = 2     # lowest node in the hierarchy
    ''')
    np.testing.assert_equal(data,{
        'general.colonel': IntegerType(1),
        'general.colonel.captain.soldier': IntegerType(2)
    })

def test_modification():
    data = parse('''
size float = 70 cm    # definition
size float = 80 cm    # modifications of value
size = 90 cm          # omitting datatype
size = 100            # omitting units
size = 1 m            # using different prefix

energy float = 1.23 J # definition
energy = 2.2 erg      # switching from SI to cgs
energy = 2.2 g*cm2/s2 # using unit expressions

angle float = 1.57079633 rad  # definition in radians
angle = 31 '                  # angle minutes

alcohol float = 34 %  # definition
alcohol = 2 ppth      # converting dimensionless units

temp float = 20 Cel
temp = 280.15 K
    ''')
    np.testing.assert_equal(data,{
        'size':   FloatType(100, 'cm'),
        'energy': FloatType(2.2000000000000004e-07, 'J'),
        'angle':  FloatType(0.0090175342, 'rad'),
        'alcohol': FloatType(0.2, '%'),
        'temp': FloatType(7, 'Cel'),
    })  
    
def test_modification_errors():
    
    with pytest.raises(Exception) as e_info:
        parse('''
age int = 34 yr
age float = 55
        ''')
    assert e_info.value.args[0] == "Datatype <class 'int'> of node 'age' cannot be changed to <class 'float'>"
    with pytest.raises(Exception) as e_info:
        parse('''
weight = 23 kg
        ''')
    assert e_info.value.args[0] == "Modifying undefined node:"
    assert e_info.value.args[1] == "weight"

def test_option_units():
    data = parse("""
width float = 2 m
  = 2 m
  = 3 m
width = 3000 mm
    """)
    np.testing.assert_equal(data,{
        'width': FloatType(3.0, 'm')
    })
    with pytest.raises(Exception) as e_info:
        parse('''
size float = 24 cm
  = 24 cm
  = 25 m
size = 25 cm
        ''')
    assert e_info.value.args[0] == "Value 'FloatType(25.0 cm)' of node 'size' doesn't match with any option:"
    assert e_info.value.args[1] == [FloatType(24.0, 'cm'), FloatType(2500.0, 'cm')]
    
if __name__ == "__main__":
    # Specify wich test to run
    test = sys.argv[1] if len(sys.argv)>1 else True

    # Loop through all tests
    for fn in dir(sys.modules[__name__]):
        if fn[:5]=='test_' and (test is True or test==fn[5:]):
            print(f"\nTesting: {fn}\n")
            locals()[fn]()
