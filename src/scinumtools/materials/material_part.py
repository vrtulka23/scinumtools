import re

from .list_elements import *

class MaterialPart:
    
    protons: int
    mass: float
    neutrons: int
    electrons: int
    
    def __init__(self, protons, mass, neutrons=None, electrons=None):
        self.protons   = int(protons)
        self.mass      = float(mass) 
        self.neutrons  = int(protons if neutrons is None else neutrons)
        self.electrons = int(protons if electrons is None else electrons)

    def __str__(self):
        return f"{self.__class__.__name__}(p={self.protons} n={self.neutrons} e={self.electrons} m={self.mass:.3f})"
            
    def __repr__(self):
        return f"{self.__class__.__name__}(p={self.protons} n={self.neutrons} e={self.electrons} m={self.mass:.3f})"
        
    def __add__(self, other):
        protons   = self.protons + other.protons
        mass      = self.mass + other.mass
        neutrons  = self.neutrons + other.neutrons
        electrons = self.electrons + other.electrons
        return MaterialPart(protons, mass, neutrons, electrons)

    def __mul__(self, other):
        protons   = self.protons * other
        mass      = self.mass * other
        neutrons  = self.neutrons * other
        electrons = self.electrons * other
        return MaterialPart(protons, mass, neutrons, electrons)
