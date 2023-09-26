from .node_base import BaseNode

class ModNode(BaseNode):
    keyword: str = 'mod'

    @staticmethod
    def is_node(parser):         
        parser.part_equal()  
        if parser.is_parsed('part_equal'): 
            parser.part_value()
            parser.part_units()
            parser.part_comment()
            return ModNode(parser)
            
    def parse(self, env):
        return None    
