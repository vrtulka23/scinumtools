from bs4 import BeautifulSoup
import json

from .settings import *
from .rst_parser import ParseRST
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
        self.rst = ParseRST()
        
    def styles(self):
        return None
        
    def build_injections(self):
        
        self.rst.title(1,'Injections')
            
        for idata in self.docs.injections:
            data = [[self.rst.link(idata.link_source, f"{idata.source[0]}:{idata.source[1]}", source=True), '']]
            merge = [(0,0,0,1)]
            data.append(['**Injectiong node:**', self.rst.link(idata.link_node, idata.name)])
            data.append(['**Request:**', "``{"+idata.reference+"}``"])
            if idata.isource:
                data.append(['**From source:**', self.rst.link(idata.link_isource, f"{idata.isource[0]}:{idata.isource[1]}", source=True)])
            if idata.ivalue:
                data.append(['**Value:**', idata.ivalue])
            self.rst.target(idata.target)
            self.rst.table(data, merge=merge, header=True)
            
    def build_imports(self):
        
        self.rst.title(1,'Imports')
        
        for idata in self.docs.imports:
            
            data = [[self.rst.link(idata.link_source, f"{idata.source[0]}:{idata.source[1]}", source=True), '','']]
            data.append(['**Request:**', "``{"+idata.reference+"}``", ''])
            merge = [(0,0,0,2),(1,1,1,2)]
            if idata.idata:
                merge.append((len(data),0,len(data),1))
                data.append(['**Imported node:**', '', "**From source:**"])
                for inode in idata.idata:
                    merge.append((len(data),0,len(data),1))
                    data.append([
                        self.rst.link(inode.link_node, inode.name), 
                        '', 
                        self.rst.link(inode.link_source, f"{inode.source[0]}:{inode.source[1]}", source=True)
                    ])
            self.rst.target(idata.target)
            self.rst.table(data, merge=merge, header=True)
        """
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
        """
            
    def build(self):
        
        self.build_injections()
        
        self.build_imports()
        
        return self.rst.parse()