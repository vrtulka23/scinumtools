import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import Quantity, Unit 
from scinumtools.materials import *

def test_preprocessing():
    
    compound = Molecule()
    with MoleculeSolver(compound.atom) as ms:
        
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
    
    compound = Molecule()
    with MoleculeSolver(compound.atom) as ms:
        
        # single atom parsing
        assert str(ms.solve('C'))       == "Molecule(A=12.011 Z=6 N=6.011 e=6)"
        assert str(ms.solve('C{12}'))   == "Molecule(A=12.000 Z=6 N=6.000 e=6)"
        assert str(ms.solve('C{-2}'))   == "Molecule(A=12.010 Z=6 N=6.011 e=4)"
        assert str(ms.solve('C{+}'))    == "Molecule(A=12.011 Z=6 N=6.011 e=7)"
        assert str(ms.solve('C{12-}'))  == "Molecule(A=11.999 Z=6 N=6.000 e=5)"
        assert str(ms.solve('C{13}'))   == "Molecule(A=13.003 Z=6 N=7.000 e=6)"
        assert str(ms.solve('C{13-2}')) == "Molecule(A=13.002 Z=6 N=7.000 e=4)"

        # nucleons
        assert str(ms.solve('[e]'))      == "Molecule(A=0.001 Z=0 N=0.000 e=1)"
        assert str(ms.solve('[n]'))      == "Molecule(A=1.009 Z=0 N=1.000 e=0)"
        assert str(ms.solve('[n]2'))     == "Molecule(A=2.017 Z=0 N=2.000 e=0)"
        assert str(ms.solve('[p]'))      == "Molecule(A=1.007 Z=1 N=0.000 e=0)"
        assert str(ms.solve('[p]2'))     == "Molecule(A=2.015 Z=2 N=0.000 e=0)"
        assert str(ms.solve('[p]B{11}')) == "Molecule(A=12.017 Z=6 N=6.000 e=5)"
        
        # hydrogen isotopes
        assert str(ms.solve('[p]'))     == str(ms.solve('H{1-1}'))
        assert str(ms.solve('H{1+}'))   == str(ms.solve('H{1+1}'))
        assert str(ms.solve('D'))       == str(ms.solve('H{2}'))
        assert str(ms.solve('D{2-2}'))  == str(ms.solve('H{2-2}'))
        assert str(ms.solve('T'))       == str(ms.solve('H{3}'))
    
        # addition       
        assert str(ms.solve('H{1-1}'))           == "Molecule(A=1.007 Z=1 N=0.000 e=0)"
        assert str(ms.solve('B{11}'))            == "Molecule(A=11.009 Z=5 N=6.000 e=5)"
        assert str(ms.solve('H{1-1} + B{11}'))   == "Molecule(A=12.017 Z=6 N=6.000 e=5)"
    
        # parentheses
        assert str(ms.solve('(H2O)'))   == "Molecule(A=18.015 Z=10 N=8.005 e=10)"
        assert str(ms.solve('H(CN)'))   == "Molecule(A=27.025 Z=14 N=13.014 e=14)"
        assert str(ms.solve('Ca(OH)2')) == "Molecule(A=74.093 Z=38 N=36.125 e=38)"

        # multiplication
        assert str(ms.solve('H{1-1}2'))             == "Molecule(A=2.015 Z=2 N=0.000 e=0)"
        assert str(ms.solve('(H{1-1} + B{11})2'))   == "Molecule(A=24.033 Z=12 N=12.000 e=10)"
        