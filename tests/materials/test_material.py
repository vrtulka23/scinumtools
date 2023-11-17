import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import Quantity, Unit
from scinumtools.materials import *

def test_preprocessing():
    
    with MaterialSolver() as ms:
        
        # implicit multiplication and addition
        assert ms.preprocess('C2B4')  == "C * 2 + B * 4"
        assert ms.preprocess('C2 B4') == "C * 2 + B * 4"
        # isotopes and ionizations
        assert ms.preprocess('C{13+2}B{11}H{-}2') == "C{13+2} + B{11} + H{-} * 2"
        # parentheses
        assert ms.preprocess('(CB2)2')                         == "(C + B * 2) * 2"
        assert ms.preprocess('((CB2)2Al)3')                    == "((C + B * 2) * 2 + Al) * 3"
        assert ms.preprocess('C{13+2}(B{11}Li2)4 H{-}2 O{+3}') == "C{13+2} + (B{11} + Li * 2) * 4 + H{-} * 2 + O{+3}"
    
        # preprocessed expressions are constant
        assert ms.preprocess("(C + B * 2) * 2")             == "(C + B * 2) * 2"
        assert ms.preprocess("C{13+2} + (B{11} + Li * 2)4") == "C{13+2} + (B{11} + Li * 2) * 4"

def test_solver():
    
    with MaterialSolver() as ms:
        
        # single atom parsing
        assert str(ms.solve('C'))       == "MaterialPart(p=6 n=6 e=6 m=12.000)"
        assert str(ms.solve('C{13}'))   == "MaterialPart(p=6 n=7 e=6 m=13.003)"
        assert str(ms.solve('C{-2}'))   == "MaterialPart(p=6 n=6 e=4 m=11.999)"
        assert str(ms.solve('C{+}'))    == "MaterialPart(p=6 n=6 e=7 m=12.001)"
        assert str(ms.solve('C{10-}'))  == "MaterialPart(p=6 n=4 e=5 m=10.016)"
        assert str(ms.solve('C{13-2}')) == "MaterialPart(p=6 n=7 e=4 m=13.002)"

        # nucleons
        assert str(ms.solve('[e]'))      == "MaterialPart(p=0 n=0 e=1 m=0.001)"
        assert str(ms.solve('[n]'))      == "MaterialPart(p=0 n=1 e=0 m=1.009)"
        assert str(ms.solve('[n]2'))     == "MaterialPart(p=0 n=2 e=0 m=2.017)"
        assert str(ms.solve('[p]'))      == "MaterialPart(p=1 n=0 e=0 m=1.007)"
        assert str(ms.solve('[p]2'))     == "MaterialPart(p=2 n=0 e=0 m=2.015)"
        assert str(ms.solve('[p]'))      == str(ms.solve('H{1-1}'))
        assert str(ms.solve('[p]B{11}')) == "MaterialPart(p=6 n=6 e=5 m=12.017)"
        
        # hydrogen isotopes
        assert str(ms.solve('H'))       == str(ms.solve('H{1}'))
        assert str(ms.solve('H{+}'))    == str(ms.solve('H{1+}'))
        assert str(ms.solve('D'))       == str(ms.solve('H{2}'))
        assert str(ms.solve('D{-2}'))   == str(ms.solve('H{2-2}'))
        assert str(ms.solve('T'))       == str(ms.solve('H{3}'))
    
        # addition       
        assert str(ms.solve('H{1-1}'))           == "MaterialPart(p=1 n=0 e=0 m=1.007)"
        assert str(ms.solve('B{11}'))            == "MaterialPart(p=5 n=6 e=5 m=11.009)"
        assert str(ms.solve('H{1-1} + B{11}'))   == "MaterialPart(p=6 n=6 e=5 m=12.017)"
    
        # parentheses
        assert str(ms.solve('(H2O)'))   == "MaterialPart(p=10 n=8 e=10 m=18.011)"
        assert str(ms.solve('H(CN)'))   == "MaterialPart(p=14 n=13 e=14 m=27.011)"

        # multiplication
        assert str(ms.solve('H{1-1}2'))             == "MaterialPart(p=2 n=0 e=0 m=2.015)"
        assert str(ms.solve('(H{1-1} + B{11})2'))   == "MaterialPart(p=12 n=12 e=10 m=24.033)"
        
def test_material():
    
    assert str(Material('C')) == "Material(p=6 n=6 e=6 m=12.000)"
    
    # binding energy
    m1 = Quantity(Material('[p][n][e]').mass, 'Da')
    m2 = Quantity(Material('H{2}').mass, 'Da')
    mb = (Quantity(2224.52,'keV')/Unit('[c]2')).to('Da')
    assert str(m1) != str(m2)
    assert m1 == m2 + mb
    #assert Material('He{2}').binding_energy()  == Quantity(2224.581351, 'keV')
    #assert Material('C').binding_energy()/13 == Quantity(7.68, 'MeV')