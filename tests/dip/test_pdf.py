import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.settings import Format
from scinumtools.dip.datatypes import FloatType, IntegerType, StringType, BooleanType
from scinumtools.dip.exports import ExportPDF

def test_logical():
    with DIP() as p:
        p.from_file("examples/definitions.dip")
        env = p.parse()
    with ExportPDF(env) as exp:
        exp.export("tests/dip/tmp/docs_test.pdf")
