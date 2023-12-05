from bs4 import BeautifulSoup
import json

from .settings import *
from ..item_parameter import ParType
from ..documentation import Documentation

class ParametersSection:
        
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
        
    def build_types(self):
        section = BeautifulSoup(Title("Node types"), features="html5lib")
        self.content.append(section)
        
        table = self.html.new_tag('table')
        for ptype in ParType:
            row = self.html.new_tag('tr')
            col = self.html.new_tag('td', **{'width': 20, 'style':'background-color:'+NTYPES[ptype.value][1]})
            col.string = ' '
            row.append(col)
            col = self.html.new_tag('td', **{'class':'pl-3'})
            col.string = NTYPES[ptype.value][0]
            row.append(col)
            table.append(row)
            
        self.content.append(table)
        
    def build_parameters(self):
        section = BeautifulSoup(Title("Parameter list"), features="html5lib")
        self.content.append(section)
            
        table = self.html.new_tag('table', **{'class':'table table-bordered'})
        row = self.html.new_tag('tr', **{'class':'thead-light'})
        col = self.html.new_tag('th', **{'class':'p-1'})
        col.string = "Property name"
        row.append(col)
        for ptype in range(len(ParType)):
            col = self.html.new_tag('th', **{'class':'p-1 text-center','style':'background-color:'+NTYPES[ptype][1]})
            col.string = "#"
            row.append(col)
        table.append(row)
        
        pnames = list(self.docs.parameters.keys())
        pnames.sort()
        for pname in pnames:
            pdata = self.docs.parameters[pname]
            row = self.html.new_tag('tr')
            col = self.html.new_tag('td', **{'class':'p-1'})
            col.string = pname
            row.append(col)
            for count in pdata.counts:
                col = self.html.new_tag('td', **{'class':'text-center p-1'})
                col.string = str(count) if count else ''
                row.append(col)
            table.append(row)
        self.content.append(table)

    def build_nodes(self):
        section = BeautifulSoup(Title("Parameter nodes"), features="html5lib")
        self.content.append(section)
        
        def add_property(pname, pvalue):
            props = self.html.new_tag('div', **{'class':'row'})
            name = self.html.new_tag('div', **{'class':'col-md-2 bg-light'})
            name.string = pname
            props.append(name)
            value = self.html.new_tag('div', **{'class':'col'})
            value.string = pvalue
            props.append(value)
            return props
        
        pnames = list(self.docs.parameters.keys())
        pnames.sort()
        for pname in pnames:
            pdata = self.docs.parameters[pname]
            param = self.html.new_tag("h6", **{'class':'mt-2'})
            param.string = pname
            self.content.append(param)
            
            for ndata in pdata.nodes:
                node = self.html.new_tag("div", **{'class':"container mt-2 border"})
                header = self.html.new_tag('div', **{'class':'row bg-light'})
                links = self.html.new_tag('div', **{'class':'col'})
                links.string = f"{ndata.source[0]}:{ndata.source[1]}"
                if ndata.injection:
                    links.string += " | injection"
                if ndata.imported:
                    links.string += " | import"
                header.append(links)
                dtype = self.html.new_tag('div', **{'class':'col-sm-3 text-right'})
                if ndata.constant:
                    dtype.string = "constant "+ndata.dtype
                else:
                    dtype.string = ndata.dtype
                header.append(dtype)
                node.append(header)
                
                if ndata.value:
                    node.append(add_property('Value:', ndata.value))
                if ndata.unit:
                    node.append(add_property('Unit:', ndata.unit))
                if ndata.condition:
                    node.append(add_property('Condition:', ndata.condition))
                if ndata.options:
                    node.append(add_property('Options:', ", ".join(ndata.options)))
                if ndata.tags:
                    node.append(add_property('Tags:', ", ".join(ndata.tags)))
                if ndata.dformat:
                    node.append(add_property('Format:', ndata.dformat))
                if ndata.description:
                    node.append(add_property('Description:', ndata.description))

                self.content.append(node)
            

    def build(self):
        
        section = self.html.new_tag("h1")
        section.append(BeautifulSoup(Title("Parameters"), 'html.parser'))
        self.content.append(section)
        
        self.build_types()
        
        self.build_parameters()
        
        self.build_nodes()
        
        self.container.div.div.append(self.content)
        self.html.body.append(self.container)
        
        with open(f"{self.dir_html}/parameters.html", "w") as file:
            file.write(str(self.html.prettify()))