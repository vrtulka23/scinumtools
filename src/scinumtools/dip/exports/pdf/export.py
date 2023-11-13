from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, KeepTogether 
from reportlab.lib.units import inch
from reportlab.platypus.flowables import KeepTogether 
import numpy as np

from .settings import *
from .sections.node import NodeSection
from .sections.types import TypesSection
from .sections.reference import ReferenceSection
from .sections.units import UnitsSection
from .sections.sources import SourcesSection
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

        # list node types
        with TypesSection() as tmpl:
            blocks += tmpl.parse()    

        # create a quick reference of nodes with links
        with ReferenceSection(self.names, self.nodes) as tmpl:
            blocks += tmpl.parse()
        
        # list all nodes and their properties
        with NodeSection(self.names, self.nodes, self.env) as tmpl:
            blocks += tmpl.parse()
 
        # list units
        with UnitsSection(self.env) as tmpl:
            blocks += tmpl.parse()    
 
        # list sources
        with SourcesSection(self.env) as tmpl:
            blocks += tmpl.parse()    
 
        # build a documentation
        doc.build(blocks, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
