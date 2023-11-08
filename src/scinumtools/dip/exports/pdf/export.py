from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, KeepTogether 
from reportlab.lib.units import inch
from reportlab.platypus.flowables import KeepTogether 
import numpy as np

from .settings import *
from .tmpl_node import NodeTemplate
from .tmpl_types import TypesTemplate
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
        
    def parse_parameters(self):
        blocks = []
        for name in self.names:
            p = Paragraph(f"<a href=\"#{name}\" color=\"blue\">{name}</a>")
            blocks.append(p)
            blocks.append(Spacer(1,0.02*inch))
        blocks.append(Spacer(1,0.2*inch))
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

        p = Paragraph(f"Instance types", SECTION_STYLE)        
        blocks.append(p)
        with TypesTemplate() as tmpl:
            blocks.append(tmpl.parse())    
        blocks.append(Spacer(1,0.2*inch))

        # list of all nodes
        p = Paragraph(f"Quick reference", SECTION_STYLE)
        blocks.append(p)
        blocks += self.parse_parameters()
        
        # collect all declarations and definitions
        p = Paragraph(f"Full node list", SECTION_STYLE)        
        blocks.append(p)
        parent_current = ''
        node_current = ''
        with NodeTemplate(self.env) as tmpl:
            for name in self.names:
                parent_new = ".".join(name.split(".")[:-1])
                if parent_new!=parent_current:
                    parent_current = parent_new
                    blocks.append(Spacer(1,0.1*inch))
                    blocks.append(Paragraph(f"<strong>{parent_new}</strong>"))
                blocks.append(Spacer(1,0.1*inch))
                blocks.append(Paragraph(f"<strong>{name}</strong><a name=\"{name}\"></a>"))
                blocks.append(Spacer(1,0.1*inch))
                for node in self.nodes[name]:
                    blocks.append(tmpl.parse(name, node))
        
        # build a documentation
        doc.build(blocks, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
