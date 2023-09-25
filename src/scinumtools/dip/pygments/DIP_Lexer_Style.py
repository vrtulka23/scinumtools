from pygments.style import Style
from pygments.token import Token

class DIP_Lexer_Style(Style):

    styles = {
        # node components
        Token.Indent:                 '#BDBDBD',        # indent tag
        Token.Keyword:                '#757575',        # directives $ and !
        Token.Name:                   'bold #616161',   # node name
        Token.Type:                   '#616161',        # node type
        Token.Dimension:              '#9E9E9E',        # node dimension
        Token.String:                 '#558B2F',        # value string
        Token.Number:                 '#B71C1C',        # value number
        Token.Boolean:                'bold #0D47A1',   # value bool
        Token.Reference:              '#E64A19',        # reference
        Token.Slice:                  '#FF8A65',        # reference slice     
        Token.Expression:             '#8D6E63',        # expression
        Token.Unit:                   '#607D8B',        # unit
        Token.Comment:                'italic #FB8C00', # comment

        # schema components
        Token.Name.Tag:               '#0097A7',        # tag

        # other components
        Token.Token.Error:            'border:#F44336', # missing highlight

        # default components
        Token.Function:               '#8D6E63',
    }

def pygments_monkeypatch_style(mod_name, cls):
    import sys
    import pygments.styles
    cls_name = cls.__name__
    mod = type(__import__("os"))(mod_name)
    setattr(mod, cls_name, cls)
    setattr(pygments.styles, mod_name, mod)
    sys.modules["pygments.styles." + mod_name] = mod
    from pygments.styles import STYLE_MAP
    STYLE_MAP[mod_name] = mod_name + "::" + cls_name
