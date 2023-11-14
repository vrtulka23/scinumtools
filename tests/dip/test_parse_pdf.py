import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.exports.pdf import ExportPDF

@pytest.fixture
def file_pdf():
    dir_tmp = "tmp" #docs/source/_static/pdf"
    if not os.path.isdir(dir_tmp):
        os.mkdir(dir_tmp)
    file_pdf  = f"{dir_tmp}/documentation.pdf"
    if os.path.isfile(file_pdf):
        os.remove(file_pdf)
    return file_pdf

@pytest.fixture
def file_definitions():
    return "../../docs/source/_static/pdf/definitions.dip"
    
@pytest.fixture
def file_cells():
    return "../../docs/source/_static/pdf/cells.dip"

def test_export_pdf(file_pdf, file_definitions, file_cells):
    with DIP() as p:
        p.add_unit("velocity", 13, 'cm/s')
        p.from_string("""
        $unit length = 1 cm
        $unit mass = 2 g
        
        cfl_factor float = 0.7  # Courant–Friedrichs–Lewy condition
        max_vare float = 0.2    # maximum energy change of electrons
        max_vari float = 0.2    # maximum energy change of ions
        """)
        p.add_source("cells", file_cells)
        p.from_file(file_definitions)
        env = p.parse_pdf()
    with ExportPDF(env) as exp:
        title = "Example documentation"
        pageinfo = "DIP Documentation"
        exp.build(file_pdf, title, pageinfo)

