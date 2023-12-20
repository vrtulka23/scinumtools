import os
from pathlib import Path

import scinumtools.dip as dipsl
from .node_base import BaseNode
from .parser import Parser
from ..settings import Namespace

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
            # append remote sources to the local sources
            for key, val in sources.items():
                env.sources[key] = val
        else:
            # inject value of a node
            parser.part_name(path=False) # parse name
            parser.part_equal()          # parse equal sign
            parser.part_value()          # parse value
            if parser.value_ref:
                self.inject_value(env, parser)
            if parser.value_raw.endswith('dip'):
                # source is a DIP file
                p = dipsl.DIP(source=self.source)
                p.env.sources = env.sources.copy()
                p.add_file(parser.value_raw, parser.name)
                penv = p.parse()
                env.sources[parser.name] = penv.sources[parser.name]
                env.sources[parser.name].nodes = penv.nodes
                env.sources[parser.name].sources = penv.sources
            else:
                # source is a text file
                filepath = parser.value_raw
                if not os.path.isabs(filepath):
                    # set relative paths with respect to the source script
                    source = env.sources[self.source[0]]
                    parent = Path(source.path).parent
                    filepath = parent / filepath
                with open(filepath,'r') as f:
                    env.sources.append(parser.name, filepath, f.read(), self.source[0])
        return None
