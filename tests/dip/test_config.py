import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.config import *

@pytest.fixture
def file_pdf():
    dir_tmp = "tmp" #docs/source/_static/pdf"
    if not os.path.isdir(dir_tmp):
        os.mkdir(dir_tmp)
    file_pdf  = f"{dir_tmp}/export_config.txt"
    if os.path.isfile(file_pdf):
        os.remove(file_pdf)
    return file_pdf

@pytest.fixture
def basic_types():
    return """
    simulation
      name str = 'Configuration test'
      output bool = true
    box
      height float = 15 cm
    num_cells int = 100
      !tags ["selection"]
    """

@pytest.fixture
def derived_types():
    return """
    box
      width float32 = 12 cm
        !tags ["selection"]
    density float128 = 23 g/cm3    
    num_groups uint64 = 2399495729
    """

@pytest.fixture
def arrays():
    return """
    primes int[3] = [3,5,7]
    sizes float[3] = [23.4,46,96.4] cm
    """
    
@pytest.fixture
def none_value():
    return """
    particles
      stars int = none
      tracers int = 23
    """
    
def test_parser_dip(basic_types, derived_types):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        env = dip.parse()
    with ExportConfig(env) as exp:
        assert exp.parse() == """
simulation.name str = "Configuration test"
simulation.output bool = true
box.height float = 15.0 cm
num_cells int = 100
box.width float32 = 12.0 cm
density float128 = 23.0 g/cm3
num_groups uint64 = 2399495729
        """.strip()
        
def test_parser_c(basic_types, derived_types, none_value):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        dip.add_string(none_value)
        env = dip.parse()
    with ExportConfigC(env) as exp:
        assert exp.parse() == """
#ifndef CONFIG_H
#define CONFIG_H

#include <stdbool.h>

const char* SIMULATION_NAME = "Configuration test";
const bool SIMULATION_OUTPUT = true;
const double BOX_HEIGHT = 15.0;
const int NUM_CELLS = 100;
const float BOX_WIDTH = 12.0;
const long double DENSITY = 23.0;
const unsigned long long int NUM_GROUPS = 2399495729;
const int PARTICLES_STARS = None;
const int PARTICLES_TRACERS = 23;

#endif /* CONFIG_H */
        """.strip()

def test_parser_cpp(basic_types, derived_types):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        env = dip.parse()
    with ExportConfigCPP(env) as exp:        
        assert exp.parse() == """
#ifndef CONFIG_H
#define CONFIG_H

constexpr char* SIMULATION_NAME = "Configuration test";
constexpr bool SIMULATION_OUTPUT = true;
constexpr double BOX_HEIGHT = 15.0;
constexpr int NUM_CELLS = 100;
constexpr float BOX_WIDTH = 12.0;
constexpr long double DENSITY = 23.0;
constexpr unsigned long long int NUM_GROUPS = 2399495729;

#endif /* CONFIG_H */
        """.strip()
        
def test_parser_rust(basic_types, derived_types):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        env = dip.parse()
    with ExportConfigRust(env) as exp:
        assert exp.parse() == """
pub const SIMULATION_NAME: &str = "Configuration test";
pub const SIMULATION_OUTPUT: bool = true;
pub const BOX_HEIGHT: f64 = 15.0;
pub const NUM_CELLS: i32 = 100;
pub const BOX_WIDTH: f32 = 12.0;
pub const DENSITY: f64 = 23.0;
pub const NUM_GROUPS: u64 = 2399495729;
        """.strip()
        
def test_parser_fortran(basic_types, derived_types):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        env = dip.parse()
    with ExportConfigFortran(env) as exp:
        assert exp.parse() == """
module ConfigurationModule
  implicit none

  character(len=20), parameter :: SIMULATION_NAME = "Configuration test";
  logical, parameter :: SIMULATION_OUTPUT = .true.;
  real(kind=8), parameter :: BOX_HEIGHT = 15.0;
  integer, parameter :: NUM_CELLS = 100;
  real, parameter :: BOX_WIDTH = 12.0;
  real(kind=16), parameter :: DENSITY = 23.0;
  integer(kind=8), parameter :: NUM_GROUPS = 2399495729;

end module ConfigurationModule
        """.strip()
        
def test_parser_yaml(basic_types, derived_types, arrays):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        dip.add_string(arrays)
        env = dip.parse()
    with ExportConfigYAML(env) as exp:
        assert exp.parse() == """
box.height:
  unit: cm
  value: 15.0
box.width:
  unit: cm
  value: 12.0
density:
  unit: g/cm3
  value: 23.0
num_cells: 100
num_groups: 2399495729
primes:
- 3
- 5
- 7
simulation.name: Configuration test
simulation.output: true
sizes:
  unit: cm
  value:
  - 23.4
  - 46.0
  - 96.4
        """.strip()
        exp.select("box.width")
        assert exp.parse(units=False) == """
width: 12.0
        """.strip()
        
