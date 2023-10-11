from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

from ..environment import Environment
from ..settings import Order

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
        nodes = self.env.query("*", order=Order.NAME)
        
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
            node_parts = node.name.split(".")
            node_path = ".".join(node_parts[:-1])
            node_name = node_parts[-1]
            if node_path:
                node_path += "."
            p = Paragraph(f"{node_path}<font color='orange'>{node_name}</font>", style)
            story.append(p)
            story.append(Spacer(1,0.2*inch))
        doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)     

    def export2(self, file_path: str):
        #self.pdf.output(file_path, 'F')
        
        # Create a PDF document
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        
        # Create a table with nested cells
        data = [
            ["Header 1", "Header 2", "Header 3"],
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"],
        ]
        
        table = Table(data)
        
        # Apply table styles, including nested cell styles
        style = TableStyle([
            ('BACKGROUND', (0, 0), (2, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (2, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        table.setStyle(style)
        
        # Build and save the PDF document
        story = []
        story.append(table)
        doc.build(story)
