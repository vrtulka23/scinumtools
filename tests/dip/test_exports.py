import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.settings import Format
from scinumtools.dip.datatypes import FloatType, IntegerType, StringType, BooleanType
from scinumtools.dip.exports import ExportPDF

@pytest.fixture
def file_pdf():
    dir_tmp = "tmp"
    if not os.path.isdir(dir_tmp):
        os.mkdir(dir_tmp)
    file_pdf  = f"{dir_tmp}/docs_test.pdf"
    if os.path.isfile(file_pdf):
        os.remove(file_pdf)
    return file_pdf

@pytest.fixture
def file_definitions():
    return "examples/pdf_definitions.dip"

def test_export_pdf(file_pdf, file_definitions):
    with DIP(docs=True) as p:
        p.from_file(file_definitions)
        env = p.parse_docs()
    with ExportPDF(env) as exp:
        exp.export(file_pdf)
