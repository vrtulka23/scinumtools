Pygments highlighter
====================

Pygments highlighter can be used in a Sphinx documentation by adding following lines into the ``conf.py`` file.

.. code-block:: python

   >>> # DIP Syntax Highlighter
   >>> from sphinx.highlighting import lexers
   >>> from scinumtools.dip.pygments import SyntaxLexer, SchemaLexer, StyleLexer, pygments_monkeypatch_style
   >>> pygments_monkeypatch_style("StyleLexer", StyleLexer)
   >>> pygments_style = 'StyleLexer'
   >>> lexers['DIP'] = SyntaxLexer(startinline=True, style=StyleLexer)
   >>> lexers['DIPSchema'] = SchemaLexer(startinline=True, style=StyleLexer)

Syntax highlighting of a DIP code block is than straightforward:

.. code-block:: rst

   .. code-block:: DIP
    
      height float = 23.4 cm

Syntax highlighter
------------------

DIP language shares many common programming concepts with other languages like Python and C.
It's syntax is, however, different enough to cause a problem for generic highlighters.
Therefore, DIP comes with its own `pygments <https://pygments.org>`_ lexer in `syntax_lexer.py <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/pygments/syntax_lexer.py>`_ and styles in `style_lexer.py <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/pygments/style_lexer.py>`_.
Below is an overview of all its highlighting capabilities:

.. note::

   All starting curly brackets in expressions are interpreted as references.
   In order to interpret a starting curly bracket as a plain text, one has to escape them with a slash sign.
   The slash sign will be automatically omitted by the lexer in the highlighted text.

