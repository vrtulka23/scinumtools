from . import Units
from ..units import Quantity

class Matter:

    mass_density: Quantity = None   # mass density
    number_density: Quantity = None # number density
    volume: Quantity = None         # volume
    mass: Quantity = None           # mass

    def __init__(self, 
        number_density:Quantity=None, mass_density:Quantity=None, volume:Quantity=None
    ):
        self.cols_matter = {
            "n":     Units.NUMBER_DENSITY, 
            "rho":   Units.MASS_DENSITY,
            "N":     None,
            "M":     Units.MATERIAL_MASS,
        }
        self.number_density = number_density
        self.mass_density = mass_density
        self.volume = volume

    def _norm(self):
      # setup densities of the composite
        if self.mass_density:
            self.mass_density.to(Units.MASS_DENSITY)
            self.number_density = (self.mass_density/self.composite_mass).to(Units.NUMBER_DENSITY)
        elif self.number_density: # !! number density of a composite, not sum of all its components
            self.mass_density = (self.number_density*self.composite_mass).to(Units.MASS_DENSITY)
            self.number_density.to(Units.NUMBER_DENSITY)
        if self.volume:
            self.mass = (self.mass_density * self.volume).to(Units.MATERIAL_MASS)
            
    def _print(self):
        print("Matter:")
        print("")
        if self.mass_density:
            print(f"Mass density:   {self.mass_density}")
            print(f"Number density: {self.number_density}")
            if self.volume:
                print(f"Volume:         {self.volume}")
                print(f"Mass:           {self.mass}")
        print("")
        self._print_table(self.cols_matter, self.data_matter)
        
    def data_matter(self, components:list=None, quantity:bool=True):
        def fn_row(s,m):
            values = {
                'proportion': m.proportion
            }
            if self.number_density:
                values['n']   = m.proportion*self.number_density
                values['rho'] = m.proportion*m.component_mass*self.number_density
            if self.volume:
                values['N'] = values['n']*self.volume
                values['M'] = values['rho']*self.volume
            return values
                # create a new copy of the column list and remove unused columns
        columns = dict(self.cols_matter) 
        if not self.mass_density:
            if 'n' in columns: del columns['n']
            if 'rho' in columns: del columns['rho']
        if not self.volume:
            if 'N' in columns and 'M' in columns: del columns['N']
            if 'M' in columns: del columns['M']
        return self._data(columns, fn_row, stats=True, weight=True, components=components, quantity=quantity)

    def print_matter(self, components:list=None):
        self._print_table(self.cols_matter, self.data_matter, components=components)
