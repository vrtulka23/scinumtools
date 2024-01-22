import numpy as np
from enum import Enum, auto

from ..parameter_table import ParameterTable
from ..row_collector import RowCollector
from .unit_types import *
from .unit_list import *

MAGNITUDE_PRECISION = 1e-7

SYMBOL_UNITID      = ":"
SYMBOL_FRACTION    = ":"
SYMBOL_MULTIPLY    = "*"
SYMBOL_SYSTEM_UNIT = "#"

DIMENSION_LIST     = ['m','g','s','K','C','cd','mol','rad']

UNIT_TYPES = [
    TemperatureUnitType,
    LogarithmicUnitType,
    StandardUnitType,
]

UNIT_PREFIXES = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], {
'Y':        (1.0e24,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e24',                   'yotta'            ), 
'Z':        (1.0e21,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e21',                   'zetta'            ), 
'E':        (1.0e18,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e18',                   'exa'              ), 
'P':        (1.0e15,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e15',                   'peta'             ), 
'T':        (1.0e12,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e12',                   'tera'             ), 
'G':        (1.0e9,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e9',                    'giga'             ), 
'M':        (1.0e6,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e6',                    'mega'             ), 
'k':        (1.0e3,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e3',                    'kilo'             ), 
'h':        (1.0e2,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e2',                    'hecto'            ), 
'da':       (1.0e1,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e1',                    'deka'             ), 
'd':        (1.0e-1,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-1',                   'deci'             ), 
'c':        (1.0e-2,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-2',                   'centi'            ), 
'm':        (1.0e-3,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-3',                   'milli'            ), 
'u':        (1.0e-6,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-6',                   'micro'            ), 
'n':        (1.0e-9,         [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-9',                   'nano'             ), 
'p':        (1.0e-12,        [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-12',                  'pico'             ), 
'f':        (1.0e-15,        [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-15',                  'femto'            ), 
'a':        (1.0e-18,        [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-18',                  'atto'             ), 
'z':        (1.0e-21,        [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-21',                  'zepto'            ), 
'y':        (1.0e-24,        [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-24',                  'yocto'            ), 
}, keys=True)
    
UNIT_STANDARD = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], {
# base physical units
'm':        (1.0,            [ 1, 0, 0, 0, 0, 0, 0, 0],  None,                     'meter',             True               ),
'g':        (1.0,            [ 0, 1, 0, 0, 0, 0, 0, 0],  None,                     'gram',              True               ),
's':        (1.0,            [ 0, 0, 1, 0, 0, 0, 0, 0],  None,                     'second',            True               ),
'K':        (1.0,            [ 0, 0, 0, 1, 0, 0, 0, 0],  None,                     'Kelvin',            True               ),
'C':        (1.0,            [ 0, 0, 0, 0, 1, 0, 0, 0],  None,                     'Coulomb',           True               ),
'cd':       (1.0,            [ 0, 0, 0, 0, 0, 1, 0, 0],  None,                     'candela',           True               ),
# base numerical units
'mol':      (1.0,            [ 0, 0, 0, 0, 0, 0, 1, 0],  None,                     'mole',              True               ),
'rad':      (1.0,            [ 0, 0, 0, 0, 0, 0, 0, 1],  None,                     'radian',            ['m']              ),

# units of length
'au':       (1.49597870e11,  [ 1, 0, 0, 0, 0, 0, 0, 0],  '149597.870691*Mm',       'astr. unit',        False              ),
'AU':       (1.49597870e11,  [ 1, 0, 0, 0, 0, 0, 0, 0],  'au',                     'astr. unit',        False              ),
'ly':       (9.460730e15,    [ 1, 0, 0, 0, 0, 0, 0, 0],  '[c]*yr_j',               'light-year',        ['k','M','G']      ),
'pc':       (3.0857e16,      [ 1, 0, 0, 0, 0, 0, 0, 0],  '3.0857e16*m',            'parsec',            ['k','M','G','T']  ),
'Ao':       (1e-10,          [ 1, 0, 0, 0, 0, 0, 0, 0],  '1e-10*m',                'Angstrom',          ['m','k']          ),
'twip':     (1.76388887e-5,  [ 1, 0, 0, 0, 0, 0, 0, 0],  '17.6388888*um',          'US twip',           False              ),
'mil':      (2.53999999e-5,  [ 1, 0, 0, 0, 0, 0, 0, 0],  '25.4*um',                'US mil',            False              ),
'p':        (0.000352778,    [ 1, 0, 0, 0, 0, 0, 0, 0],  '352.778*um',             'US point',          False              ),
'pi':       (0.004233,       [ 1, 0, 0, 0, 0, 0, 0, 0],  '4.233*mm',               'US pica',           False              ),
'in':       (0.0254,         [ 1, 0, 0, 0, 0, 0, 0, 0],  '25.4*mm',                'US inch',           False              ),
'ft':       (0.3048,         [ 1, 0, 0, 0, 0, 0, 0, 0],  '0.3048*m',               'US foot',           False              ),
'yd':       (0.9144,         [ 1, 0, 0, 0, 0, 0, 0, 0],  '0.9144*m',               'US yard',           False              ),
'mi':       (1609.344,       [ 1, 0, 0, 0, 0, 0, 0, 0],  '1.609344*km',            'US mile',           False              ),
'le':       (4828.032,       [ 1, 0, 0, 0, 0, 0, 0, 0],  '4.828032*km',            'US league',         False              ),
# units of mass
'u':        (1.6605391e-24,  [ 0, 1, 0, 0, 0, 0, 0, 0],  'g/[N_0]',                'atomic mass unit',  False              ),
'amu':      (1.6605391e-24,  [ 0, 1, 0, 0, 0, 0, 0, 0],  'u',                      'atomic mass unit',  False              ),
'Da':       (1.6605391e-24,  [ 0, 1, 0, 0, 0, 0, 0, 0],  'u',                      'Dalton',            False              ),
't':        (1e6,            [ 0, 1, 0, 0, 0, 0, 0, 0],  '1e3*kg',                 'tonne',             ['k','m','G']      ),
'oz':       (28.349523125,   [ 0, 1, 0, 0, 0, 0, 0, 0],  '28.349523125*g',         'US ounce',          False              ),
'lb':       (453.59237,      [ 0, 1, 0, 0, 0, 0, 0, 0],  '453.59237*g',            'US pound',          False              ),
'ton':      (907184.74,      [ 0, 1, 0, 0, 0, 0, 0, 0],  '907.18474*kg',           'US ton',            False              ),
# units of time
'min':      (6.0e1,          [ 0, 0, 1, 0, 0, 0, 0, 0],  '60*s',                   'minute',            False              ),
'h':        (3.6e3,          [ 0, 0, 1, 0, 0, 0, 0, 0],  '60*min',                 'hour',              False              ),
'day':      (8.64e4,         [ 0, 0, 1, 0, 0, 0, 0, 0],  '24*h',                   'day',               False              ),
'yr_t':     (3.1556925e7,    [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.24219*day',          'tropical year',     ['k','m','G']      ),
'yr_j':     (3.1557600e7,    [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.25*day',             'Julian year',       ['k','m','G']      ),
'yr_g':     (3.155695e7,     [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.2425*day',           'Gregorian year',    ['k','m','G']      ),
'yr':       (3.155760e7,     [ 0, 0, 1, 0, 0, 0, 0, 0],  'yr_j',                   'year',              ['k','m','G']      ),
# units of temperature
'Cel':      (1,              [ 0, 0, 0, 1, 0, 0, 0, 0],  TemperatureUnitType,      'degree Celsius',    False              ),
'degR':     (5/9,            [ 0, 0, 0, 1, 0, 0, 0, 0],  '5/9*K',                  'degree Rankine',    False              ),
'degF':     (1,              [ 0, 0, 0, 1, 0, 0, 0, 0],  TemperatureUnitType,      'degree Fahrenheit', False              ),
# angular units
'deg':      (1.7453292e-2,   [ 0, 0, 0, 0, 0, 0, 0, 1],  '2*[pi]*rad/360',         'angle degree',      False              ),
"'":        (2.908882e-4,    [ 0, 0, 0, 0, 0, 0, 0, 1],  'deg/60',                 'angle minute',      False              ),
"''":       (4.848137e-6,    [ 0, 0, 0, 0, 0, 0, 0, 1],  "'/60",                   'angle second',      False              ),

# units of surface
'ar':       (1.0e2,          [ 2, 0, 0, 0, 0, 0, 0, 0],  '100*m2',                 'are',               ['c','d','da','h'] ),
'acre':     (4046.873,       [ 2, 0, 0, 0, 0, 0, 0, 0],  '4046.873*m2',            'US acre',           False              ),
# units of volume
'l':        (1e-3,           [ 3, 0, 0, 0, 0, 0, 0, 0],  'dm3',                    'liter',             True               ),
'L':        (1e-3,           [ 3, 0, 0, 0, 0, 0, 0, 0],  'l',                      'liter',             True               ),
'floz':     (2.95735295e-05, [ 3, 0, 0, 0, 0, 0, 0, 0],  '29.5735295625*mL',       'US fluid ounce',    False              ),
'pt':       (4.73176473e-04, [ 3, 0, 0, 0, 0, 0, 0, 0],  '473.176473*mL',          'US pint',           False              ),
'gal':      (3.78541178e-03, [ 3, 0, 0, 0, 0, 0, 0, 0],  '3.785411784*L',          'US gallon',         False              ),
'bbl':      (0.158987294928, [ 3, 0, 0, 0, 0, 0, 0, 0],  '158.987294928*L',        'US barrel',         False              ),
# units of energy
'J':        (1.0e3,          [ 2, 1,-2, 0, 0, 0, 0, 0],  'N*m',                    'Joule',             True               ),
'eV':       (1.602176634e-16,[ 2, 1,-2, 0, 0, 0, 0, 0],  '[e]*V',                  'electronvolt',      True               ),
'erg':      (1.0e-4,         [ 2, 1,-2, 0, 0, 0, 0, 0],  'dyn*cm',                 'erg',               False              ),
'cal':      (4184.0,         [ 2, 1,-2, 0, 0, 0, 0, 0],  '4.184*J',                'calorie',           ['k','M']          ),
'Cal':      (4.184e6,        [ 2, 1,-2, 0, 0, 0, 0, 0],  'kcal',                   'Calorie',           False              ),
'Ha':       (4.35974472e-15, [ 2, 1,-2, 0, 0, 0, 0, 0],  '4.3597447222071e-18*J',  'Hartree',           ['k','M']          ),
'E_h':      (4.35974472e-15, [ 2, 1,-2, 0, 0, 0, 0, 0],  'Ha',                     'Hartree',           ['k','M']          ),
# units of pressure
'Pa':       (1.0e3,          [-1, 1,-2, 0, 0, 0, 0, 0],  'N/m2',                   'Pascal',            True               ),
'atm':      (1.013250e8,     [-1, 1,-2, 0, 0, 0, 0, 0],  '101325*Pa',              'atm. pressure',     False              ),
'bar':      (1e8,            [-1, 1,-2, 0, 0, 0, 0, 0],  '100*kPa',                'bar',               ['m','k']          ),
'Ba':       (1e2,            [-1, 1,-2, 0, 0, 0, 0, 0],  '0.1*Pa',                 'Barye',             False              ),
# units of force
'N':        (1.0e3,          [ 1, 1,-2, 0, 0, 0, 0, 0],  'kg*m/s2',                'Newton',            True               ),
'dyn':      (1.0e-2,         [ 1, 1,-2, 0, 0, 0, 0, 0],  'g*cm/s2',                'dyne',              True               ),
# units of energy absorption
'Gy':       (1.0e0,          [ 2, 0,-2, 0, 0, 0, 0, 0],  'J/kg',                   'Gray',              False              ),
'Sv':       (1.0e0,          [ 2, 0,-2, 0, 0, 0, 0, 0],  'J/kg',                   'Sivert',            False              ),
# units of magnetic flux density
'T':        (1.0e3,          [ 0, 1,-1, 0,-1, 0, 0, 0],  'Wb/m2',                  'Tesla',             True               ),
'G':        (1.0e-1,         [ 0, 1,-1, 0,-1, 0, 0, 0],  '1e-4*T',                 'Gauss',             True               ),
# units of frequency
'Hz':       (1.0e0,          [ 0, 0,-1, 0, 0, 0, 0, 0],  's-1',                    'Hertz',             True               ),
'Bq':       (1.0e0,          [ 0, 0,-1, 0, 0, 0, 0, 0],  's-1',                    'Becquerel',         False              ),
# units of power
'W':        (1.0e3,          [ 2, 1,-3, 0, 0, 0, 0, 0],  'J/s',                    'Watt',              True               ),
'hp':       (745700.0,       [ 2, 1,-3, 0, 0, 0, 0, 0],  '745.7*W',                'horse power',       False              ),
# units of velocity
'mph':      (0.44704,        [ 1, 0,-1, 0, 0, 0, 0, 0],  '0.44704*m/s',            'US miles per hour', False              ),
'kn':       (0.514444,       [ 1, 0,-1, 0, 0, 0, 0, 0],  '0.514444*m/s',           'knot',              False              ),
# units of magnetic flux
'Mx':       (1.0e-5,         [ 2, 1,-1, 0,-1, 0, 0, 0],  '1e-8*Wb',                'Maxwell',           False              ),
'Wb':       (1.0e3,          [ 2, 1,-1, 0,-1, 0, 0, 0],  'V*s',                    'Weber',             False              ),

# other CGS units
'P':        (1.0e2,          [-1, 1,-1, 0, 0, 0, 0, 0],  'g/(cm*s)',               'Poise',             ['c']              ),
'St':       (1.0e-4,         [ 2, 0,-1, 0, 0, 0, 0, 0],  'cm2/s',                  'Stokes',            ['c']              ),
'Ka':       (1.0e2,          [-1, 0, 0, 0, 0, 0, 0, 0],  'cm-1',                   'Kayser',            False              ),
'D':        (3.33564e-30,    [ 1, 0, 0, 0, 1, 0, 0, 0],  '3.33564e-30*C*m',        'Debye',             True               ),
'Oe':       (79.57747,       [-1, 0,-1, 0, 1, 0, 0, 0],  '1e3*A/(4*[pi]*m)',       'Oersted',           False              ),
'Gal':      (0.01,           [ 1, 0,-2, 0, 0, 0, 0, 0],  'cm/s2',                  'Gal',               False              ),
'Bi':       (10,             [ 0, 0,-1, 0, 1, 0, 0, 0],  '10*A',                   'Biot',              False              ),
'Rad':      (1e-2,           [ 2, 0,-2, 0, 0, 0, 0, 0],  '0.01*Gy',                'radiation dose',    False              ),

# other derived units
'sr':       (1.0e0,          [ 0, 0, 0, 0, 0, 0, 0, 2],  'rad2',                   'steradian',         False              ),
'lm':       (1.0e0,          [ 0, 0, 0, 0, 0, 1, 0, 2],  'cd*sr',                  'lumen',             False              ),
'A':        (1.0e0,          [ 0, 0,-1, 0, 1, 0, 0, 0],  'C/s',                    'Ampere',            True               ),
'H':        (1.0e3,          [ 2, 1, 0, 0,-2, 0, 0, 0],  'Wb/A',                   'Henry',             True               ),
'Ohm':      (1.0e3,          [ 2, 1,-1, 0,-2, 0, 0, 0],  'V/A',                    'Ohm',               True               ),
'V':        (1.0e3,          [ 2, 1,-2, 0,-1, 0, 0, 0],  'J/C',                    'Volt',              True               ),
'lx':       (1.0e0,          [-2, 0, 0, 0, 0, 1, 0, 2],  'lm/m2',                  'lux',               False              ),
'F':        (1.0e-3,         [-2,-1, 2, 0, 2, 0, 0, 0],  'C/V',                    'Farad',             True               ),
'S':        (1.0e-3,         [-2,-1, 1, 0, 2, 0, 0, 0],  'Ohm-1',                  'Siemens',           True               ),
'kat':      (1,              [ 0, 0,-1, 0, 0, 0, 1, 0],  'mol/s',                  'katal',             True               ),
# logarithmic units and ratios
'PR':       (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  '1',                      'Power ratio',       False              ), 
'AR':       (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  '1',                      'Amplitude ratio',   False              ),
'Np':       (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'Nepers',            ['c','d']          ),
'B':        (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'Bel',               ['d']              ),
'Bm':       (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'bel-milliwatt',     ['d']              ),
'BmW':      (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'bel-milliwatt',     ['d']              ),
'BW':       (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'bel-watt',          ['d']              ),
'BV':       (1,              [ 2, 1,-2, 0,-1, 0, 0, 0],  LogarithmicUnitType,      'bel-volt',          ['d']              ),
'BuV':      (1,              [ 2, 1,-2, 0,-1, 0, 0, 0],  LogarithmicUnitType,      'bel-microvolt',     ['d']              ),
'BA':       (1,              [ 0, 0,-1, 0, 1, 0, 0, 0],  LogarithmicUnitType,      'bel-amps',          ['d']              ),
'BuA':      (1,              [ 0, 0,-1, 0, 1, 0, 0, 0],  LogarithmicUnitType,      'bel-microamps',     ['d']              ),
'BOhm':     (1,              [ 2, 1,-1, 0,-2, 0, 0, 0],  LogarithmicUnitType,      'bel-ohms',          ['d']              ),
'BSPL':     (1,              [-1, 1,-2, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'bel-SPL (Pa)',      ['d']              ),
'BSIL':     (1,              [ 0, 1,-3, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'bel-SIL (W/m2)',    ['d']              ), 
'BSWL':     (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicUnitType,      'bel-SWL (W)',       ['d']              ),
# percentages
'%':        (1e-2,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-2',                   'percent',           False              ),
'ppth':     (1e-3,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-3',                   'promile',           False              ),
# dimensionless constants
'[alpha]':  (7.29735256e-3,  [ 0, 0, 0, 0, 0, 0, 0, 0],  '7.29735256e-3',          "fine str. const.",  False              ),
'[euler]':  (np.e,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '2.718282',               "Euler's num.",      False              ),
'[N_0]':    (6.02214076e23,  [ 0, 0, 0, 0, 0, 0, 0, 0],  '6.02214076e23',          "Avogadro's num.",   False              ),
'[pi]':     (np.pi,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '3.1415926',              'pi num.',           False              ),
# natural constants    
'[a_0]':    (5.291772109e-11,[ 1, 0, 0, 0, 0, 0, 0, 0],  '5.29177210903e-11*m',    'Bohr radius',       False              ),
'[c]':      (2.99792458e8,   [ 1, 0,-1, 0, 0, 0, 0, 0],  '299792458*m/s',          'speed of light',    False              ),
'[e]':      (1.602176634e-19,[ 0, 0, 0, 0, 1, 0, 0, 0],  '1.602176634e-19*C',      'elem. charge',      False              ),
'[eps_0]':  (8.854188e-15,   [-3,-1, 2, 0, 2, 0, 0, 0],  '8.854187817e-12*F/m',    'permit. of vac.',   False              ),
'[G]':      (6.672590e-14,   [ 3,-1,-2, 0, 0, 0, 0, 0],  '6.67259e-11*m3/(kg*s2)', 'grav. const.',      False              ),
'[g]':      (9.806650e0,     [ 1, 0,-2, 0, 0, 0, 0, 0],  '9.80665*m/s2',           'grav. accel.',      False              ),
'[h]':      (6.626076e-31,   [ 2, 1,-1, 0, 0, 0, 0, 0],  '6.6260755e-34*J*s',      'Planck const.',     False              ),
'[hbar]':   (1.054572748e-31,[ 2, 1,-1, 0, 0, 0, 0, 0],  '[h]/(2*[pi])',           'Reduced Pl. con.',  False              ),
'[H_0]':    (2.197232394e-18,[ 0, 0,-1, 0, 0, 0, 0, 0],  '67.8*km/(s*Mpc)',        'Hubble const.',     False              ),
'[k]':      (1.380658e-20,   [ 2, 1,-2,-1, 0, 0, 0, 0],  '1.380658e-23*J/K',       'Boltzmann const.',  False              ),
'[k_B]':    (1.380658e-20,   [ 2, 1,-2,-1, 0, 0, 0, 0],  '[k]',                    'Boltzmann const.',  False              ),
'[k_e]':    (8.9875517923e12,[ 3, 1,-2, 0,-2, 0, 0, 0],  '8.9875517923e9*N*m2/C2', 'Coulomb const.',    False              ),
'[L_sol]':  (3.826e29,       [ 2, 1,-3, 0, 0, 0, 0, 0],  '3.826e33*erg/s',         'Solar luminosity',  False              ),
'[M_sol]':  (1.98847e33,     [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.98847e30*kg',          'Solar mass',        False              ),
'[mu_0]':   (1.256637e-3,    [ 1, 1, 0, 0,-2, 0, 0, 0],  '4*[pi]*1e-7*N/A2',       'permeab. of vac.',  False              ),
'[mu_B]':   (1.67262e-24,    [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.67262e-24*g',          'Bohr magneton',     False              ),
'[m_e]':    (9.109383e-28,   [ 0, 1, 0, 0, 0, 0, 0, 0],  '9.1093837015e-31*kg',    'electron mass',     False              ),
'[m_p]':    (1.672623e-24,   [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.6726231e-24*g',        'proton mass',       False              ),
'[m_n]':    (1.6749286e-24,  [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.6749286e-24*g',        'neutron mass',      False              ),
'[R_inf]':  (1.09737e7,      [-1, 0, 0, 0, 0, 0, 0, 0],  '1.09737e5/cm',           'Rydberg constant',  False              ),
'[R_sol]':  (6.9558e8,       [ 1, 0, 0, 0, 0, 0, 0, 0],  '6.9558e10*cm',           'Solar radius',      False              ),
'[sigma]':  (5.67037e-5,     [ 0, 1,-3,-4, 0, 0, 0, 0],  '5.67037e-8*W/(m2*K4)',   'Stef.Bolt. const.', False              ),
'[N_A]':    (6.02214076e23,  [ 0, 0, 0, 0, 0, 0,-1, 0],  '[N_0]/mol',              "Avogadro's const.", False              ),

# Gaussian based units (GBU), EMU and ESU
'statC':    (1.0e-3,         [(3,2), (1,2),  -1, 0, 0, 0, 0, 0],  'dyn1:2*cm',      'statcoulomb GBU',   False              ),
'Fr':       (1.0e-3,         [(3,2), (1,2),  -1, 0, 0, 0, 0, 0],  'statC',          'Franklin GBU',      False              ),
'esu':      (1.0e-3,         [(3,2), (1,2),  -1, 0, 0, 0, 0, 0],  'statC',          'el.stat. unit GBU', False              ),
'statA':    (1.0e-3,         [(3,2), (1,2),  -2, 0, 0, 0, 0, 0],  'statC/s',        'statampere GBU',    False              ),
'statV':    (1.0e-1,         [(1,2), (1,2),  -1, 0, 0, 0, 0, 0],  'erg/statC',      'statvolt GBU',      False              ),
'statG':    (1.0e1,          [(-1,2), (1,2), -1, 0, 0, 0, 0, 0],  'cm-1:2*g1:2/s',  'Gauss GBU',         False              ),
'statOe':   (1.0e1,          [(-1,2), (1,2), -1, 0, 0, 0, 0, 0],  'cm-1:2*g1:2/s',  'Oersted GBU',       False              ),
#'statOhm':  (8.987551787e14, [ 2, 1,-1, 0,-2, 0, 0, 0],  '8.987551787e11*Ohm',     'statohm',           False              ),
#'statF':    (1.11265005e-15, [-4,-1, 4, 0, 2, 0, 0, 0],  '1e5*[c]-2*F',            'statfarad',         False              ),
'abC':      (0.1,            [(1,2), (1,2),   0, 0, 0, 0, 0, 0],  'g1:2*cm1:2',     'abcoulomb GBU',     False              ),
'abA':      (0.1,            [(1,2), (1,2),  -1, 0, 0, 0, 0, 0],  'g1:2*cm1:2/s',   'abampere GBU',      False              ),
'abBi':     (0.1,            [(1,2), (1,2),  -1, 0, 0, 0, 0, 0],  'abA',            'Biot GBU',          False              ),
'abH':      (1e-6,           [    2,     1,   0, 0,-2, 0, 0, 0],  'nH',             'Henry GBU',         False              ),
'abOhm':    (1e-2,           [    1,     0,  -1, 0, 0, 0, 0, 0],  'cm/s',           'Ohm GBU',           False              ),
# Constants specific for GBU
'[emu_mu_B]':  (9.27401007e-26, [(5,2), (1,2), -1, 0, 0, 0, 0, 0],  '9.274010078e-21*erg/statG', 'Bohr magneton', False   ),
'[esu_mu_B]':  (2.78027800e-17, [(7,2), (1,2), -2, 0, 0, 0, 0, 0],  '2.78027800e-10*statA*cm2',  'Bohr magneton', False   ),
'[esu_e]':     (4.80320427e-13, [(3,2), (1,2), -1, 0, 0, 0, 0, 0],  '4.80320427e-10*statC', 'elem. charge', False         ),
'[emu_e]':     (1.60217663e-21, [(1,2), (1,2),  0, 0, 0, 0, 0, 0],  '1.602176634e-20*abC',  'elem. charge', False         ),
}, keys=True)

QUANTITY_LIST = RowCollector(['name','symbol', 'SI', 'AU', 'CGS', 'GAUSS', 'ESU', 'EMU'], [
('AbsorbedDose',          'ADO',   'Gy',       None,                   'Rad',      'Rad',            'Rad',            'Rad',             ),
('Acceleration',          'ACC',   'm/s2',     None,                   'Gal',      'Gal',            'Gal',            'Gal',            ),
('Action',                'ACT',   'J*s',      '[hbar]',               None,       None,             None,             None,             ),
('AmountOfSubstance',     'AOS',   'mol',      None,                   None,       None,             None,             None,             ),
('AngularFrequency',      'AFR',   'rad/s',    None,                   None,       None,             None,             None,             ),
('Capacitance',           'CAP',   'F',        None,                   None,       'cm',             'cm',             'abF',            ),
('CatalyticActivity',     'CAC',   'kat',      None,                   None,       None,             None,             None,             ),
('Conductance',           'CON',   'S',        None,                   None,       None,             None,             None,             ),
('DynamicViscosity',      'DVI',   'Pa*s',     None,                   'P',        'P',              'P',              'P',              ),
('ElectricCurrent',       'ECU',   'A',        '[e]*E_h/[hbar]',       'Bi',       'statA',          'statA',          'abA',            ),
('ElectricCharge',        'ECH',   'C',        '[e]',                  None,       'statC',          'statC',          'abC',            ),
('ElectricChargeDensity', 'ECD',   'C/m3',     '[e]/[a_0]3',           None,       None,             None,             None,             ),
('ElectricPotential',     'EPO',   'V',        'E_h/[e]',              None,       'statV',          'statV',          'abV',            ),
('ElectricDipoleMoment',  'EDM',   'C*m',      '[e]*[a_0]',            None,       'statC*cm',       'statC*cm',       'abC*cm',         ),
('ElectricDisplField',    'EDF',   'C*m2',     None,                   None,       'statC/cm2',      'statC/cm2',      'abC/cm2',        ),
('ElectricField',         'EFI',   'V/m',      'E_h/([e]*[a_0])',      None,       'statV/cm',       'statV/cm',       'abV/cm',         ),
('ElectricFieldGradient', 'EFG',   'V/m2',     'E_h/([e]*[a_0]2)',     None,       None,             None,             None,             ),
('ElectricFlux',          'EFL',   'V*m',      None,                   None,       'statC',          'statC',          'abC',            ),
('ElectricPolarizability','EPL',   'm2/J',     '[e]2*[a_0]2/E_h',      None,       None,             None,             None,             ),
('ElectromotiveForce',    'EFO',   'V',        None,                   None,       None,             None,             None,             ),
('Energy',                'ENE',   'J',        'E_h',                  'erg',      'erg',            'erg',            'erg',            ),
('EquivalentDose',        'EDO',   'Sv',       None,                   None,       None,             None,             None,             ),
('Force',                 'FOR',   'N',        'E_h/[a_0]',            'dyn',      'dyn',            'dyn',           'dyn',             ),
('Frequency',             'FRE',   'Hz',       None,                   None,       None,             None,             None,             ),
('Heat',                  'HEA',   'J',        None,                   None,       None,             None,             None,             ),
('Illuminance',           'ILL',   'lx',       None,                   None,       None,             None,             None,             ),
('Impedance',             'IMP',   'Ohm',      None,                   None,       None,             None,             None,             ),
('Inductance',            'IND',   'H',        None,                   None,       's2/cm',          'c2/cm',          'abH',            ),
('Irradience',            'IRR',   'W/m2',     'E_h2/([hbar]*[a_0]2)', None,       None,             None,             None,             ),
('KinematicViscosity',    'KVI',   'm2/s',     None,                   'St',       'St',             'St',             'St',             ),
('Length',                'LEN',   'm',        '[a_0]',                'cm',       'cm',             'cm',             'cm',             ),
('LuminousIntensity',     'LIN',   'cd',       None,                   None,       None,             None,             None,             ),
('LuminousFlux',          'LFL',   'lm',       None,                   None,       None,             None,             None,             ),
('MagneticField',         'MFI',   'A/m',      None,                   'Oe',       'statOe',         'statA/cm',       'statOe',         ), # Mag. H field
('MagneticFlux',          'MFL',   'Wb',       None,                   'Mx',       'statG*cm2',      'statWb',         'statG*cm2',      ),
('MagneticFluxDensity',   'MFD',   'T',        '[hbar]/([e]*[a_0]2)',  'G',        'statG',          'statT',          'statG',          ), # Mag. B field
('MagneticDipoleMoment',  'MDM',   'J/T',      '[hbar]*[e]/[m_e]',     None,       'erg/statG',      'statC*cm2',      'abA*cm2',        ),
('Magnetizability',       'MAG',   'J/T2',     '[e]2*[a_0]2/[m_e]',    None,       None,             None,             None,             ),
('Mass',                  'MAS',   'kg',       '[m_e]',                'g',        'g',              'g',              'g',              ),
('Momentum',              'MOM',   'kg*m/s',   '[hbar]/[a_0]',         None,       None,             None,             None,             ),
('Permittivity',          'PER',   'F/m',      '[e]2/([a_0]*E_h)',     None,       None,             None,             None,             ),
('PlaneAngle',            'PAN',   'rad',      None,                   None,       None,             None,             None,             ),
('Power',                 'POW',   'W',        None,                   'erg/s',    'erg/s',          'erg/s',          'erg/s',          ),
('Pressure',              'PRE',   'Pa',       'E_h/[a_0]3',           'Ba',       'Ba',             'Ba',             'Ba',             ),
('RadiantFlux',           'RFL',   'W',        None,                   None,       None,             None,             None,             ),
('Radioactivity',         'RAD',   'Bq',       None,                   None,       None,             None,             None,             ),
('Reactance',             'REA',   'Ohm',      None,                   None,       None,             None,             None,             ),
('Resistance',            'RES',   'Ohm',      None,                   None,       's/cm',           's/cm',           'abOhm',          ),
('Resistivity',           'REI',   'Ohm*m',    None,                   None,       's',              's',              'abOhm*cm',       ),
('SolidAnge',             'SAN',   'sr',       None,                   None,       None,             None,             None,             ),
('Stress',                'STR',   'Pa',       None,                   None,       None,             None,             None,             ),
('Temperature',           'TEM',   'K',        None,                   None,       None,             None,             None,             ),
('Time',                  'TIM',   's',        '[hbar]/E_h',           's',        's',              's',              's',              ),
('Velocity',              'VEL',   'm/s',      '[a_0]*E_h/[hbar]',     'cm/s',     'cm/s',           'cm/s',           'cm/s',           ),
('Voltage',               'VOL',   'V',        None,                   None,       None,             None,             None,             ),
('Wavenumber',            'WAV',   'm-1',      None,                   'Ka',       'Ka',             'Ka',             'Ka',             ),
('Weight',                'WEI',   'N',        None,                   None,       None,             None,             None,             ),
('Work',                  'WOR',   'J',        None,                   None,       None,             None,             None,             ),
# Constants
('BohrMagneton',          'BMA',   '[mu_B]',   '[mu_B]',               '[mu_B]',   '[esu_mu_B]',    '[emu_mu_B]',      '[emu_mu_B]',     ),
('CoulombConst',          'CCO',   '[k_e]',    '[k_e]',                '[k_e]',    '1',             '1',               '[c]2',           ),
('ElementaryCharge',      'ELC',   '[e]',      '[e]',                  '[e]',      '[esu_e]',       '[esu_e]',         '[emu_e]',        ),
('PermeabilityVacuum',    'PBV',   '[mu_0]',   '[mu_0]',               '[mu_0]',   '1',             '[c]-2',           '1',              ),
('PermittivityVacuum',    'PTV',   '[eps_0]',  '[eps_0]',              '[eps_0]',  '1',             '1',               '[c]-2',          ),
])
SI    = Enum('SI',    dict(zip(QUANTITY_LIST.name, [f"{SYMBOL_SYSTEM_UNIT}S{symbol}" for symbol in QUANTITY_LIST.symbol])))
AU    = Enum('AU',    dict(zip(QUANTITY_LIST.name, [f"{SYMBOL_SYSTEM_UNIT}A{symbol}" for symbol in QUANTITY_LIST.symbol])))
CGS   = Enum('CGS',   dict(zip(QUANTITY_LIST.name, [f"{SYMBOL_SYSTEM_UNIT}C{symbol}" for symbol in QUANTITY_LIST.symbol])))
GAUSS = Enum('GAUSS', dict(zip(QUANTITY_LIST.name, [f"{SYMBOL_SYSTEM_UNIT}G{symbol}" for symbol in QUANTITY_LIST.symbol])))
ESU   = Enum('ESU',   dict(zip(QUANTITY_LIST.name, [f"{SYMBOL_SYSTEM_UNIT}E{symbol}" for symbol in QUANTITY_LIST.symbol])))
EMU   = Enum('EMU',   dict(zip(QUANTITY_LIST.name, [f"{SYMBOL_SYSTEM_UNIT}M{symbol}" for symbol in QUANTITY_LIST.symbol])))
