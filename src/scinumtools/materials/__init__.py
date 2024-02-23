from enum import Enum
MAGNITUDE_PRECISION = 1e-7

# Fraction input type
class FracType(Enum):
    NUMBER = 1    # number fraction
    MASS   = 2    # mass fraction

from .element import Element
from .molecule import Molecule
from .mixture import Mixture
from .molecule_solver import MoleculeSolver
from .mixture_solver import MixtureSolver
