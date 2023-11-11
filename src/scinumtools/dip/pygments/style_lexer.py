from pygments.style import Style
from pygments.token import Token

class StyleLexer(Style):

    styles = {
        # node components
        Token.DIP.Indent:                 '#BDBDBD',        # indent tag
        Token.DIP.Keyword:                '#757575',        # directives $ and !
        Token.DIP.Name:                   'bold #616161',   # node name
        Token.DIP.Type:                   '#616161',        # node type
        Token.DIP.Dimension:              '#9E9E9E',        # node dimension
        Token.DIP.String:                 '#558B2F',        # value string
        Token.DIP.Number:                 '#B71C1C',        # value number
        Token.DIP.Boolean:                'bold #0D47A1',   # value bool
        Token.DIP.Reference:              '#E64A19',        # reference
        Token.DIP.Slice:                  '#FF8A65',        # reference slice     
        Token.DIP.Expression:             '#8D6E63',        # expression
        Token.DIP.Unit:                   '#607D8B',        # unit
        Token.DIP.Comment:                'italic #FB8C00', # comment

        # schema components
        Token.DIP.Tag:                    '#0097A7',        # tag

        # other components
        Token.Token.Error:            'border:#F44336', # missing highlight

        # default highlighting
        Token.Whitespace:                "#bbbbbb",
        Token.Comment:                   "italic #3D7B7B",
        Token.Comment.Preproc:           "noitalic #9C6500",

        #Keyword:                   "bold #AA22FF",
        Token.Keyword:                   "bold #008000",
        Token.Keyword.Pseudo:            "nobold",
        Token.Keyword.Type:              "nobold #B00040",

        Token.Operator:                  "#666666",
        Token.Operator.Word:             "bold #AA22FF",

        Token.Name.Builtin:              "#008000",
        Token.Name.Function:             "#0000FF",
        Token.Name.Class:                "bold #0000FF",
        Token.Name.Namespace:            "bold #0000FF",
        Token.Name.Exception:            "bold #CB3F38",
        Token.Name.Variable:             "#19177C",
        Token.Name.Constant:             "#880000",
        Token.Name.Label:                "#767600",
        Token.Name.Entity:               "bold #717171",
        Token.Name.Attribute:            "#687822",
        Token.Name.Tag:                  "bold #008000",
        Token.Name.Decorator:            "#AA22FF",

        Token.String:                    "#BA2121",
        Token.String.Doc:                "italic",
        Token.String.Interpol:           "bold #A45A77",
        Token.String.Escape:             "bold #AA5D1F",
        Token.String.Regex:              "#A45A77",
        #Token.String.Symbol:             "#B8860B",
        Token.String.Symbol:             "#19177C",
        Token.String.Other:              "#008000",
        Token.Number:                    "#666666",

        Token.Generic.Heading:           "bold #000080",
        Token.Generic.Subheading:        "bold #800080",
        Token.Generic.Deleted:           "#A00000",
        Token.Generic.Inserted:          "#008400",
        Token.Generic.Error:             "#E40000",
        Token.Generic.Emph:              "italic",
        Token.Generic.Strong:            "bold",
        Token.Generic.EmphStrong:        "bold italic",
        Token.Generic.Prompt:            "bold #000080",
        Token.Generic.Output:            "#717171",
        Token.Generic.Traceback:         "#04D",

        Token.Error:                     "border:#FF0000"
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
