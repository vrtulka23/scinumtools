Conditions
==========

.. code-block:: DIPSchema
   :caption: Schemas of condition directives

   # condition with only one case
   @case ("<expression>")
     ...
   @end                 # end is optional
   
   # condition with multiple cases
   @case ("<expression>")
     ...
   @case ("<expression>")
     ...
   @else                # else is optional
     ...
   @end                 # end is optional

   # consecutive conditions
   @case ("<expression>")   # first condition
     ...
   @else
     ...
   @end                 # end is necessary
   @case ("<expression>")   # second condition
     ...

Parameters in DIP can also be branched using conditions.
There are 3 clauses used in conditions.
Child nodes must have higher indent than the parent clause.

``@case ("<expression>")``
  is a starting clause of each condition and requires as an argument result of a logical expression.
  If the expression is evaluated as true, child nodes of the corresponding ``@case`` will be taken and the condition is terminated.
  If the expression is false, its child nodes are skipped and subsequent clauses are evaluated.
  For testing purposes, one can also use direct ``true`` or ``false`` keywords instead of expressions.

``@else``
  is a special, optional, clause that is at the very end of conditions and does not require any expression.
  Each condition can have only one ``@else`` clause.
  If all previous ``@case``-s are evaluated as false, child nodes of ``@else`` are taken.

``@end``
  is a terminating clause whose main purpose is to separate two consecutive conditions.
  If omitted, a single condition terminates after last ``@case`` or ``@else``.
      
.. code-block:: DIP
		
   winner int = 1
   
   @case ("{?winner} == 1")     # first case
     name str = "John"
   @case ("{?winner} == 2")     # second case
     name str = "Jenny"
   @else                        # default case
     name str = "Jonas"
   @end                         # end of first condition
   
   @case ("{?name} == 'Jenny'")
     toy str = "doll"
   @else
     toy str = "robot"

Nested conditions are also possible, provided that each child condition has indent higher than the parent condition.

.. code-block:: DIP

   @case false
     flower str = 'rose'
   @else
     flower str = 'dandelion'
     @case false
       color str = 'red'
     @case false
       color str = 'blue'
     @else
       @case true
	 leaves int = 234
       color str = 'yellow'
     tree str = 'maple'

     # The nodes above will be parsed as:
     #
     # flower = 'dandelion'
     # leaves = 234
     # color  = 'yellow'
     # tree   = 'maple'

.. note::

   Even though children nodes have higher indent than their parent clauses, this does not have an effect on naming hierarchy. 
