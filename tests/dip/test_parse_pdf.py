import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.exports import ExportPDF

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
    return "examples/pdf_definitions.dip"

def test_export_pdf(file_pdf, file_definitions):
    with DIP(docs=True) as p:
        p.from_file(file_definitions)
        env = p.parse_pdf()
    with ExportPDF(env) as exp:
        title = "Example documentation"
        pageinfo = "DIP Documentation"
        exp.build(file_pdf, title, pageinfo)

