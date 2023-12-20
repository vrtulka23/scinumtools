import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.solvers import TemplateSolver

def test_formatting():
    with DIP() as dip:
        dip.add_string("""
id int = 345
name str = 'Tina'
body
  weight float = 62.3 kg
  height float = 177 cm
married bool = true
        """)
        env = dip.parse()
    with TemplateSolver(env) as p:
        assert p.solve("""
ID:      {{?id}:05d}
Name:    {{?name}}
Weight:  {{?body.weight}:.3e}
Height:  {{?body.height}:.2f}
Married: {{?married}}
        """) == """
ID:      00345
Name:    Tina
Weight:  6.230e+01
Height:  177.00
Married: True
        """

def test_arrays():
    with DIP() as dip:
        dip.add_string("""
name str = "Will Smith"
widths float[2,3] = [[23.4,235.4,34],[1e10,2e23,5e20]]
        """)
        env = dip.parse()
    with TemplateSolver(env) as p:
        assert p.solve("""
Surname:  {{?name}[5:]}
Scalar:   {{?widths}[1,1]:.2e}
Array:
{{?widths}[:,1:]}
        """) == """
Surname:  Smith
Scalar:   2.00e+23
Array:
[[2.354e+02 3.400e+01]
 [2.000e+23 5.000e+20]]
        """

def test_strings():
    with DIP() as dip:
        dip.add_string("""
name str = "William Smith"
        """)
        env = dip.parse()
    with TemplateSolver(env) as p:
        assert p.solve("""
Surname: {{?name}[8:]}
        """) == """
Surname: Smith
        """
        
if __name__ == "__main__":
    # Specify wich test to run
    test = sys.argv[1] if len(sys.argv)>1 else True

    # Loop through all tests
    for fn in dir(sys.modules[__name__]):
        if fn[:5]=='test_' and (test is True or test==fn[5:]):
            print(f"\nTesting: {fn}\n")
            locals()[fn]()
