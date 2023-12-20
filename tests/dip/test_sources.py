import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')
from pathlib import Path
from inspect import getframeinfo, stack
from dataclasses import asdict

from scinumtools.dip import DIP
from scinumtools.dip.settings import ROOT_SOURCE, FILE_SOURCE, STRING_SOURCE

def test_root_source():
    
    with DIP() as dip:

        # test if root source is correct
        assert ROOT_SOURCE in dip.source[0]
        assert dip.source[0] in dip.env.sources
        rs = dip.env.sources[dip.source[0]]
        assert rs.path == __file__
        
def test_file_sources():
        
    with DIP() as dip:
        
        source_fa = f"{dip.name}_{FILE_SOURCE}1"
        source_fb = f"{dip.name}_{FILE_SOURCE}2"
        file_sources = {
            source_fa: dict(
                name   = source_fa,
                path   = str(Path(__file__).parent/"examples/source_fa.dip"),   # absoute path
                nodes  = None,
                sources = None,
            ),
            source_fb: dict(
                name   = source_fb,
                path   = "examples/source_fb.dip",   # relative path
                nodes  = None,
                sources = None,
            )
        }
        
        # import code from file
        dip.add_file(file_sources[source_fa]['path'])
        dip.add_file(file_sources[source_fb]['path'])
        
        # get the line numbers of the callings above
        caller = getframeinfo(stack()[0][0])
        file_sources[source_fa]['parent'] = (dip.source[0], caller.lineno-4)
        file_sources[source_fb]['parent'] = (dip.source[0], caller.lineno-3)
        
        # get code from files
        with open(file_sources[source_fa]['path'],'r') as f:  # absolute path
            file_sources[source_fa]['code'] = f.read()
        file_sources[source_fb]['path'] = str(Path(__file__).parent/file_sources[source_fb]['path'])
        with open(file_sources[source_fb]['path'],'r') as f:  # relative path
            file_sources[source_fb]['code'] = f.read()
    
        # test if file sources have correct data
        for source_name, match in file_sources.items():
            assert source_name in dip.env.sources
            assert asdict(dip.env.sources[source_name]) == match
    
        # test if nodes have correct sources and line numbers
        nodes = [
            ('runtime.timestep', source_fa,  3),
            ('size',             source_fb,  1),
        ]
        env = dip.parse()
        for name, source, lineno in nodes:
            node = env.nodes.query(name)[0]
            assert node.source == (source, lineno)

def test_string_sources():

    with DIP() as dip:
        
        source_sa = f"{dip.name}_{STRING_SOURCE}1"
        source_sb = f"{dip.name}_{STRING_SOURCE}2"
        string_sources = {
            source_sa: dict(
                name   = source_sa,
                path   = __file__,
                code   = """name str = 'John Smith'
                age int = 23""",
                nodes  = None,
                sources = None,
            ),
            source_sb: dict(
                name   = source_sb,
                path   = __file__,
                code   = """salary float = 60000""",
                nodes  = None,
                sources = None,
            ),
        }
        
        # import code from string
        dip.add_string(string_sources[source_sa]['code'])
        dip.add_string(string_sources[source_sb]['code'])
  
        # get the line numbers of the callings above
        caller = getframeinfo(stack()[0][0])
        string_sources[source_sa]['parent'] = (dip.source[0], caller.lineno-4)
        string_sources[source_sb]['parent'] = (dip.source[0], caller.lineno-3)

        
        # test if string sources have correct data
        for source_name, match in string_sources.items():
            assert source_name in dip.env.sources
            assert asdict(dip.env.sources[source_name]) == match
       
        # test if nodes have correct sources and line numbers
        nodes = [
            ('name',             source_sa,  1),
            ('salary',           source_sb,  1),
        ]
        env = dip.parse()
        for name, source, lineno in nodes:
            node = env.nodes.query(name)[0]
            assert node.source == (source, lineno)

def test_explicit_sources():
    
    with DIP() as dip:
        
        source_file = "examples/source_fa.dip"
        
        dip.add_source("explicit", source_file)   # explicitely added
        env = dip.parse()
        
        # get line number
        caller = getframeinfo(stack()[0][0])
        
        # read code from the source file
        source_path = str(Path(__file__).parent/source_file)
        with open(source_path,'r') as f:  # relative path
            source_code = f.read()

        # check the sources
        assert 'explicit' in env.sources
        source = env.sources['explicit']
        assert source.name == 'explicit'
        assert source.path == source_path
        assert source.code == source_code
        assert ROOT_SOURCE in source.parent[0]
        assert source.parent[1] == caller.lineno-4
        
        # test if nodes have correct sources and line numbers
        nodes = [
            ('explicit?runtime.timestep', 'explicit',  3),
        ]
        for name, source, lineno in nodes:
            node = env.request(name)[0]
            assert node.source == (source, lineno)

def test_inline_sources():
    
    with DIP() as dip:
        
        source_file = "examples/source_fa.dip"
        
        dip.add_string(f"""
        $source inline = {source_file}            # source added in code
        name str = 'John Smith'
        """)
        env = dip.parse()
        
        # read code from the source file
        source_path = str(Path(__file__).parent/source_file)
        with open(source_path,'r') as f:  # relative path
            source_code = f.read()

        # check the sources
        source_name = f"{dip.name}_{STRING_SOURCE}1"
        assert source_name in env.sources
        assert 'inline' in env.sources
        source = env.sources['inline']
        assert source.name == 'inline'
        assert source.path == source_path
        assert source.code == source_code
        assert source.parent == (source_name, 1)

        # test if nodes have correct sources and line numbers
        nodes = [
            ('inline?runtime.timestep', 'inline',  3),
        ]
        for name, source, lineno in nodes:
            node = env.request(name)[0]
            assert node.source == (source, lineno)