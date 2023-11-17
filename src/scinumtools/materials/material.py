from .material_part import MaterialPart
from .solve_material import MaterialSolver
from .list_elements import *
from ..units import Quantity, Unit

class Material(MaterialPart):

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
        
    def __add__(self, other):
        protons   = self.protons + other.protons
        mass      = self.mass + other.mass
        neutrons  = self.neutrons + other.neutrons
        electrons = self.electrons + other.electrons
        return Material(protons, mass, neutrons, electrons)

    def __mul__(self, other):
        protons   = self.protons * other
        mass      = self.mass * other
        neutrons  = self.neutrons * other
        electrons = self.electrons * other
        return Material(protons, mass, neutrons, electrons)
