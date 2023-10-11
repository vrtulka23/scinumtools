Schema highliter
================

DIP schema highliter is design to highlight only the most basic concepts of DIP language.
Definition of the schema highlighter is in file `schema_lexer.py <https://github.com/vrtulka23/scinumtools/tree/main/tools/pygments/schema_lexer.py>`_. 
The following block summarizes all highliter possibilities.

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