.. code-block:: DIP

   # group nodes
   
   name
   hierarchy.path  # comment
   name-with.more_words.and.stuff34

   # modifications
   
   name = 1
   name = foo
   name = "foo bar"       # comment
   name = 'foo bar'
   name = """
   foo bar
   """
   name = {source?query}

   # declarations
   
   name bool
   name int
   name int32
   name uint32
   name str
   name float
   name float             # comment
   name float64
   name table

   name float[:1,2]
   name float[:1,2]       # comment

   # scalar definitions
   
   name bool = true
   name bool = false      # comment
   name bool = {source?query}
   name bool = ('({?a} == 23.43 cm')
   name bool = ("({?a} == 23.43 cm && true")  # comment
   name bool = ("""
   false || ({?a} == 23.43 cm || ~{?b}) && {?c} || ~!{?d}
   """)
   
   name int = 12
   name float = 12
   name float = 12.3
   name float = 12.3e23   # comment
   name float = 12.3e-23
   name float = -12.3e23
   name float = {source?query}
   name float = (function)
   name float = ('2 kg * pow({?const.c},2)')
   name float = ("2 kg * pow({?const.c},2)")  # comment
   name float = ("""
   2 kg * pow({?const.c},2)
   """)
   
   name str = foo
   name str = "foo bar"   # comment
   name str = 'foo bar'
   name str = """
   foo bar " "" '
   """
   name str = {source?query}  # comment
   name str = ('ID: {{?id}:05d}')
   name str = ("ID: {{?id}:05d}") # comment
   name str = ("""
   ID:      {{?id}:05d}
   Name:    {{?name}}
   Surname:  {{?name}[5:]}
   Scalar:   {{?widths}[1,1]:.2e}
   Array:
   {{?widths}[:,1:]}
   \{no-reference}   <-  starting curly bracket was escaped
   """)

   # array definitions
   
   name bool[2,2] = [[true,false],[false,true]]       
   name bool[2,2] = "[[true, false], [false, true]]"
   name bool[2,2] = '[[true, false], [false, true]]'
   name bool[2,2] = """
   [[true, false], [false, true]]
   """
   name bool[2,2] = {source?query}[:2,:2]
   
   name int[2,3] = [[1,2,3],[4,5,6]]
   name float[2,3] = [[1,2,3],[4,5,6]]                # comment
   name float[2,3] = "[[1, 2, 3], [4, 5, 6]]"
   name float[2,3] = '[[1, 2, 3], [4, 5, 6]]'
   name float[2,3] = """
   [[1, 2, 3], [4, 5, 6]]
   """
   name float[2,3] = {source?query}[:2,:3]
   
   name str[2,2] = [[a,b],[c,d]]
   name str[2,2] = [['a','b'],["c","""
   foo bar
   """]]                                              # comment
   name str[3] = ['John','Peter',"Simon"]             # comment
   name str[2,2] = "[['a','b'],[\"c\",\"d\"]]"
   name str[2,2] = '\[[\'a\',\'b\'],["c","d"]]'
   name str[2,2] = """
   [['a','b'],[\"c\",\"d\"]]
   """
   name str[2,2] = {source?query}[:2,:2]              # comment

   # units
   
   name = 1 cm
   name = 1 cm            # comment
   name float cm
   name float cm          # comment
   name float[:1,2] cm
   name float[:1,2] cm    # comment
   name int = 12 cm       
   name int = 12 cm       # comment
   name float = 12 cm       
   name float = 12 cm     # comment
   name float = {source?query} cm                 # comment
   name float[2,3] = [[1,2,3],[4,5,6]] cm
   name float[2,3] = [[1,2,3],[4,5,6]] cm         # comment
   name float[2,3] = "[[1, 2, 3], [4, 5, 6]]" cm
   name float[2,3] = "[[1, 2, 3], [4, 5, 6]]" cm  # comment
   name float[2,3] = '[[1, 2, 3], [4, 5, 6]]' cm
   name float[2,3] = '[[1, 2, 3], [4, 5, 6]]' cm  # comment
   name float[2,3] = """
   [[1, 2, 3], [4, 5, 6]]
   """ cm
   name float[2,3] = """
   [[1, 2, 3], [4, 5, 6]]
   """ cm                   # comment
   name float[2,2] = {source?query}[:2,:2] cm     # comment
   name float = ('2 kg * pow({?const.c},2)') kg
   name float = ("2 kg * pow({?const.c},2)") kg   # comment
   name float = ("""
   2 kg * pow({?const.c},2)
   """) kg

   # properties
   
   weight float = 23.3 kg
     = 28 g
     = 23
     = 83 kg   # comment
     = 23      # comment
     !options [28,29,30]      
     !options [28,29,30]       # comment
     !options [28,29,30] kg   
     !options [28,29,30] kg    # comment
     !constant
     !constant            # comment
     !format '[a-zA-Z]'
     !format "[a-zA-Z]"
     !format "[a-zA-Z]"   # comment
     !condition ('23 < {?} && {?} < 26')
     !condition ("23 < {?} && {?} < 26")
     !condition ("""
     23 < {?} && {?} < 26
     """)
     !tags ["foo","bar"]
     !description "Node description"
     !desc "Node description"
     
   # special nodes

   $unit length = 1 cm          # comment
   $source file = path          # comment 
   $source {init?*}             # comment
   $unit {units?*}              # comment
   @case ("{?winner} == 1")     # comment
   @else                        # comment
   @end                         # comment
       
   # hierarchy
   
   family str = Smith
     parents
       father str = 'John'
       mother str = 'Mary'
     children int = 1
       infant bool = true  # comment
       weight float = 9 kg 


Schema highlighter
------------------

DIP schema highlighter is design to highlight only the most basic concepts of DIP language.
Definition of the schema highlighter is in file `schema_lexer.py <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/pygments/schema_lexer.py>`_. 
The following block summarizes all highlighter possibilities.

.. code-block:: DIPSchema

   <indent><name> <type> = <value> <unit> # comment
   
   <indent>= <value> <unit>               # comment
   <indent>!options <value> <unit>        # comment
   <indent>!condition ('<expression>')      
   <indent>!condition ("<expression>")    # comment
   <indent>!condition ("""
   <expression>
   """)
   <indent>!format <value>
   <indent>!constant
   
   $source <name> = <path>

   {<source>?<query>}
   {<source>?<query>}[<slice>] 

   (<function>)
   ("<expression>")
   ('<expression>')
   ("""
   <expression>
   """)
