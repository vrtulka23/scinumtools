from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Token
    
class DIP_Lexer_Schema(RegexLexer):
    name = 'DIP'
    tokens = {
        'root': [
            (r'<indent>',     Token.Indent),
            (r'<name>',       Token.Name),
            (r'<type>',       Token.Type),
            (r'<unit>',       Token.Unit),
            (r'<value>',      Token.String),
            (r'<path>',       Token.String),
            (r'\.\.\.',       Token.Text),
            (r'(\()("""\n|"|\')(<expression>)(\n"""|"|\')(\))',
              bygroups(Token.Text, Token.Expression, Token.Expression,
                       Token.Expression, Token.Text)),
            (r'(\()(<function>)(\))',
              bygroups(Token.Text, Token.Expression,  Token.Text)),
            (r'<[^ ]',        Token.Name.Tag, 'tag'),
            (r'{',            Token.Reference, 'reference'),
            (r'!(options|format|condition|constant)',  Token.Keyword),
            (r'\$(source|unit)',     Token.Keyword),
            (r'\@(case|else|end)',     Token.Keyword),
            (r'( |=|<|>|\.\*|\*)',    Token.Text),
            (r'#[^\n]*',  Token.Comment),
            (r'[ ]*\n',   Token.Text), 
        ],
        'tag': [
            (r'[a-zA-Z0-9_-]+', Token.Name.Tag),
            (r'>',              Token.Name.Tag, '#pop'),
        ],
        'reference': [
            (r'[^}]+',          Token.Reference),
            (r'{',              Token.Reference, '#push'),
            (r'}\[',            Token.Reference, 'reference_slice'),
            (r'}',              Token.Reference, '#pop'),
        ],
        'reference_slice': [
            (r'[^\]]+',         Token.Slice),
            (r',',              Token.Reference),
            (r'\]',             Token.Reference, '#pop:2'),
        ],

    }
