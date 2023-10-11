from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from ..environment import Environment
from ..settings import Order, Sign

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
        
        nodes = self.env.nodes.query("*", order=Order.NAME)
        
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
        story = [Spacer(1,2*inch)]
        style = styles["Normal"]
        
        # Define a style for your title
        #title_style = getSampleStyleSheet()["Title"]
        #title_style.alignment = 1  # Center alignment
        #title = Paragraph('Title', style)
        #story.append(title)
        
        for node in nodes:
            node_parts = node.name.split(Sign.SEPARATOR)
            node_path = Sign.SEPARATOR.join(node_parts[:-1])
            node_name = node_parts[-1]
            if node_path:
                node_path += Sign.SEPARATOR
            p = Paragraph(f"{node_path}<font color='orange'>{node_name}</font>", style)
            story.append(p)
            story.append(Spacer(1,0.2*inch))
        doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)     
