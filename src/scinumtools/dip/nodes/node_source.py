import os
from pathlib import Path

import scinumtools.dip as dipsl
from .node_base import BaseNode
from .parser import Parser
from ..settings import Namespace
from ..source import Source

class SourceNode(BaseNode):
    keyword: str = 'source'

    @staticmethod
    def is_node(parser):
        parser.kwd_source()
        if parser.is_parsed('kwd_source'):
            parser.part_comment()
            return SourceNode(parser)
            
    def parse(self, env):
        parser = Parser(
            code=self.value_raw,
            source=self.source
        )
        # import a remote source
        parser.part_reference()
        if parser.is_parsed('part_reference'):
            sources = env.request(parser.value_ref, namespace=Namespace.SOURCES)
            for key, val in sources.items():
                env.add_source(key, val.source, val.path)
        else:
            # inject value of a node
            parser.part_name(path=False) # parse name
            parser.part_equal()          # parse equal sign
            parser.part_value()          # parse value
            if parser.value_ref:
                self.inject_value(env, parser)
            if parser.value_raw.endswith('dip'):
                source = Source(**self.source.__dict__)
                source.primary = False
                p = dipsl.DIP(source=source)
                p.from_file(parser.value_raw)
                p.parse()
                env.add_source(parser.name, p, parser.value_raw)
            else:
                filepath = parser.value_raw
                if not os.path.isabs(filepath):
                    # set relative paths with respect to the source script
                    parent = Path(self.source.filename).parent
                    filepath = parent / filepath
                with open(filepath,'r') as f:
                    env.add_source(parser.name, f.read(), filepath)
        return None
