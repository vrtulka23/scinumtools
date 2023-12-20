Example of use
==============

The main implementation of DIP is written in Python.
For implementations in other languages, look into corresponding documentations.

A first step to parse a DIP code is to import its main class ``DIP``.

.. code-block:: python

   >>> from scinumtools.dip import DIP, Format
   
Multiple code sources (from strings, or files) can be loaded and combined into one parameter list.
Files containing DIP code should have an extension ``.dip``, otherwise they will be interpreted as normal text files.

.. code-block:: DIP
   :caption: settings.dip

   runtime
     t_max float = 10 ns
     timestep float = 0.01 ns

   box
     geometry int = 3
     size
       x float = 10 nm
       y float = 3e7 nm

   modules
     heating bool = false
     radiation bool = true

Parsing DIP code
----------------
     
It is recommended to create DIP objects using ``with`` statement.

.. code-block:: python

   >>> with DIP() as dip:            # create DIP object
   >>>     dip.add_string("""           
   >>>     mpi
   >>>       nodes int = 36
   >>>       cores int = 96
   >>>     """)                      # get code from a string
   >>>     env1 = dip.parse()        # parse the code

Parsed nodes, sources and units are stored in an environment object of class ``Environment``. This object can be easily transferred into a new instance of ``DIP`` and immediately used without additional parsing. 

.. code-block:: python

   >>> with DIP(env1) as dip:              # pass environment to a new DIP instance
   >>>     dip.add_file("settings.dip").  # add new parameter
   >>>     env2 = dip.parse()              # parse new parameters
       
.. note::

   In the example above, we actually use DIP code from file `settings2.dip <https://github.com/vrtulka23/scinumtools/blob/main/tests/dip/examples/settings2.dip>`_ that includes datatypes.

Getting parsed data
-------------------
       
Particular nodes can be selected using :doc:`references <../syntax/references>`.

.. code-block:: python
       
   >>> nodes = env2.nodes.query("mpi.*")                       # select nodes using a query method
   >>> nodes = env2.nodes.query("runtime.*", tags=['step'])    # refine selection using tags
   >>> geom = env2.request("?box.geometry")                    # select a node using a request method
   >>> geom = env2.request("?runtime.*", tags=['step'])        # refine selection using tags

In the example above, variable ``nodes`` is a list of two nodes: ``mpi.nodes`` and ``mpi.cores``.
The variable ``geom`` is a list with only one node ``box.geometry`` that was loaded from a file ``settings.dip``.
Additionally one can select nodes according to their tags.

.. code-block:: 

   nodes = env2.nodes.query("mpi.*", tags=['step'])

All environmental data can be parsed as a dictionary.

.. code-block:: python

   >>> # Values are returned as Python datatypes
   >>> env2.data()
   {
      'mpi.nodes':         36,
      'mpi.cores':         96,
      'runtime.t_max':     10,
      'runtime.timestep':  0.01,
      'box.geometry':      3,
      'box.size.x':        10,
      'box.size.y':        3e7,
      'modules.heating':   False,
      'modules.radiation': True,
   }
   >>> # Numbers with units are returned as tuples
   >>> env2.data(Format.TUPLE)
   {
      'mpi.nodes':         36,
      'mpi.cores':         96,
      'runtime.t_max':     (10, 'ns'),
      'runtime.timestep':  (0.01, 'ns'),
      'box.geometry':      3,
      'box.size.x':        (10, 'nm'),
      'box.size.y':        (3e7,'nm'),
      'modules.heating':   False,
      'modules.radiation': True,
   }
   >>> # Numbers are returned as Quantity objects
   >>> env2.data(Format.QUANTITY)
   {
      'mpi.nodes':         Quantity(36),
      'mpi.cores':         Quantity(96),
      'runtime.t_max':     Quantity(10, 'ns'),
      'runtime.timestep':  Quantity(0.01, 'ns'),
      'box.geometry':      Quantity(3),
      'box.size.x':        Quantity(10, 'nm'),
      'box.size.y':        Quantity(3e7, 'nm'),
      'modules.heating':   False,
      'modules.radiation': True,
   }
   >>> # Values are returned as DIP datatypes
   >>> env2.data(Format.TYPE)
   {
      'mpi.nodes':         IntegerType(36),
      'mpi.cores':         IntegerType(96),
      'runtime.t_max':     FloatType(10, 'ns'),
      'runtime.timestep':  FloatType(0.01, 'ns'),
      'box.geometry':      IntegerType(3),
      'box.size.x':        FloatType(10, 'nm'),
      'box.size.y':        FloatType(3e7, 'nm'),
      'modules.heating':   BooleanType(False),
      'modules.radiation': BooleanType(True),
   }
   
