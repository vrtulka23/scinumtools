from enum import Flag, auto

from ..settings import ROOT_SOURCE, Sign

class DocsType(Flag):  # node type in documentation
    UNKNOWN      = auto()
    DECLARATION  = auto()
    DEFINITION   = auto()
    MODIFICATION = auto()
    INJECTION    = auto()
    
def NormalizeTargetName(name: str):
    name = name.replace('.','_')
    name = name.replace(Sign.CONDITION,'CASE')
    return name
    
def ParameterItemTarget(name: str):
    name = NormalizeTargetName(name)
    return f"PARAM_{name}"
    
def NodeItemTarget(name:str, source:str, lineno:int):
    name = NormalizeTargetName(name)
    return f"NODE_{name}_{source}_{lineno}"
    
def InjectionItemTarget(name:str, source:str, lineno:int):
    name = NormalizeTargetName(name)
    return f"INJECT_{name}_{source}_{lineno}"

def ImportItemTarget(source:str, lineno:int):
    return f"IMPORT_{source}_{lineno}"

def UnitItemTarget(name: str):
    name = NormalizeTargetName(name)
    return f"UNIT_{name}"
    
def SourceItemTarget(source:str, lineno:int=None):
    if ROOT_SOURCE in source or lineno is None:
        return f"SOURCE_{source}"
    else:
        return f"SOURCE_{source}_{lineno}"
        