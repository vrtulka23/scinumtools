import numpy as np
import pytest
from math import isclose
from io import StringIO 
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.units import Quantity, Unit 
from scinumtools.materials import *

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def test_empty():
    compound = Compound()
    assert compound.data_compound() == None

def test_add_element():
    compound = Compound()
    compound.add_element(Element('B'))
    assert compound.data_compound(quantity=False).to_text() == """
  expression  count          A    Z      N    e
0          B    1.0  10.811028  5.0  5.801  5.0
1        avg    1.0  10.811028  5.0  5.801  5.0
2        sum    1.0  10.811028  5.0  5.801  5.0
""".strip('\n')

def test_expression():
    compound = Compound('B{11}N{14}H{1}6')
    assert compound.data_compound(quantity=False).to_text() == """
  expression     count          A      Z       N      e
0      B{11}  1.000000  11.009305   5.00   6.000   5.00
1      N{14}  1.000000  14.003074   7.00   7.000   7.00
2       H{1}  6.000000   6.046950   6.00   0.000   6.00
3        avg  2.666667   3.882416   2.25   1.625   2.25
4        sum  8.000000  31.059330  18.00  13.000  18.00
""".strip('\n')

def test_context():
    with Compound('H2O') as c:
        assert c.data_compound(quantity=False).to_text() == """
  expression  count          A          Z         N          e
0          H    2.0   2.015882   2.000000  0.000230   2.000000
1          O    1.0  15.999405   8.000000  8.004480   8.000000
2        avg    1.5   6.005095   3.333333  2.668237   3.333333
3        sum    3.0  18.015286  10.000000  8.004710  10.000000
""".strip('\n')

def test_partial_data():
    compound = Compound('B{11}N{14}H{1}6')
    assert compound.data_compound(['B{11}','N{14}'], quantity=False).to_text() == """
  expression  count          A     Z     N     e
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
    assert compound.data_compound(quantity=False).to_text() == """
  expression     count          A      Z       N      e             n       rho          X
0      B{11}  1.000000  11.009305   5.00   6.000   5.00  1.512354e+22  0.276479   35.44605
1      N{14}  1.000000  14.003074   7.00   7.000   7.00  1.512354e+22  0.351662   45.08492
2       H{1}  6.000000   6.046950   6.00   0.000   6.00  9.074123e+22  0.151858   19.46903
3        avg  2.666667   3.882416   2.25   1.625   2.25  1.512354e+22  0.097500   12.50000
4        sum  8.000000  31.059330  18.00  13.000  18.00  1.209883e+23  0.780000  100.00000
""".strip('\n')
    
def test_density_volume():
    
    compound = Compound('B{11}N{14}H{1}6')
    compound.set_amount(
        Quantity(780,'kg/m3'),
        Quantity(1,'l')
    )
    assert compound.data_compound(quantity=False).to_text() == """
  expression     count          A      Z       N      e             n       rho          X           n_V         M_V
0      B{11}  1.000000  11.009305   5.00   6.000   5.00  1.512354e+22  0.276479   35.44605  1.512354e+25  276.479187
1      N{14}  1.000000  14.003074   7.00   7.000   7.00  1.512354e+22  0.351662   45.08492  1.512354e+25  351.662379
2       H{1}  6.000000   6.046950   6.00   0.000   6.00  9.074123e+22  0.151858   19.46903  9.074123e+25  151.858434
3        avg  2.666667   3.882416   2.25   1.625   2.25  1.512354e+22  0.097500   12.50000  1.512354e+25   97.500000
4        sum  8.000000  31.059330  18.00  13.000  18.00  1.209883e+23  0.780000  100.00000  1.209883e+26  780.000000
""".strip('\n')

def test_from_elements():
    
    compound = Compound.from_elements([
            Element('B{11}',1),
            Element('N{14}',1),
            Element('H{1}',6),
    ])
    assert compound.data_elements(quantity=False).to_text() == """
  expression element  isotope  ionisation          A  Z  N  e
0      B{11}       B       11           0  11.009305  5  6  5
1      N{14}       N       14           0  14.003074  7  7  7
2       H{1}       H        1           0   1.007825  1  0  1
""".strip('\n')
    assert compound.data_compound(quantity=False).to_text() == """
  expression     count          A      Z       N      e
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
    
