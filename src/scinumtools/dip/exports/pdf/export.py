from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, KeepTogether, PageBreak
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.flowables import KeepTogether 
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, cm
import numpy as np

from .settings import *
from .sections.node import NodeSection
from .sections.injections import InjectionsSection
from .sections.imports import ImportsSection
from .sections.types import TypesSection
from .sections.parameters import ParametersSection
from .sections.units import UnitsSection
from .sections.sources import SourcesSection
from ...environment import Environment
from ...settings import Order, Sign, Keyword, EnvType, DocsType, DocsType
from ...lists import NodeList
from ...nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode, ModNode, ImportNode

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * cm, "Page %d " % (doc.page))
    canvas.restoreState()

class DocsTemplate(BaseDocTemplate):    
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1')], onPage=myLaterPages)
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))

class ExportPDF:
    
    env: Environment
    nodes: dict         # list of nodes grouped by name
    imports: list       # list of import nodes
    injections: list    # list of injected nodes
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
        self.injections = {}
        self.imports = []
        for node in nodes:
            if node.keyword==ImportNode.keyword:
                self.imports.append(node)
            else:
                name = node.clean_name()
                if name in self.nodes:
                    self.nodes[name].append(node)
                else:
                    self.nodes[name] = [node]
                if node.value_ref:
                    ref_source, ref_node = node.value_ref.split(Sign.QUERY)
                    if ref_source in self.env.sources:
                        inode = self.env.request(node.value_ref)[0]
                        inode.name = ref_node
                        iname = inode.clean_name()
                        if iname in self.injections:
                            self.injections[iname].append(inode)
                        else:
                            self.injections[iname] = [inode]
        
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

        blocks = []

        blocks.append(Paragraph(pageinfo, TITLE))
        
        toc = TableOfContents()
        toc.levelStyles = [
            ParagraphStyle(name='TOCHeading1', fontSize=16, leftIndent=20, firstLineIndent=-20, spaceBefore=10, leading=16, fontName='Times-Bold'),
            ParagraphStyle(name='TOCHeading2', fontSize=14, leftIndent=40, firstLineIndent=-20, spaceBefore=5, leading=12),
        ]
        blocks.append(toc)
    
    
        blocks.append(PageBreak())
        blocks.append(Paragraph(f"Parameters", H1))
        
        # list node types
        with TypesSection() as tmpl:
            blocks += tmpl.parse()    

        # create a quick reference of nodes with links
        with ParametersSection(self.nodes) as tmpl:
            blocks += tmpl.parse()
        
        blocks.append(PageBreak())

        # list all nodes and their properties
        with NodeSection(self.nodes, self.env) as tmpl:
            blocks += tmpl.parse()
            
        blocks.append(PageBreak())

        # list all injected nodes
        with InjectionsSection(self.injections, self.env) as tmpl:
            blocks += tmpl.parse()
            
        blocks.append(PageBreak())

        # list all imports
        with ImportsSection(self.imports, self.env) as tmpl:
            blocks += tmpl.parse()
            
        blocks.append(PageBreak())
        blocks.append(Paragraph(f"Settings", H1))
        
        # list units
        with UnitsSection(self.env) as tmpl:
            blocks += tmpl.parse()    
 
        # list sources
        blocks.append(PageBreak())
        with SourcesSection(self.env) as tmpl:
            blocks += tmpl.parse()    
 
        doc = DocsTemplate(file_path)
        doc.multiBuild(blocks)
            