from ..structs import ParameterDict
from enum import Enum
from dataclasses import dataclass

@dataclass
class ConstCGS:
    c: float     = 2.99792458e10     # speed of light            (cm s-1)            
    h: float     = 6.6260755e-27     # Planck constant           (erg s)             
    hbar: float  = 1.05457266e-27    # reduced Planck constant   (erg s)             
    G: float     = 6.67259e-8        # gravitational constant    (cm3 g-1 s-2)       
    e: float     = 4.8032068e-10     # electron charge           (esu)               
    m_e: float   = 9.1093897e-28     # electron mass             (g)                 
    m_p: float   = 1.6726231e-24     # proton mass               (g)                 
    m_n: float   = 1.6749286e-24     # neutron mass              (g)                 
    u: float     = 1.6605402e-24     # atomic mass unit          (g)                 
    k_B: float   = 1.380658e-16      # Boltzmann constant        (erg K-1)           
    eV: float    = 1.6021772e-12     # electron-Volt             (erg)               
    sigma: float = 5.67051e-5        # Stefan-Boltzmann constant (erg cm-2 K-4 s-1)   
    alpha: float = 7.29735308-3      # fine structure constant
    N_a: float   = 6.0221367e23      # Avogadro's number                             

@dataclass
class ConstMKS:
    c: float     = 299792.458        # speed of light            (km s-1)            
    h: float     = 6.62607015e-34    # Planck constant           (J s)             
    hbar: float  = 1.054571817e-34   # reduced Planck constant   (J s)             
    G: float     = 6.67430e10-11     # gravitational constant    (m3 kg-1 s-2)       
    e: float     = 1.602176634e-19   # electron charge           (C)
    m_e: float   = 9.1093837015e-31  # electron mass             (kg)
    m_p: float   = 1.67262192e-27    # proton mass               (kg)                 
    m_n: float   = 1.67492749804e-27 # neutron mass              (kg)                 
    u: float     = 1.66053906660e-27 # atomic mass unit          (kg)                 
    k_B: float   = 1.380649e-2       # Boltzmann constant        (J K-1)
    eV: float    = 1.602176634e-19   # electron-Volt             (J)
    sigma: float = 5.670374419e-8    # Stefan-Boltzmann constant (W m-2 K-4)   
    alpha: float = 7.29735308-3      # fine structure constant              
    N_a: float   = 6.0221367e23      # Avogadro's number                             
