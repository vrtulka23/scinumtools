import numpy as np
import os
import sys
sys.path.insert(0, os.environ['DIR_SOURCE'])

from scinumtools import RowCollector, ParameterTable
from scinumtools.units import Dimensions
from scinumtools.units.settings import *
from scinumtools.units.unit_types import *
from scinumtools.dip import DIP
from scinumtools.materials.periodic_table import *

path_docs_static = os.environ['DIR_DOCS']+'/source/_static/tables'

def build_prefixes():
    
    # Create table of unit prefixes
    rc = RowCollector(['Symbol','Name','Magnitude'])
    for symbol, prefix in UNIT_PREFIXES.items():
        exponent = int(np.log10(prefix.magnitude))
        rc.append([symbol, prefix.name, ":math:`10^{"+f"{exponent:d}"+"}`"])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/prefixes.csv"
    df.to_csv(file_path, index=False)
    print(file_path)

def build_base_units():

    # create table of base units
    rc = RowCollector(['Symbol','Name','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if unit.definition is not None:
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        rc.append([symbol, unit.name, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_base.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_standard_units():    

    # create table of standard units
    rc = RowCollector(['Symbol','Name','Definition','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if not isinstance(unit.definition, str):
            continue
        if symbol in ['K','degR','AR','PR']:
            continue
        if symbol.startswith('['):
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        if len(rc) and unit.name in rc.Name:
            idx = rc.Name.index(unit.name)
            rc.Symbol[idx] += ", "+symbol
            rc.Prefixes[idx] += ", "+prefixes if rc.Prefixes[idx] else ""
        else:
            rc.append([symbol, unit.name, unit.definition, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_standard.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_constants():
    
    # create table of constants
    rc = RowCollector(['Symbol','Name','Definition'])
    for symbol, unit in UNIT_STANDARD.items():
        if not symbol.startswith('['):
            continue
        if len(rc) and unit.name in rc.Name:
            idx = rc.Name.index(unit.name)
            rc.Symbol[idx] += ", "+symbol
        else:
            rc.append([symbol, unit.name, unit.definition])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/constants.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_logarithmic_units():
    
    # create table of logarithmic units
    rc = RowCollector(['Symbol','Name','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if symbol not in ['AR','PR'] and unit.definition != LogarithmicUnitType:
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        if len(rc) and unit.name in rc.Name:
            idx = rc.Name.index(unit.name)
            rc.Symbol[idx] += ", "+symbol
            rc.Prefixes[idx] += ", "+prefixes if rc.Prefixes[idx] else ""
        else:
            rc.append([symbol, unit.name, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_logarithmic.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_temperature_units():
    
    # create table of temperature units
    rc = RowCollector(['Symbol','Name','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if symbol not in ['K','degR'] and unit.definition != TemperatureUnitType:
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        rc.append([symbol, unit.name, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_temperature.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_si_quantities():

    # create table of physical quantities SI
    rc = RowCollector(['Symbol','Name','Definition','Dimensions'])
    for q in range(len(QUANTITY_LIST)):
        name = QUANTITY_LIST.name[q]
        symbol = QUANTITY_LIST.symbol[q]
        definition = QUANTITY_LIST.SI[q]
        magnitude, dimensions = QUANTITY_UNITS[f"#S{symbol}"]
        rc.append([f"#S{symbol}", f"SI.{name}", definition, dimensions])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/quantities_si.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_cgs_quantities():
    
    # create table of physical quantities CGS
    rc = RowCollector(['Symbol','Name','Definition'])
    for q in range(len(QUANTITY_LIST)):
        symbol = QUANTITY_LIST.symbol[q]
        if f"#C{symbol}" not in QUANTITY_UNITS:
            continue
        name = QUANTITY_LIST.name[q]
        definition = QUANTITY_LIST.CGS[q]
        rc.append([f"#C{symbol}", f"CGS.{name}", definition])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/quantities_cgs.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_au_quantities():
    
    # create table of physical quantities AU
    rc = RowCollector(['Symbol','Name','Definition'])
    for q in range(len(QUANTITY_LIST)):
        symbol = QUANTITY_LIST.symbol[q]
        if f"#A{symbol}" not in QUANTITY_UNITS:
            continue
        name = QUANTITY_LIST.name[q]
        definition = QUANTITY_LIST.AU[q]
        rc.append([f"#A{symbol}", f"AU.{name}", definition])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/quantities_au.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_constants():
    
    pt = ParameterTable(PT_HEADER, PT_DATA, keys=True)
    # create table of constants
    rc = RowCollector(['Symbol','Z','A','Relative atomic mass (Da)', 'Natural abundance'])
    for symbol, e in pt.items():
        first = True
        for A, (M, NA) in e.A.items():
            if first:
                rc.append([f"``{symbol}``", e.Z, A, M, NA])
                first = False
            else:
                rc.append(['', '', A, M, NA])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/elements.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    