import re
import numpy as np

from .periodic_table import *
from ..units import Quantity, Unit
from .. import RowCollector, ParameterTable

PERIODIC_TABLE = ParameterTable(PT_HEADER, PT_DATA, keys=True)

class Element:
    expression: str
    count: int
    element: str
    isotope: int
    ionisation: int
    A: Quantity = None
    Z: float = None
    N: float = None
    e: float = None
    n: Quantity = None
    rho: Quantity = None

    @staticmethod
    def get_isotope(element:str, isotope: int, ionisation: int):
        isotopes = PERIODIC_TABLE[element]
        Z = isotopes.Z
        iso = isotope if isotope else Z*2
        ion = ionisation if ionisation else 0
        if str(iso) not in isotopes.A:
            raise Exception("Required isotope could not be found:", element, iso)
        M, NA = isotopes.A[str(iso)]
        A = Quantity(M, 'Da') + Quantity(ion, '[m_e]')
        N = int(iso-isotopes.Z)
        e = isotopes.Z+ion
        return NA, A, Z, N, e, iso, ion
        
    @staticmethod
    def get_average(element:str, ionisation:int):
        elements = PERIODIC_TABLE[element]
        with RowCollector(['NA', 'A', 'Z', 'N', 'e', 'iso', 'ion']) as rc:
            for iso in elements.A.keys():
                rc.append(Element.get_isotope(element, int(iso), ionisation))
            return (
                np.sum(rc.NA), 
                np.average(rc.A, weights=rc.NA),
                np.average(rc.Z, weights=rc.NA),
                np.average(rc.N, weights=rc.NA),
                np.average(rc.e, weights=rc.NA),
                np.average(rc.iso, weights=rc.NA),
                np.average(rc.ion, weights=rc.NA),
            )

    def __init__(self, expression:str, count:int=1):
        self.expression = expression
        self.count = count
        # parse the expression
        if m := re.match("(\[(p|n|e)\])", expression):
            nucleon = m.group(2)
            self.element = expression
            NA, iso, ion = 100.0, None, None
            A = Unit(f"[m_{nucleon}]").to('Da')
            nucleons = {'p':(1,0,0),'n':(0,1,0),'e':(0,0,1)}
            Z, N, e = nucleons[nucleon]
        elif m := re.match("([a-zA-Z]{1,2})(\{([0-9]+)([+-]{1}[0-9]*)\}|\{([0-9]+)\}|\{([+-]{1}[0-9]*)\}|)", expression):
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
                self.isotope, self.ionisation = int(iso2), None
            elif ion3:
                if ion3=="-": ion3="-1"
                elif ion3=="+": ion3="1"
                self.isotope, self.ionisation = None, int(ion3)
            else:
                self.isotope, self.ionisation = None, None
            # set element values
            if self.isotope:
                NA, A, Z, N, e, iso, ion = Element.get_isotope(self.element, self.isotope, self.ionisation)
            else:
                NA, A, Z, N, e, iso, ion = Element.get_average(self.element, self.ionisation)
        else:
            raise Exception('Unrecognized expression', expression)
        self.A = self.count*A
        self.Z = self.count*Z
        self.N = self.count*N
        self.e = self.count*e
        
    def __mul__(self, other:float):
        return Element(self.expression, self.count*other)
            
    def __add__(self, other:'Element'):
        if self.expression!=other.expression:
            raise Exception("Only same elements can be added up:", self.expression, other.expression)
        return Element(self.expression, self.count+other.count)
        
    def set_density(self, n:Quantity):
        self.n = self.count * n
        self.rho = self.A * n
