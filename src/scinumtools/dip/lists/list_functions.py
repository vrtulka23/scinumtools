from dataclasses import dataclass, field
from typing import List, Dict, Union

@dataclass
class FunctionList:
    functions: Dict = field(default_factory = dict)
    
    def __getitem__(self, key: str):
        return self.functions[key]
            
    def append(self, name, function):
        self.functions[name] = function