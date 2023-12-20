import json

from .settings import *
from .rst_parser import ParseRST
from ..item_parameter import ParType
from ..documentation import Documentation

class ParametersSection:
        
    docs: Documentation
    rst: ParseRST
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, docs: Documentation, **kwargs):
        self.docs = docs
        self.rst = ParseRST()

    def styles(self):
        return None
        
    def build_types(self):
        
        self.rst.title(1,'Node types')
        text = ""
        for ptype in ParType:
            text += f"| {ptype.name} - {NTYPES[ptype.value][0]}\n"
        self.rst.paragraph(text)
            
    def build_parameters(self):
        
        self.rst.title(1,'Parameter list')
        header = ['Property name']
        for ptype in ParType:
            th = str(ptype.name)
            header.append(f"{th}")
        data = [header]
        pnames = list(self.docs.parameters.keys())
        pnames.sort()
        for pname in pnames:
            pdata = self.docs.parameters[pname]
            row = [self.rst.link(pdata.target,pname)] + [c if c else '' for c in pdata.counts]
            data.append(row)
            
        self.rst.table_csv(data, **{'widths':'50 5 5 5 5 5 5 5', 'header-rows': 1})

    def build_nodes(self):
        
        self.rst.title(1,'Parameter nodes')
        
        pnames = list(self.docs.parameters.keys())
        pnames.sort()
        for pname in pnames:
            pdata = self.docs.parameters[pname]
            self.rst.target(pdata.target)
            self.rst.title(2, pname)
            for ndata in pdata.nodes:
                source = self.rst.link(ndata.link_source, f"{ndata.source[0]}:{ndata.source[1]}", source=True)
                if ndata.injection:
                    source += " | "+self.rst.link(ndata.link_injection,"injection")
                if ndata.imported:
                    source += " | "+self.rst.link(ndata.link_import,"import")
                ntype = str(list(ParType)[ndata.ntype].name)
                dtype = 'constant '+ndata.dtype if ndata.constant else ndata.dtype
                merge = [] 
                data = [[ntype,source,dtype]]
                if ndata.value:
                    merge.append((len(data),1,len(data),2))
                    data.append(['**Value:**', f"``{ndata.value}``", ''])
                if ndata.unit:
                    merge.append((len(data),1,len(data),2))
                    data.append(['**Unit:**', f"``{ndata.unit}``", ''])
                if ndata.condition:
                    merge.append((len(data),1,len(data),2))
                    data.append(['**Condition:**', f"``{ndata.condition}``", ''])
                if ndata.options:
                    merge.append((len(data),1,len(data),2))
                    data.append(['**Options:**', ", ".join(ndata.options), ''])
                if ndata.tags:
                    merge.append((len(data),1,len(data),2))
                    data.append(['**Tags:**', ", ".join(ndata.tags), ''])
                if ndata.dformat:
                    merge.append((len(data),1,len(data),2))
                    data.append(['**Format:**', f"``{ndata.dformat}``", ''])
                if ndata.description:
                    merge.append((len(data),1,len(data),2))
                    data.append(['**Description:**', ndata.description, ''])
                self.rst.target(ndata.target)
                self.rst.table(data, merge=merge, header=True)

    def build(self):
        
        self.build_types()
        
        self.build_parameters()
        
        self.build_nodes()

        return self.rst.parse()