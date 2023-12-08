from bs4 import BeautifulSoup

NTYPES = [
    ('Declaration',                '#698D3F',),
    ('Definition',                 '#AABA78',),
    ('Declaration / Modification', '#D77F33',),
    ('Definition / Modification',  '#DDA15E',),
    ('Modification',               '#FBE974',),
    ('Injection',                  '#AB88BF',),
    ('Import',                     '#D0BCDC',),
]

PAGE_TYPES      = "parameters.html"
PAGE_PARAMETERS = "parameters.html"
PAGE_NODES      = "parameters.html"
PAGE_INJECTIONS = "references.html"
PAGE_IMPORTS    = "references.html"
PAGE_UNITS      = "settings.html"
PAGE_SOURCES    = "settings.html"

def Title(name:str='', h:int=2):
    return f"<a name=\"SECTION_{name}\"></a><h{h}>{name}</h{h}>"

def Target(key:str, name:str=''):
    return BeautifulSoup(f"<a name=\"{key}\"></a>{name}", 'html.parser')
    
def Link(page:str, key:str, name:str=''):
    return BeautifulSoup(f"<a href=\"{page}#{key}\" color=\"blue\">{name}</a>", 'html.parser')