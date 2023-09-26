from .node_base import BaseNode

class FormatNode(BaseNode):
    keyword: str = 'format'

    @staticmethod
    def is_node(parser):
        parser.kwd_format()
        if parser.is_parsed('kwd_format'):
            parser.part_value()
            parser.part_comment()
            return FormatNode(parser)
            
    def parse(self, env):
        if env.nodes[-1].keyword!='str':
            raise Exception("Format can be set only to string nodes", env.nodes[-1].code)
        env.nodes[-1].format = self.value_raw
        return None
