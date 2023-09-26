import os
import sphinx
import pathlib
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from inspect import getframeinfo, stack
import collections

from ..dip import DIP
from ..source import Source
from ..settings import Format
from ..datatypes import NumberType
from ..nodes import IntegerNode, StringNode, FloatNode

class SphinxDocs(Directive):

    has_content = True

    option_spec = {
        'show-code': directives.flag,
    }
    
    def run(self):

        # We are calling this script from a Sphinx base directory,
        # so DIP file paths are defined relative to it.
        source = Source(lineno=1, filename=os.getcwd())
        file_dip = self.content[0]
        
        with DIP(source=source, docs=True) as dip:
            dip.from_file(file_dip)
            env = dip.parse()
            sources = env.sources
            units = env.units
            data = env.data(format=Format.NODE)

        data = collections.OrderedDict(sorted(data.items()))

        def add_field(key, value, literal=False, options=False):
            field = nodes.field()
            field += nodes.field_name('',key)
            if literal:
                field += nodes.field_body('',nodes.literal(text=value))
            elif options:
                opts = []
                for v in value:
                    if v.units_raw:
                        opts.append(f"{v.value_raw} {v.units_raw}")
                    else:
                        opts.append(f"{v.value_raw}")
                field += nodes.field_body('',nodes.inline('',", ".join(opts))) #blist)
            else:
                field += nodes.field_body('',nodes.inline(text=value))
            return field

        nodelist = []
        
        section = nodes.section(ids=["dip-sources"])
        section += nodes.title('','Sources')
        if sources:
            deflist = nodes.definition_list()
            for name, source in sources.items():
                props = nodes.field_list()
                props += add_field('File', source.path)
                defitem = nodes.definition_list_item()
                defitem += nodes.term('', '', nodes.strong(text=name))
                defitem += nodes.definition('', props)
                deflist += defitem
            section += deflist
        else:
            section += nodes.paragraph('','There are no reference sources in this DIP file')
        nodelist.append(section)
        
        section = nodes.section(ids=["dip-units"])
        section += nodes.title('','Units')
        if units:
            deflist = nodes.definition_list()
            for name, unit in units.items():
                props = nodes.field_list()
                props += add_field('Definition', f"{unit['magnitude']} {unit['name']}")
                defitem = nodes.definition_list_item()
                defitem += nodes.term('', '', nodes.strong(text=unit['name']))
                defitem += nodes.definition('', props)
                deflist += defitem
            section += deflist
        else:
            section += nodes.paragraph('','There are no custom units in this DIP file')
        nodelist.append(section)
        
        section = nodes.section(ids=["dip-parameters"])
        section += nodes.title('','Parameters')
        deflist = nodes.definition_list()
        for name,node in data.items():
            text =  name+"\n"
            props = nodes.field_list()
            if 'show-code' in self.options:
                props += add_field("Line", node.source.lineno)
            if node.defined:
                props += add_field("Node type", 'declaration')
            else:
                if node.constant:
                    props += add_field("Node type", 'constant definition')
                else:
                    props += add_field("Node type", 'definition')
            props += add_field("Data type", node.keyword)
            if node.value:
                props += add_field("Default value", node.value.value, literal=True)
            if node.units_raw:
                props += add_field("Unit", node.units_raw)
            if node.condition:
                props += add_field("Condition", node.condition, literal=True)
            if isinstance(node,(IntegerNode,FloatNode,StringNode)):
                props += add_field("Options", node.options, options=True)
            defitem = nodes.definition_list_item()
            defitem += nodes.term('', '', nodes.strong(text=text))
            defitem += nodes.definition('', props)
            deflist += defitem
        section += deflist
        nodelist.append(section)
        

        if 'show-code' in self.options:
            section = nodes.section(ids=["dip-code"])
            section += nodes.title('','Code')
            section += sphinx.addnodes.highlightlang('', nodes.paragraph(text='width float = 23 cm'), lang='DIP', force=False, linenothreshold=-1)
            with open(file_dip) as f:
                text = f.read()
                text = text.replace("\t"," "*8)
                block = nodes.literal_block(text=text)
                section += block
            nodelist.append(section)
        
        return nodelist


def setup(app):
    app.add_directive("dipdocs", SphinxDocs)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
