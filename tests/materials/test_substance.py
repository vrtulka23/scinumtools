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
    substance = Substance()
    assert substance.data_composite() == None

def test_add_element():
    substance = Substance()
    substance.add('B')
    assert substance.expr == 'B'
    assert substance.data_composite(quantity=False).to_text() == """
  expr       mass    Z      N    e      x      X
0    B  10.811028  5.0  5.801  5.0  100.0  100.0
1  avg  10.811028  5.0  5.801  5.0  100.0  100.0
2  sum  10.811028  5.0  5.801  5.0  100.0  100.0
""".strip('\n')

def test_expression():
    substance = Substance('B{11}N{14}H{1}6')
    assert substance.expr == 'B{11}N{14}H{1}6'
    assert substance.data_composite(quantity=False).to_text() == """
    expr       mass      Z       N      e      x          X
0  B{11}  11.009305   5.00   6.000   5.00   12.5   35.44605
1  N{14}  14.003074   7.00   7.000   7.00   12.5   45.08492
2   H{1}   6.046950   6.00   0.000   6.00   75.0   19.46903
3    avg   3.882416   2.25   1.625   2.25   12.5   12.50000
4    sum  31.059330  18.00  13.000  18.00  100.0  100.00000
""".strip('\n')

def test_quantity():
    s = Substance('H2O')
    assert s.data_composite(quantity=False).to_text() == """
  expr       mass          Z         N          e           x           X
0    H   2.015882   2.000000  0.000230   2.000000   66.666667   11.189839
1    O  15.999405   8.000000  8.004480   8.000000   33.333333   88.810161
2  avg   6.005095   3.333333  2.668237   3.333333   33.333333   33.333333
3  sum  18.015286  10.000000  8.004710  10.000000  100.000000  100.000000
""".strip('\n')
    data = s.data_composite()
    assert str(data.H.mass) == "Quantity(2.016e+00 Da)"
    assert str(data.H.Z) == "2.0"
    
def test_context():
    with Substance('H2O') as c:
        assert c.data_composite(quantity=False).to_text() == """
  expr       mass          Z         N          e           x           X
0    H   2.015882   2.000000  0.000230   2.000000   66.666667   11.189839
1    O  15.999405   8.000000  8.004480   8.000000   33.333333   88.810161
2  avg   6.005095   3.333333  2.668237   3.333333   33.333333   33.333333
3  sum  18.015286  10.000000  8.004710  10.000000  100.000000  100.000000
""".strip('\n')

def test_partial_data():
    substance = Substance('B{11}N{14}H{1}6')
    assert substance.data_composite(['B{11}','N{14}'], quantity=False).to_text() == """
    expr       mass     Z     N     e     x          X
0  B{11}  11.009305   5.0   6.0   5.0  12.5  35.446050
1  N{14}  14.003074   7.0   7.0   7.0  12.5  45.084920
2    avg  12.506190   6.0   6.5   6.0  12.5  40.265485
3    sum  25.012379  12.0  13.0  12.0  25.0  80.530970
""".strip('\n')

def test_number_density():
    # here we set the average number density from the test_mass_density()
    # the "n" here is the number density of the molecule and not of all atoms
    substance = Substance('B{11}N{14}H{1}6', number_density=Quantity(1.5123538e+22,'cm-3'))
    assert substance.data_matter(quantity=False).to_text() == """
    expr             n       rho
0  B{11}  1.512354e+22  0.276479
1  N{14}  1.512354e+22  0.351662
2   H{1}  9.074123e+22  0.151858
3    avg  1.512354e+22  0.097500
4    sum  1.209883e+23  0.780000
""".strip('\n')

def test_mass_density():
    
    substance = Substance('B{11}N{14}H{1}6', mass_density=Quantity(780,'kg/m3'))
    assert substance.data_matter(quantity=False).to_text() == """
    expr             n       rho
0  B{11}  1.512354e+22  0.276479
1  N{14}  1.512354e+22  0.351662
2   H{1}  9.074123e+22  0.151858
3    avg  1.512354e+22  0.097500
4    sum  1.209883e+23  0.780000
""".strip('\n')

