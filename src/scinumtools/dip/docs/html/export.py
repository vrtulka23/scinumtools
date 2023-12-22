from bs4 import BeautifulSoup
import os

from .settings import *
from .section_parameters import ParametersSection
from .section_references import ReferencesSection
from .section_settings import SettingsSection
from ..documentation import Documentation

class ExportDocsHTML:
        
    docs: Documentation

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, docs: Documentation, **kwargs):
        self.docs = docs
        
    def build(self, dir_build: str, title: str, intro=None):

        sections = {
            "Parameters": {
                'filename':'parameters',
                'content':  ParametersSection,
                'sections': {
                    "types":"Node types",
                    "parameters":"Parameter list",
                    "nodes":"Parameter nodes"
                }
            },
            "References": {
                'filename':'references',
                'content':  ReferencesSection,
                'sections': {
                    "injections":"Injections",
                    "imports":"Imports"
                }
            },
            "Settings":   {
                'filename':'settings',
                'content':  SettingsSection,
                'sections': {
                    "units":"Units",
                    "sources":"Sources"
                }
            },
        }        
        
        # parse default layout
        
        file_layout = os.path.dirname(os.path.abspath(__file__))+'/layout.html'
        with open(file_layout, 'r', encoding='utf-8') as file:
            html = BeautifulSoup(file.read(), 'html.parser')
            html.find(id='title_docs').string = title
        
        # parse menu
        
        menu = html.find(id='menu')
        row = BeautifulSoup(f"<div><a href='./index.html'>Index</a></div>", 'html.parser')
        menu.append(row)

        for i2, (name, settings) in enumerate(sections.items()):
            
            row = BeautifulSoup(f"<div><a href='./{settings['filename']}.html#SECTION_{name}'>{name}</a></div>", 'html.parser')
            menu.append(row)
            
            sect = settings['sections'].items() if settings['sections'] else []
            for i3, (target,name3) in enumerate(sect):
                row = BeautifulSoup(f"<div class='row ps-4'><a href='./{settings['filename']}.html#SECTION_{name3}'>{name3}</a></div>", 'html.parser')
                menu.append(row)
    
        # parse index
    
        title = html.find(id='title_section')
        content = html.find(id='content')
        style = html.find(id='styles')

        title.append(BeautifulSoup(Title("Index"), 'html.parser')) 
        if intro:
            title.append(BeautifulSoup(Title('Introduction',3), 'html.parser'))
            paragraph = html.new_tag("p")
            paragraph.append(BeautifulSoup(intro, 'html.parser'))
            content.append(paragraph)
        
        with open(f"{dir_build}/index.html", "w") as file:
            file.write(str(html.prettify()))
        
        # parse sections
        
        for i2, (name, settings) in enumerate(sections.items()):
            content.clear()
            title.clear()
            style.string = ''
            title.append(BeautifulSoup(Title(name), 'html.parser'))
            with settings['content'](self.docs) as sect:
                if css := sect.styles():
                    style.string = css
                content.append(sect.build())
            with open(f"{dir_build}/{settings['filename']}.html", "w") as file:
                file.write(str(html.prettify()))
        