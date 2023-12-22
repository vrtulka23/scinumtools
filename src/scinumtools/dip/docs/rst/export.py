import os

from .settings import *
from .rst_parser import ParseRST
from .section_parameters import ParametersSection
from .section_references import ReferencesSection
from .section_settings import SettingsSection
from ..documentation import Documentation

class ExportDocsRST:
        
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
        
        # parse index page

        rst = ParseRST()
        rst.title(0, title)
        
        if intro:
            rst.paragraph(intro)
        
        pages = [values['filename'] for key, values in sections.items()]
        rst.toc(pages, maxdepth=2, caption="Contents")
        
        with open(f"{dir_build}/index.rst", "w") as file:
            file.write(rst.parse())

        for name, settings in sections.items():
            with settings['content'](self.docs) as section:
                section.rst.title(0, name)
                with open(f"{dir_build}/{settings['filename']}.rst", "w") as file:
                    file.write(section.build())
