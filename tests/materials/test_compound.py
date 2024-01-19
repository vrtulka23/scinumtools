import numpy as np
import pytest
from math import isclose
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import Quantity, Unit 
from scinumtools.materials import *

def test_empty():
    compound = Compound()
    assert compound.data_compound() == None

def test_add_element():
    compound = Compound()
    compound.add_element(Element('B'))
    assert compound.data_compound().to_text() == """
  expression  count      A[Da]    Z      N    e
0          B    1.0  10.811028  5.0  5.801  5.0
1        avg    1.0  10.811028  5.0  5.801  5.0
2        sum    1.0  10.811028  5.0  5.801  5.0
""".strip('\n')

def test_expression():
    compound = Compound('B{11}N{14}H{1}6')
    assert compound.data_compound().to_text() == """
  expression     count      A[Da]      Z       N      e
0      B{11}  1.000000  11.009305   5.00   6.000   5.00
1      N{14}  1.000000  14.003074   7.00   7.000   7.00
2       H{1}  6.000000   6.046950   6.00   0.000   6.00
3        avg  2.666667   3.882416   2.25   1.625   2.25
4        sum  8.000000  31.059330  18.00  13.000  18.00
""".strip('\n')

def test_partial_data():
    compound = Compound('B{11}N{14}H{1}6')
    assert compound.data_compound(['B{11}','N{14}']).to_text() == """
  expression  count      A[Da]     Z     N     e
0      B{11}    1.0  11.009305   5.0   6.0   5.0
1      N{14}    1.0  14.003074   7.0   7.0   7.0
2        avg    1.0  12.506190   6.0   6.5   6.0
3        sum    2.0  25.012379  12.0  13.0  12.0
""".strip('\n')

def test_density():
    
    compound = Compound('B{11}N{14}H{1}6')
    compound.set_amount(
        Quantity(780,'kg/m3')
    )
    assert compound.data_compound().to_text() == """
  expression     count      A[Da]      Z       N      e       n[cm-3]  rho[g/cm3]       X[%]
0      B{11}  1.000000  11.009305   5.00   6.000   5.00  1.512354e+22    0.276479   35.44605
1      N{14}  1.000000  14.003074   7.00   7.000   7.00  1.512354e+22    0.351662   45.08492
2       H{1}  6.000000   6.046950   6.00   0.000   6.00  9.074123e+22    0.151858   19.46903
3        avg  2.666667   3.882416   2.25   1.625   2.25  1.512354e+22    0.097500   12.50000
4        sum  8.000000  31.059330  18.00  13.000  18.00  1.209883e+23    0.780000  100.00000
""".strip('\n')
    
def test_density_volume():
    
    compound = Compound('B{11}N{14}H{1}6')
    compound.set_amount(
        Quantity(780,'kg/m3'),
        Quantity(1,'l')
    )
    assert compound.data_compound().to_text() == """
  expression     count      A[Da]      Z       N      e       n[cm-3]  rho[g/cm3]       X[%]           n_V      M_V[g]
0      B{11}  1.000000  11.009305   5.00   6.000   5.00  1.512354e+22    0.276479   35.44605  1.512354e+25  276.479187
1      N{14}  1.000000  14.003074   7.00   7.000   7.00  1.512354e+22    0.351662   45.08492  1.512354e+25  351.662379
2       H{1}  6.000000   6.046950   6.00   0.000   6.00  9.074123e+22    0.151858   19.46903  9.074123e+25  151.858434
3        avg  2.666667   3.882416   2.25   1.625   2.25  1.512354e+22    0.097500   12.50000  1.512354e+25   97.500000
4        sum  8.000000  31.059330  18.00  13.000  18.00  1.209883e+23    0.780000  100.00000  1.209883e+26  780.000000
""".strip('\n')

def test_from_elements():
    
    compound = Compound.from_elements([
            Element('B{11}',1),
            Element('N{14}',1),
            Element('H{1}',6),
    ])
    assert compound.data_elements().to_text() == """
  expression element isotope ionisation      A[Da]  Z  N  e  A_nuc[Da]  E_bin[MeV]
0      B{11}       B      11          0  11.009305  5  6  5  11.091122    6.928315
1      N{14}       N      14          0  14.003074  7  7  7  14.115439    7.476214
2       H{1}       H       1          0   1.007825  1  0  1   1.007826    0.000598
""".strip('\n')
    assert compound.data_compound().to_text() == """
  expression     count      A[Da]      Z       N      e
0      B{11}  1.000000  11.009305   5.00   6.000   5.00
1      N{14}  1.000000  14.003074   7.00   7.000   7.00
2       H{1}  6.000000   6.046950   6.00   0.000   6.00
3        avg  2.666667   3.882416   2.25   1.625   2.25
4        sum  8.000000  31.059330  18.00  13.000  18.00
""".strip('\n')

def test_arithmetic():
    
    c1 = Compound('B{11}N{14}')
    c2 = Compound('H{1}6')
    c3 = Compound('B{11}N{14}H{1}6')
    e1 = Element('H{1}',6)
    
    # addition two different compounds
    c12 = c1 + c2
    for expr, element in c12.elements.items():
        assert expr in c3.elements
        assert element.count == c3.elements[expr].count
        
    # adding two same compounds
    c22 = c2 + c2
    for expr, element in c22.elements.items():
        assert expr in c2.elements
        assert element.count == c2.elements[expr].count * 2
        
    # addition of an element to a compound
    c1e = c1 + e1
    for expr, element in c1e.elements.items():
        assert expr in c3.elements
        assert element.count == c3.elements[expr].count

    # multiplication of a compound  
    c1m = c2 * 2
    for expr, element in c1m.elements.items():
        assert expr in c2.elements
        assert element.count == c2.elements[expr].count * 2
    