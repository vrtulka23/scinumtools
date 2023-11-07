from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, KeepTogether 
from reportlab.lib.units import inch
from reportlab.platypus.flowables import KeepTogether 
import numpy as np

from .settings import *
from .tpl_node import NodeTemplate
from ...environment import Environment
from ...settings import Order, Sign, Keyword, EnvType, DocsType
from ...lists import NodeList
from ...nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode, ModNode

class ExportPDF:
    
    env: Environment
    nodes: dict         # list of nodes grouped by name
    names: list         # sorted list of node names
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, env: Environment, **kwargs):
        if env.envtype != EnvType.DOCS:
            raise Exception("Given environment is not a documentation environment")
        self.env = env
        
        # group nodes according to their names
        nodes = self.env.nodes.query("*")
        self.nodes = {}
        for node in nodes:
            name = node.clean_name()
            if name in self.nodes:
                self.nodes[name].append(node)
            else:
                self.nodes[name] = [node]

        # create a sorted list of node names
        self.names = list(self.nodes.keys())
        self.names.sort()
        
    def parse_instances(self, name):
        blocks = []
        #blocks.append(Paragraph(f"<strong>{name}</strong>"))
        blocks.append(Paragraph(f"<a name=\"{name}\"></a>"))
        for node in self.nodes[name]:
            with NodeTemplate(name, node, self.env) as nt:
                blocks.append(nt.parse())
        #blocks.append(Spacer(1,0.05*inch))
        return blocks
        
    def parse_groups(self):
        blocks = []
        parent_current = ''
        node_current = ''
        for name in self.names:
            parent_new = ".".join(name.split(".")[:-1])
            if parent_new!=parent_current:
                parent_current = parent_new
                blocks.append(Spacer(1,0.2*inch))
                blocks.append(Paragraph(f"<strong>{parent_new}</strong>"))
            blocks += self.parse_instances(name)
        return blocks
        
    def build(self, file_path: str, title, pageinfo):
        
        def myFirstPage(canvas, doc):
            canvas.saveState()
            canvas.setFont('Times-Bold',16)
            canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, title)
            canvas.setFont('Times-Roman',9)
            canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
            canvas.restoreState()
            
        def myLaterPages(canvas, doc):
            canvas.saveState()
            canvas.setFont('Times-Roman',9)
            canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
            canvas.restoreState()

        doc = SimpleDocTemplate(file_path)
        blocks = [Spacer(1,1*inch)]

        # list of all nodes
        p = Paragraph(f"Parameter list", SECTION_STYLE)
        blocks.append(p)
        for name in self.names:
            p = Paragraph(f"<a href=\"#{name}\" color=\"blue\">{name}</a>")
            blocks.append(p)
            blocks.append(Spacer(1,0.02*inch))
        blocks.append(Spacer(1,0.2*inch))
        
        # collect all declarations and definitions
        p = Paragraph(f"Node list", SECTION_STYLE)        
        blocks.append(p)
        blocks.append(NodeTemplate.legend())
        #blocks.append(Spacer(1,0.2*inch))
        blocks += self.parse_groups()
        #blocks.append(Spacer(1,0.2*inch))
        
        # build a documentation
        doc.build(blocks, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
