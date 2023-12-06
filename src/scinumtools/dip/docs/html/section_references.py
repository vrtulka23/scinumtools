from bs4 import BeautifulSoup
import json

from .settings import *
from ..item_parameter import ParType
from ..documentation import Documentation

class ReferencesSection:
        
    docs: Documentation
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, docs: Documentation, dir_html: str, menu, **kwargs):
        self.docs = docs
        self.dir_html = dir_html
        
        self.html = BeautifulSoup("<html><head></head><body></body></html>", 'html.parser')
        style = self.html.new_tag("link", rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css", integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T", crossorigin="anonymous")
        self.html.head.append(style)
        
        self.container = BeautifulSoup(f"<div class='container'><div class='row'></div></div>", 'html.parser')
        self.content = self.html.new_tag("div", **{'class':"col"})
        
        self.container.div.div.append(menu)
        
    def build_injections(self):
        section = BeautifulSoup(Title("Injections"), features="html5lib")
        self.content.append(section)
        
        def add_prop(name, value, append=False):
            props = self.html.new_tag('div', **{'class':'row'})
            pname = self.html.new_tag('div', **{'class':'col-md-2 bg-light'})
            pname.string = name
            props.append(pname)
            pvalue = self.html.new_tag('div', **{'class':'col'})
            if append:
                pvalue.append(value)
            else:
                pvalue.string = value
            props.append(pvalue)
            return props
        
        for idata in self.docs.injections:
            item = self.html.new_tag("div", **{'class':"container mt-3 border"})
            
            header = self.html.new_tag('div', **{'class':'row bg-light'})
            name = self.html.new_tag('div', **{'class':'col'})
            name.append(Target(idata.target))
            name.append(Link(PAGE_SOURCES, idata.link_source, f"{idata.source[0]}:{idata.source[1]}"))
            header.append(name)
            item.append(header)
            
            item.append(add_prop('Injectiong node:', Link(PAGE_NODES,idata.link_node, idata.name), append=True))
            item.append(add_prop('Request:', "{"+idata.reference+"}"))
            if idata.isource:
                item.append(add_prop('From source:', f"{idata.isource[0]}:{idata.isource[1]}"))
            if idata.ivalue:
                item.append(add_prop('Value:', idata.ivalue))
            self.content.append(item)
        
    def build_imports(self):
        section = BeautifulSoup(Title("Imports"), 'html.parser')
        self.content.append(section)
        
        for idata in self.docs.imports:
            item = self.html.new_tag("div", **{'class':"container mt-3 border"})
            
            header = self.html.new_tag('div', **{'class':'row bg-light'})
            name = self.html.new_tag('div', **{'class':'col'})
            name.append(Target(idata.target))
            name.append(Link(PAGE_SOURCES,idata.link_source,f"{idata.source[0]}:{idata.source[1]}"))
            header.append(name)
            item.append(header)
            
            props = self.html.new_tag('div', **{'class':'row'})
            pname = self.html.new_tag('div', **{'class':'col-md-2 bg-light'})
            pname.string = 'Request:'
            props.append(pname)
            pvalue = self.html.new_tag('div', **{'class':'col'})
            pvalue.string = "{"+idata.reference+"}"
            props.append(pvalue)
            item.append(props)
            
            if idata.idata:
                props = self.html.new_tag('div', **{'class':'row'})
                pname = self.html.new_tag('div', **{'class':'col-6 bg-light'})
                pname.string = 'Imported node:'
                props.append(pname)
                pvalue = self.html.new_tag('div', **{'class':'col-6 bg-light'})
                pvalue.string = "From source:"
                props.append(pvalue)
                item.append(props)
            
            for inode in idata.idata:
                props = self.html.new_tag('div', **{'class':'row'})
                pname = self.html.new_tag('div', **{'class':'col-6'})
                pname.append(Link(PAGE_NODES, inode.link_node, inode.name))
                props.append(pname)
                pvalue = self.html.new_tag('div', **{'class':'col-6'})
                pvalue.append(Link(PAGE_SOURCES, inode.link_source, f"{inode.source[0]}:{inode.source[1]}"))
                props.append(pvalue)
                item.append(props)
            
            self.content.append(item)        
            
    def build(self):
        
        section = self.html.new_tag("h1")
        section.append(BeautifulSoup(Title("References"), 'html.parser'))
        self.content.append(section)
        
        self.build_injections()
        
        self.build_imports()

        self.container.div.div.append(self.content)  
        self.container.div.append(BeautifulSoup("<div class='p-3'> </div>", 'html.parser'))
        self.html.body.append(self.container)
        
        with open(f"{self.dir_html}/references.html", "w") as file:
            file.write(str(self.html.prettify()))