def test_density_volume():
    
    substance = Substance('B{11}N{14}H{1}6', mass_density=Quantity(780,'kg/m3'), volume=Quantity(1,'l'))
    assert substance.data_matter(quantity=False).to_text() == """
    expr             n       rho             N           M
0  B{11}  1.512354e+22  0.276479  1.512354e+25  276.479187
1  N{14}  1.512354e+22  0.351662  1.512354e+25  351.662379
2   H{1}  9.074123e+22  0.151858  9.074123e+25  151.858434
3    avg  1.512354e+22  0.097500  1.512354e+25   97.500000
4    sum  1.209883e+23  0.780000  1.209883e+26  780.000000
""".strip('\n')

def test_from_dict():
    
    substance = Substance({
        'B{11}': 1,
        'N{14}': 1,
        'H{1}':  6,
    })
    assert substance.data_components(quantity=False).to_text() == """
    expr element  isotope  ionisation       mass  count  Z  N  e
0  B{11}       B       11           0  11.009305      1  5  6  5
1  N{14}       N       14           0  14.003074      1  7  7  7
2   H{1}       H        1           0   1.007825      6  1  0  1
""".strip('\n')
    assert substance.data_composite(quantity=False).to_text() == """
    expr       mass      Z       N      e      x          X
0  B{11}  11.009305   5.00   6.000   5.00   12.5   35.44605
1  N{14}  14.003074   7.00   7.000   7.00   12.5   45.08492
2   H{1}   6.046950   6.00   0.000   6.00   75.0   19.46903
3    avg   3.882416   2.25   1.625   2.25   12.5   12.50000
4    sum  31.059330  18.00  13.000  18.00  100.0  100.00000
""".strip('\n')

def test_arithmetic():
    
    c1 = Substance('B{11}N{14}')
    c2 = Substance('H{1}6')
    c3 = Substance('B{11}N{14}H{1}6')
    e1 = Element('H{1}',6)
    
    # addition two different substances
    c12 = c1 + c2
    for expr, element in c12.components.items():
        assert expr in c3.components
        assert element.proportion == c3.components[expr].proportion
        
    # adding two same substances
    c22 = c2 + c2
    for expr, element in c22.components.items():
        assert expr in c2.components
        assert element.proportion == c2.components[expr].proportion * 2
        
    # addition of an element to a substance
    c1e = c1 + e1
    for expr, element in c1e.components.items():
        assert expr in c3.components
        assert element.proportion == c3.components[expr].proportion

    # multiplication of a substance  
    c1m = c2 * 2
    for expr, element in c1m.components.items():
        assert expr in c2.components
        assert element.proportion == c2.components[expr].proportion * 2
    
def test_most_abundant():
    with Substance('H2O', natural=False, mass_density=Quantity(997,'kg/m3'), volume=Quantity(1,'l')) as c:
        with Capturing() as output:
            c.print()
        assert output == [
            'Components:', 
            '', 
            'expr element  isotope  ionisation  mass[Da]  count  Z  N  e', 
            '   H       H        1           0  1.007825    2.0  1  0  1', 
            '   O       O       16           0 15.994915    1.0  8  8  8', 
            '', 
            'Composite:', 
            '', 
            'Total mass:     Quantity(1.801e+01 Da)', 
            'Total number:   3.0', 
            '', 
            'expr  mass[Da]         Z        N         e       x[%]       X[%]', 
            '   H  2.015650  2.000000 0.000000  2.000000  66.666667  11.191487', 
            '   O 15.994915  8.000000 8.000000  8.000000  33.333333  88.808513', 
            ' avg  6.003522  3.333333 2.666667  3.333333  33.333333  33.333333', 
            ' sum 18.010565 10.000000 8.000000 10.000000 100.000000 100.000000',
            '',
            'Matter:', 
            '', 
            'Mass density:   Quantity(9.970e-01 g*cm-3)', 
            'Number density: Quantity(3.334e+22 cm-3)', 
            'Volume:         Quantity(1.000e+00 l)', 
            'Mass:           Quantity(9.970e+02 g)',
            '',
            'expr      n[cm-3]  rho[g/cm3]            N       M[g]',
            '   H 6.667280e+22    0.111579 6.667280e+25 111.579129',
            '   O 3.333640e+22    0.885421 3.333640e+25 885.420871',
            ' avg 3.333640e+22    0.332333 3.333640e+25 332.333333',
            ' sum 1.000092e+23    0.997000 1.000092e+26 997.000000',
        ]

