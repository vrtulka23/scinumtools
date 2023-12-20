import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.datatypes import FloatType

def test_node_list():
    with DIP() as p:
        p.add_file("examples/definitions.dip")
        env = p.parse()
        
    assert env.nodes.keys()                       == ['box', 'modules', 'runtime', 'simulation']
    assert env.nodes['runtime'].keys()            == ['t_max', 'timestep']
    assert env.nodes['runtime']['timestep'].value == FloatType(1.0000000000000001e-11, 's')
    assert env.nodes['runtime.t_max'].value       == FloatType(1e-08, 's')