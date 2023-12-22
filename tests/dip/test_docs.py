import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.docs import ExportDocsPDF
from scinumtools.dip.docs.settings import DocsType
from scinumtools.dip.docs.item_parameter import ParType

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
        p.add_string("""
        $unit length = 1 cm
        $unit mass = 2 g
        
        cfl_factor float = 0.7  # Courant–Friedrichs–Lewy condition
        max_vare float = 0.2    # maximum energy change of electrons
        max_vari float = 0.2    # maximum energy change of ions
        """)
        p.add_source("cells", file_cells)
        p.add_file(file_definitions)
        docs = p.parse_docs()
    with ExportDocsPDF(docs) as exp:
        title = "Example documentation"
        pageinfo = "DIP Documentation"
        exp.build(file_pdf, title, pageinfo)


def check_node(node, name, keyword, value):
    assert node.name == name
    assert node.keyword == keyword
    assert node.value.value == value

def test_definition_before_case():
    
    with DIP(docs=True) as p:
        p.add_string("""
        a int = 3        # definition
        @case false
          a float = 4.0  # modification
        @case true
          a str = "4.0"  # modification
        @else
          a bool = true  # modification
        a = 4            # modification
        """)
        docs = p.parse_docs()
        assert len(docs.env.nodes) == 5
        check_node(docs.env.nodes[0], 'a', 'int', 3)
        
        assert 'a' in docs.parameters
        nodes = docs.parameters['a'].nodes
        assert nodes[0].ntype == ParType.DEF.value
        assert nodes[1].ntype == ParType.MOD.value
        assert nodes[2].ntype == ParType.MOD.value
        assert nodes[3].ntype == ParType.MOD.value
        assert nodes[4].ntype == ParType.MOD.value
    
def test_branch_definition():

    # full definition in branch
    with DIP(docs=True) as p:
        p.add_string("""
        @case false
          a float = 4.0  # definition
        @case true
          a str = "4.0"  # definition
        @else
          a bool = true  # definition
        a = 4            # modification
        """)
        docs = p.parse_docs()
        assert len(docs.env.nodes) == 4
        check_node(docs.env.nodes[0], '@1.a', 'float', 4.0)
        check_node(docs.env.nodes[1], '@2.a', 'str',   "4.0")
        check_node(docs.env.nodes[2], '@3.a', 'bool',  True)
        
        assert 'a' in docs.parameters
        nodes = docs.parameters['a'].nodes
        assert nodes[0].ntype == ParType.DEF.value
        assert nodes[1].ntype == ParType.DEF.value
        assert nodes[2].ntype == ParType.DEF.value
        assert nodes[3].ntype == ParType.MOD.value

def test_incomplete_case_definition():

    # definition in else case is missing
    with DIP(docs=True) as p:
        p.add_string("""
        @case true
          a float = 4.0  # definition
        a float = 3      # definition, or modification
        """)
        docs = p.parse_docs()
        assert len(docs.env.nodes) == 2
        check_node(docs.env.nodes[0], '@1.a', 'float', 4.0)
        check_node(docs.env.nodes[1], 'a',    'float', 3)

    # all but one branch has definition
    with DIP(docs=True) as p:
        p.add_string("""
        @case true
          b float = 4.0  
        @else
          a float = 5.0  # definition
        a float = 3      # modification
        """)
        docs = p.parse_docs()
        assert len(docs.env.nodes) == 3
        check_node(docs.env.nodes[0], '@1.b', 'float', 4.0)
        check_node(docs.env.nodes[1], '@2.a', 'float', 5.0)
        check_node(docs.env.nodes[2], 'a',    'float', 3.0)

def test_nested_incomplete():

    # incomplete nested definition
    with DIP(docs=True) as p:
        p.add_string("""
        @case true
          @case true
            b float = 4.0  
          @else
            a float = 8.0  # definition
        @else
          a float = 5.0  # definition
        a float = 3      # modification
        """)
        docs = p.parse_docs()
        assert len(docs.env.nodes) == 4
        check_node(docs.env.nodes[0], '@1.@2.b', 'float', 4.0)
        check_node(docs.env.nodes[1], '@1.@3.a', 'float', 8.0)
        check_node(docs.env.nodes[2], '@4.a',    'float', 5.0)
        check_node(docs.env.nodes[3], 'a',       'float', 3.0)
