import numpy as np
import os
import sys
sys.path.insert(0, 'src')
import pytest
import glob

import scinumtools as snt

@pytest.fixture()
def file_cache():
    dir_cache = "tmp"
    name_cache = "cached_data"
    if os.path.isdir(dir_cache):
        for item in os.listdir(dir_cache):
            if item.startswith(name_cache):
                os.remove(f"{dir_cache}/{item}")
    else:
        os.mkdir(dir_cache)
    return f"{dir_cache}/{name_cache}.npy"

def cache_exists(file_cache, *args, **kwargs):
    file_data = snt.cached_function.hash_file_name(file_cache, args, kwargs)
    return True if glob.glob(file_data) else False

def test_arguments(file_cache):
    
    @snt.CachedFunction(file_cache)
    def read_data(a, b):
        return dict(a=a, b=b)
    
    data = read_data('foo','bar')    
    assert data == dict(a='foo', b='bar')

    # same cache when arguments are the same
    data = read_data('foo','bar')
    assert cache_exists(file_cache,'foo','bar')
    assert data == dict(a='foo', b='bar')
    
    # new cache when arguments are different
    data = read_data('foo2','bar2')
    assert cache_exists(file_cache,'foo2','bar2')
    assert data == dict(a='foo2', b='bar2')

def test_caching(file_cache):

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