def test_print():
    
    assert str(Substance('DT'))                 == "Substance(mass=5.030 Z=2 N=3.000 e=2)"
    assert str(Substance('H2O', natural=False)) == "Substance(mass=18.011 Z=10 N=8.000 e=10)"
    
    c = Substance({
        'B{11}': 1,
        'N{14}': 1,
        'H{1}':  6,
    })
    assert (str(c)) == "Substance(mass=31.059 Z=18 N=13.000 e=18)"
    
def test_nucleons():
    
    c = Substance('[p]3[n]2[e]')
    data = c.data_components(quantity=False)
    assert data.to_text() == """
  expr element  isotope  ionisation      mass  count  Z  N  e
0  [p]     [p]        0           0  1.007277    3.0  1  0  0
1  [n]     [n]        0           0  1.008666    2.0  0  1  0
2  [e]     [e]        0           0  0.000549    1.0  0  0  1
""".strip('\n')
    data = c.data_composite(quantity=False)
    assert data.to_text() == """
  expr      mass    Z         N         e           x           X
0  [p]  3.021831  3.0  0.000000  0.000000   50.000000   59.960408
1  [n]  2.017331  0.0  2.000000  0.000000   33.333333   40.028707
2  [e]  0.000549  0.0  0.000000  1.000000   16.666667    0.010885
3  avg  0.839952  0.5  0.333333  0.166667   16.666667   16.666667
4  sum  5.039711  3.0  2.000000  1.000000  100.000000  100.000000
""".strip('\n')
    
def test_parameter_selection():
    
    with Substance('H2O', natural=False) as c:
        data = c.data_components()
        assert data.O['N'] == 8
        assert data.H.count == 2
        data = c.data_composite()
        assert data['sum'].e == 10
        assert data.H.mass == Quantity(2.015650, 'Da')
        data = c.data_composite(['H'], quantity=False)
        assert data.to_text() == """
  expr      mass    Z    N    e          x          X
0    H  2.015650  2.0  0.0  2.0  66.666667  11.191487
1  avg  1.007825  1.0  0.0  1.0  33.333333   5.595744
2  sum  2.015650  2.0  0.0  2.0  66.666667  11.191487
""".strip('\n')


def test_prints():

    with Substance('H2O', natural=False) as c:
        with Capturing() as output:
            c.print_components()
        assert output == [
            'expr element  isotope  ionisation  mass[Da]  count  Z  N  e', 
            '   H       H        1           0  1.007825    2.0  1  0  1', 
            '   O       O       16           0 15.994915    1.0  8  8  8'
        ]

        with Capturing() as output:
            c.print_composite()
        assert output == [
            'expr  mass[Da]         Z        N         e       x[%]       X[%]',
            '   H  2.015650  2.000000 0.000000  2.000000  66.666667  11.191487',
            '   O 15.994915  8.000000 8.000000  8.000000  33.333333  88.808513',
            ' avg  6.003522  3.333333 2.666667  3.333333  33.333333  33.333333',
            ' sum 18.010565 10.000000 8.000000 10.000000 100.000000 100.000000',
        ]
        
    with Substance('H2O', natural=False, mass_density=Quantity(997,'kg/m3'), volume=Quantity(1,'l')) as c:
        with Capturing() as output:
            c.print_matter()
        assert output == [
            'expr      n[cm-3]  rho[g/cm3]            N       M[g]', 
            '   H 6.667280e+22    0.111579 6.667280e+25 111.579129', 
            '   O 3.333640e+22    0.885421 3.333640e+25 885.420871', 
            ' avg 3.333640e+22    0.332333 3.333640e+25 332.333333', 
            ' sum 1.000092e+23    0.997000 1.000092e+26 997.000000'
        ]
