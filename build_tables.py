import numpy as np
import os
import sys
sys.path.insert(0, 'src')

from scinumtools import RowCollector
from scinumtools.units.settings import *
from scinumtools.units.unit_types import *

path_docs_static = 'docs/source/_static/tables'

# Create table of unit prefixes
rc = RowCollector(['Symbol','Name','Magnitude'])
for symbol, prefix in UNIT_PREFIXES.items():
    exponent = int(np.log10(prefix.magnitude))
    rc.append([symbol, prefix.name, ":math:`10^{"+f"{exponent:d}"+"}`"])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/prefixes.csv", index=False)

# create table of base units
rc = RowCollector(['Symbol','Name','Dimensions','Prefixes'])
for symbol, unit in UNIT_STANDARD.items():
    if unit.definition is not None:
        continue
    if unit.prefixes is True:
        prefixes = 'all'
    elif isinstance(unit.prefixes, list):
        prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
    else:
        prefixes = ''
    rc.append([symbol, unit.name, unit.dimensions, prefixes])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/unit_base.csv", index=False)

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
    rc.append([symbol, unit.name, unit.definition, prefixes])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/unit_standard.csv", index=False)

# create table of constants
rc = RowCollector(['Symbol','Name','Definition'])
for symbol, unit in UNIT_STANDARD.items():
    if not symbol.startswith('['):
        continue
    rc.append([symbol, unit.name, unit.definition])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/constants.csv", index=False)

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
    rc.append([symbol, unit.name, prefixes])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/unit_logarithmic.csv", index=False)

# create table of logarithmic units
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
df.to_csv(f"{path_docs_static}/unit_temperature.csv", index=False)
