from .material_base import MaterialBase
from .solve_material import MaterialSolver
from .list_elements import *
from ..units import Quantity, Unit

class Material(MaterialBase):

    def __init__(self, expr: str):
        with MaterialSolver() as ms:
            mb = ms.solve(expr)
        self.protons   = mb.protons
        self.neutrons  = mb.neutrons
        self.electrons = mb.electrons
        self.mass      = mb.mass

    def binding_energy(self, unit:str = 'MeV'):
        #mass =  NUCLEONS['[e]'][3] * self.electrons
        mass = NUCLEONS['[n]'][3] * self.neutrons
        mass += NUCLEONS['[p]'][3] * self.protons
        return (Quantity(mass - self.mass, 'Da') * Unit('[c]2')).to(unit)