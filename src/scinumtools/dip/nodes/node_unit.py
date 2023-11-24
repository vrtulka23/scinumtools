from .node_base import BaseNode
from .parser import Parser
from ..settings import Namespace
from ...units import Quantity, UnitEnvironment

class UnitNode(BaseNode):
    keyword: str = 'unit'

    @staticmethod
    def is_node(parser):
        parser.kwd_unit()
        if parser.is_parsed('kwd_unit'):
            parser.part_comment()
            return UnitNode(parser)
    
    def parse(self, env):
        parser = Parser(
            code=self.value_raw,
            source=self.source
        )
        parser.part_reference()
        if parser.is_parsed('part_reference'):
            # import a remote source
            units = env.request(parser.value_ref, namespace=Namespace.UNITS)
            for key,val in units.items():
                env.units.append(key, val.unit)
        else:
            parser.part_name(path=False) # parse name
            parser.part_equal()          # parse equal sign
            parser.part_value()          # parse value
            if parser.value_ref:
                # inject value of a node
                self.inject_value(env, parser)
            parser.part_units()          # parse unit
            with UnitEnvironment(env.units):
                unit = Quantity(float(parser.value_raw), parser.units_raw)
                unit.symbol = '['+parser.name+']'
                unit.dfn = f"{parser.value_raw}*{parser.units_raw}"
                env.units.append(parser.name, parser.value_raw, parser.units_raw, unit, self.source)
        return None
