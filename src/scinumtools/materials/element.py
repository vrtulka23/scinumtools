import re
import numpy as np

from .compound import Component, Units
from .periodic_table import *
from ..units import Quantity, Unit
from .. import RowCollector, ParameterTable

PERIODIC_TABLE = ParameterTable(PT_HEADER, PT_DATA, keys=True)

class Element(Component):
    natural: bool
    element: str
    isotope: int
    ionisation: int
    Z: float = None
    N: float = None
    e: float = None

    # get a specific isotope
    def get_isotope(self, element:str, isotope: int, ionisation: int):
        isotopes = PERIODIC_TABLE[element]
        Z = isotopes.Z
        iso = isotope if isotope else Z*2
        ion = ionisation if ionisation else 0
        if str(iso) not in isotopes.A:
            raise Exception("Required isotope could not be found:", element, iso)
        M, NA = isotopes.A[str(iso)]
        A = Quantity(M, Units.ATOMIC_MASS) + Quantity(ion, '[m_e]')
        N = int(iso-isotopes.Z)
        e = isotopes.Z+ion
        return NA, A, Z, N, e, iso, ion
        
    # get the most abundant isotope
    def get_abundant(self, element:str, ionisation:int):
        isotopes = PERIODIC_TABLE[element]
        idmax = np.argmax([iso[1] for iso in isotopes.A.values()])
        isotope = int(list(A for A in isotopes.A.keys())[idmax])
        return self.get_isotope(element, isotope, ionisation)        

    # get a natural isotopic average
    def get_natural(self, element:str, ionisation:int):
        isotopes = PERIODIC_TABLE[element]
        with RowCollector(['NA', 'A', 'Z', 'N', 'e', 'iso', 'ion']) as rc:
            for iso in isotopes.A.keys():
                rc.append(self.get_isotope(element, int(iso), ionisation))
            return (
                np.sum(rc.NA), 
                np.average(rc.A, weights=rc.NA),
                np.average(rc.Z, weights=rc.NA),
                np.average(rc.N, weights=rc.NA),
                np.average(rc.e, weights=rc.NA),
                np.average(rc.iso, weights=rc.NA),
                int(rc.ion[0]),
            )

    def __init__(self, expr:str, count:int=1, natural:bool=True):
        Component.__init__(self, count)
        self.expr = expr
        self.natural = natural
        # parse the expr
        if m := re.match("(\[(p|n|e)\])", expr):
            nucleon = m.group(2)
            self.element = expr
            NA, iso, ion = 100.0, None, None
            self.mass = Unit(f"[m_{nucleon}]").to(Units.ATOMIC_MASS)
            nucleons = {'p':(1,0,0),'n':(0,1,0),'e':(0,0,1)}
            self.Z, self.N, self.e = nucleons[nucleon]
            self.isotope = 0
            self.ionisation = 0
        elif m := re.match("([a-zA-Z]{1,2})(\{([0-9]+)([+-]{1}[0-9]*)\}|\{([0-9]+)\}|\{([+-]{1}[0-9]*)\}|)", expr):
            # Extract information about isos
            element, variant, iso1, ion1, iso2, ion3 = m.groups()
            if element=='D':
                element, variant, iso1, ion1, iso2, ion3 = 'H', True, 2, ion1, 2, None
            elif element=='T':
                element, variant, iso1, ion1, iso2, ion3 = 'H', True, 3, ion1, 3, None
            self.element = element
            if iso1 and ion1:
                if ion1=="-": ion1="-1"
                elif ion1=="+": ion1="1"
                self.isotope, self.ionisation = int(iso1), int(ion1)
            elif iso2:
                self.isotope, self.ionisation = int(iso2), 0
            elif ion3:
                if ion3=="-": ion3="-1"
                elif ion3=="+": ion3="1"
                self.isotope, self.ionisation = None, int(ion3)
            else:
                self.isotope, self.ionisation = None, 0
            # set element values
            if self.isotope:
                NA, self.mass, self.Z, self.N, self.e, iso, ion = self.get_isotope(self.element, self.isotope, self.ionisation)
            elif self.natural:
                NA, self.mass, self.Z, self.N, self.e, self.isotope, self.ionisation = self.get_natural(self.element, self.ionisation)
            else:
                NA, self.mass, self.Z, self.N, self.e, self.isotope, self.ionisation = self.get_abundant(self.element, self.ionisation)
        else:
            raise Exception('Unrecognized expr', expr)

    def __mul__(self, other:float):
        return Element(self.expr, self.count*other, natural=self.natural)
    
    def __add__(self, other:'Element'):
        if self.expr!=other.expr:
            raise Exception("Only same elements can be added up:", self.expr, other.expr)
        return Element(self.expr, self.count+other.count, natural=self.natural)
        
    def __str__(self):
        if self.count>1:
            return f"Element({self.expr}{self.count} mass={self.count*self.mass.value(Units.ATOMIC_MASS):.3f} Z={self.count*self.Z} N={self.count*self.N:.3f} e={self.count*self.e})"
        else:
            return f"Element({self.expr} mass={self.mass.value(Units.ATOMIC_MASS):.3f} Z={self.Z} N={self.N:.3f} e={self.e})"
        