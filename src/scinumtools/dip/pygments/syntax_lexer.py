from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Token
    
class SyntaxLexer(RegexLexer):
    name = 'DIP'
    tokens = {
        'root': [
            (r'([ ]*)(#[^\n]*|)(\n)', 
             bygroups(Token.DIP.Text, Token.DIP.Comment, Token.DIP.Text)),
            (r'([ ]*)(\$source|\$unit)([ ]+)({)',
             bygroups(Token.DIP.Text, Token.DIP.Keyword, Token.DIP.Text,
                      Token.DIP.Reference),'reference'),
            (r'([ ]*)(\$source|\$unit)([ ]+)([a-zA-Z0-9-_]+)([ ]+=)',
             bygroups(Token.DIP.Text, Token.DIP.Keyword, Token.DIP.Text,
                      Token.DIP.Name, Token.DIP.Text),'node_value'),
            (r'[ ]*\@case', Token.DIP.Keyword, 'node_value'),
            (r'[ ]*\@(else|end)', Token.DIP.Keyword),
            (r'[ ]*!(options|format|condition|constant|tags|description)',
             Token.DIP.Keyword, 'node_value'), # full keywords
            (r'[ ]*!(desc)',
             Token.DIP.Keyword, 'node_value'), # abbreviated forms
            (r'^([ ]*)(=)',
             bygroups(Token.DIP.Text, Token.DIP.Keyword), 'node_value'),
            (r'^([ ]*)([a-zA-Z0-9-_.]+)([ ]+=)',
             bygroups(Token.DIP.Text, Token.DIP.Name, Token.DIP.Text), 'node_value'),
            (r'^([ ]*)([a-zA-Z0-9-_.]+)',
             bygroups(Token.DIP.Text, Token.DIP.Name), 'node_type'),
            (r'([ ]*)({)',
             bygroups(Token.DIP.Text, Token.DIP.Reference), 'reference'),
        ],
        'node_type': [
            (r'([ ]*)({)',
             bygroups(Token.DIP.Text, Token.DIP.Reference), 'reference'),
            (r'([ ]*)(bool|[u]?int[0-9]*|float[0-9]*|str|table)(\[)',
             bygroups(Token.DIP.Text, Token.DIP.Type, Token.DIP.Type), 'type_dim'),
            (r'([ ]*)(bool|[u]?int[0-9]*|float[0-9]*|str|table)([ ]+=)',
             bygroups(Token.DIP.Text, Token.DIP.Type, Token.DIP.Text), 'node_value'),
            (r'([ ]*)(bool|[u]?int[0-9]*|float[0-9]*|str|table)', 
             bygroups(Token.DIP.Text, Token.DIP.Type), 'unit'), 
            (r'([ ]*)(bool|[u]?int[0-9]*|float[0-9]*|str|table)',
             bygroups(Token.DIP.Text, Token.DIP.Type), '#pop'),
            (r' ', Token.DIP.Text, '#pop'),
        ],
        'type_dim': [
            (f'[0-9.:]+',              Token.DIP.Dimension),
            (f',',                     Token.DIP.Type),
            (r'(\])([ ]+=)',
             bygroups(Token.DIP.Type, Token.DIP.Text), 'node_value'),
            (r'\]',                    Token.DIP.Type, 'unit'),
            (r' ', Token.DIP.Text, '#pop:2'),
        ],
        'node_value': [
            # booleans
            (r"([ ]*)(true|false)",
             bygroups(Token.DIP.Text, Token.DIP.Boolean)),
            # numbers
            (r"([ ]*)(-[0-9.]+|[0-9.]+)(e-[0-9]+|e[0-9]+|)([ ]+[^#\n ]+|)",
             bygroups(Token.DIP.Text, Token.DIP.Number, Token.DIP.Number, Token.DIP.Unit)),
            # strings
            (r"([ ]*)(')",
             bygroups(Token.DIP.Text, Token.DIP.String),   'str_single'),
            (r'([ ]*)(""")',
             bygroups(Token.DIP.Text, Token.DIP.String),   'str_triple'),            
            (r'([ ]*)(")',
             bygroups(Token.DIP.Text, Token.DIP.String),   'str_double'),
            # function
            (r"([ ]*\()([a-zA-Z0-9_-]+)(\))",
             bygroups(Token.DIP.Text, Token.DIP.Expression, Token.DIP.Text), 'unit'),
            # expressions
            (r"([ ]*\()(')",
             bygroups(Token.DIP.Text, Token.DIP.Expression),   'expr_single'),
            (r'([ ]*\()(""")',
             bygroups(Token.DIP.Text, Token.DIP.Expression),   'expr_triple'),            
            (r'([ ]*\()(")',
             bygroups(Token.DIP.Text, Token.DIP.Expression),   'expr_double'),
            # references
            (r'([ ]*)({)',
             bygroups(Token.DIP.Text, Token.DIP.Reference), 'reference'),
            # arrays
            (r"([ ]*)(\[)",
             bygroups(Token.DIP.Text, Token.DIP.Text), '#push'),
            (r"(,)", Token.DIP.Text),
            (r"(\])([ ]+[^#\n ]*)",
             bygroups(Token.DIP.Text,  Token.DIP.Unit), '#pop:4'),
            (r"(\])", Token.DIP.Text, '#pop'),
            # units
            (r"([ ]*)([^#\n ]+)",
             bygroups(Token.DIP.Text, Token.DIP.String)),
            # end of definition
            (r'[ ]', Token.DIP.Text, '#pop:4'),
        ],
        'str_single' : [
            (r"[^'\\]+",               Token.DIP.String),
            (r"\\'",                   Token.DIP.String),
            (r"\\[^']",                Token.DIP.String),
            ("(')(,)",
             bygroups(Token.DIP.String, Token.DIP.Text), "#pop"),
            ("(')(\])",
             bygroups(Token.DIP.String, Token.DIP.Text), "#pop:2"),  # pop if in array
            ("(')", Token.DIP.String, "unit"),
        ],
        'str_double' : [
            (r'[^"\\]+',               Token.DIP.String),
            (r'\\"',                   Token.DIP.String),
            (r'\\[^"]',                Token.DIP.String),
            ('(")(,)',
             bygroups(Token.DIP.String, Token.DIP.Text), "#pop"),
            ('(")(\])',
             bygroups(Token.DIP.String, Token.DIP.Text), "#pop:2"),  # pop if in array
            ('"', Token.DIP.String, "unit"),
        ],
        'str_triple' : [
            (r'[^"\\]+',               Token.DIP.String),
            (r'\\"',                   Token.DIP.String),
            (r'\\[^"]',                Token.DIP.String),
            (r'"[^"]',                 Token.DIP.String),
            (r'""[^"]',                Token.DIP.String),
            (r'(""")(,)',
             bygroups(Token.DIP.String, Token.DIP.Text), "#pop"),
            (r'(""")(\])',
             bygroups(Token.DIP.String, Token.DIP.Text), "#pop:2"),  # pop if in array
            (r'"""', Token.DIP.String, "unit"),
        ],
        'expr_single' : [
            (r"\\({)",
             bygroups(Token.DIP.Expression)),
            (r'{',                     Token.DIP.Reference, 'reference_expr'),
            (r"[^'\\{]+",              Token.DIP.Expression),
            (r"\\'",                   Token.DIP.Expression),
            (r"\\[^']",                Token.DIP.Expression),
            ("(')(\))",
             bygroups(Token.DIP.Expression, Token.DIP.Text), "unit"),
        ],
        'expr_double' : [
            (r"\\({)",
             bygroups(Token.DIP.Expression)),
            (r'{',                     Token.DIP.Reference, 'reference_expr'),
            (r'[^"\\{]+',              Token.DIP.Expression),
            (r'\\"',                   Token.DIP.Expression),
            (r'\\[^"]',                Token.DIP.Expression),
            ('(")(\))',
             bygroups(Token.DIP.Expression, Token.DIP.Text), "unit"),
        ],
        'expr_triple' : [
            (r"\\({)",
             bygroups(Token.DIP.Expression)),
            (r'{',                     Token.DIP.Reference, 'reference_expr'),
            (r'[^"\\{]+',              Token.DIP.Expression),
            (r'\\"',                   Token.DIP.Expression),
            (r'\\[^"]',                Token.DIP.Expression),
            (r'"[^"]',                 Token.DIP.Expression),
            (r'""[^"]',                Token.DIP.Expression),
            (r'(""")(\))',
             bygroups(Token.DIP.Expression, Token.DIP.Text), "unit"),
        ],
        'reference' : [
            (r"{",                     Token.DIP.Reference, "#push"),
            (r"[^{}]+",                Token.DIP.Reference),
            (r"}\[",                   Token.DIP.Reference, "reference_slice"),
            (r"}",                     Token.DIP.Reference, "unit"),
        ],
        'reference_expr' : [
            (r"{",                     Token.DIP.Reference, "#push"),
            (r"[^{}]+",                Token.DIP.Reference),
            (r"}\[",                   Token.DIP.Reference, "reference_slice"),
            (r"(}:)([0-9sdef.]+)",
             bygroups(Token.DIP.Reference, Token.DIP.Slice), "#pop"),
            (r"}",                     Token.DIP.Reference, "#pop"),
        ],
        'reference_slice': [
            (r'[0-9.:]+',              Token.DIP.Slice),
            (r',',                     Token.DIP.Reference),
            (r'\]}',                   Token.DIP.Reference, '#pop:3'),
            (r'(\]:)([0-9sdef.]+)',
             bygroups(Token.DIP.Reference, Token.DIP.Slice), '#pop:2'),
            (r'\]',                    Token.DIP.Reference, 'unit'),
        ],
        'unit': [
            (r'([ ]+[^=#\n ]+|)',      Token.DIP.Unit, "#pop:6")
        ],
    }
