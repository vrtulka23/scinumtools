import numpy as np
import pytest
from math import isclose
import os
import sys
import time
import cProfile
import pstats
sys.path.insert(0, 'src')

from scinumtools.units import *

def test_scalars():
    q = Quantity(23, 'erg')
    
    tstart = time.time()
    for i in range(100):
        q.to('keV')
    ttotal = time.time() - tstart
    assert ttotal < 3.e-1
    
def test_arrays():
    q = Quantity(np.linspace(1,100,40), 'cm')
    
    tstart = time.time()
    for i in range(100):
        r = q.to('au')
    ttotal = time.time() - tstart
    assert ttotal < 3.e-1
    
    tstart = time.time()
    for i in q:
        r = i
    ttotal = time.time() - tstart
    assert ttotal < 3.e-1

def test_profiling():
    
    with cProfile.Profile() as pr:
        
        q = Quantity(np.linspace(1,100,40), 'cm')
    
        for i in range(100):
            r = q.to('au')
        
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    