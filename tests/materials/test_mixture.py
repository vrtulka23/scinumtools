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
    
def test_from_molecules():
    mixture = Mixture.from_dict({
        'H2O':  0.2,
        'NaCl': 0.8,
    })
    assert mixture.data_molecules(quantity=False).to_text() == """
  expression    X          M
0        H2O  0.2  18.015286
1       NaCl  0.8  58.442707
2        avg  0.5  38.228997
3        sum  1.0  76.457993
""".strip('\n')
    
def test_add_molecules():
    mixture = Mixture()
    mixture.add_molecule(Molecule('H2O'))
    assert mixture.data_molecules(quantity=False).to_text() == """
  expression    X          M
0        H2O  1.0  18.015286
1        avg  1.0  18.015286
2        sum  1.0  18.015286
""".strip('\n')

    mixture = Mixture()
    mixture.add_molecule(Molecule('H2O'), 0.2)
    mixture.add_molecule(Molecule('NaCl'), 0.8)
    assert mixture.data_molecules(quantity=False).to_text() == """
  expression    X          M
0        H2O  0.2  18.015286
1       NaCl  0.8  58.442707
2        avg  0.5  38.228997
3        sum  1.0  76.457993
""".strip('\n')

def test_expression():
    mixture = Mixture('0.2 <H2O> 0.8 <NaCl>')
    assert mixture.data_molecules(quantity=False).to_text() == """
  expression    X          M
0        H2O  0.2  18.015286
1       NaCl  0.8  58.442707
2        avg  0.5  38.228997
3        sum  1.0  76.457993
""".strip('\n')

def test_print_data():
    mixture = Mixture('0.2 <H2O> 0.8 <NaCl>')
    with Capturing() as output:
        mixture.print_molecules()
    assert output == [
        'expression   X     M[Da]', 
        '       H2O 0.2 18.015286', 
        '      NaCl 0.8 58.442707', 
        '       avg 0.5 38.228997', 
        '       sum 1.0 76.457993'
    ]