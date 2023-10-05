import json

from .node_base import BaseNode

class TagsNode(BaseNode):
    keyword: str = 'tags'

    @staticmethod
    def is_node(parser):
        parser.kwd_tags()
        if parser.is_parsed('kwd_tags'):
            parser.part_value()
            parser.part_comment()
            return TagsNode(parser)
            
    def parse(self, env):
        if env.nodes[-1].keyword not in ['str','int','float','bool']:
            raise Exception("Format can be set only to str, int, float and bool nodes:", env.nodes[-1].code)
        tags = json.loads(self.value_raw)
        if not isinstance(tags, list):
            raise Exception("Tags can be input only as an array of strings, instead received:", tags)
        if env.nodes[-1].tags == None:
            env.nodes[-1].tags = tags
        else:
            env.nodes[-1].tags += tags
        return None
