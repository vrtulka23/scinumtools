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
    mixture = Mixture()
    assert mixture.data_molecules() == None
    
def test_set_dictionary():
    mixture = Mixture({
        'H2O': 1.0
    })
    assert mixture.data_molecules(quantity=False).to_text() == """
  expression  count          M
0        H2O    1.0  18.015286
1        avg    1.0  18.015286
2        sum    1.0  18.015286
""".strip('\n')

    mixture = Mixture({
        'H2O':  0.2,
        'NaCl': 0.8,
    })
    assert mixture.data_molecules(quantity=False).to_text() == """
  expression  count          M
0        H2O    0.2  18.015286
1       NaCl    0.8  58.442707
2        avg    0.5  38.228997
3        sum    1.0  76.457993
""".strip('\n')

def test_expression():
    mixture = Mixture('0.2 <H2O> 0.8 <NaCl>')
    assert mixture.data_molecules(quantity=False).to_text() == """
  expression  count          M
0        H2O    0.2  18.015286
1       NaCl    0.8  58.442707
2        avg    0.5  38.228997
3        sum    1.0  76.457993
""".strip('\n')

def test_print_data():
    mixture = Mixture('0.2 <H2O> 0.8 <NaCl>')
    with Capturing() as output:
        mixture.print_molecules()
    assert output == [
        'expression  count     M[Da]', 
        '       H2O    0.2 18.015286', 
        '      NaCl    0.8 58.442707', 
        '       avg    0.5 38.228997', 
        '       sum    1.0 76.457993',
    ]
    with Capturing() as output:
        mixture.print_mixture()
    assert output == [
        'expression   x       X', 
        '       H2O 0.2 0.07155', 
        '      NaCl 0.8 0.92845', 
        '       avg 0.5 0.50000', 
        '       sum 1.0 1.00000'
    ]

def test_norm_number():
    mixture = Mixture('2 <H2O> 3 <NaCl>')
    assert mixture.data_mixture(quantity=False).to_text() == """
  expression    x         X
0        H2O  0.4  0.170471
1       NaCl  0.6  0.829529
2        avg  0.5  0.500000
3        sum  1.0  1.000000
""".strip('\n')

def test_norm_number_fraction():
    mixture = Mixture('0.2 <H2O> 0.3 <NaCl>')
    assert mixture.data_mixture(quantity=False).to_text() == """
  expression    x         X
0        H2O  0.4  0.170471
1       NaCl  0.6  0.829529
2        avg  0.5  0.500000
3        sum  1.0  1.000000
""".strip('\n')
    
def test_norm_mass_fraction():
    # setting mass fraction
    mixture = Mixture('0.2 <H2O> 0.3 <NaCl>', fractype=FracType.MASS)
    assert mixture.data_mixture(quantity=False).to_text() == """
  expression         x    X
0        H2O  0.683815  0.4
1       NaCl  0.316185  0.6
2        avg  0.500000  0.5
3        sum  1.000000  1.0
""".strip('\n')
    
    # checking if number fractions given above produce the same mass fractions
    mixture = Mixture('0.683815 <H2O> 0.316185 <NaCl>', fractype=FracType.NUMBER)
    assert mixture.data_mixture(quantity=False).to_text() == """
  expression         x    X
0        H2O  0.683815  0.4
1       NaCl  0.316185  0.6
2        avg  0.500000  0.5
3        sum  1.000000  1.0
""".strip('\n')

def test_natural_abundances():
    # natural abundances
    mixture = Mixture({
        'H2O': 1.0
    }, natural=True)
    assert isclose(
        mixture.data_molecules(quantity=False)['H2O'].M, 
        18.015286, 
        rel_tol=MAGNITUDE_PRECISION
    )
    
    # highest abundances
    mixture = Mixture({
        'H2O': 1.0
    }, natural=False)
    assert isclose(
        mixture.data_molecules(quantity=False)['H2O'].M, 
        18.010565, 
        rel_tol=MAGNITUDE_PRECISION
    )
