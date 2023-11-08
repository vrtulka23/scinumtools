import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP

def check_node(node, name, keyword, value):
    assert node.name == name
    assert node.keyword == keyword
    assert node.value.value == value

def test_definition_before_case():
    
    with DIP(docs=True) as p:
        p.from_string("""
        a int = 3        # definition
        @case false
          a float = 4.0  # modification
        @case true
          a str = "4.0"  # modification
        @else
          a bool = true  # modification
        a = 4            # modification
        """)
        env = p.parse_sphinx()
        assert len(env.nodes) == 1
        check_node(env.nodes[0], 'a', 'int', 3)
    
def test_branch_definition():

    # full definition in branch
    with DIP(docs=True) as p:
        p.from_string("""
        @case false
          a float = 4.0  # definition
        @case true
          a str = "4.0"  # definition
        @else
          a bool = true  # definition
        a = 4            # modification
        """)
        env = p.parse_sphinx()
        assert len(env.nodes) == 3
        check_node(env.nodes[0], '@1.a', 'float', 4.0)
        check_node(env.nodes[1], '@2.a', 'str',   "4.0")
        check_node(env.nodes[2], '@3.a', 'bool',  True)

def test_incomplete_case_definition():

    # definition in else case is missing
    with DIP(docs=True) as p:
        p.from_string("""
        @case true
          a float = 4.0  # definition
        a float = 3      # definition, or modification
        """)
        env = p.parse_sphinx()
        assert len(env.nodes) == 2
        check_node(env.nodes[0], '@1.a', 'float', 4.0)
        check_node(env.nodes[1], 'a',    'float', 3)

    # all but one branch has definition
    with DIP(docs=True) as p:
        p.from_string("""
        @case true
          b float = 4.0  
        @else
          a float = 5.0  # definition
        a float = 3      # modification
        """)
        env = p.parse_sphinx()
        assert len(env.nodes) == 3
        check_node(env.nodes[0], '@1.b', 'float', 4.0)
        check_node(env.nodes[1], '@2.a', 'float', 5.0)
        check_node(env.nodes[2], 'a',    'float', 3.0)

def test_nested_incomplete():

    # incomplete nested definition
    with DIP(docs=True) as p:
        p.from_string("""
        @case true
          @case true
            b float = 4.0  
          @else
            a float = 8.0  # definition
        @else
          a float = 5.0  # definition
        a float = 3      # modification
        """)
        env = p.parse_sphinx()
        assert len(env.nodes) == 4
        check_node(env.nodes[0], '@1.@2.b', 'float', 4.0)
        check_node(env.nodes[1], '@1.@3.a', 'float', 8.0)
        check_node(env.nodes[2], '@4.a',    'float', 5.0)
        check_node(env.nodes[3], 'a',       'float', 3.0)
