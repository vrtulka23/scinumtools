import numpy as np
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.phys import *

def test_constants():

    assert ConstCGS.k_B == 1.380658e-16
    assert ConstMKS.k_B == 1.380649e-2 
    
