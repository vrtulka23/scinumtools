from bs4 import BeautifulSoup

from ..documentation import Documentation
from .section_parameters import ParametersSection
from .section_references import ReferencesSection
from .section_settings import SettingsSection

class ExportHTML:
        
    docs: Documentation
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, docs: Documentation, **kwargs):
        self.docs = docs
        
    def build(self, dir_html: str, title: str, intro=None):
        
        html = BeautifulSoup("<html><head></head><body></body></html>", features="html5lib")
        
        style = html.new_tag("link", rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css", integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T", crossorigin="anonymous")
        html.head.append(style)
        
        meta = html.new_tag("meta", charset="UTF-8")
        html.head.append(meta)
        
        container = BeautifulSoup(f"<div class='container'><div class='row'></div></div>", features="html5lib")
        menu = html.new_tag("div", **{'class':'col-xs'})
        content = html.new_tag("div", **{'class':"col"})
        
        section = html.new_tag("h1")
        section.string = title
        content.append(section)
        
        section = html.new_tag("h3")
        section.string = "Table of contents"
        menu.append(section)
        
        sections = {
            "Parameters": {
                'filename':'parameters.html',
                'sections': {
                    "types":"Node types",
                    "parameters":"Parameter list",
                    "nodes":"Parameter nodes"
                }
            },
            "References": {
                'filename':'references.html',
                'sections': {
                    "injections":"Injections",
                    "imports":"Imports"
                }
            },
            "Settings":   {
                'filename':'settings.html',
                'sections': {
                    "units":"Units",
                    "sources":"Sources"
                }
            },
        }
        if intro:
            row = BeautifulSoup(f"<div><a href='./index.html'>Introduction</a></div>", features="html5lib")
            menu.append(row)
        for i2, (name2, settings2) in enumerate(sections.items()):
            row = BeautifulSoup(f"<div><a href='./{settings2['filename']}#SECTION_{name2}'>{name2}</a></div>", features="html5lib")
            menu.append(row)
            for i3, (target,name3) in enumerate(settings2['sections'].items()):
                row = BeautifulSoup(f"<div class='row pl-4'><a href='./{settings2['filename']}#SECTION_{name3}'>{name3}</a></div>", features="html5lib")
                menu.append(row)
        
        if intro:
            section = html.new_tag("h2")
            section.string = "Introduction"
            content.append(section)
            paragraph = html.new_tag("p")
            paragraph.append(BeautifulSoup(intro, features="html5lib"))
            content.append(paragraph)
            
        container.div.div.append(menu)
        container.div.div.append(content)
        html.body.append(container)
        
        with open(f"{dir_html}/index.html", "w") as file:
            file.write(str(html.prettify()))
            
        with ParametersSection(self.docs, dir_html, menu) as sect:
            sect.build()
            
        with ReferencesSection(self.docs, dir_html, menu) as sect:
            sect.build()
            
        with SettingsSection(self.docs, dir_html, menu) as sect:
            sect.build()