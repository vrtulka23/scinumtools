import numpy as np
import re

NL = "\n"

class ParseRST:
    
    blocks: list
    
    def __init__(self):
        self.blocks = []

    def title(self, level:int, text:str, doc:bool=False):
        underscore = "=-~^"[level]
        if doc:
            text = underscore*len(text) + NL + text + NL + underscore*len(text)
        else:
            text = text + NL + underscore*len(text)
        self.blocks.append(text)
        
    def paragraph(self, text:str):
        #text = NL.join([line.strip() for line in text.split(NL)])
        self.blocks.append(text)
        
    def table_csv(self, data, **kwargs):
        text = ".. csv-table::"
        for key, value in kwargs.items():
            text += f"   :{key}: {value}" + NL
        text += NL+NL
        for row in data:
            text += "   " + ", ".join([f'"{col}"' for col in row]) + NL
        self.blocks.append(text)
        
    def table(self, data, **kwargs):
        # Calculate maximum column widths
        widths = np.zeros_like(data, dtype=int)
        for r,row in enumerate(data):
            widths[r] = [len(col)+2 for col in row]
        widths = widths.max(axis=0)
        # Construct table matrix
        shape = np.array(data).shape
        table = np.full((shape[0]*2+1, shape[1]*2+1), '', dtype=object)
        for r,row in enumerate(data):
            for c,col in enumerate(row):
                m, n = 1+r*2, 1+c*2
                table[m, n] = f" {col:{widths[c]-1}s}"
        # Create borders
        hcol = 1 if 'header' in kwargs and kwargs['header'] else -1
        for r,row in enumerate(data):
            for c,col in enumerate(row):
                ls = "=" if r==hcol else "-"
                table[r*2, 1+c*2] = ls*widths[c]
                table[r*2, c*2] = "+"
                table[1+r*2, c*2] = "|"
            table[r*2,-1] = "+"
            table[1+r*2,-1] = "|"
        r += 1
        for c,col in enumerate(row):
            table[r*2, 1+c*2] = '-'*widths[c]
            table[r*2, c*2] = "+"
        table[r*2,-1] = "+"
        # Merge cells
        if 'merge' in kwargs:
            for r0,c0,r1,c1 in kwargs['merge']:
                for r in range(1+r0*2,2+r1*2):
                    for c in range(1+c0*2,2+c1*2):
                        table[r,c] = ''
                w = sum([widths[w] for w in range(c0,1+c1)])
                w += c1-c0-1
                table[1+r0*2,1+c0*2] = f" {data[r0][c0]:{w}s}"
        # Create table text
        text = table.sum(axis=1)
        text = NL.join(text)
        self.blocks.append(text)
    
    def target(self, key:str):
        text = f".. _{key}:"
        self.blocks.append(text)
    
    def link(self, key:str, name:str, source:bool=False):
        if source:
            key = re.sub('_[0-9]+$', '', key)
        return f":ref:`{name}<{key}>`" 

    def code(self, code:str, language:str='', **kwargs):
        text = f".. code-block:: {language}" + NL
        for key, value in kwargs.items():
            if key in ['linenos']:
                text += f"   :{key}:" + NL
            else:
                text += f"   :{key}: {str(value)}" + NL
        text += NL
        text += "   "+code.replace(NL,f"{NL}   ")
        self.blocks.append(text)

    def toc(self, pages:list, **kwargs):
        text = ".. toctree::" + NL
        for key, value in kwargs.items():
            text += f"   :{key}: {str(value)}" + NL
        text += NL
        for page in pages:
            text += f"   {page}" + NL
        self.blocks.append(text)
        
    def parse(self):
        return (NL+NL).join(self.blocks)