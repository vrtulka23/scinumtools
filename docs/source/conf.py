# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
sys.path.insert(0,"../../src")
import scinumtools

import toml
data = toml.load("../../pyproject.toml")

project = data['project']['name']
copyright = '2023, '+data['project']['authors'][0]['name']
author = data['project']['authors'][0]['name']
release = data['project']['version']
version = data['project']['version']

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'scinumtools.dip.docs.SphinxDocsClass',
    "sphinx.ext.autodoc", 
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/logo/dip_logo_64.png"
html_theme_options = {
    'logo_only': False,
    'display_version': True,
}
html_css_files = [
    'css/sphinxdoc.css'
]

# DIP Syntax Highlighter
from sphinx.highlighting import lexers
from scinumtools.dip.pygments.SyntaxLexerClass import SyntaxLexer
from scinumtools.dip.pygments.SchemaLexerClass import SchemaLexer
from scinumtools.dip.pygments.StyleLexerClass import StyleLexer, pygments_monkeypatch_style
pygments_monkeypatch_style("StyleLexer", StyleLexer)
pygments_style = 'StyleLexer'
lexers['DIP'] = SyntaxLexer(startinline=True, style=StyleLexer)
lexers['DIPSchema'] = SchemaLexer(startinline=True, style=StyleLexer)
