import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP, Environment
from scinumtools.dip.settings import Format
from scinumtools.dip.datatypes import IntegerType, FloatType, StringType, BooleanType
from scinumtools.dip.solvers import TemplateSolver

@pytest.fixture
def test_path():
    return "examples/"

def test_example_of_use(test_path):

    with DIP() as dip:
        dip.from_string("""
        mpi
          nodes int = 36
          cores int = 96
        """)                               # get code from a string
        env1 = dip.parse()                 # parse the code

    with DIP(env1) as dip:                 # pass environment to a new DIP instance
        dip.from_file(test_path+"settings2.dip") # add new parameter
        env2 = dip.parse()                 # parse new parameters

    nodes = env2.query("mpi.*")            # select nodes using a query
    geom = env2.request("?box.geometry")   # select a node using a request
    
    assert nodes[0].value == IntegerType(36)
    assert nodes[1].value == IntegerType(96)
    assert geom[0].value == IntegerType(3)

    data = env2.data(verbose=True)
    np.testing.assert_equal(data,{
        'mpi.nodes': 36,
        'mpi.cores': 96,
        'runtime.t_max': 10,
        'runtime.timestep': 0.01,
        'box.geometry': 3,
        'box.size.x': 10,
        'box.size.y': 3e7,
        'modules.heating': False,
        'modules.radiation': True,
    })

    data = env2.data(verbose=True, format=Format.TUPLE)
    np.testing.assert_equal(data,{
        'mpi.nodes': 36,
        'mpi.cores': 96,
        'runtime.t_max': (10, 'ns'),
        'runtime.timestep': (0.01, 'ns'),
        'box.geometry': 3,
        'box.size.x': (10, 'nm'),
        'box.size.y': (3e7,'nm'),
        'modules.heating': False,
        'modules.radiation': True,
    })
    
    data = env2.data(verbose=True, format=Format.TYPE)
    np.testing.assert_equal(data,{
        'mpi.nodes':         IntegerType(36),
        'mpi.cores':         IntegerType(96),
        'runtime.t_max':     FloatType(10, 'ns'),
        'runtime.timestep':  FloatType(0.01, 'ns'),
        'box.geometry':      IntegerType(3),
        'box.size.x':        FloatType(10, 'nm'),
        'box.size.y':        FloatType(3e7, 'nm'),
        'modules.heating':   BooleanType(False),
        'modules.radiation': BooleanType(True),
    })
    
def test_definition_template(test_path):
    
    with DIP() as dip:
        dip.from_file(test_path+'definitions.dip')
        env3 = dip.parse()
        data = env3.data(format=Format.TYPE)
    np.testing.assert_equal(data,{
        'runtime.t_max':        FloatType(1e-08, 's'),
        'runtime.timestep':     FloatType(1.0000000000000001e-11, 's'),
        'box.geometry':         IntegerType(3),
        'box.size.x':           FloatType(1e-06, 'cm'),
        'box.size.y':           FloatType(3.0, 'cm'),
        'box.size.z':           FloatType(23.0, 'cm'),
        'modules.hydrdynamics': BooleanType(True),
        'modules.heating':      BooleanType(False),
        'modules.radiation':    BooleanType(True)
    })
    with TemplateSolver(env3) as ts:
        text = ts.template(test_path+'template.txt', test_path+'processed.txt')
    assert text == "Geometry: 3\nBox size: [1e-06, 3.0, 23.0]\n"

def test_units_sources(test_path):

    with DIP() as dip:
        dip.add_source("settings", test_path+'settings.dip')
        dip.add_unit("length", 1, "m")
        dip.from_string("""
        width float = 23 [length]
        x_size float = {settings?box.size.x}
        """)
        env = dip.parse()
        data = env.data(format=Format.TYPE)
    np.testing.assert_equal(data,{
        'width':  FloatType(23, '[length]'),
        'x_size': FloatType(10, 'nm'),
    })
        
def test_functions():

    def fn_volume(data):
        side = data['side'].convert('cm').value
        return side**3

    def fn_surface(data):
        side = data['side'].convert('cm').value
        return IntegerType(6*side**2, 'cm2')
    
    def is_prime(data):
        side = data['side'].convert('cm').value
        return side in [1,2,3,5,7,11]

    def print_value(data):
        return str(data['side'])
    
    with DIP() as dip:
        dip.add_function("fn_volume", fn_volume)
        dip.add_function("fn_surface", fn_surface)
        dip.add_function("is_prime", is_prime)
        dip.add_function("print_value", print_value)
        dip.from_string("""
        side float = 5 cm
        volume float = (fn_volume) cm3
        surface int = (fn_surface) mm2
        prime bool = (is_prime)
        value str = (print_value)
        """)
        env = dip.parse()
        data = env.data(format=Format.TYPE)
        np.testing.assert_equal(data,{
            'side':    FloatType(5, 'cm'),
            'volume':  FloatType(125, 'cm3'),
            'surface': IntegerType(15000, 'mm2'),
            'prime':   BooleanType(True),
            'value':   StringType("FloatType(5.0 cm)")
        })
