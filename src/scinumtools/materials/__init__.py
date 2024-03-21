from enum import Enum
MAGNITUDE_PRECISION = 1e-7

# Fraction input type
class Norm(Enum):
    NUMBER          = 0    # number
    NUMBER_FRACTION = 1    # number fraction
    MASS_FRACTION   = 2    # mass fraction

from .element import Element
from .substance import Substance
from .substance_solver import SubstanceSolver
from .material import Material
from .material_solver import MaterialSolver
