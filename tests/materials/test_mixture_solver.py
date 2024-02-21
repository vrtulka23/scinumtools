import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import Quantity, Unit 
from scinumtools.materials import *

def test_preprocessing():
    
    mixture = Mixture()
    with MixtureSolver(mixture.atom) as ms:
        
        # implicit multiplication and addition
        assert ms.preprocess('1.0 <H2O>')             == "1.0 * <H2O>"
        assert ms.preprocess('0.5 <H2O> 0.5 <NaCl>')  == "0.5 * <H2O> + 0.5 * <NaCl>"
        assert ms.preprocess('<H2O>')                 == "<H2O>"
        assert ms.preprocess('<H2O> <NaCl>')          == "<H2O> + <NaCl>"
        
def test_solver():
    
    mixture = Mixture()
    with MixtureSolver(mixture.atom) as ms:
        
        # single atom parsing
        assert str(ms.solve('<H2O>'))                 == "Mixture(1.0 H2O)"
        assert str(ms.solve('0.5 <H2O>'))             == "Mixture(0.5 H2O)"
        assert str(ms.solve('0.2 <H2O> 0.8 <NaCl>'))  == "Mixture(0.2 H2O; 0.8 NaCl)"
        assert str(ms.solve('0.7808 <N2> 0.2095 <O2> 0.0093 <Ar> 0.0004 <CO2>')) == \
                    "Mixture(0.7808 N2; 0.2095 O2; 0.0093 Ar; 0.0004 CO2)"
