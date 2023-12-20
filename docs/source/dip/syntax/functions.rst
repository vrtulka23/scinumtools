Functions
=========

In addition to expressions described in previous sections, DIP code can access functions of its interpreter language and use them to fill parameter values.
This is especially useful when syntax of expressions is not enough to solve some complicated problem.

Function calls are, similarly as expressions, wrapped in parentheses.
Instead of an expression string, the inner argument is simply a function name.

.. code-block:: DIPSchema
   :caption: Function schema
      
   # using double quotes
   (<function>)

An example of functions used in DIP code is below.

.. code-block:: DIP
   :caption: function_calls.dip

   side float = 5 cm
   volume float = (fn_volume) cm3
   surface int = (fn_surface) mm2
   prime bool = (is_prime)
   value str = (print_value)

Function names in parentheses correspond to function defined by the interpreter language (e.g. Python) and receive an argument ``data`` that holds a copy of current node values. Each function must return a value that correspond to the node type defined in DIP. This can be either a native data type or DIP data type.
	     
.. code-block:: python

   >>> def fn_volume(data):
   >>>     side = data['side'].convert('cm').value
   >>>     return side**3
   >>> 
   >>> def fn_surface(data):
   >>>     side = data['side'].convert('cm').value
   >>>     return IntegerType(6*side**2, 'cm2')
   >>> 
   >>> def is_prime(data):
   >>>     side = data['side'].convert('cm').value
   >>>     return side in [1,2,3,5,7,11]
   >>> 
   >>> def print_value(data):
   >>>     return str(data['side'])

Functions are registered to DIP before parsing using method ``DIP::.add_function()``.

.. code-block:: python
       
   >>> with DIP() as dip:
   >>>     dip.add_function("fn_volume", fn_volume)
   >>>     dip.add_function("fn_surface", fn_surface)
   >>>     dip.add_function("is_prime", is_prime)
   >>>     dip.add_function("print_value", print_value)
   >>>     dip.add_file("function_calls.dip")
   >>>     env = dip.parse()
   >>>     data = env.data()
   {
      'side':    FloatType(5, 'cm'),
      'volume':  FloatType(125, 'cm3'),
      'surface': IntegerType(15000, 'mm2'),
      'prime':   BooleanType(True),
      'value':   StringType("FloatType(5.0 cm)")
   }
