import numpy as np
import os
import sys
sys.path.insert(0, os.environ['DIR_SOURCE'])

from scinumtools import RowCollector
from scinumtools.units import Dimensions
from scinumtools.units.settings import *
from scinumtools.units.unit_types import *
from scinumtools.dip import DIP
from scinumtools.dip.docs import *

def build_docs_pdf():
    
    # Generate a PDF documentation from a DIP file
    dir_pdf = os.environ['DIR_DOCS']+"/source/_static/pdf"
    file_definitions = f"{dir_pdf}/definitions.dip"
    file_cells = f"{dir_pdf}/cells.dip"
    file_pdf = f"{dir_pdf}/documentation.pdf"
    # Create directory if missing
    if not os.path.isdir(dir_pdf):
        os.mkdir(dir_pdf)
    # Create a DIP environment
    with DIP(name="PDF") as p:
        p.add_unit("velocity", 13, 'cm/s')
        p.add_string("""
        $unit length = 1 cm
        $unit mass = 2 g
        
        cfl_factor float = 0.7  # Courant–Friedrichs–Lewy condition
        max_vare float = 0.2    # maximum energy change of electrons
        max_vari float = 0.2    # maximum energy change of ions
        """)
        p.add_source("cells", file_cells)
        p.add_file(file_definitions)
        docs = p.parse_docs()    # Export parameters as a PDF
    with ExportDocsPDF(docs) as exp:
        exp.build(
            file_pdf, 
            "Example DIP documentation", 
            """In this document we want to demonstrate basic capabilities of a DIP documentation.<br/><br/>
            The documentation is structured into 3 main sections. The first section summarizes all parameters
            in a DIP code, as well as their corresponding node definitions, declarations, modifications and corresponding properties.
            Following section summarizes all references of injected values and lists imported nodes.
            The final section gives an overview of custom units and code sources.<br/><br/>
            Parameters, nodes, sections and many other items in this documentation are cross-linked between
            each other. All hyperlinks are denoted with a blue text.
        """)
    print(file_pdf)

def build_docs_html():
    
    # Generate a PDF documentation from a DIP file
    dir_docs = os.environ['DIR_DOCS']+"/source/_static/htmldocs"
    dir_docs_build = f"{dir_docs}/build"
    file_definitions = f"{dir_docs}/definitions.dip"
    file_cells = f"{dir_docs}/cells.dip"
    file_html = f"{dir_docs}/documentation.pdf"
    # Create directory if missing
    if not os.path.isdir(dir_docs_build):
        os.mkdir(dir_docs_build)
    if not os.path.isdir(dir_docs):
        os.mkdir(dir_docs)
    # Create a DIP environment
    with DIP(name="PDF") as p:
        p.add_unit("velocity", 13, 'cm/s')
        p.add_string("""
        $unit length = 1 cm
        $unit mass = 2 g
        
        cfl_factor float = 0.7  # Courant-Friedrichs-Lewy condition
        max_vare float = 0.2    # maximum energy change of electrons
        max_vari float = 0.2    # maximum energy change of ions
        """)
        p.add_source("cells", file_cells)
        p.add_file(file_definitions)
        docs = p.parse_docs()    # Export parameters as a PDF
    with ExportDocsHTML(docs) as exp:
        exp.build(
            dir_docs_build, 
            "Example DIP documentation", 
            """In this document we want to demonstrate basic capabilities of a DIP documentation.<br/><br/>
            The documentation is structured into 3 main sections. The first section summarizes all parameters
            in a DIP code, as well as their corresponding node definitions, declarations, modifications and corresponding properties.
            Following section summarizes all references of injected values and lists imported nodes.
            The final section gives an overview of custom units and code sources.<br/><br/>
            Parameters, nodes, sections and many other items in this documentation are cross-linked between
            each other. All hyperlinks are denoted with a blue text.
        """)
    print(dir_docs_build)

def build_docs_rst():
    
    # Generate a PDF documentation from a DIP file
    dir_docs = os.environ['DIR_DOCS']+"/source/dip/docs/rst"
    dir_docs_build = f"{dir_docs}/build"
    file_definitions = f"{dir_docs}/definitions.dip"
    file_cells = f"{dir_docs}/cells.dip"
    file_html = f"{dir_docs}/documentation.pdf"
    # Create directory if missing
    if not os.path.isdir(dir_docs_build):
        os.mkdir(dir_docs_build)
    if not os.path.isdir(dir_docs):
        os.mkdir(dir_docs)
    # Create a DIP environment
    with DIP(name="PDF") as p:
        p.add_unit("velocity", 13, 'cm/s')
        p.add_string("""
        $unit length = 1 cm
        $unit mass = 2 g
        
        cfl_factor float = 0.7  # Courant-Friedrichs-Lewy condition
        max_vare float = 0.2    # maximum energy change of electrons
        max_vari float = 0.2    # maximum energy change of ions
        """)
        p.add_source("cells", file_cells)
        p.add_file(file_definitions)
        docs = p.parse_docs()    # Export parameters as a PDF
    with ExportDocsRST(docs) as exp:
        exp.build(
            dir_docs_build, 
            "RST documentation", """
DIP package comes with an automatized RST export of parameters.
As an example, we use the same files as in HTML and PDF documentations.

Environment suitable for a documentation has to be parsed with a special method ``parse_docs()``, that processes node differently as the standard ``parse()`` method.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.docs import ExportDocsRST
   >>> with DIP() as p:
   >>>     p.add_file('definitions.dip')
   >>>     docs = p.parse_docs()
   >>> with ExportDocsRST(docs) as exp:
   >>>     exp.build(
   >>>         './build', 
   >>>         "Example DIP documentation", 
   >>>         "In this document we want to demonstrate basic capabilities of a DIP documentation..... "
   >>>     )

``ExportDocsRST`` class provided above can be used as it is, or as a template for your own personalized documentation.
When building your own documentation, you can simply take the `existing source code <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/docs/rst>`_ and modify it according to your needs.
RST code is generated using a custom `RST parser class <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/docs/rst/rst_parser.py>`_.

Code above will generate the following default RST documentation.
        """)
    print(dir_docs_build)