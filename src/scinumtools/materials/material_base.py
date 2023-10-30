import re
from .list_elements import *

class MaterialBase:
    
    protons: int
    mass: float
    neutrons: int
    electrons: int

    @staticmethod
    def from_string(expr: str):
        # Match elements
        pattern = "([A-Z]+[a-z]?)(\{([0-9]*)([+-]?[0-9]*)\}|)"
        if m := re.match(pattern, expr):
            exceptions = {
                'H': ('H',1,1),
                'D': ('H',1,2),
                'T': ('H',1,3),
            }
            # parse atom and mass numbers
            if not m.group(3) and m.group(1) in exceptions:
                S, Z, A = exceptions[m.group(1)]
            elif m.group(1) in ELEMENTS:
                S = m.group(1)
                Z = ELEMENTS[S][0]
                A = int(m.group(3)) if m.group(3) else Z*2
            else:
                raise Exception("Unknown element:", m.group(1))
            # parse ionization state
            if m.group(4) in ['-','+']:
                I = int(m.group(4)+'1')
            elif m.group(4):
                I = int(m.group(4))
            else:
                I = 0
            # parse mass
            M = ELEMENTS[S][2][str(A)][0] + I * NUCLEONS['[e]'][3]
            return MaterialBase(Z, M, A-Z, Z+I)
        elif expr in NUCLEONS:
            Z, N, E, M, name = NUCLEONS[expr]
            return MaterialBase(Z, M, N, E)
        else:
            raise Exception("Atom canot be parsed from given string:", expr)

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
        return MaterialBase(protons, mass, neutrons, electrons)

    def __mul__(self, other):
        protons   = self.protons * other
        mass      = self.mass * other
        neutrons  = self.neutrons * other
        electrons = self.electrons * other
        return MaterialBase(protons, mass, neutrons, electrons)
        
