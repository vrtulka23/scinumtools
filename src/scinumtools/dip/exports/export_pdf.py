from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
import numpy as np

from ..environment import Environment
from ..settings import Order, Sign
from ..lists import NodeList
from ..nodes import Node

class ExportPDF:
    
    env: Environment
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, env: Environment, **kwargs):
        self.env = env
        
    def export(self, file_path: str):
        
        PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
        styles = getSampleStyleSheet()
        title = "DIP Documentation"
        pageinfo = "DIP Documentation"
        
        
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
        style = ParagraphStyle(
            "CustomStyle",
            parent=styles["Normal"],
            spaceBefore=5, 
            spaceAfter=5,  # Add 20 points of space after the paragraph
        )
        
        # Define a style for your title
        #title_style = getSampleStyleSheet()["Title"]
        #title_style.alignment = 1  # Center alignment
        #title = Paragraph('Title', style)
        #blocks.append(title)

        def prepare_values(node):
            unit = ''
            if node.value and node.value.unit:
                unit = node.value.unit
            elif node.units_raw:
                unit = node.units_raw
            value = ''
            if node.dtype == int:
                dtype = 'int'
                if node.value:
                    value = str(int(node.value.value))
            elif node.dtype == float:
                dtype = 'float'
                if node.value:
                    exp = np.log10(node.value.value)
                    if exp<=3 or exp>=-3:
                        value = f"{node.value.value:.03f}"
                    else:
                        value = f"{node.value.value:.03e}"
            elif node.dtype == bool:
                dtype = 'bool'
                if node.value:
                    value = 'true' if node.value.value else 'false'
            elif node.dtype == str:
                dtype = 'str'
                if node.value:
                    value = str(node.value.value)
            return dtype, value, unit
        
        def print_node(node, parent_name:str=''):
            #if parent_name:
            #    name = f"{parent_name}{Sign.SEPARATOR}<font color='orange'>{node.name}</font>"
            #else:
            #    name = f"<font color='orange'>{node.name}</font>"
            name = f"<strong>{node.name}</strong>"
            const = "const" if node.constant else ""
            p = Paragraph(name, style)
            dtype, value, unit = prepare_values(node)
            data = [
                [p, '', dtype, const, value, unit],
                ['Description:', node.description, '', '', '', '']
            ]
            if node.condition:
                condition = node.condition
                condition = condition.replace("{","<font color='orange'>{")
                condition = condition.replace("}","}</font>")
                #print(condition)
                condition = Paragraph(condition, style=ParagraphStyle(
                    "CustomStyle",
                    parent=styles["Normal"],
                    fontSize=8,
                ))
                data.append(['Condition:', condition, '', '', '', ''])
            colWidths = list(np.array([0.2, 0.2, 0.1, 0.1, 0.2, 0.2])*(PAGE_WIDTH-2*inch))
            t = Table(data,style=[
                ('GRID',(0,0),(-1,-1),0.5,    colors.goldenrod),
                ('TEXTCOLOR',(0,0),(-1,0),   colors.saddlebrown),
                ('SPAN',(0,0),(1,0)),
                ('SPAN',(1,1),(-1,1)),
                ('SPAN',(1,2),(-1,2)),
                ('BACKGROUND',(0,0),(-1,0),  colors.navajowhite),
                ('BACKGROUND',(0,1),(0,-1),  colors.antiquewhite),
                ('BACKGROUND',(1,1),(-1,-1), colors.floralwhite),
                ('FONTSIZE',(0,1),(-1,-1),   8),
                #('SPAN',(-2,-2),(-1,-1)),
            ], hAlign='LEFT', colWidths=colWidths)
            return t

        def collect_blocks(nodes, parent_name:str=''):
            blocks = []
            for group_name in nodes.keys():
                if parent_name:
                    group_path = f"{parent_name}{Sign.SEPARATOR}{group_name}"
                else:
                    group_path = group_name
                child = nodes[group_name]
                if isinstance(child, NodeList) and len(child):
                    blocks += collect_blocks(child, group_path)
                elif isinstance(child, Node):
                    blocks.append(print_node(child, parent_name))
                    blocks.append(Spacer(inch, inch/12))
                #blocks.append(Spacer(1,0.2*inch))
            if blocks:
                p = Paragraph(f"<strong>{parent_name}</strong>", style)
                blocks.insert(0, p)
            return blocks
            
        for block in collect_blocks(self.env.nodes):
            blocks.append(block)
            
        """
        for node in nodes:
            node_parts = node.name.split(Sign.SEPARATOR)
            node_path = Sign.SEPARATOR.join(node_parts[:-1])
            node_name = node_parts[-1]
            if node_path:
                node_path += Sign.SEPARATOR
            p = Paragraph(f"{node_path}<font color='orange'>{node_name}</font>", style)
            blocks.append(p)
            blocks.append(Spacer(1,0.2*inch))
        """
        doc.build(blocks, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
