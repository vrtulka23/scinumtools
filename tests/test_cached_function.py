import numpy as np
import os
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

def test_caching():

    file_cache = "tests/cached_data.npy"
    
    if os.path.isfile(file_cache):
        os.remove(file_cache)
    assert not os.path.isfile(file_cache)
    
    @snt.CachedFunction(file_cache)
    def read_data(a, b):
        return dict(a=a, b=b)

    data = read_data('foo','bar')    
    assert data == dict(a='foo', b='bar')

    data = read_data('foo2','bar2')
    assert os.path.isfile(file_cache)
    assert data == dict(a='foo', b='bar')
    
    if os.path.isfile(file_cache):
        os.remove(file_cache)
    assert not os.path.isfile(file_cache)

    @snt.CachedFunction(file_cache)
    def read_data():
        return {
            'array': np.linspace(1,100,100),
            'scalar': 34,
            'string': 'foo',
        }
    
    data = read_data()
    np.testing.assert_equal(data, dict(
        array=np.linspace(1,100,100),
        scalar=34,
        string='foo',
    ))
