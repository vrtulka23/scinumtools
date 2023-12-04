from .settings import *

class UnitItem:
    target: str
    link_source: str
    name: str
    value: str
    units: str
    source: tuple

    def __init__(self, name, unit):
        self.target = UnitItemTarget(name)
        self.link_source = SourceItemTarget(unit['source'][0],unit['source'][1])
        self.name   = name
        self.value  = unit['value']
        self.units  = unit['units']
        self.source = unit['source']
