import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import Quantity, Unit 
from scinumtools.materials import *

def test_preprocessing():
    
    compound = Compound()
    with MaterialSolver(compound.atom) as ms:
        
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
    
    compound = Compound()
    with MaterialSolver(compound.atom) as ms:
        
        # single atom parsing
        assert str(ms.solve('C'))       == "Compound(p=6 n=6.011 e=6 A=12.011)"
        assert str(ms.solve('C{12}'))   == "Compound(p=6 n=6.000 e=6 A=12.000)"
        assert str(ms.solve('C{-2}'))   == "Compound(p=6 n=6.011 e=4 A=12.010)"
        assert str(ms.solve('C{+}'))    == "Compound(p=6 n=6.011 e=7 A=12.011)"
        assert str(ms.solve('C{12-}'))  == "Compound(p=6 n=6.000 e=5 A=11.999)"
        assert str(ms.solve('C{13}'))   == "Compound(p=6 n=7.000 e=6 A=13.003)"
        assert str(ms.solve('C{13-2}')) == "Compound(p=6 n=7.000 e=4 A=13.002)"

        # nucleons
        assert str(ms.solve('[e]'))      == "Compound(p=0 n=0.000 e=1 A=0.001)"
        assert str(ms.solve('[n]'))      == "Compound(p=0 n=1.000 e=0 A=1.009)"
        assert str(ms.solve('[n]2'))     == "Compound(p=0 n=2.000 e=0 A=2.017)"
        assert str(ms.solve('[p]'))      == "Compound(p=1 n=0.000 e=0 A=1.007)"
        assert str(ms.solve('[p]2'))     == "Compound(p=2 n=0.000 e=0 A=2.015)"
        assert str(ms.solve('[p]B{11}')) == "Compound(p=6 n=6.000 e=5 A=12.017)"
        
        # hydrogen isotopes
        assert str(ms.solve('[p]'))     == str(ms.solve('H{1-1}'))
        assert str(ms.solve('H{1+}'))   == str(ms.solve('H{1+1}'))
        assert str(ms.solve('D'))       == str(ms.solve('H{2}'))
        assert str(ms.solve('D{2-2}'))  == str(ms.solve('H{2-2}'))
        assert str(ms.solve('T'))       == str(ms.solve('H{3}'))
    
        # addition       
        assert str(ms.solve('H{1-1}'))           == "Compound(p=1 n=0.000 e=0 A=1.007)"
        assert str(ms.solve('B{11}'))            == "Compound(p=5 n=6.000 e=5 A=11.009)"
        assert str(ms.solve('H{1-1} + B{11}'))   == "Compound(p=6 n=6.000 e=5 A=12.017)"
    
        # parentheses
        assert str(ms.solve('(H2O)'))   == "Compound(p=10 n=8.005 e=10 A=18.015)"
        assert str(ms.solve('H(CN)'))   == "Compound(p=14 n=13.014 e=14 A=27.025)"
        assert str(ms.solve('Ca(OH)2')) == "Compound(p=38 n=36.125 e=38 A=74.093)"

        # multiplication
        assert str(ms.solve('H{1-1}2'))             == "Compound(p=2 n=0.000 e=0 A=2.015)"
        assert str(ms.solve('(H{1-1} + B{11})2'))   == "Compound(p=12 n=12.000 e=10 A=24.033)"
        