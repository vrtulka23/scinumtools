import sys, os
sys.path.insert(0, os.environ['DIR_SOURCE'])

from scinumtools.units.settings import *
from scinumtools.units.unit_solver import UnitSolver
from scinumtools.units.base_units import BaseUnits

def build_unit_systems():

    text = [
        "#############################################",
        "# Do not modify this file!                  #",
        "# It is generated automatically in:         #",
        "# tools/generator/build_units.py            #",
        "#############################################",
        ""
        "QUANTITY_UNITS = {",
    ]
    symbols = []
    for q in range(len(QUANTITY_LIST)):
        name = QUANTITY_LIST.name[q]
        text.append(f"  # {name}")
        for system in ['SI','CGS','AU']:
            definition = getattr(QUANTITY_LIST,system)[q]
            if definition is None:
                continue
            else:
                symbol = QUANTITY_LIST.symbol[q]
                unitid = f"#{system[0]}{symbol}"
                atom = UnitSolver(definition)
                base = BaseUnits(atom.baseunits)
                c1 = f"{atom.magnitude*base.magnitude},"
                c2 = f"{base.dimensions.value()}"
                symbols.append(unitid)
                text.append(f"  '{unitid}': ({c1:25s}{c2:27s}), # {definition}") 
    text.append("}")
    text = "\n".join(text)
    
    # test if new symbols are unique
    try:
        assert len(np.unique(symbols)) == len(symbols)
    except:
        unique = np.unique(symbols)
        notunique = [s for s in unique if symbols.count(s)>1]
        raise Exception("Some units symbols are not unique:", notunique)
    
    # test if we produced a valid Python code
    exec(text)
    assert QUANTITY_UNITS
    
    # save the new version of the code
    path_units = os.environ['DIR_SOURCE']+"/scinumtools/units"
    path_list = f'{path_units}/unit_list.py'
    assert os.path.isdir(path_units)
    with open(path_list,'w') as f:
        f.write(text)
    print(path_list)