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

def Title(name:str=''):
    return f"<a name=\"SECTION_{name}\"></a><h2>{name}</h2>"

def Target(key:str, name:str=''):
    return f"<a name=\"{key}\"></a>{name}"
    
def Link(key:str, name:str=''):
    return f"<a href=\"#{key}\" color=\"blue\">{name}</a>"