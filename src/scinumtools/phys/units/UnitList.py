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
    'm':        (1.0,            [ 1, 0, 0, 0, 0, 0, 0, 0],  None,                     'meter'            ),
    'g':        (1.0,            [ 0, 1, 0, 0, 0, 0, 0, 0],  None,                     'gram'             ),
    's':        (1.0,            [ 0, 0, 1, 0, 0, 0, 0, 0],  None,                     'second'           ),
    'K':        (1.0,            [ 0, 0, 0, 1, 0, 0, 0, 0],  None,                     'kelvin'           ),
    'C':        (1.0,            [ 0, 0, 0, 0, 1, 0, 0, 0],  None,                     'coulomb'          ),
    'cd':       (1.0,            [ 0, 0, 0, 0, 0, 1, 0, 0],  None,                     'candela'          ),
    # base numerical units
    'mol':      (1.0,            [ 0, 0, 0, 0, 0, 0, 1, 0],  None,                     'mole'             ),
    'rad':      (1.0,            [ 0, 0, 0, 0, 0, 0, 0, 1],  None,                     'radian'           ),
    # Derived units              
    'sr':       (1.0e0,          [ 0, 0, 0, 0, 0, 0, 0, 2],  'rad2',                   'steradian'        ),
    'Hz':       (1.0e0,          [ 0, 0,-1, 0, 0, 0, 0, 0],  's-1',                    'hertz'            ),
    'W':        (1.0e3,          [ 2, 1,-3, 0, 0, 0, 0, 0],  'J/s',                    'watt'             ),
    'A':        (1.0e0,          [ 0, 0,-1, 0, 1, 0, 0, 0],  'C/s',                    'ampere'           ),
    'V':        (1.0e3,          [ 2, 1,-2, 0,-1, 0, 0, 0],  'J/C',                    'volt'             ),
    'F':        (1.0e-3,         [-2,-1, 2, 0, 2, 0, 0, 0],  'C/V',                    'farad'            ),
    'Ohm':      (1.0e3,          [ 2, 1,-1, 0,-2, 0, 0, 0],  'V/A',                    'ohm'              ),
    'S':        (1.0e-3,         [-2,-1, 1, 0, 2, 0, 0, 0],  'Ohm-1',                  'siemens'          ),
    'Wb':       (1.0e3,          [ 2, 1,-1, 0,-1, 0, 0, 0],  'V*s',                    'weber'            ),
    'H':        (1.0e3,          [ 2, 1, 0, 0,-2, 0, 0, 0],  'Wb/A',                   'henry'            ),
    'lm':       (1.0e0,          [ 0, 0, 0, 0, 0, 1, 0, 2],  'cd*sr',                  'lumen'            ),
    'lx':       (1.0e0,          [-2, 0, 0, 0, 0, 1, 0, 2],  'lm/m2',                  'lux'              ),
    'Bq':       (1.0e0,          [ 0, 0,-1, 0, 0, 0, 0, 0],  's-1',                    'becquerel'        ),
    'ar':       (1.0e2,          [ 2, 0, 0, 0, 0, 0, 0, 0],  '100*m2',                 'are'              ),
    # units of energy absorption
    'Gy':       (1.0e0,          [ 2, 0,-2, 0, 0, 0, 0, 0],  'J/kg',                   'gray'             ),
    'Sv':       (1.0e0,          [ 2, 0,-2, 0, 0, 0, 0, 0],  'J/kg',                   'sivert'           ),
    # units of magnetic flux density
    'T':        (1.0e3,          [ 0, 1,-1, 0,-1, 0, 0, 0],  'Wb/m2',                  'tesla'            ),
    'G':        (1.0e-1,         [ 0, 1,-1, 0,-1, 0, 0, 0],  '1e-4*T',                 'Gauss'            ),
    # units of energy
    'J':        (1.0e3,          [ 2, 1,-2, 0, 0, 0, 0, 0],  'N*m',                    'joule'            ),
    'eV':       (1.60217733e-16, [ 2, 1,-2, 0, 0, 0, 0, 0],  '[e]*V',                  'electronvolt'     ),
    'erg':      (1.0e-4,         [ 2, 1,-2, 0, 0, 0, 0, 0],  'dyn*cm',                 'erg'              ),
    # units of pressure
    'Pa':       (1.0e3,          [-1, 1,-2, 0, 0, 0, 0, 0],  'N/m2',                   'pascal'           ),
    'atm':      (1.013250e8,     [-1, 1,-2, 0, 0, 0, 0, 0],  '101325*Pa',              'atm. pressure'    ),
    # units of force
    'N':        (1.0e3,          [ 1, 1,-2, 0, 0, 0, 0, 0],  'kg*m/s2',                'newton'           ),
    'dyn':      (1.0e-2,         [ 1, 1,-2, 0, 0, 0, 0, 0],  'g*cm/s2',                'dyne'             ),
    # angular units
    'deg':      (1.7453292e-2,   [ 0, 0, 0, 0, 0, 0, 0, 1],  '2*[pi]*rad/360',         'angle degree'     ),
    "'":        (2.908882e-4,    [ 0, 0, 0, 0, 0, 0, 0, 1],  'deg/60',                 'angle minute'     ),
    "''":       (4.848137e-6,    [ 0, 0, 0, 0, 0, 0, 0, 1],  "'/60",                   'angle second'     ),
    # units of distance
    'au':       (1.49597870e11,  [ 1, 0, 0, 0, 0, 0, 0, 0],  '149597.870691*Mm',       'astr. unit'       ),
    'AU':       (1.49597870e11,  [ 1, 0, 0, 0, 0, 0, 0, 0],  'au',                     'astr. unit'       ),
    'ly':       (9.460730e15,    [ 1, 0, 0, 0, 0, 0, 0, 0],  '[c]*yr_j',               'light-year'       ),
    # units of volume
    'l':        (1e-3,           [ 3, 0, 0, 0, 0, 0, 0, 0],  'dm3',                    'liter'            ),
    'L':        (1e-3,           [ 3, 0, 0, 0, 0, 0, 0, 0],  'l',                      'liter'            ),
    # units of time
    'min':      (6.0e1,          [ 0, 0, 1, 0, 0, 0, 0, 0],  '60*s',                   'minute'           ),
    'h':        (3.6e3,          [ 0, 0, 1, 0, 0, 0, 0, 0],  '60*min',                 'hour'             ),
    'day':      (8.64e4,         [ 0, 0, 1, 0, 0, 0, 0, 0],  '24*h',                   'day'              ),
    'yr_t':     (3.1556925e7,    [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.24219*day',          'tropical year'    ),
    'yr_j':     (3.1557600e7,    [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.25*day',             'Julian year'      ),
    'yr_g':     (3.155695e7,     [ 0, 0, 1, 0, 0, 0, 0, 0],  '365.2425*day',           'Gregorian year'   ),
    'yr':       (3.155760e7,     [ 0, 0, 1, 0, 0, 0, 0, 0],  'yr_j',                   'year'             ),
    # units of temperature
    'Cel':      (1,              [ 0, 0, 0, 1, 0, 0, 0, 0],  TemperatureConverter,     'Degree Celsius'   ),
    'degF':     (1,              [ 0, 0, 0, 1, 0, 0, 0, 0],  TemperatureConverter,     'Degree Fahrenheit'),
    'degR':     (5/9,            [ 0, 0, 0, 1, 0, 0, 0, 0],  '5/9*K',                  'Degree Rankine'   ),
    # logarithmic units and ratios
    #'ratP':     (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  '1',                      'Power ratio'      ),      
    #'ratA':     (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  '1',                      'Amplitude ratio'  ),      
    #'B':        (1,              [ 0, 0, 0, 0, 0, 0, 0, 0],  None,                     'Bell'             ),
    #'Np':       (1.151277918,    [ 0, 0, 0, 0, 0, 0, 0, 0],  '1.151277918*B',          'Nepers'           ),
    'dBm':      (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicConverter,     'decibel-milliwatt'),
    'dBmW':     (1,              [ 2, 1,-3, 0, 0, 0, 0, 0],  LogarithmicConverter,     'decibel-milliwatt'),
    # percentages
    '%':        (1e-2,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-2',                   'percent'          ),
    'ppth':     (1e-3,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '1e-3',                   'promile'          ),
    # natural constants    
    '[c]':      (2.99792458e8,   [ 1, 0,-1, 0, 0, 0, 0, 0],  '299792458*m/s',          'velocity of light'),
    '[h]':      (6.626076e-31,   [ 2, 1,-1, 0, 0, 0, 0, 0],  '6.6260755e-34*J*s',      'Planck const.'    ),
    '[k]':      (1.380658e-20,   [ 2, 1,-2,-1, 0, 0, 0, 0],  '1.380658e-23*J/K',       'Boltzmann const.' ),
    '[eps_0]':  (8.854188e-15,   [-3,-1, 2, 0, 2, 0, 0, 0],  '8.854187817e-12*F/m',    'permit. of vac.'  ),
    '[mu_0]':   (1.256637e-3,    [ 1, 1, 0, 0,-2, 0, 0, 0],  '4*[pi]*1e-7*N/A2',       'permeab. of vac.' ),
    '[e]':      (1.60217733e-19, [ 0, 0, 0, 0, 1, 0, 0, 0],  '1.60217733e-19*C',       'elem. charge'     ),
    '[m_e]':    (9.109390e-28,   [ 0, 1, 0, 0, 0, 0, 0, 0],  '9.1093897e-28*g',        'electron mass'    ),
    '[m_p]':    (1.672623e-24,   [ 0, 1, 0, 0, 0, 0, 0, 0],  '1.6726231e-24*g',        'proton mass'      ),
    '[G]':      (6.672590e-14,   [ 3,-1,-2, 0, 0, 0, 0, 0],  '6.67259e-11*m3/(kg*s2)', 'grav. const.'     ),
    '[g]':      (9.806650e0,     [ 1, 0,-2, 0, 0, 0, 0, 0],  '9.80665*m/s2',           'grav. accel.'     ),
    # dimensionless constants
    '[pi]':     (np.pi,          [ 0, 0, 0, 0, 0, 0, 0, 0],  '3.1415926',              'pi'               ),
    '[euler]':  (np.e,           [ 0, 0, 0, 0, 0, 0, 0, 0],  '2.718282',               "Euler's num."     ),
    '[N_A]':    (6.0221367e23,   [ 0, 0, 0, 0, 0, 0, 0, 0],  '6.022137e23',            "Avogadro's num."  ),
}
