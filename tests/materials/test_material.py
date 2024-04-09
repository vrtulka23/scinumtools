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
    material = Material()
    assert material.data_components() == None
    
def test_set_dictionary():
    material = Material({
        'H2O': 1.0
    })
    assert material.data_components(quantity=False).to_text() == """
  expr  fraction       mass     Z        N     e
0  H2O       1.0  18.015286  10.0  8.00471  10.0
""".strip('\n')

    material = Material({
        'H2O':  0.2,
        'NaCl': 0.8,
    })
    assert material.data_components(quantity=False).to_text() == """
   expr  fraction       mass     Z         N     e
0   H2O       0.2  18.015286  10.0   8.00471  10.0
1  NaCl       0.8  58.442707  28.0  30.48480  28.0
""".strip('\n')

def test_quantities():
    material = Material({
        'H2O': 1.0
    })
    assert material.data_components(quantity=False).to_text() == """
  expr  fraction       mass     Z        N     e
0  H2O       1.0  18.015286  10.0  8.00471  10.0
""".strip('\n')
    data = material.data_components()
    assert str(data.H2O.mass) == "Quantity(1.802e+01 Da)"
    assert str(data.H2O.Z) == "10.0"
    
def test_expr():
    material = Material('0.2 <H2O> 0.8 <NaCl>')
    assert material.data_components(quantity=False).to_text() == """
   expr  fraction       mass     Z         N     e
0   H2O       0.2  18.015286  10.0   8.00471  10.0
1  NaCl       0.8  58.442707  28.0  30.48480  28.0
""".strip('\n')

def test_print_data():
    material = Material('0.2 <H2O> 0.8 <NaCl>')
    with Capturing() as output:
        material.print_components()
    assert output == [
        'expr  fraction  mass[Da]    Z        N    e', 
        ' H2O       0.2 18.015286 10.0  8.00471 10.0', 
        'NaCl       0.8 58.442707 28.0 30.48480 28.0', 
    ]
    with Capturing() as output:
        material.print_composite()
    assert output == [
        'expr  x[%]       X[%]', 
        ' H2O  20.0   7.154996', 
        'NaCl  80.0  92.845004', 
        ' avg  50.0  50.000000', 
        ' sum 100.0 100.000000',
    ]

def test_norm_number():
    material = Material('2 <H2O> 3 <NaCl>')
    assert material.data_composite(quantity=False).to_text() == """
   expr      x           X
0   H2O   40.0   17.047121
1  NaCl   60.0   82.952879
2   avg   50.0   50.000000
3   sum  100.0  100.000000
""".strip('\n')

def test_norm_number_fraction():
    material = Material('0.2 <H2O> 0.3 <NaCl>')
    assert material.data_composite(quantity=False).to_text() == """
   expr      x           X
0   H2O   40.0   17.047121
1  NaCl   60.0   82.952879
2   avg   50.0   50.000000
3   sum  100.0  100.000000
""".strip('\n')
    
def test_norm_mass_fraction():
    # setting mass fraction
    material = Material('0.2 <H2O> 0.3 <NaCl>', norm_type=Norm.MASS_FRACTION)
    assert material.data_composite(quantity=False).to_text() == """
   expr           x      X
0   H2O   68.381526   40.0
1  NaCl   31.618474   60.0
2   avg   50.000000   50.0
3   sum  100.000000  100.0
""".strip('\n')
    
    # checking if number fractions given above produce the same mass fractions
    material = Material('0.683815 <H2O> 0.316185 <NaCl>', norm_type=Norm.NUMBER_FRACTION)
    assert material.data_composite(quantity=False).to_text() == """
   expr         x           X
0   H2O   68.3815   39.999971
1  NaCl   31.6185   60.000029
2   avg   50.0000   50.000000
3   sum  100.0000  100.000000
""".strip('\n')

def test_natural_abundances():
    # natural abundances
    material = Material({
        'H2O': 1.0
    }, natural=True)
    assert isclose(
        material.data_components(quantity=False).H2O.mass, 
        18.015286, 
        rel_tol=MAGNITUDE_PRECISION
    )
    
    # highest abundances
    material = Material({
        'H2O': 1.0
    }, natural=False)
    assert isclose(
        material.data_components(quantity=False).H2O.mass, 
        18.010565, 
        rel_tol=MAGNITUDE_PRECISION
    )

