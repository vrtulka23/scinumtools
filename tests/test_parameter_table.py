import numpy as np
import pandas as pd
from textwrap import dedent
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

def test_parameter_list():
    def test(params):
        assert params[0].a == 1
        assert params[1]['a'] == 4
        for param in params:
            assert param['a'] in [1,4]
        for index,settings in params.items():
            assert param['b'] in [2,5]        
    # append values
    with snt.ParameterTable(['a','b','c']) as params:
        params.append([1, 2, 3])
        params.append([4, 5, 6])
        test(params)
    # direct value insertion
    params = snt.ParameterTable(['a','b','c'],[
        [1, 2, 3],
        [4, 5, 6]
    ])
    test(params)

def test_parameter_dict():
    def test(params):
        assert params['d'].a == 1
        assert params['e']['a'] == 4
        for param in params:
            assert param['a'] in [1,4]
        for index,settings in params.items():
            assert param['b'] in [2,5]
    # append values
    with snt.ParameterTable(['a','b','c'], keys=True) as params:
        params['d'] = [1, 2, 3]
        params.append( 'e', [4, 5, 6] )
        test(params)
    # direct value insertion
    params = snt.ParameterTable(['a','b','c'],{
        'd': [1, 2, 3],
        'e': [4, 5, 6]
    }, keys=True)
    test(params)
    
def test_shape():
    
    with snt.ParameterTable(['a','b','c']) as params:
        params.append([1, 2, 3])
        params.append([4, 5, 6])
        assert params.shape() == (2, 3)
        
def test_rows_attributes():
    
    with snt.ParameterTable(['a','b','c'], keys=True) as params:
        params['d'] = [1, 2, 3]
        params.append( 'e', [4, 5, 6] )
        
        assert str(params.d)   == "ParameterSettings(a=1 b=2 c=3)"
        assert params.d.a      == 1
        
def test_delete_item():
    
    with snt.ParameterTable(['a','b','c']) as params:
        params.append([1, 2, 3])
        params.append([4, 5, 6])
        
        assert len(params) == 2
        del params[0]
        assert len(params) == 1
        assert params[0].a == 4
        assert params[0].b == 5
        assert params[0].c == 6
        
    with snt.ParameterTable(['a','b','c'], keys=True) as params:
        params['d'] = [1, 2, 3]
        params.append( 'e', [4, 5, 6] )
        
        del params['d']
        assert params._keys == ['e']
        assert 'd' not in params._data
        assert params['e'].a == 4
        assert params['e'].b == 5
        assert params['e'].c == 6

def test_data():
    
    with snt.ParameterTable(['a','b','c']) as params:
        params.append([1, 2, 3])
        params.append([4, 5, 6])
        assert params.data() == [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 4, 'b': 5, 'c': 6},
        ]
        
    with snt.ParameterTable(['a','b','c'], keys=True) as params:
        params['d'] = [1, 2, 3]
        params['e'] = [4, 5, 6]
        assert params.data() == {
            'd': {'a': 1, 'b': 2, 'c': 3},
            'e': {'a': 4, 'b': 5, 'c': 6},
        }
        
def test_to_dataframe():
    
    with snt.ParameterTable(['a','b','c']) as params:
        params.append([1, 2, 3])
        params.append([4, 5, 6])
        assert params.to_dataframe().equals(pd.DataFrame({
            'a': [1, 4],
            'b': [2, 5],
            'c': [3, 6],
        }))
        
    with snt.ParameterTable(['a','b','c'], keys=True) as params:
        params['d'] = [1, 2, 3]
        params['e'] = [4, 5, 6]
        assert params.to_dataframe().equals(pd.DataFrame({
            '#': ['d','e'],
            'a': [1, 4],
            'b': [2, 5],
            'c': [3, 6],
        }))
        
def test_to_text():
    
    with snt.ParameterTable(['a','b','c']) as params:
        params.append([1, 2, 3])
        params.append([4, 5, 6])
        assert params.to_text() == """
   a  b  c
0  1  2  3
1  4  5  6
""".strip('\n')
        
    with snt.ParameterTable(['a','b','c'], keys=True, keyname='x') as params:
        params['d'] = [1, 2, 3]
        params['e'] = [4, 5, 6]
        assert params.to_text() == """
   x  a  b  c
0  d  1  2  3
1  e  4  5  6
""".strip('\n')
