from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, KeepTogether, PageBreak
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.flowables import KeepTogether 
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
import numpy as np
from dataclasses import dataclass

from .settings import *
from .sections.node import NodeSection
from .sections.injections import InjectionsSection
from .sections.imports import ImportsSection
from .sections.types import TypesSection
from .sections.parameters import ParametersSection
from .sections.units import UnitsSection
from .sections.sources import SourcesSection
from ...documentation import Documentation
from ...settings import Order, Sign, Keyword, EnvType, DocsType, DocsType
from ...lists import NodeList
from ...nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode, ModNode, ImportNode

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(2.5*cm, 2*cm, "Page %d " % (doc.page))
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
            text = AnchorLink(AnchorType.SECTION,flowable.getPlainText())
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))
                
class ExportPDF:
    
    docs: Documentation
    nodes: dict         # list of nodes grouped by name
    names: list         # sorted list of node names
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, docs: Documentation, **kwargs):
        if docs.env.envtype != EnvType.DOCS:
            raise Exception("Given environment is not a documentation environment")
        self.docs = docs
        
    def build(self, file_path: str, title, intro=None):

        blocks = []

        blocks.append(Paragraph(title, TITLE))
        
        blocks.append(Paragraph(AnchorTitle(AnchorType.SECTION,"Table of contents"), H0))
        
        toc = TableOfContents()
        toc.levelStyles = [
            ParagraphStyle(name='TOCHeading1', fontSize=16, leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16, fontName='Times-Bold'),
            ParagraphStyle(name='TOCHeading2', fontSize=14, leftIndent=40, firstLineIndent=-20, spaceBefore=5, leading=12),
        ]
        blocks.append(toc)
    
        if intro:
            blocks.append(PageBreak())
            blocks.append(Paragraph(AnchorTitle(AnchorType.SECTION,"Introduction"), H1))
            blocks.append(Paragraph(intro))
            blocks.append(Spacer(1,cm))
        
        blocks.append(PageBreak())
        blocks.append(Paragraph(AnchorTitle(AnchorType.SECTION,"Parameters"), H1))
        
        # list node types
        with TypesSection(self.docs.types) as tmpl:
            blocks += tmpl.parse()    

        # create a quick reference of nodes with links
        with ParametersSection(self.docs.parameters) as tmpl:
            blocks += tmpl.parse()
        
        blocks.append(PageBreak())

        # list all nodes and their properties
        with NodeSection(self.docs.parameters) as tmpl:
            blocks += tmpl.parse()
            
        blocks.append(PageBreak())
        blocks.append(Paragraph(AnchorTitle(AnchorType.SECTION,"References"), H1))

        # list all injected nodes
        with InjectionsSection(self.docs.injections) as tmpl:
            blocks += tmpl.parse()
            
        blocks.append(PageBreak())

        # list all imports
        with ImportsSection(self.docs.imports) as tmpl:
            blocks += tmpl.parse()
            
        blocks.append(PageBreak())
        blocks.append(Paragraph(AnchorTitle(AnchorType.SECTION,"Settings"), H1))
        
        # list units
        with UnitsSection(self.docs.units) as tmpl:
            blocks += tmpl.parse()    
 
        # list sources
        blocks.append(PageBreak())
        with SourcesSection(self.docs.sources) as tmpl:
            blocks += tmpl.parse()    
 
        doc = DocsTemplate(file_path)
        doc.multiBuild(blocks)
            