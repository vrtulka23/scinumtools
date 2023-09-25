from dataclasses import dataclass

@dataclass
class Source:
    filename: str          # file from which the source was called
    lineno: int            # line from which the source was called
    primary: bool = True   # is this a primary or imported source
