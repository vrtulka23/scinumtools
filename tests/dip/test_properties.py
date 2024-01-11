import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.settings import Format
from scinumtools.dip.datatypes import FloatType, IntegerType, StringType

def parse(code):
    with DIP() as p:
        p.add_string(code)
        return p.parse().data(verbose=True,format=Format.TYPE)

def test_option():
    data = parse('''
coordinates int = 1
  = 1  # linear
  = 2  # cylindrical
  = 3  # spherical
    ''')
    np.testing.assert_equal(data,{
        'coordinates': IntegerType(1),
    })
    with pytest.raises(Exception) as e_info:
        parse("""
length float cm
  = 12 cm
  = 34 cm
        """)
    assert e_info.value.args[0] == "Node value must be defined:"
    with pytest.raises(Exception) as e_info:
        parse("""
deposition bool = true
  = true
  = false
        """)
    assert e_info.value.args[0] == "Node 'bool' does not support options"
    
def test_options():
    data = parse('''
size float cm
  !options [12,13,14,15,16] cm
  !options [22,23,24,25] m
size = 23 m
    ''')
    np.testing.assert_equal(data,{
        'size': FloatType(2300, 'cm')
    })
    with pytest.raises(Exception) as e_info:
        parse("""
size float cm
  !options [12,13,14,15,16] cm
size = 11
        """)
    assert e_info.value.args[0] == "Value 'FloatType(11.0 cm)' of node 'size' doesn't match with any option:"

def test_constant():
    data = parse('''
size float = 30 cm
  !constant
    ''')
    np.testing.assert_equal(data,{
        'size': FloatType(30, 'cm')
    })
    with pytest.raises(Exception) as e_info:
        parse("""
size float = 30 cm
  !constant
size = 23
        """)
    assert e_info.value.args[0] == "Node 'size' is constant and cannot be modified:"
    
def test_format():
    data = parse('''
name str = John
  !format "[a-zA-Z]+"
    ''')
    np.testing.assert_equal(data,{
        'name': StringType('John')
    })
    with pytest.raises(Exception) as e_info:
        parse("""
name str = 7-up
  !format '[a-zA-Z]+'
        """)
    assert e_info.value.args[0] == "Node value does not match the format:"
    with pytest.raises(Exception) as e_info:
        parse("""
size float = 23 cm
  !format '[a-zA-Z]+'
        """)
    assert e_info.value.args[0] == "Format can be set only to string nodes"

def test_condition():
    data = parse('''
size float = 23 cm
  !condition ('200 mm < {?} && {?} < 30 cm')
    ''')
    np.testing.assert_equal(data,{
        'size': FloatType(23, 'cm')
    })
    with pytest.raises(Exception) as e_info:
        parse("""
size float = 23 cm
  !condition ('250 mm < {?} && {?} < 30 cm')
        """)
    assert e_info.value.args[0] == "Node does not fullfil a condition:"

def test_tags():
    with DIP() as p:
        p.add_string('''
        name str = John
          !tags ["name","male"]
        age int = 34
        ''')
        env = p.parse()

    nodes = env.nodes.query("*", tags=['male'])
    assert len(nodes)     == 1
    assert nodes[0].tags  == ['name','male']
    
    data = env.data(verbose=True,format=Format.TYPE)
    np.testing.assert_equal(data,{
        'name': StringType('John'),
        'age':  IntegerType(34)
    })
    
    data = env.data(verbose=True,format=Format.TYPE,query="age")
    np.testing.assert_equal(data,{
        'age':  IntegerType(34)
    })

    data = env.data(verbose=True,format=Format.TYPE,query="age",tags=['name'])
    np.testing.assert_equal(data,{})

    data = env.data(verbose=True,format=Format.TYPE,tags=['name'])
    np.testing.assert_equal(data,{
      'name': StringType('John')
    })

def test_description():
    with DIP() as p:
        p.add_string('''
        name str = John
          !description "Name of a person"
        age int = 34
          !desc "Age of a person"
        ''')
        env = p.parse()

    nodes = env.nodes.query("*")
    assert nodes[0].description == "Name of a person"
    assert nodes[1].description == "Age of a person"
