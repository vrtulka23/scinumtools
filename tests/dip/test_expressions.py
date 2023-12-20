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

def test_logical():
    data = parse('''
    a bool = true
    b float = 23.43 cm
    c bool = ("""
      false || {?b} == 23.43 cm && {?a}
    """)
    ''')
    np.testing.assert_equal(data,{
        'a': BooleanType(True),
        'b': FloatType(23.43, 'cm'),
        'c': BooleanType(True),
    })

def test_numerical():
    data = parse('''
    a float = 14.24 mm
    b int = 220 cm
    c float = ("{?a} + {?b} + 10 m") cm
    d int = ("{?b} + 1 cm + 10 m + 1 nm") cm
    ''')
    np.testing.assert_equal(data,{
        'a': FloatType(14.24, 'mm'),
        'b': IntegerType(220, 'cm'),
        'c': FloatType(1221.424, 'cm'),
        'd': IntegerType(1221, 'cm'),
    })
    with pytest.raises(Exception) as e_info:
        parse('''
        a float = ("10 dm + 1 m") J
        ''')
    """xxx
    assert e_info.value.args[0] == "Expression result dimensions do not match node dimensions:"
    """
    assert e_info.value.args[0] == "Unsupported conversion between units:"

def test_template():
    data = parse('''
    a float[2] = [14.24,15.23] mm
    b str = ("a = {{?a}[0]:.3e}")
    ''')
    np.testing.assert_equal(data,{
        'a': FloatType([14.24, 15.23], 'mm'),
        'b': StringType('a = 1.424e+01'),
    })
    
    
if __name__ == "__main__":
    # Specify wich test to run
    test = sys.argv[1] if len(sys.argv)>1 else True

    # Loop through all tests
    for fn in dir(sys.modules[__name__]):
        if fn[:5]=='test_' and (test is True or test==fn[5:]):
            print(f"\nTesting: {fn}\n")
            locals()[fn]()
    
