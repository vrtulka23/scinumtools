import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.settings import Format
from scinumtools.dip.datatypes import FloatType, IntegerType, StringType, BooleanType

def parse(code):
    with DIP() as p:
        p.add_string(code)
        return p.parse().data(verbose=True,format=Format.TYPE)

def test_name():
    
    data = parse('''
very-long.node23_NAME int = 1
    ''')
    np.testing.assert_equal(data,{
        'very-long.node23_NAME': IntegerType(1),
    })
    with pytest.raises(Exception) as e_info:
        parse('wrong$name int = 3')
    assert e_info.value.args[0] == "Name has an invalid format: wrong$name int = 3"
    
def test_types():
    
    data = parse('''
adult bool = true
age int = 20 yr
weight float = 63.3 kg
name str = 'Laura'
    ''')
    np.testing.assert_equal(data,{
        'adult':  BooleanType(True),
        'age':    IntegerType(20, 'yr'),
        'weight': FloatType(63.3, 'kg'),
        'name':   StringType('Laura')
    })
    with pytest.raises(Exception) as e_info:
        parse('age bool = true a')
    assert e_info.value.args[0] == "Boolean datatype does not support units:"
    assert e_info.value.args[1] == "age bool = true a"
    with pytest.raises(Exception) as e_info:
        parse("age str = 23 a")
    assert e_info.value.args[0] == "String datatype does not support units:"
    assert e_info.value.args[1] == "age str = 23 a"

def test_dimensions():
    
    data = parse('''
counts int[3] = [4234,34,2]
lengths float[2:,2] = [[4234,34],[234,34]] cm
colleagues str[:] = ["John","Patricia","Lena"]
logic bool[2] = [true,false]
    ''')
    np.testing.assert_equal(data,{
        'counts':      IntegerType([4234,   34,    2]),
        'lengths':     FloatType([[4234.,   34.],[ 234.,   34.]], 'cm'),
        'colleagues':  StringType(['John', 'Patricia', 'Lena']),
        'logic':       BooleanType([ True, False])
    })
    with pytest.raises(Exception) as e_info:
        parse('counts int[2] = [4234,34,2]')
    assert e_info.value.args[0] == "Node 'counts' has invalid dimension: dim(0)=3 > 2"
    with pytest.raises(Exception) as e_info:
        parse('counts int[2] = [4234]')
    assert e_info.value.args[0] == "Node 'counts' has invalid dimension: dim(0)=1 < 2"
    with pytest.raises(Exception) as e_info:
        parse('counts int[:2] = [4234,34,2]')
    assert e_info.value.args[0] == "Node 'counts' has invalid dimension: dim(0)=3 > 2"
    with pytest.raises(Exception) as e_info:
        parse('counts int[2:] = [4234]')
    assert e_info.value.args[0] == "Node 'counts' has invalid dimension: dim(0)=1 < 2"
    with pytest.raises(Exception) as e_info:
        parse('counts int[2,3:] = [[234,4234],[234,34]]')
    assert e_info.value.args[0] == "Node 'counts' has invalid dimension: dim(1)=2 < 3"
    with pytest.raises(Exception) as e_info:
        parse('counts int = [[234,4234],[234,34]]')
    assert e_info.value.args[0] == "Could not convert raw value to type:"
    
def test_declarations():
    
    data = parse('''
cash bool
cash = true
weight float kg
weight = 77
''')
    np.testing.assert_equal(data,{
        'cash':   BooleanType(True),
        'weight': FloatType(77, 'kg')
    })
    with pytest.raises(Exception) as e_info:
        parse('counts int')
    assert e_info.value.args[0] == "Node value must be defined:"

def test_strings():
    
    data = parse('''
country str = Canada              # strings without whitespace
name str = "Johannes Brahms"      # strings with a whitespace
counts int[3] = "[0, 1, 2]"       # arrays with whitespaces between items
answers bool[2] = "[true, false]" 
names str[2] = '["Jolana", "Anastasia"]'
girl_friend str = "\"l'amie\""    # escaping of double quotes
boy_friend str = '"l\'ami"'       # escaping of single quotes
hashtag str = '#nocomment'        # comment
anticommutator str = '{a,b}'      # this is not an import
    ''')
    np.testing.assert_equal(data,{
        'country':        StringType('Canada'),
        'name':           StringType('Johannes Brahms'),
        'counts':         IntegerType([0, 1, 2]),
        'answers':        BooleanType([ True, False]),
        'names':          StringType(['Jolana', 'Anastasia']),
        'girl_friend':    StringType('"l\'amie"'),
        'boy_friend':     StringType('"l\'ami"'),
        'hashtag':        StringType('#nocomment'),
        'anticommutator': StringType('{a,b}')
      })
    with pytest.raises(Exception) as e_info:
        parse('name str = Johannes Brahms')
    assert e_info.value.args[0] == "String datatype does not support units:"
    assert e_info.value.args[1] == "name str = Johannes Brahms"
        
if __name__ == "__main__":
    # Specify wich test to run
    test = sys.argv[1] if len(sys.argv)>1 else True

    # Loop through all tests
    for fn in dir(sys.modules[__name__]):
        if fn[:5]=='test_' and (test is True or test==fn[5:]):
            print(f"\nTesting: {fn}\n")
            locals()[fn]()

def test_integer_subtypes():
    
    data = parse('''
    integer int = -34
    unsignedInteger uint = 235
    unsignedLongInteger uint64 = 29349850209348495020394849
    longInteger int64 = -239490304
    ''')
    np.testing.assert_equal(data,{
        'integer':              IntegerType(-34),
        'unsignedInteger':      IntegerType(235),
        'unsignedLongInteger':  IntegerType(29349850209348495020394849),
        'longInteger':          IntegerType(-239490304),
    })
    # test unsigned property
    assert  data['integer'].unsigned              == False
    assert  data['unsignedInteger'].unsigned      == True
    assert  data['unsignedLongInteger'].unsigned  == True
    assert  data['longInteger'].unsigned          == False
    # test precision
    assert  data['integer'].precision             == 32
    assert  data['unsignedInteger'].precision     == 32
    assert  data['unsignedLongInteger'].precision == 64
    assert  data['longInteger'].precision         == 64

def test_float_subtypes():
    
    data = parse('''
    float float = -34
    longFloat float128 = -239490304
    ''')
    np.testing.assert_equal(data,{
        'float':              FloatType(-34),
        'longFloat':          FloatType(-239490304),
    })
    # test precision
    assert  data['float'].precision             == 64
    assert  data['longFloat'].precision         == 128
    
def test_none_values():
    
    data = parse('''
    name str = none
    age int = none
    height float = none
    married bool = none
    
    surname str = {?name}
    
    age = 20
    adult bool = ("{?age} > 18")
    ''')
    np.testing.assert_equal(data,{
        'name':     StringType(None),
        'age':      IntegerType(20),
        'height':   FloatType(None),
        'married':  BooleanType(None),
        'surname':  StringType(None),
        'adult':    BooleanType(True),
    })