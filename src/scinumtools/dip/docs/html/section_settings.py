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
from ..item_parameter import ParType
from ..documentation import Documentation
from ...settings import Sign, ROOT_SOURCE
from ...pygments import SyntaxLexer, StyleLexer

class SettingsSection:
        
    docs: Documentation
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, docs: Documentation, **kwargs):
        self.docs = docs
        self.html = BeautifulSoup(f"", 'html.parser')
                
    def highlight_python_code(self, code, target):
        # format text using pygments
        lexer = SyntaxLexer()
        style = StyleLexer

        # format text with a lexer
        formatter = get_formatter_by_name(
            'html', style=style, cssclass='pt-2 pb-2',
            linenos='inline', wrapcode=True, 
            prestyles='margin-bottom: 0',
            lineanchors=target
        ) 
        code = highlight(code, lexer, formatter)
        code = code.replace(f"{target}-",f"{target}_")
        #code = code.replace(f"linenos",f"")
        return code
        
    def styles(self):
        style = StyleLexer
        formatter = HtmlFormatter(style=style)
        css = formatter.get_style_defs()
        css += "\n .linenos {width:50px; display: inline-block; text-align:right; margin-right: 10px; border-right: 1px grey solid; user-select: none;}"
        return css
        
    def build_units(self):
        section = BeautifulSoup(Title("Units",3), 'html.parser')
        self.html.append(section)
        
        table = self.html.new_tag('table', **{'class':'table table-bordered'})
        row = self.html.new_tag('tr', **{'class':'thead-light'})
        names = ['Name','Value','Units','Source']
        for name in names:
            col = self.html.new_tag('th', **{'class':'p-1 bg-body-secondary'})
            col.string = name
            row.append(col)
        table.append(row)
        for unit in self.docs.units:
            row = self.html.new_tag('tr', **{'class':''})
            values = [unit.name, unit.value, unit.units]
            for value in values:
                col = self.html.new_tag('td', **{'class':'p-1'})
                col.string = value
                row.append(col)
            col = self.html.new_tag('td', **{'class':'p-1'})
            col.append(Link(PAGE_SOURCES,unit.link_source,f"{unit.source[0]}:{unit.source[1]}"))
            row.append(col)
            table.append(row)
        self.html.append(table)
        
    def build_sources(self):
        section = BeautifulSoup(Title("Sources",3), 'html.parser')
        self.html.append(section)
        
        for sdata in self.docs.sources:
            source = self.html.new_tag("div", **{'class':"container mt-2 border bg-white"})
            
            header = self.html.new_tag('div', **{'class':'row bg-dark-subtle'})
            name = self.html.new_tag('div', **{'class':'col'})
            name.append(Target(sdata.target, sdata.name))
            header.append(name)
            source.append(header)
            
            props = self.html.new_tag('div', **{'class':'row'})
            name = self.html.new_tag('div', **{'class':'col-2 bg-body-secondary'})
            name.string = 'File:'
            props.append(name)
            value = self.html.new_tag('div', **{'class':'col bg-white'})
            value.string = Path(sdata.path).name
            props.append(value)
            source.append(props)

            if sdata.parent:
                props = self.html.new_tag('div', **{'class':'row'})
                name = self.html.new_tag('div', **{'class':'col-2 bg-body-secondary'})
                name.string = 'Source:'
                props.append(name)
                value = self.html.new_tag('div', **{'class':'col bg-white'})
                value.append(Link(PAGE_SOURCES, sdata.link_source, f"{sdata.parent[0]}:{sdata.parent[1]}"))
                props.append(value)
                source.append(props)
            
            if sdata.code:
                code = self.highlight_python_code(sdata.code, sdata.target)
                code = BeautifulSoup(code, 'html.parser') 
                source.append(code)

            self.html.append(source)
        
    def build(self):
        
        self.build_units()
        
        self.build_sources()

        return self.html