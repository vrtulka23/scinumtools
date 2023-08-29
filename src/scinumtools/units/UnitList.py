import numpy as np

from .UnitConverters import *
        
UnitPrefixes = {
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
}                                                                                        
            
UnitStandard = {
    # base physical units
    'm':        (1.0,            [ 1, 0, 0, 0, 0, 0, 0, 0],  None,                     'meter',             True               ),
    'g':        (1.0,            [ 0, 1, 0, 0, 0, 0, 0, 0],  None,                     'gram',              True               ),
    's':        (1.0,            [ 0, 0, 1, 0, 0, 0, 0, 0],  None,                     'second',            True               ),
    'K':        (1.0,            [ 0, 0, 0, 1, 0, 0, 0, 0],  None,                     'kelvin',            True               ),
    'C':        (1.0,            [ 0, 0, 0, 0, 1, 0, 0, 0],  None,                     'coulomb',           True               ),
    'cd':       (1.0,            [ 0, 0, 0, 0, 0, 1, 0, 0],  None,                     'candela',           True               ),
    # base numerical units
    'mol':      (1.0,            [ 0, 0, 0, 0, 0, 0, 1, 0],  None,                     'mole',              True               ),
    'rad':      (1.0,            [ 0, 0, 0, 0, 0, 0, 0, 1],  None,                     'radian',            ['m']              ),
    
    # units of distance
    'mi':       (1609.344,       [ 1, 0, 0, 0, 0, 0, 0, 0],  '1609.344*m',             'intern. mile',      False              ),
    'au':       (1.49597870e11,  [ 1, 0, 0, 0, 0, 0, 0, 0],  '149597.870691*Mm',       'astr. unit',        False              ),
    'AU':       (1.49597870e11,  [ 1, 0, 0, 0, 0, 0, 0, 0],  'au',                     'astr. unit',        False              ),
    'ly':       (9.460730e15,    [ 1, 0, 0, 0, 0, 0, 0, 0],  '[c]*yr_j',               'light-year',        ['k','M','G']      ),
    'pc':       (3.0857e16,      [ 1, 0, 0, 0, 0, 0, 0, 0],  '3.0857e16*m',            'parsec',            ['k','M','G','T']  ),
    # units of mass
    'u':        (1.6605402e-24,  [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.6605402e-24*g',        'atomic mass unit',  False              ),
    'amu':      (1.6605402e-24,  [ 0, 1, 0, 0, 0, 0, 0, 0],  'u',                      'atomic mass unit',  False              ),
    't':        (1e6,            [ 0, 1, 0, 0, 0, 0, 0, 0],  '1e3*kg',                 'tonne',             ['k','m','G']      ),
    'Msol':     (1.98847e33,     [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.98847e30*kg',          'Solar mass',        False              ),
    # units of time
    'min':      (6.0e1,          [ 0, 0, 1, 0, 0, 0, 0, 0],  '60*s',                   'minute',            False              ),
    'h':        (3.6e3,          [ 0, 0, 1, 0, 0, 0, 0, 0],  '60*min',                 'hour',              False              ),
    'day':      (8.64e4,         [ 0, 0, 1, 0, 0, 0, 0, 0],  '24*h',                   'day',               False              ),
    'yr_t':     (3.1556925e7,    [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.24219*day',          'tropical year',     ['k','m','G']      ),
    'yr_j':     (3.1557600e7,    [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.25*day',             'Julian year',       ['k','m','G']      ),
    'yr_g':     (3.155695e7,     [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.2425*day',           'Gregorian year',    ['k','m','G']      ),
    'yr':       (3.155760e7,     [ 0, 0, 1, 0, 0, 0, 0, 0],  'yr_j',                   'year',              ['k','m','G']      ),
    # units of temperature
    'Cel':      (1,              [ 0, 0, 0, 1, 0, 0, 0, 0],  TemperatureConverter,     'degree Celsius',    False              ),
    'degF':     (1,              [ 0, 0, 0, 1, 0, 0, 0, 0],  TemperatureConverter,     'degree Fahrenheit', False              ),
    'degR':     (5/9,            [ 0, 0, 0, 1, 0, 0, 0, 0],  '5/9*K',                  'degree Rankine',    False              ),
    # angular units
    'deg':      (1.7453292e-2,   [ 0, 0, 0, 0, 0, 0, 0, 1],  '2*[pi]*rad/360',         'angle degree',      False              ),
    "'":        (2.908882e-4,    [ 0, 0, 0, 0, 0, 0, 0, 1],  'deg/60',                 'angle minute',      False              ),
    "''":       (4.848137e-6,    [ 0, 0, 0, 0, 0, 0, 0, 1],  "'/60",                   'angle second',      False              ),
    
    # units of surface
    'ar':       (1.0e2,          [ 2, 0, 0, 0, 0, 0, 0, 0],  '100*m2',                 'are',               ['c','d','da','h'] ),
    # units of volume
    'l':        (1e-3,           [ 3, 0, 0, 0, 0, 0, 0, 0],  'dm3',                    'liter',             False              ),
    'L':        (1e-3,           [ 3, 0, 0, 0, 0, 0, 0, 0],  'l',                      'liter',             False              ),
    # units of energy
    'J':        (1.0e3,          [ 2, 1,-2, 0, 0, 0, 0, 0],  'N*m',                    'joule',             True               ),
    'eV':       (1.60217733e-16, [ 2, 1,-2, 0, 0, 0, 0, 0],  '[e]*V',                  'electronvolt',      True               ),
    'erg':      (1.0e-4,         [ 2, 1,-2, 0, 0, 0, 0, 0],  'dyn*cm',                 'erg',               False              ),
    # units of pressure
    'Pa':       (1.0e3,          [-1, 1,-2, 0, 0, 0, 0, 0],  'N/m2',                   'pascal',            True               ),
    'atm':      (1.013250e8,     [-1, 1,-2, 0, 0, 0, 0, 0],  '101325*Pa',              'atm. pressure',     False              ),
    'bar':      (1e8,            [-1, 1,-2, 0, 0, 0, 0, 0],  '100*kPa',                'bar',               ['m']              ),
    'Ba':       (1e2,            [-1, 1,-2, 0, 0, 0, 0, 0],  '0.1*Pa',                 'Barye',             False              ),
    # units of force
    'N':        (1.0e3,          [ 1, 1,-2, 0, 0, 0, 0, 0],  'kg*m/s2',                'newton',            True               ),
    'dyn':      (1.0e-2,         [ 1, 1,-2, 0, 0, 0, 0, 0],  'g*cm/s2',                'dyne',              True               ),
    # units of energy absorption
    'Gy':       (1.0e0,          [ 2, 0,-2, 0, 0, 0, 0, 0],  'J/kg',                   'gray',              False              ),
    'Sv':       (1.0e0,          [ 2, 0,-2, 0, 0, 0, 0, 0],  'J/kg',                   'sivert',            False              ),
    # units of magnetic flux density
    'T':        (1.0e3,          [ 0, 1,-1, 0,-1, 0, 0, 0],  'Wb/m2',                  'tesla',             True               ),
    'G':        (1.0e-1,         [ 0, 1,-1, 0,-1, 0, 0, 0],  '1e-4*T',                 'Gauss',             True               ),
    # units of frequency
    'Hz':       (1.0e0,          [ 0, 0,-1, 0, 0, 0, 0, 0],  's-1',                    'hertz',             True               ),
    'Bq':       (1.0e0,          [ 0, 0,-1, 0, 0, 0, 0, 0],  's-1',                    'becquerel',         False              ),
    
    # other derived units              
    'sr':       (1.0e0,          [ 0, 0, 0, 0, 0, 0, 0, 2],  'rad2',                   'steradian',         False              ),
    'lm':       (1.0e0,          [ 0, 0, 0, 0, 0, 1, 0, 2],  'cd*sr',                  'lumen',             False              ),
    'A':        (1.0e0,          [ 0, 0,-1, 0, 1, 0, 0, 0],  'C/s',                    'ampere',            True               ),
    'H':        (1.0e3,          [ 2, 1, 0, 0,-2, 0, 0, 0],  'Wb/A',                   'henry',             False              ),
    'Ohm':      (1.0e3,          [ 2, 1,-1, 0,-2, 0, 0, 0],  'V/A',                    'ohm',               True               ),
    'Wb':       (1.0e3,          [ 2, 1,-1, 0,-1, 0, 0, 0],  'V*s',                    'weber',             False              ),
    'V':        (1.0e3,          [ 2, 1,-2, 0,-1, 0, 0, 0],  'J/C',                    'volt',              True               ),
    'W':        (1.0e3,          [ 2, 1,-3, 0, 0, 0, 0, 0],  'J/s',                    'watt',              True               ),
    'lx':       (1.0e0,          [-2, 0, 0, 0, 0, 1, 0, 2],  'lm/m2',                  'lux',               False              ),
    'F':        (1.0e-3,         [-2,-1, 2, 0, 2, 0, 0, 0],  'C/V',                    'farad',             True               ),
    'S':        (1.0e-3,         [-2,-1, 1, 0, 2, 0, 0, 0],  'Ohm-1',                  'siemens',           True               ),
    # logarithmic units and ratios
    #'ratP':     (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  '1',                      'Power ratio',       False              ),      
    #'ratA':     (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  '1',                      'Amplitude ratio',   False              ),      
    #'B':        (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  None,                     'Bell',              ['d']),
    #'Np':       (1.151277918,    [ 0, 0, 0, 0, 0, 0, 0, 0],  '1.151277918*B',          'Nepers',            False              ),
    'dBm':      (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicConverter,     'decibel-milliwatt', False              ),
    'dBmW':     (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicConverter,     'decibel-milliwatt', False              ),
    # percentages
    '%':        (1e-2,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-2',                   'percent',           False              ),
    'ppth':     (1e-3,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-3',                   'promile',           False              ),
    # natural constants    
    '[c]':      (2.99792458e8,   [ 1, 0,-1, 0, 0, 0, 0, 0],  '299792458*m/s',          'velocity of light', False              ),
    '[h]':      (6.626076e-31,   [ 2, 1,-1, 0, 0, 0, 0, 0],  '6.6260755e-34*J*s',      'Planck const.',     False              ),
    '[hbar]':   (1.054572748e-31,[ 2, 1,-1, 0, 0, 0, 0, 0],  '[h]/(2*[pi])',           'Reduced Pl. con.',  False              ),
    '[k]':      (1.380658e-20,   [ 2, 1,-2,-1, 0, 0, 0, 0],  '1.380658e-23*J/K',       'Boltzmann const.',  False              ),
    '[k_B]':    (1.380658e-20,   [ 2, 1,-2,-1, 0, 0, 0, 0],  '[k]',                    'Boltzmann const.',  False              ),
    '[eps_0]':  (8.854188e-15,   [-3,-1, 2, 0, 2, 0, 0, 0],  '8.854187817e-12*F/m',    'permit. of vac.',   False              ),
    '[mu_0]':   (1.256637e-3,    [ 1, 1, 0, 0,-2, 0, 0, 0],  '4*[pi]*1e-7*N/A2',       'permeab. of vac.',  False              ),
    '[e]':      (1.60217733e-19, [ 0, 0, 0, 0, 1, 0, 0, 0],  '1.60217733e-19*C',       'elem. charge',      False              ),
    '[m_e]':    (9.109390e-28,   [ 0, 1, 0, 0, 0, 0, 0, 0],  '9.1093897e-28*g',        'electron mass',     False              ),
    '[m_p]':    (1.672623e-24,   [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.6726231e-24*g',        'proton mass',       False              ),
    '[m_n]':    (1.6749286e-24,  [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.6749286e-24*g',        'neutron mass',      False              ),
    '[G]':      (6.672590e-14,   [ 3,-1,-2, 0, 0, 0, 0, 0],  '6.67259e-11*m3/(kg*s2)', 'grav. const.',      False              ),
    '[g]':      (9.806650e0,     [ 1, 0,-2, 0, 0, 0, 0, 0],  '9.80665*m/s2',           'grav. accel.',      False              ),
    '[sigma]':  (5.67037e-5,     [ 0, 1,-3,-4, 0, 0, 0, 0],  '5.67037e-8*W/(m2*K4)',   'Stef.-Boltz. const.', False            ),
    # dimensionless constants
    '[pi]':     (np.pi,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '3.1415926',              'pi',                False              ),
    '[euler]':  (np.e,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '2.718282',               "Euler's num.",      False              ),
    '[N_A]':    (6.0221367e23,   [ 0, 0, 0, 0, 0, 0, 0, 0],  '6.022137e23',            "Avogadro's num.",   False              ),
    '[alpha]':  (7.29735256e-3,  [ 0, 0, 0, 0, 0, 0, 0, 0],  '7.29735256e-3',          "fine str. const.",  False              ),
}
