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
    
    def __init__(self, docs: Documentation, **kwargs):
        self.docs = docs
        self.html = BeautifulSoup(f"", 'html.parser')
        
    def styles(self):
        return None
        
    def build_injections(self):
        section = BeautifulSoup(Title("Injections",3), 'html.parser')
        self.html.append(section)
        
        def add_prop(name, value, append=False):
            pname = self.html.new_tag('div', **{'class':'col-md-3 bg-body-secondary'})
            props = self.html.new_tag('div', **{'class':'row bg-white'})
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
            
            header = self.html.new_tag('div', **{'class':'row bg-dark-subtle'})
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
            self.html.append(item)
        
    def build_imports(self):
        section = BeautifulSoup(Title("Imports",3), 'html.parser')
        self.html.append(section)
        
        for idata in self.docs.imports:
            item = self.html.new_tag("div", **{'class':"container mt-3 border"})
            
            header = self.html.new_tag('div', **{'class':'row bg-dark-subtle'})
            name = self.html.new_tag('div', **{'class':'col'})
            name.append(Target(idata.target))
            name.append(Link(PAGE_SOURCES,idata.link_source,f"{idata.source[0]}:{idata.source[1]}"))
            header.append(name)
            item.append(header)
            
            props = self.html.new_tag('div', **{'class':'row'})
            pname = self.html.new_tag('div', **{'class':'col-md-2 bg-body-secondary'})
            pname.string = 'Request:'
            props.append(pname)
            pvalue = self.html.new_tag('div', **{'class':'col bg-white'})
            pvalue.string = "{"+idata.reference+"}"
            props.append(pvalue)
            item.append(props)
            
            if idata.idata:
                props = self.html.new_tag('div', **{'class':'row'})
                pname = self.html.new_tag('div', **{'class':'col-6 bg-body-secondary'})
                pname.string = 'Imported node:'
                props.append(pname)
                pvalue = self.html.new_tag('div', **{'class':'col-6 bg-body-secondary'})
                pvalue.string = "From source:"
                props.append(pvalue)
                item.append(props)
            
            for inode in idata.idata:
                props = self.html.new_tag('div', **{'class':'row'})
                pname = self.html.new_tag('div', **{'class':'col-6 bg-white'})
                pname.append(Link(PAGE_NODES, inode.link_node, inode.name))
                props.append(pname)
                pvalue = self.html.new_tag('div', **{'class':'col-6 bg-white'})
                pvalue.append(Link(PAGE_SOURCES, inode.link_source, f"{inode.source[0]}:{inode.source[1]}"))
                props.append(pvalue)
                item.append(props)
            
            self.html.append(item)        
            
    def build(self):
        
        self.build_injections()
        
        self.build_imports()

        return self.html