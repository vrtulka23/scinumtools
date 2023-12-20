# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
sys.path.insert(0,"../../src")              # import recent version of scinumtools
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
    'sphinx.ext.autosectionlabel',
    "sphinx.ext.autodoc", 
    'sphinx_rtd_theme',
    'sphinx_simplepdf',
]
autosectionlabel_prefix_document = True  # Make sure the target is unique
templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/snt/snt.svg"
html_theme_options = {
    'logo_only': False,
    'display_version': True,
}
html_css_files = [
    'css/sphinxdoc.css'
]

# DIP Syntax Highlighter
from sphinx.highlighting import lexers
from scinumtools.dip.pygments import SyntaxLexer, SchemaLexer, StyleLexer, pygments_monkeypatch_style
pygments_monkeypatch_style("StyleLexer", StyleLexer)
pygments_style = 'StyleLexer'
lexers['DIP'] = SyntaxLexer(startinline=True, style=StyleLexer)
lexers['DIPSchema'] = SchemaLexer(startinline=True, style=StyleLexer)
