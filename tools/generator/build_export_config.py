import numpy as np
import os
import sys
sys.path.insert(0, os.environ['DIR_SOURCE'])

from scinumtools import RowCollector
from scinumtools.units import Dimensions
from scinumtools.units.settings import *
from scinumtools.units.unit_types import *
from scinumtools.dip import DIP
from scinumtools.dip.config import *

dir_export = os.environ['DIR_DOCS']+"/source/_static/export_config"
file_code = f"{dir_export}/config.dip"

def build_config_c():
    
    file_export = f"{dir_export}/config_c.h"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigC(env) as exp:
        exp.parse(
            guard='CONFIG_H',
            define=['radiation','simulation.name']
        )
        exp.save(file_export)
        
def build_config_cpp():
    
    file_export = f"{dir_export}/config_cpp.h"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigCPP(env) as exp:
        exp.parse(
            guard='CONFIG_H',
            define=['radiation','simulation.name'],
            const=['box.width','box.height']
        )
        exp.save(file_export)
        
def build_config_rust():
    
    file_export = f"{dir_export}/config_rust.rs"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigRust(env) as exp:
        exp.parse()
        exp.save(file_export)

def build_config_fortran():
    
    file_export = f"{dir_export}/config_fortran.f90"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigFortran(env) as exp:
        exp.parse()
        exp.save(file_export)
        
def build_config_bash():
    
    file_export = f"{dir_export}/config_bash.sh"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigBash(env) as exp:
        exp.parse()
        exp.save(file_export)
        
def build_config_yaml():
    
    file_export = f"{dir_export}/config_yaml.yaml"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigYAML(env) as exp:
        exp.parse(units=True, default_flow_style=False)
        exp.save(file_export)
        
def build_config_toml():
    
    file_export = f"{dir_export}/config_toml.toml"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigTOML(env) as exp:
        exp.parse()
        exp.save(file_export)

def build_config_json():
    
    file_export = f"{dir_export}/config_json.json"
    print(file_export)
    
    with DIP() as dip:
       dip.add_file(file_code)
       env = dip.parse()
    with ExportConfigJSON(env) as exp:
        exp.parse(indent=2)
        exp.save(file_export)