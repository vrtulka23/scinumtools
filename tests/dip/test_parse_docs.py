import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP

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
        env = p.parse_docs()
        assert len(env.nodes) == 1
        assert env.nodes[0].name == 'a'
        assert env.nodes[0].keyword == 'int'
        assert env.nodes[0].value.value == 3
    
def test_case_definition():
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
        env = p.parse_docs()
        assert len(env.nodes) == 3
        assert env.nodes[0].name == '@1.a'
        assert env.nodes[0].keyword == 'float'
        assert env.nodes[0].value.value == 4.0
        assert env.nodes[1].name == '@2.a'
        assert env.nodes[1].keyword == 'str'
        assert env.nodes[1].value.value == "4.0"
        assert env.nodes[2].name == '@3.a'
        assert env.nodes[2].keyword == 'bool'
        assert env.nodes[2].value.value == True

def test_incomplete_case_definition():
    with DIP(docs=True) as p:
        p.from_string("""
        @case true
          a float = 4.0  # definition
        a float = 3      # definition, or modification
        """)
        env = p.parse_docs()
        """
        assert len(env.nodes) == 2
        assert env.nodes[0].name == '@1.a'
        assert env.nodes[0].keyword == 'float'
        assert env.nodes[0].value.value == 4.0
        assert env.nodes[2].name == 'a'
        assert env.nodes[2].keyword == 'float'
        assert env.nodes[2].value.value == 3
        """