def test_parser_toml(basic_types, derived_types, arrays):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        dip.add_string(arrays)
        env = dip.parse()
    with ExportConfigTOML(env) as exp:
        assert exp.parse() == """
"simulation.name" = "Configuration test"
"simulation.output" = true
num_cells = 100
num_groups = 2399495729
primes = [ 3, 5, 7,]

["box.height"]
value = 15.0
unit = "cm"

["box.width"]
value = 12.0
unit = "cm"

[density]
value = 23.0
unit = "g/cm3"

[sizes]
value = [ 23.4, 46.0, 96.4,]
unit = "cm"
        """.strip()
        exp.select("box.width")
        assert exp.parse(units=False) == """
width = 12.0
        """.strip()
        
def test_parser_json(basic_types, derived_types, arrays):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        dip.add_string(arrays)
        env = dip.parse()
    with ExportConfigJSON(env) as exp:
        assert exp.parse(indent=2) == """
{
  "simulation.name": "Configuration test",
  "simulation.output": true,
  "box.height": {
    "value": 15.0,
    "unit": "cm"
  },
  "num_cells": 100,
  "box.width": {
    "value": 12.0,
    "unit": "cm"
  },
  "density": {
    "value": 23.0,
    "unit": "g/cm3"
  },
  "num_groups": 2399495729,
  "primes": [
    3,
    5,
    7
  ],
  "sizes": {
    "value": [
      23.4,
      46.0,
      96.4
    ],
    "unit": "cm"
  }
}
        """.strip()
        exp.select("box.width")
        assert exp.parse(units=False) == """
{"width": 12.0}
        """.strip()
        
def test_parser_bash(basic_types, derived_types, arrays):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        dip.add_string(arrays)
        env = dip.parse()
    with ExportConfigBash(env) as exp:
        assert exp.parse() == """
export SIMULATION_NAME="Configuration test"
export SIMULATION_OUTPUT=0
export BOX_HEIGHT=15.0
export NUM_CELLS=100
export BOX_WIDTH=12.0
export DENSITY=23.0
export NUM_GROUPS=2399495729
export PRIMES=("3" "5" "7")
export SIZES=("23.4" "46.0" "96.4")
        """.strip()
        
def test_selection(basic_types):

    # select nodes using a query
    with DIP() as dip:
        dip.add_string(basic_types)
        env = dip.parse()
    with ExportConfigC(env) as exp:
        exp.select(query="box.*")        
        assert exp.parse() == """
#ifndef CONFIG_H
#define CONFIG_H

const double HEIGHT = 15.0;

#endif /* CONFIG_H */
        """.strip()

    # select nodes by tags
    with DIP() as dip:
        dip.add_string(basic_types)
        env = dip.parse()
    with ExportConfigC(env) as exp:
        exp.select(tags=["selection"])        
        assert exp.parse() == """
#ifndef CONFIG_H
#define CONFIG_H

const int NUM_CELLS = 100;

#endif /* CONFIG_H */
        """.strip()

def test_saving(file_pdf, basic_types, derived_types):

    with DIP() as dip:
        dip.add_string(basic_types)
        dip.add_string(derived_types)
        env = dip.parse()
    with ExportConfigC(env) as exp:
        exp.parse() 
        exp.save(file_pdf)
        
        with open(file_pdf,'r') as f:
            assert f.read() == """
#ifndef CONFIG_H
#define CONFIG_H

#include <stdbool.h>

const char* SIMULATION_NAME = "Configuration test";
const bool SIMULATION_OUTPUT = true;
const double BOX_HEIGHT = 15.0;
const int NUM_CELLS = 100;
const float BOX_WIDTH = 12.0;
const long double DENSITY = 23.0;
const unsigned long long int NUM_GROUPS = 2399495729;

#endif /* CONFIG_H */
            """.strip()
            
def test_renaming(basic_types):
    
    with DIP() as dip:
        dip.add_string(basic_types)
        env = dip.parse()
    with ExportConfigC(env, rename=False) as exp:
        assert exp.parse() == """
#ifndef CONFIG_H
#define CONFIG_H

#include <stdbool.h>

const char* simulation.name = "Configuration test";
const bool simulation.output = true;
const double box.height = 15.0;
const int num_cells = 100;

#endif /* CONFIG_H */
        """.strip()