def test_example():
    m = Material({
       'N2':  78.0840,
       'O2':  20.9460,
       'Ar':  0.93400,
       'CO2': 0.03600,
    }, norm_type=Norm.NUMBER_FRACTION)
    assert m.data_components(quantity=False).to_text() == """
  expr  fraction       mass     Z          N     e
0   N2    78.084  28.013406  14.0  14.007280  14.0
1   O2    20.946  31.998810  16.0  16.008960  16.0
2   Ar     0.934  39.947799  18.0  21.985398  18.0
3  CO2     0.036  44.009546  22.0  22.019660  22.0
""".strip('\n')
    assert m.data_composite(quantity=False).to_text() == """
  expr        x           X
0   N2   78.084   75.517607
1   O2   20.946   23.139564
2   Ar    0.934    1.288131
3  CO2    0.036    0.054698
4  avg   25.000   25.000000
5  sum  100.000  100.000000
""".strip('\n')

def test_matter():
    material = Material('0.2 <H2O> 0.3 <NaCl>')
    assert material.data_components(quantity=False).to_text() == """
   expr  fraction       mass     Z         N     e
0   H2O       0.2  18.015286  10.0   8.00471  10.0
1  NaCl       0.3  58.442707  28.0  30.48480  28.0
""".strip('\n')
    assert material.data_composite(quantity=False).to_text() == """
   expr      x           X
0   H2O   40.0   17.047121
1  NaCl   60.0   82.952879
2   avg   50.0   50.000000
3   sum  100.0  100.000000
""".strip('\n')
    material = Material('0.2 <H2O> 0.3 <NaCl>', mass_density=Quantity(0.3,'g/cm3'))
    assert material.data_matter(quantity=False).to_text() == """
   expr             n       rho
0   H2O  1.709551e+21  0.051141
1  NaCl  2.564326e+21  0.248859
2   avg  2.136939e+21  0.150000
3   sum  4.273877e+21  0.300000
""".strip('\n')
    material = Material('0.2 <H2O> 0.3 <NaCl>', mass_density=Quantity(0.3,'g/cm3'), volume=Quantity(1,'l'))
    assert material.data_matter(quantity=False).to_text() == """
   expr             n       rho             N           M
0   H2O  1.709551e+21  0.051141  1.709551e+24   51.141364
1  NaCl  2.564326e+21  0.248859  2.564326e+24  248.858636
2   avg  2.136939e+21  0.150000  2.136939e+24  150.000000
3   sum  4.273877e+21  0.300000  4.273877e+24  300.000000
""".strip('\n')

def test_print():
    material = Material('0.2 <H2O> 0.3 <NaCl>', mass_density=Quantity(0.3,'g/cm3'), volume=Quantity(1,'l'))
    with Capturing() as output:
        material.print()
    assert output == [
        'Components:', 
        '', 
        'expr  fraction  mass[Da]    Z        N    e', 
        ' H2O       0.2 18.015286 10.0  8.00471 10.0', 
        'NaCl       0.3 58.442707 28.0 30.48480 28.0', 
        '', 
        'Composite:', 
        '', 
        'expr  x[%]       X[%]', 
        ' H2O  40.0  17.047121', 
        'NaCl  60.0  82.952879', 
        ' avg  50.0  50.000000', 
        ' sum 100.0 100.000000', 
        '',
        'Matter:', 
        '', 
        'Mass density:   Quantity(3.000e-01 g*cm-3)', 
        'Number density: Quantity(8.548e+21 cm-3)', 
        'Volume:         Quantity(1.000e+00 l)', 
        'Mass:           Quantity(3.000e+02 g)', 
        '', 
        'expr      n[cm-3]  rho[g/cm3]            N       M[g]', 
        ' H2O 1.709551e+21    0.051141 1.709551e+24  51.141364', 
        'NaCl 2.564326e+21    0.248859 2.564326e+24 248.858636', 
        ' avg 2.136939e+21    0.150000 2.136939e+24 150.000000', 
        ' sum 4.273877e+21    0.300000 4.273877e+24 300.000000'
    ]