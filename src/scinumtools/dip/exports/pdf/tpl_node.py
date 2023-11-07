from reportlab.platypus import Paragraph, Table
from reportlab.lib.units import inch
import numpy as np
import re

from .settings import *
from ...nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode, ModNode
from ...settings import Order, Sign, Keyword, EnvType, DocsType

class NodeTemplate:
    
    name: str
    value: str
    unit: str
    dtype: str
    options: list
    dformat: str
    tags: list
    description: str
    condition: str
    color: str
    
    palette: list = {
        'dec/def':     '#fc9e4f',
        'dec/def/mod': '#edd382',
        'mod':         '#f2f3ae',
        'c4': colors.saddlebrown, #'#',
        'node_name': '#E7CCB1', #colors.navajowhite, 
        'prop_name': '#FAEDCD', #colors.antiquewhite, #'#',
        'prop_value': '#FEFAE0', #colors.floralwhite, #'#',
    }
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, name, node, env):
        # save name
        self.name = node.name
        
        # find out units
        self.unit = ''
        if node.keyword != ModNode.keyword and node.value and node.value.unit:
            self.unit = node.value.unit
        elif node.units_raw:
            self.unit = node.units_raw
            
        # condition
        """
        parent_name = ".".join(node.name.split(".")[:-1])
        if m := re.match(f".*({Sign.CONDITION}[0-9]+)$", parent_name):
            cid = m.group(1)
            case = env.branching.cases[m.group(1)]
            if case.expr is None:
                self.condition = None
            else:
                condition = case.expr.replace("{","<font color='orange'>{")
                condition = condition.replace("}","}</font>")
                self.condition = condition
        else:
            self.condition = None
        """
        self.condition = None
        if node.condition:
            condition = node.condition.replace("{","<font color='orange'>{")
            condition = condition.replace("}","}</font>")
            self.condition = condition
        
        # type specific initialization
        self.value = None
        self.options = None
        getattr(self,f"_init_{node.keyword}")(node)
        
        # additional settings
        if node.constant:
            self.dtype = f"constant {self.dtype}"
        self.dformat = node.format if node.keyword == StringNode.keyword else None
        if node.keyword == ModNode.keyword or node.tags is None:
            self.tags = ''
        else:
            self.tags = ", ".join(node.tags)
        self.description = None if node.keyword ==ModNode.keyword else node.description
        
        colors = {
        }
        if DocsType.DEFINITION in node.docs_type:
            if DocsType.MODIFICATION in node.docs_type:
                self.color = self.palette['dec/def/mod']
            else:
                self.color = self.palette['dec/def']
        elif DocsType.DECLARATION in node.docs_type:
            if DocsType.MODIFICATION in node.docs_type:
                self.color = self.palette['dec/def/mod']
            else:
                self.color = self.palette['dec/def']
        elif DocsType.MODIFICATION in node.docs_type:
            self.color = self.palette['mod']

    def _init_bool(self, node):
        self.dtype = node.keyword
        if node.value:
            self.value = Keyword.TRUE if node.value.value else Keyword.FALSE
            
    def _init_int(self, node):
        if node.units_raw:
            self.options = [f"{option.value.value} {option.value.unit}" for option in node.options]
        else:
            self.options = [f"{option.value.value}" for option in node.options]
        self.dtype = node.keyword
        if node.value:
            self.value = str(int(node.value.value))
            if node.value.unsigned:
                self.dtype = f"u{self.dtype}"
            if node.value.precision:
                self.dtype = f"{self.dtype}{node.value.precision}"
            
    def _init_float(self, node):
        if node.units_raw:
            self.options = [f"{option.value.value} {option.value.unit}" for option in node.options]
        else:
            self.options = [f"{option.value.value}" for option in node.options]
        self.dtype = node.keyword
        if node.value:
            exp = np.log10(node.value.value)
            if exp<=3 or exp>=-3:
                self.value = f"{node.value.value:.03f}"
            else:
                self.value = f"{node.value.value:.03e}"
            if node.value.precision:
                self.dtype = f"{self.dtype}{node.value.precision}"
            
    def _init_str(self, node):
        self.options = [str(option.value.value) for option in node.options]
        self.dtype = node.keyword
        if node.value:
            self.value = str(node.value.value)
            
    def _init_mod(self, node):
        self.value = node.value
        self.dtype = node.keyword
       
    @staticmethod
    def legend():       
        TABLE_STYLE = [
            ('BACKGROUND', (1,0), (1,0),   NodeTemplate.palette['dec/def']),  
            ('BACKGROUND', (1,1), (1,1),   NodeTemplate.palette['dec/def/mod']),  
            ('BACKGROUND', (1,2), (1,2),   NodeTemplate.palette['mod']),  
        ]
    
        data = [   
            ['','','Declaration / Definition'],
            ['','','Declaration / Definition / Modification'],
            ['','','Modification'],
        ]
        colWidths = list(np.array([0.015, 0.035,0.95])*(PAGE_WIDTH-2*inch))
        return Table(data, style=TABLE_STYLE, colWidths=colWidths)
            
    def parse(self):
    
        TABLE_STYLE = [
            # whole grid
            #('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod),
            ('FONTNAME',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontName),
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontSize),
            # top panel
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_HEADER_STYLE.fontSize),
            ('TEXTCOLOR',  (0,0), (-1,0),   self.palette['c4']),   
            ('BACKGROUND', (0,0), (-1,0),   self.palette['node_name']),
            ('ALIGN',      (-2,0),(-1,0),   'RIGHT'),
            ('BACKGROUND', (1,1), (1,-1),   self.palette['prop_name']),  
            ('BACKGROUND', (2,1), (-1,-1),  self.palette['prop_value']),   
            ('SPAN',       (1,0), (2,0)     ),                            # parameter name
            ('BACKGROUND', (0,0), (0,-1),   self.color),                  # instance type
        ]
        
        # construct a node table
        pname = Paragraph(f"<strong>{self.name}</strong>", )
        data = [
            ['', pname, '', self.dtype],
        ]
        if self.value:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Default value:', Paragraph(self.value, TABLE_BODY_STYLE)])
        if self.unit:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Default unit:', Paragraph(self.unit, TABLE_BODY_STYLE)])
        if self.condition:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Condition:', Paragraph(self.condition, style=TABLE_BODY_STYLE)])
        if self.tags:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Tags:', Paragraph(self.tags, TABLE_BODY_STYLE)])
        if self.options: 
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Options:', Paragraph(", ".join(self.options), TABLE_BODY_STYLE)])
        if self.dformat:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Format:', Paragraph(self.dformat, TABLE_BODY_STYLE)])
        if self.description:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Description:',Paragraph(self.description, TABLE_BODY_STYLE)])
            
        colWidths = list(np.array([0.01,0.2, 0.57, 0.22])*(PAGE_WIDTH-2*inch))
        return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
