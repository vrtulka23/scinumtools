from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

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
        style = styles["Normal"]
        
        # Define a style for your title
        #title_style = getSampleStyleSheet()["Title"]
        #title_style.alignment = 1  # Center alignment
        #title = Paragraph('Title', style)
        #blocks.append(title)
        
        def print_node(node, parent_name:str=''):
            if parent_name:
                name = f"{parent_name}{Sign.SEPARATOR}<font color='orange'>{node.name}</font>"
            else:
                name = f"<font color='orange'>{node.name}</font>"
            p = Paragraph(name, style)
            
            data = [[node.name, '', '02', '03', '04'],
                ['', '', '12', '13', '14'],
                ['20', '21', '22', node.description, ''],
                ['30', '31', '32', '', '']]
            t = Table(data,style=[
                ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                ('TEXTCOLOR',(0,0),(1,1),colors.palegreen),
                ('SPAN',(0,0),(1,1)),
                ('BACKGROUND',(-2,-2),(-1,-1), colors.pink),
                ('SPAN',(-2,-2),(-1,-1)),
            ])
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
                #blocks.append(Spacer(1,0.2*inch))
            if blocks:
                p = Paragraph(parent_name, style)
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
