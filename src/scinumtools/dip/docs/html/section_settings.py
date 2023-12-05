from bs4 import BeautifulSoup
import json
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import get_formatter_by_name
from pygments.styles import get_style_by_name
from pygments.token import STANDARD_TYPES, Token
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
    
    def __init__(self, docs: Documentation, dir_html: str, menu, **kwargs):
        self.docs = docs
        self.dir_html = dir_html
        
        self.html = BeautifulSoup("<html><head></head><body></body></html>", features="html5lib")
        style = self.html.new_tag("link", rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css", integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T", crossorigin="anonymous")
        self.html.head.append(style)
        
        self.container = BeautifulSoup(f"<div class='container'><div class='row'></div></div>", features="html5lib")
        self.content = self.html.new_tag("div", **{'class':"col"})
        
        self.container.div.div.append(menu)
                
    def highlight_python_code(self, code, target):
        # format text using pygments
        lexer = SyntaxLexer()
        style = StyleLexer

        # format text with a lexer
        formatter = get_formatter_by_name('html', style=style, 
        linenos='inline', wrapcode=True, prestyles='margin-bottom: 0',
        lineanchors='SOURCE') 
        code = highlight(code, lexer, formatter)
        code = BeautifulSoup(code, features="html5lib")
        
        return code
        
    def build_units(self):
        section = BeautifulSoup(Title("Units"), features="html5lib")
        self.content.append(section)
        
        table = self.html.new_tag('table', **{'class':'table table-bordered'})
        row = self.html.new_tag('tr', **{'class':'thead-light'})
        names = ['Name','Value','Units','Source']
        for name in names:
            col = self.html.new_tag('th', **{'class':'p-1 bg-light'})
            col.string = name
            row.append(col)
        table.append(row)
        for unit in self.docs.units:
            row = self.html.new_tag('tr', **{'class':''})
            values = [unit.name, unit.value, unit.units, f"{unit.source[0]}:{unit.source[1]}"]
            for value in values:
                col = self.html.new_tag('th', **{'class':'p-1'})
                col.string = value
                row.append(col)
            table.append(row)
        self.content.append(table)
        
    def build_sources(self):
        section = BeautifulSoup(Title("Sources"), features="html5lib")
        self.content.append(section)
        
        for sdata in self.docs.sources:
            source = self.html.new_tag("div", **{'class':"container mt-2 border"})
            
            header = self.html.new_tag('div', **{'class':'row bg-light'})
            name = self.html.new_tag('div', **{'class':'col'})
            name.string = sdata.name
            header.append(name)
            source.append(header)
            
            props = self.html.new_tag('div', **{'class':'row'})
            name = self.html.new_tag('div', **{'class':'col-2 bg-light'})
            name.string = 'File:'
            props.append(name)
            value = self.html.new_tag('div', **{'class':'col'})
            value.string = Path(sdata.path).name
            props.append(value)
            source.append(props)

            if sdata.parent:
                props = self.html.new_tag('div', **{'class':'row'})
                name = self.html.new_tag('div', **{'class':'col-2 bg-light'})
                name.string = 'Source:'
                props.append(name)
                value = self.html.new_tag('div', **{'class':'col'})
                value.string = f"{sdata.parent[0]}:{sdata.parent[1]}"
                props.append(value)
                source.append(props)
            
            if sdata.code:
                code = self.highlight_python_code(sdata.code, sdata.target)
                source.append(code)

            self.content.append(source)
        
    def build(self):
        
        section = self.html.new_tag("h1")
        section.append(BeautifulSoup(Title("Settings"), 'html.parser'))
        self.content.append(section)
        
        self.build_units()
        
        self.build_sources()

        self.container.div.div.append(self.content)
        self.html.body.append(self.container)
        
        with open(f"{self.dir_html}/settings.html", "w") as file:
            file.write(str(self.html.prettify()))