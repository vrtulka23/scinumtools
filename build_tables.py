import numpy as np
import os
import sys
sys.path.insert(0, 'src')

from scinumtools import RowCollector
from scinumtools.units import Dimensions
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
    if len(rc) and unit.name in rc.Name:
        idx = rc.Name.index(unit.name)
        rc.Symbol[idx] += ", "+symbol
        rc.Prefixes[idx] += ", "+prefixes if rc.Prefixes[idx] else ""
    else:
        rc.append([symbol, unit.name, unit.definition, prefixes])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/unit_standard.csv", index=False)

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
    if len(rc) and unit.name in rc.Name:
        idx = rc.Name.index(unit.name)
        rc.Symbol[idx] += ", "+symbol
        rc.Prefixes[idx] += ", "+prefixes if rc.Prefixes[idx] else ""
    else:
        rc.append([symbol, unit.name, prefixes])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/unit_logarithmic.csv", index=False)

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
df.to_csv(f"{path_docs_static}/unit_temperature.csv", index=False)

# create table of physical quantities SI
rc = RowCollector(['Symbol','Name','Definition','Dimensions'])
for q in range(len(QUANTITY_LIST)):
    name = QUANTITY_LIST.name[q]
    symbol = QUANTITY_LIST.symbol[q]
    definition = QUANTITY_LIST.SI[q]
    magnitude, dimensions = QUANTITY_UNITS[f"#S{symbol}"]
    rc.append([f"#S{symbol}", f"SI.{name}", definition, dimensions])
df = rc.to_dataframe()
df.to_csv(f"{path_docs_static}/quantities_si.csv", index=False)

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
df.to_csv(f"{path_docs_static}/quantities_cgs.csv", index=False)

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
df.to_csv(f"{path_docs_static}/quantities_au.csv", index=False)

