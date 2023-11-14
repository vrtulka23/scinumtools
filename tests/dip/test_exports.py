import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.exports.config import ExportConfig

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
def code_string():
    return """
    simulation
      name str = 'Configuration test'
      output bool = true
    box
      width float32 = 12 cm
        !tags ["selection"]
      height float = 15 cm
    density float128 = 23 g/cm3
    num_cells int = 100
      !tags ["selection"]
    num_groups uint64 = 2399495729
    """

def test_config_languages(code_string):

    with DIP() as dip:
        dip.from_string(code_string)
        env = dip.parse()
    with ExportConfig(env) as exp:
        
        assert exp.build_c() == """
#ifndef CONFIG_H
#define CONFIG_H

#define SIMULATION_NAME "Configuration test"
#define SIMULATION_OUTPUT 1
#define BOX_WIDTH 12.0
#define BOX_HEIGHT 15.0
#define DENSITY 23.0
#define NUM_CELLS 100
#define NUM_GROUPS 2399495729

#endif /* CONFIG_H */
        """.strip()
        
        assert exp.build_cpp() == """
#ifndef CONFIG_H
#define CONFIG_H

constexpr const char* SIMULATION_NAME = "Configuration test";
constexpr bool SIMULATION_OUTPUT = true;
constexpr float BOX_WIDTH = 12.0;
constexpr double BOX_HEIGHT = 15.0;
constexpr long double DENSITY = 23.0;
constexpr int NUM_CELLS = 100;
constexpr unsigned long long int NUM_GROUPS = 2399495729;

#endif /* CONFIG_H */
        """.strip()
        
        assert exp.build_rust() == """
pub const SIMULATION_NAME: &str = "Configuration test";
pub const SIMULATION_OUTPUT: bool = true;
pub const BOX_WIDTH: f32 = 12.0;
pub const BOX_HEIGHT: f64 = 15.0;
pub const DENSITY: f128 = 23.0;
pub const NUM_CELLS: i32 = 100;
pub const NUM_GROUPS: u64 = 2399495729;
        """.strip()
        
        assert exp.build_fortran() == """
module ConfigurationModule
  implicit none

  character(len=20), parameter :: SIMULATION_NAME = "Configuration test";
  logical, parameter :: SIMULATION_OUTPUT = .true.;
  real, parameter :: BOX_WIDTH = 12.0;
  real(kind=8), parameter :: BOX_HEIGHT = 15.0;
  real(kind=8), parameter :: DENSITY = 23.0;
  integer, parameter :: NUM_CELLS = 100;
  integer(kind=8), parameter :: NUM_GROUPS = 2399495729;

end module ConfigurationModule
        """.strip()
        
def test_config_selection(code_string):

    # select nodes using a query
    with DIP() as dip:
        dip.from_string(code_string)
        env = dip.parse()
    with ExportConfig(env) as exp:
        exp.select(query="box.*")        
        assert exp.build_c() == """
#ifndef CONFIG_H
#define CONFIG_H

#define WIDTH 12.0
#define HEIGHT 15.0

#endif /* CONFIG_H */
        """.strip()

    # select nodes by tags
    with DIP() as dip:
        dip.from_string(code_string)
        env = dip.parse()
    with ExportConfig(env) as exp:
        exp.select(tags=["selection"])        
        assert exp.build_c() == """
#ifndef CONFIG_H
#define CONFIG_H

#define BOX_WIDTH 12.0
#define NUM_CELLS 100

#endif /* CONFIG_H */
        """.strip()

def test_config_save(file_pdf, code_string):

    with DIP() as dip:
        dip.from_string(code_string)
        env = dip.parse()
    with ExportConfig(env) as exp:
        exp.build_c() 
        exp.save(file_pdf)
        
        with open(file_pdf,'r') as f:
            assert f.read() == """
#ifndef CONFIG_H
#define CONFIG_H

#define SIMULATION_NAME "Configuration test"
#define SIMULATION_OUTPUT 1
#define BOX_WIDTH 12.0
#define BOX_HEIGHT 15.0
#define DENSITY 23.0
#define NUM_CELLS 100
#define NUM_GROUPS 2399495729

#endif /* CONFIG_H */
            """.strip()