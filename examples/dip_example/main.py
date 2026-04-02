import sys
sys.path.insert(1, '../../src')   # run with local SNT version
from scinumtools.dip import DIP, Format

with DIP() as dip:
    dip.add_source("settings", "settings.dip")  # add an external source
    dip.add_string("""                          # add some more DIP code
    system
      # import number of spheres
      {settings?box.num_spheres}
      # calculate mass in gramms
      total_mass float = (" {settings?sphere.mass} * {?system.num_spheres} ") g
    """)
    env = dip.parse()                 # parse DIP code
    data = env.data(Format.QUANTITY)  # extract parameters in a dictionary

print("Number of spheres:", data['system.num_spheres'])
print("Total mass:       ", data['system.total_mass'].to('kg'))  # convert to kg
