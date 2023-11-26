from reportlab.platypus import Paragraph, Table, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np
import re

from ..settings import *
from ....nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode, ModNode, ImportNode
from ....settings import Order, Sign, Keyword, EnvType, DocsType
from ....environment import Environment

class NodeSection:
    
    names: list
    nodes: list
    env: Environment
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, nodes, env):
        self.nodes = nodes
        self.names = list(self.nodes.keys())
        self.names.sort()
        self.env = env

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
            if isinstance(node.value.value, (np.ndarray, list)):
                self.value = str(node.value.value)
            else:
                self.value = str(int(node.value.value))
        if node.unsigned:
            self.dtype = f"u{self.dtype}"
        if node.precision:
            self.dtype = f"{self.dtype}{node.precision}"
            
    def _init_float(self, node):
        if node.units_raw:
            self.options = [f"{option.value.value} {option.value.unit}" for option in node.options]
        else:
            self.options = [f"{option.value.value}" for option in node.options]
        self.dtype = node.keyword
        if node.value:
            if isinstance(node.value.value, (np.ndarray, list)):
                self.value = str(node.value.value)
            else:
                exp = np.log10(node.value.value)
                if exp<=3 or exp>=-3:
                    self.value = f"{node.value.value:.03f}"
                else:
                    self.value = f"{node.value.value:.03e}"
        if node.precision:
            self.dtype = f"{self.dtype}{node.precision}"
            
    def _init_str(self, node):
        self.options = [str(option.value.value) for option in node.options]
        self.dtype = node.keyword
        if node.value:
            self.value = str(node.value.value)
            
    def _init_mod(self, node):
        self.value = node.value
        self.dtype = node.keyword
            
    def _init_node(self, node):
        # find out units
        self.unit = ''
        if node.keyword != ModNode.keyword and node.value and node.value.unit:
            self.unit = node.value.unit
        elif node.units_raw:
            self.unit = node.units_raw
            
        """
        parent = ".".join(node.name.split(".")[:-1])
        if m := re.match(f".*({Sign.CONDITION}[0-9]+)$", parent):
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
        # condition
        self.condition = None
        if node.condition:
            condition = node.condition.replace("{","<font color='orange'>{")
            condition = condition.replace("}","}</font>")
            self.condition = condition
        
        # type specific initialization
        self.value = None
        self.options = None
        getattr(self,f"_init_{node.keyword}")(node)
        if self.options:
            self.options = ", ".join(self.options)
        
        # additional settings
        self.injection = None
        if node.value_ref:
            self.injection = "<font color='orange'>{"+node.value_ref+"}</font>"
        if node.constant:
            self.dtype = f"constant {self.dtype}"
        self.dformat = node.format if node.keyword == StringNode.keyword else None
        if node.keyword == ModNode.keyword or node.tags is None:
            self.tags = ''
        else:
            self.tags = ", ".join(node.tags)
        self.description = None if node.keyword ==ModNode.keyword else node.description
    
    def parse_color(self, node):
        if DocsType.DEFINITION|DocsType.MODIFICATION in node.docs_type:
            self.color = PALETTE['def/mod']
        elif DocsType.DEFINITION in node.docs_type:
            self.color = PALETTE['def']
        elif DocsType.DECLARATION|DocsType.MODIFICATION in node.docs_type:
            self.color = PALETTE['dec/mod'] 
        elif DocsType.DECLARATION in node.docs_type:
            self.color = PALETTE['dec']
        elif DocsType.MODIFICATION in node.docs_type:
            self.color = PALETTE['mod']
            
    def parse_node(self, name, node):
    
        self._init_node(node)
    
        # define table style
        TABLE_STYLE = [
            # whole grid
            #('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod), 
            ('GRID',       (1,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('FONTNAME',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontName),
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontSize),
            # top panel
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_HEADER_STYLE.fontSize),
            ('TEXTCOLOR',  (0,0), (-1,0),   PALETTE['c4']),   
            ('BACKGROUND', (0,0), (-1,0),   PALETTE['node_name']),
            ('ALIGN',      (-2,0),(-1,0),   'RIGHT'),
            ('BACKGROUND', (1,1), (1,-1),   PALETTE['prop_name']),  
            ('BACKGROUND', (2,1), (-1,-1),  PALETTE['prop_value']),   
            ('SPAN',       (1,0), (2,0)     ),                            # parameter name
            ('BACKGROUND', (0,0), (0,-1),   self.color),                  # instance type
        ]
        
        # construct a node table
        pname = Paragraph(f"<strong>{name}</strong>", )
        source = Paragraph(f"<a href=\"#source_{node.source[0]}_{node.source[1]}\" color=\"blue\">{node.source[0]}:{node.source[1]}</a>")
        data = [
            ['', source, '', self.dtype],
        ]
        if self.value:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Value:', Paragraph(self.value, TABLE_BODY_STYLE)])
        if self.injection:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Injection:', Paragraph(self.injection, TABLE_BODY_STYLE)])
        if self.unit:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Default Unit:',  Paragraph(self.unit, TABLE_BODY_STYLE)])
        if self.condition:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Condition:',     Paragraph(self.condition, style=TABLE_BODY_STYLE)])
        if self.tags:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Tags:',          Paragraph(self.tags, TABLE_BODY_STYLE)])
        if self.options: 
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Options:',       Paragraph(self.options, TABLE_BODY_STYLE)])
        if self.dformat:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Format:',        Paragraph(self.dformat, TABLE_BODY_STYLE)])
        if self.description:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Description:',   Paragraph(self.description, TABLE_BODY_STYLE)])
            
        colWidths = list(np.array([0.01,0.2, 0.57, 0.22])*(PAGE_WIDTH-2*inch))
        return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)

    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"Parameter nodes", H2) )
        for name in self.names:
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(Paragraph(f"<strong>{name}</strong><a name=\"node_{name}\"></a>"))
            blocks.append(Spacer(1,0.1*inch))
            for node in self.nodes[name]:
                if node.keyword==ImportNode.keyword:
                    continue
                self.parse_color(node)
                blocks.append(self.parse_node(name, node))
        blocks.append(Spacer(1,0.2*inch))
        return blocks