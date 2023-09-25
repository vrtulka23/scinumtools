Validation
==========

Numerical codes usually require initial parameter values with a specific format.
In this section, we summarize validation tools that can be used in DIP to restrict node values.
Each node validation directive is given on a new line immediately after node definitions, declarations or modification.
All validation directives must have consistent indent, higher than their parent node.

Options
-------

Initial code parameters often accept only a few discrete input values, also called options.
These can be explicitly described during node definition or declaration.

.. code-block:: DIPSchema
   :caption: Schema of a node option
      
   <indent>= <value> <unit>
   <indent>= <value>

Node options can be specified for all data types except boolean.
In case of boolean, the two options (``true`` or ``false``) are implicitly set.
Individual options are specified directly under particular nodes starting with equal sign.
Options cannot be separated from nodes by an empty line.
All options corresponding to the same node must have the same indent, higher than the node.

.. code-block:: DIP

   coordinates int = 1
     = 1  # carthesian
     = 2  # polar
     = 3  # spherical

If the node has an other value than one of the options, DIP will throw an error message.

Node definition and individual options can have different units, but they must have the same dimensionality. The final value of such modified node will be, however, converted into units specified in the definition.

.. code-block:: DIP

   animal str = 'dog'
     = cat
     = dog
     = horse

   energy float = 23 erg   # definition
     = 43                  # option in same units
     = 23 erg              # option in same units
     = 3e-7 J              # option in different unit of energy

   energy = 3e-7 J         # modification
   # energy = 3 erg        # final value

If the number of options is too large, and it is not practical to write each option on a new line, it is also possible to use a shorthand ``!options`` option notation.

.. code-block:: DIPSchema
   :caption: Schema of an option array
		
   <indent>!options <value> <unit>
   <indent>!options <value>

The expected value of this clause is a list of values.
It can be given explicitly or as a :doc:`reference <references>`.
Similiarly as in the cases above, units are optional and must be of the same dimension as those given in a corresponding definition.
   
Several ``!options`` clauses are allowed for the same node (e.g. each with different units).
They combine into a single array of options against which the node value is evaluated.
     
.. code-block:: DIP
   
   animal str = 'dog'
     !options ['cat','dog','horse']

   energy float = 23 J
     !options [23, 45, 10, 234, 490, 1939] J
     !options [34, 234] erg
   # all options: [23, 45, 10, 234, 490, 1939, 3.4e-6, 2.34e-7] J

Condition
---------

Numerical values can usually have values ranging in some intervals.
In order to restrict node values to some particular interval, it is possible to set logical using ``!condition`` directive and logical expression.
A given expression has to be evaluated as `true` after each definition or modification of a node.

.. code-block:: DIPSchema
   :caption: Schema of a node condition requirement
      
   <indent>!condition ('<expression>')    
   <indent>!condition ("<expression>")    
   <indent>!condition ("""
   <expression>
   """)                                   

In the example below, node `energy` can have values in a range of 23 and 26 erg.
The actual value of node `energy` is matched using a special self-reference sign ``{?}``.

.. code-block:: DIP

   energy float = 25 erg
     !condition ("23 < {?} && {?} < 26")

Format
------

In general, string values wrapped into quote marks can contain all characters and can be arbitrary long.
This can be restricted by defining their ``!format`` using standard (Python based) regular expressions.

.. code-block:: DIPSchema
   :caption: Schema of a node format requirement

   <indent>!format <value>

In the following example, node 'name' can contain only small and capital letters:
   
.. code-block:: DIP

   name str = 'Ferdinant'
     !format '[a-zA-Z]+'

Constants
---------

Sometimes nodes have to stay constant and exclude all possible modifications.
This can be achieved by a directive ``!constant``.

.. code-block:: DIPSchema
   :caption: Schema of a constant node requirement

   <indent>!constant

Node `name` in the following example cannot be further modified.
     
.. code-block:: DIP

   name str = 'John'
     !constant

   name = 'Mary'   # this modification will raise an error exception
