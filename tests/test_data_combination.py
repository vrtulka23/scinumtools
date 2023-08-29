import numpy as np
import os
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

def test_data_combinations():
    
    pc = snt.DataCombination([
        ['a','b'],
        ['c','d','e']
    ])

    # test keys
    keys = [(0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2)]
    for i,key in enumerate(pc.keys()):
        assert keys[i] == key

    # test values
    values = [('a', 'c'),
              ('a', 'd'),
              ('a', 'e'),
              ('b', 'c'),
              ('b', 'd'),
              ('b', 'e')]
    for i,value in enumerate(pc.values()):
        assert values[i] == value

    # test items
    for i,(key,value) in enumerate(pc.items()):
        assert keys[i] == key
        assert values[i] == value
