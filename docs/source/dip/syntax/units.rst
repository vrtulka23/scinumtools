Units
=====

Parsing of units in DIP and their conversion is done using the `Physical Quantities <https://vrtulka23.github.io/scinumtools/units/index.html>`_ module of this package.
For more information about unit expressions consult the corresponding documentation.

Each node has default units assigned at definition, or declaration.
Subsequent modification without given units assume to be in default units.
Values of modifications with different units (but same dimension) are converted to default units.

.. code-block:: DIP

   # definitions
   age int = 30 a
   height float = 185 cm
   weight float = 80 kg

   # modifications
   age = 35
   height = 190 cm      
   weight = 90000 g

   # Modified values:
   #
   # age = 35 a
   # height = 190 cm
   # weight = 90 kg

Custom units
------------

Similarly as in case of references, it is also possible to define new units directly in the DIP code. This can be achieved by a special node directive ``$unit``.

.. code-block:: DIPSchema
   :caption: Schema of a custom unit definition
	     
   <indent>$unit <name> = <value> <unit>  # if value is a number
   <indent>$unit <name> = <value>         # if value is reference, or expression

Names of the custom units are automatically wrapped into square brackets.
If the name of a custom unit is already used, the code will raise an error.

.. code-block:: DIP

   $unit mass = 30 AU
   $unit length = 10 pc
   $unit time = 1 Gy

   velocity float = 2 [length]/[time]
   density float = 34 [mass]/[lenght]3

Units can also be defined outside the code using ``DIP::add_unit()`` method before code is parsed:

.. code-block:: python

   >>> with DIP() as dip:
   >>>     dip.add_unit("length", 1, "m")
   >>>     dip.add_string("""
   >>>     width float = 23 [length]
   >>>     """)
   >>>     env = dip.parse()
