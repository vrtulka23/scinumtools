Values
======

Empty values
------------

Similarly, as in Python, DIP parameters can also be set empty using a special keyword ``none``.
Operations with empty parameters conform to basic Python rules and may lead to corresponding warnings, or errors.
DIP parameters with ``none`` values are considered to be fully defined, rather than only declared.

Scalars
-------

Nodes with a single boolean, number or string value are called scalar nodes.
If a node is scalar at its definition, it can be modified only with one value, or as empty.
Example of scalar node values were already shown in section about :ref:`dip/syntax/datatypes:standard data types`.

Arrays
------

Nodes can also store multiple values in arrays.
Dimensionality of such arrays have to be specified next to the type using bracket notation.

.. csv-table:: Dimensionality of arrays
   :widths: 20 60
   :header-rows: 1

   Example,            Description
   "``[:]``",          "Array can have arbitrary number of values"
   "``[3:]``",         "Array must have minimum of 3 values"
   "``[:5]``",         "Array must have maximum of 5 values"
   "``[1:4]``",        "Array must have between 1 and 4 values"
   "``[6:,:8,2:7]``",  "Settings of individual dimensions are separated by comma"

Parsing of array values is handled by a standard JSON parser.
Final values of nodes are automatically validated according to defined conditions.

.. code-block:: DIP

   data1 bool[4]   = [true,false,false,true]  # exactly four values
   data2 int[:]    = [0,1,2,3,4,5,6]          # any number of values
   data3 float[3:] = [0,1.34,1.34e4]          # at least 3 values
   data4 float[:4] = [0,1.34,1.34e4]          # maximum of 4 values
   data4 str[3:4]  = ['John','Peter','Simon'] # between 3 and 4 values

Multiple values above are written in a tight notation without empty spaces.
If one wants to use loose notation with empty spaces in between individual values, it is necessary to wrap values into single or double quotes.

.. code-block:: DIP

   data1 bool[4]   = '[true, false, false, true]'
   data2 str[3:4]  = "['John', 'Peter', 'Simon']"

Multidimensional arrays are defined similarly using nested bracket notation.

.. code-block:: DIP

   matrix int[2,3] = [[0,1,2],[3,4,5]]

Node units apply to all values in an array.

.. code-block:: DIP

   mass float[2:,:2] = [[25,50],[34.2,95.1],[1e3,1e4]] kg


.. _blocks:
   
Blocks
------

If node values are large or span over several lines, it is possible to use block notation.
Block notation wraps values into triple quote marks, similarly as in Python.
For numerical data types, units can be set after the end of a block.

.. code-block:: DIP

   # velocity field
   velocity int[4,4] = """
   [[ 0, 1, 2, 4],
    [ 5, 6, 7, 8],
    [ 9,10,11,12],
    [13,14,15,16]]
   """ km/s   # units are optional for numerical data types

   # large text
   text str = """
   Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
   sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
   Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
   nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
   reprehenderit in voluptate velit esse cillum dolore eu fugiat 
   nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
   sunt in culpa qui officia deserunt mollit anim id est laborum.
   """

Tables
------

Sometimes it is easier and compendious to put large amount of data into a tabular format.
For this reason, there is a special type of node called ``table``.
This data type parses DIP nodes from tabulated data sets given as a block value.
The table format is very similar to a standard CSV table format, with special header format.

Table header consists of node declarations corresponding to each table column.
Each declaration starts on a new line without indentation.
Table values are separated by an empty line from the header, and individual values are separated by an empty space.

.. code-block:: DIP

   output table = """
   snapshot int
   time float s
   intensity float W/m2

   0 0.234 2.34
   1 1.355 9.4
   2 2.535 3.4
   3 3.255 2.3
   4 4.455 23.4
   """
   
Table notation above is equivalent to:

.. code-block:: DIP

   output
     snapshot int[5] = [0,1,2,3,4]
     time float[5] = [0.234,1.355,2.535,3.255,4.455]
     intensity float[5] = [2.34,9.4,3.4,2.3,23.4] W/m2