def test_most_abundant():
    with Compound('H2O', natural=False) as c:
        c.set_amount(rho=Quantity(997,'kg/m3'), V=Quantity(1,'l'))
        with Capturing() as output:
            c.print()
        assert output == [
            'Properties:', '', 'Molecular mass: Quantity(1.801e+01 Da)', 
            'Mass density: Quantity(9.970e+02 kg*m-3)', 
            'Molecular density: Quantity(3.334e+28 m-3)', 
            'Volume: Quantity(1.000e+00 l)', 
            '', 
            'Elements:', 
            '', 
            'expression element  isotope  ionisation     A[Da]  Z  N  e', 
            '         H       H        1           0  1.007825  1  0  1', 
            '         O       O       16           0 15.994915  8  8  8', 
            '', 
            'Compound:', 
            '', 
            'expression  count     A[Da]         Z        N         e      n[cm-3]  rho[g/cm3]       X[%]          n_V     M_V[g]', 
            '         H    2.0  2.015650  2.000000 0.000000  2.000000 6.667280e+22    0.111579  11.191487 6.667280e+25 111.579129', 
            '         O    1.0 15.994915  8.000000 8.000000  8.000000 3.333640e+22    0.885421  88.808513 3.333640e+25 885.420871', 
            '       avg    1.5  6.003522  3.333333 2.666667  3.333333 3.333640e+22    0.332333  33.333333 3.333640e+25 332.333333', 
            '       sum    3.0 18.010565 10.000000 8.000000 10.000000 1.000092e+23    0.997000 100.000000 1.000092e+26 997.000000'
        ]

def test_print():
    
    assert str(Compound('DT'))                 == "Compound(p=2 n=3.000 e=2 A=5.030)"
    assert str(Compound('H2O', natural=False)) == "Compound(p=10 n=8.000 e=10 A=18.011)"
    
    c = Compound.from_elements([
        Element('B{11}',1),
        Element('N{14}',1),
        Element('H{1}',6),
    ])
    assert (str(c)) == "Compound(p=18 n=13.000 e=18 A=31.059)"
    
def test_nucleons():
    
    c = Compound('[p]3[n]2[e]')
    data = c.data_elements(quantity=False)
    assert data.to_text() == """
  expression element  isotope  ionisation         A  Z  N  e
0        [p]     [p]        0           0  1.007277  1  0  0
1        [n]     [n]        0           0  1.008666  0  1  0
2        [e]     [e]        0           0  0.000549  0  0  1
""".strip('\n')
    data = c.data_compound(quantity=False)
    assert data.to_text() == """
  expression  count         A    Z         N         e
0        [p]    3.0  3.021831  3.0  0.000000  0.000000
1        [n]    2.0  2.017331  0.0  2.000000  0.000000
2        [e]    1.0  0.000549  0.0  0.000000  1.000000
3        avg    2.0  0.839952  0.5  0.333333  0.166667
4        sum    6.0  5.039711  3.0  2.000000  1.000000
""".strip('\n')
    
def test_parameter_selection():
    
    with Compound('H2O', natural=False) as c:
        data = c.data_elements()
        assert data.O['N'] == 8
        data = c.data_compound()
        assert data['sum'].e == 10
        assert data.H.count == 2
        assert data.H.A == Quantity(2.015650, 'Da')
        data = c.data_compound(['H'], quantity=False)
        assert data.to_text() == """
  expression  count         A    Z    N    e
0          H    2.0  2.015650  2.0  0.0  2.0
1        avg    2.0  1.007825  1.0  0.0  1.0
2        sum    2.0  2.015650  2.0  0.0  2.0
""".strip('\n')


def test_prints():

    with Compound('H2O', natural=False) as c:
        with Capturing() as output:
            c.print_elements()
        assert output == [
            'expression element  isotope  ionisation     A[Da]  Z  N  e', 
            '         H       H        1           0  1.007825  1  0  1', 
            '         O       O       16           0 15.994915  8  8  8'
        ]

        with Capturing() as output:
            c.print_compound()
        assert output == [
            'expression  count     A[Da]         Z        N         e',
            '         H    2.0  2.015650  2.000000 0.000000  2.000000',
            '         O    1.0 15.994915  8.000000 8.000000  8.000000',
            '       avg    1.5  6.003522  3.333333 2.666667  3.333333',
            '       sum    3.0 18.010565 10.000000 8.000000 10.000000',
        ]
        c.set_amount(rho=Quantity(997,'kg/m3'), V=Quantity(1,'l'))
        with Capturing() as output:
            c.print_compound()
        assert output == [
            'expression  count     A[Da]         Z        N         e      n[cm-3]  rho[g/cm3]       X[%]          n_V     M_V[g]', 
            '         H    2.0  2.015650  2.000000 0.000000  2.000000 6.667280e+22    0.111579  11.191487 6.667280e+25 111.579129', 
            '         O    1.0 15.994915  8.000000 8.000000  8.000000 3.333640e+22    0.885421  88.808513 3.333640e+25 885.420871', 
            '       avg    1.5  6.003522  3.333333 2.666667  3.333333 3.333640e+22    0.332333  33.333333 3.333640e+25 332.333333', 
            '       sum    3.0 18.010565 10.000000 8.000000 10.000000 1.000092e+23    0.997000 100.000000 1.000092e+26 997.000000'
        ]
