from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Token
    
class SchemaLexer(RegexLexer):
    name = 'DIP'
    tokens = {
        'root': [
            (r'<indent>',     Token.DIP.Indent),
            (r'<name>',       Token.DIP.Name),
            (r'<type>',       Token.DIP.Type),
            (r'<unit>',       Token.DIP.Unit),
            (r'<value>',      Token.DIP.String),
            (r'<path>',       Token.DIP.String),
            (r'\.\.\.',       Token.DIP.Text),
            (r'(\()("""\n|"|\')(<expression>)(\n"""|"|\')(\))',   # """
              bygroups(Token.DIP.Text, Token.DIP.Expression, Token.DIP.Expression,
                       Token.DIP.Expression, Token.DIP.Text)),
            (r'(\()(<function>)(\))',
              bygroups(Token.DIP.Text, Token.DIP.Expression,  Token.DIP.Text)),
            (r'<[^ ]',        Token.DIP.Tag, 'tag'),
            (r'{',            Token.DIP.Reference, 'reference'),
            (r'!(options|format|condition|constant|tags|description)',  Token.DIP.Keyword),
            (r'\$(source|unit)',     Token.DIP.Keyword),
            (r'\@(case|else|end)',     Token.DIP.Keyword),
            (r'( |=|<|>|\.\*|\*)',    Token.DIP.Text),
            (r'#[^\n]*',  Token.DIP.Comment),
            (r'[ ]*\n',   Token.DIP.Text), 
        ],
        'tag': [
            (r'[a-zA-Z0-9_-]+', Token.DIP.Tag),
            (r'>',              Token.DIP.Tag, '#pop'),
        ],
        'reference': [
            (r'[^}]+',          Token.DIP.Reference),
            (r'{',              Token.DIP.Reference, '#push'),
            (r'}\[',            Token.DIP.Reference, 'reference_slice'),
            (r'}',              Token.DIP.Reference, '#pop'),
        ],
        'reference_slice': [
            (r'[^\]]+',         Token.DIP.Slice),
            (r',',              Token.DIP.Reference),
            (r'\]',             Token.DIP.Reference, '#pop:2'),
        ],

    }
