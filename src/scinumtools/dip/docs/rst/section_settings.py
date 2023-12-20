from bs4 import BeautifulSoup
import json
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import get_formatter_by_name
from pygments.styles import get_style_by_name
from pygments.token import STANDARD_TYPES, Token
from pygments.formatters import HtmlFormatter
import re

from .settings import *
from .rst_parser import ParseRST
from ..item_parameter import ParType
from ..documentation import Documentation
from ...settings import Sign, ROOT_SOURCE

class SettingsSection:
        
    docs: Documentation
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, docs: Documentation, **kwargs):
        self.docs = docs
        self.rst = ParseRST()
        
    def build_units(self):
        
        self.rst.title(1,'Units')
        
        data = [['Name','Value','Units','Source']]
        for unit in self.docs.units:
            data.append([
                unit.name, 
                f"``{unit.value}``", 
                f"``{unit.units}``", 
                self.rst.link(unit.link_source, f"{unit.source[0]}:{unit.source[1]}", source=True)
            ])
        self.rst.table(data, header=True)
        
    def build_sources(self):
        
        self.rst.title(1,'Sources')
        
        for sdata in self.docs.sources:
            
            if sdata.parent:
                data = [[sdata.name,'']]
            else:
                data = [[sdata.name,'']] 
            merge = [(0,0,0,1)]
        
            file_name = Path(sdata.path).name
            data.append(['File:',file_name])
        
            if sdata.parent:
                data.append(['Source:', self.rst.link(sdata.link_source, f"{sdata.parent[0]}:{sdata.parent[1]}", source=True)])
        
            self.rst.target(sdata.target)
            self.rst.table(data, merge=merge, header=True)
            
            if sdata.code:
                self.rst.code(sdata.code,'DIP',linenos=True,caption=file_name) #,name=sdata.target)
        
    def build(self):
        
        self.build_units()
        
        self.build_sources()
        
        return self.rst.parse()