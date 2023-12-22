Parameter parsing
=================

DIP code is used both: for definition of parameters by a code developer and for their modification by a code user.
The definitions and modifications can be composed together and parsed as a parameter list that is later used by the code.

The ``DIP`` class has following methods that can be used to combine various parts of DIP code together and parse resulting parameters.

.. csv-table:: Methods of ``DIP`` class
   :header-rows: 1
   
   Method, Description
   "add_string(code:str)", "adds DIP code from a string"
   "add_file(filepath:str, source_name:str, absolute:bool)", "adds DIP code from a file"
   "add_source(name:str, path:str)", "adds a custom source"
   "add_unit(name:str, value:float, unit:str)", "adds a custom unit"
   "add_function(name:str, fn:Callable)", "adds a custom function"
   "parse()", "parse parameter environment"
   "parse_docs()", "parse documentation environment"

Direct modifications
--------------------

Consider the following parameter definition file of a generic astrophysical numerical code

.. code-block:: DIP
   :caption: definitions.dip

   module
     hydrodynamics bool = true
     radiation bool = false
     gravitation bool = false
     
   simulation_box
     grid str = "cartesian"
       = "cartesian"
       = "cylindrical"
       = "spherical"
     size float = 2 Mpc

and a modification file created by its user

.. code-block:: DIP
   :caption: modifications.dip

   module.radiation = true
   module.gravitation = true
   simulation_box.size = 5 Mpc

The final set of parameters can be obtained by parsing these two files together:

.. code-block::

   >>> from scinumtools.dip import DIP
   >>> 
   >>> with DIP() as dip:
   >>>     dip.add_file('definitions.dip')
   >>>     dip.add_file('modifications.dip')
   >>>     env = dip.parse()

Parsed parameters can be then obtained in a form of a Python dictionary, while several output formats are available:

.. code-block::

   >>> from scinumtools.dip.settings import Format
   >>>
   >>> # Values are returned as Python datatypes
   >>> env.data()
   {
   'module.hydrodynamics': True, 
   'module.radiation': True, 
   'module.gravitation': True, 
   'simulation_box.grid': 'cartesian', 
   'simulation_box.size': 5.0
   }
   >>> # Numbers with units are returned as tuples
   >>> env.data(Format.TUPLE)
   {
   'module.hydrodynamics': True, 
   'module.radiation': True, 
   'module.gravitation': True, 
   'simulation_box.grid': 'cartesian', 
   'simulation_box.size': (5.0, 'Mpc')
   }
   >>> # Numbers are returned as Quantity objects
   >>> env.data(Format.QUANTITY)
   {
   'module.hydrodynamics': True, 
   'module.radiation': True, 
   'module.gravitation': True, 
   'simulation_box.grid': 'cartesian', 
   'simulation_box.size': Quantity(5.000e+00 Mpc)
   }
   >>> # Values are returned as DIP datatypes
   >>> env.data(Format.TYPE)
   {
   'module.hydrodynamics': BooleanType(True), 
   'module.radiation': BooleanType(True), 
   'module.gravitation': BooleanType(True), 
   'simulation_box.grid': StringType(cartesian), 
   'simulation_box.size': FloatType(5.0 Mpc)
   }

Modifications using references
------------------------------

References and branching in DIP files bring an additional level of complication to the parameter parsing. In the case below, some of the nodes (e.g. box dimensions) depend on user settings.

.. code-block:: DIP
   :caption: definitions.dip

   module
     hydrodynamics bool = true
     radiation bool = false
     gravitation bool = false
     {mods?module.*}
     
   simulation_box
     grid str = {mods?simulation_box.grid}
       = "cartesian"
       = "cylindrical"
       = "spherical"
     size float = {mods?simulation_box.size} Mpc
     @case ("{?simulation_box.grid}=='cartesian'")
       size.x float = {?simulation_box.size} Mpc
       size.y float = {?simulation_box.size} Mpc
       size.z float = {?simulation_box.size} Mpc
     @case ("{?simulation_box.grid}=='cylindrical'")
       size.r float = {?simulation_box.size} Mpc
       size.h float = {?simulation_box.size} Mpc
     @else
       size.r float = {?simulation_box.size} Mpc

The definition file cannot be simply modified, as in the previous section. One has to define a modification source first.

.. code-block:: DIP
   :caption: modifications.dip

   module.radiation = true
   simulation_box.grid = "cylindrical"
   simulation_box.size = 5 Mpc
   
Parsing of parameters in this case can be done in the following way:

.. code-block::

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.settings import Format
   >>> 
   >>> with DIP() as dip:
   >>>     dip.add_source('mods','modifications.dip')
   >>>     dip.add_file('definitions.dip')
   >>>     env = dip.parse()
   >>> env.data(Format.TUPLE)
   {
   'module.hydrodynamics': True, 
   'module.radiation': True, 
   'module.gravitation': False, 
   'simulation_box.grid': 'cylindrical', 
   'simulation_box.size': (5.0, 'Mpc'), 
   'simulation_box.size.r': (5.0, 'Mpc'),
   'simulation_box.size.h': (5.0, 'Mpc')
   }
   