Besides specifying output format, it is also possible to select specific nodes using ``query`` or ``tag`` selectors:

.. code-block:: python

   >>> env2.data(query="mpi.*")                # selects all nodes in the mpi group
   >>> env2.data(tags=['step'])                # selects all nodes with corresponding tags
   >>> env2.data(query="mpi.*", tags=['step']) # combination of a query and tag selectors

Definitions
-----------

Often code users can modify initial settings in order to choose functionality of a code to what they currently need.
DIP gives code developers a tool to manage such input parameter lists and control what parameters are compulsory or mandatory and what is their format.
In the following example, we first create a definition file with description of all input parameters of a fictional numerical code:

.. code-block:: DIP
   :caption: definitions.dip

   $source settings = settings.dip

   runtime
     t_max float s                 # mandatory
       !condition ("{?} > 0")
     timestep float s
       !condition ("{?} < {?runtime.t_max} && {?} > 0")  # mandatory
     {settings?runtime.*}

   box
     geometry int = {settings?box.geometry}  # mandatory
       = 1  # linear
       = 2  # cylindrical
       = 3  # spherical

     size
       x float cm                  # mandatory
	 !condition ("{?} > 0")
       @case ("{?box.geometry} > 1")
	 y float cm                # mandatory if geometry is non-linear
	   = 3 cm
	   = 4 cm
       @end
       @case ("{?box.geometry} == 3")
	 z float = 23 cm           # constant
	   !constant
       @end
       {settings?box.size.*}

   modules
     hydrdynamics bool = true      # optional
     heating bool                  # mandatory
     radiation bool                # mandatory

     {settings?modules.*}

Some nodes in ``definitions.dip`` are constant and some can be modified by user via ``settings.dip`` given above.

Parsing of such DIP code will result in the following:

.. code-block::
   
   >>> with DIP() as dip:
   >>>     dip.add_file('definitions.dip')
   >>>     env3 = dip.parse()
   >>>     env3.data(format=Format.TYPE)
   {
      'runtime.t_max':        FloatType(1e-08, 's'),
      'runtime.timestep':     FloatType(1e-11, 's'),
      'box.geometry':         IntegerType(3),
      'box.size.x':           FloatType(1e-06, 'cm'),
      'box.size.y':           FloatType(3.0, 'cm'),
      'box.size.z':           FloatType(23.0, 'cm'),
      'modules.hydrdynamics': BooleanType(True),
      'modules.heating':      BooleanType(False),
      'modules.radiation':    BooleanType(True)
   }

.. note::

   An important feature of DIP is, that it automatically converts units from user modifications to definition units. E.g. user set ``box.size.x`` in ``nm``, but resulting value is given in definition units of ``cm``.
   
Quick use
---------

In all examples above we showed how to parse DIP code using ``DIP`` class.
Nevertheless, this approach might feel impractical and lengthy when one wants to use DIP language for simple configuration files, or as a data parser.
For this purpose we wrapped basic functionality of ``DIP`` class into a lightweight `Python module <https://github.com/vrtulka23/dipl>`_ called ``dipl``.
It implements ``load()`` and ``dump()`` methods similarly as e.g. YAML (``import yaml``) or TOML (``import toml``) modules.

Below is a small example how to parse data from DIP code into a Python dictionary:

.. code-block:: python

   >>> import dipl
   >>> from dipl import Format
   >>>
   >>> text = """
   >>> width float = 23.34 cm
   >>> age int = 23 yr
   >>>   !tags ["body"]
   >>> """
   >>> dipl.load(text, Format.QUANTITY)
   {
     'width': Quantity(23.34, 'cm'),
     'age': Quantity(23, 'yr'),
   }

Parsing Python dictionaries into a DIP code is also possible:

.. code-block:: python

   >>> import dipl
   >>> import numpy as np
   >>> from scinumtools.units import Quatity
   >>>
   >>> data = {
   >>>     'body': {
   >>>         'width': Quantity(172.34, 'cm'),
   >>>         'age': (23, 'yr'),
   >>>     },
   >>>     'married': True,
   >>>     'name': "John",
   >>>     'kids': ["Alice","Williams"],
   >>>     'lucky_numbers': np.array([23, 34, 5]),
   >>> }
   >>> dipl.dump(data)
   body
     width float = 172.34 cm
     age int = 23 yr
   married bool = true
   name str = "John"
   kids str[2] = ["Alice","Williams"]
   lucky_numbers int[3] = [23,34,5]