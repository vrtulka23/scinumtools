Example of use
==============

The main implementation of DIP is written in Python.
For implementations in other languages, look into corresponding documentations.

A first step to parse a DIP code is to import its main class ``DIP``.

.. code-block:: python

   from dipsl import DIP
   from dipsl.settings import Format
   
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

   with DIP() as dip:            # create DIP object
       dip.from_string("""           
       mpi
	 nodes int = 36
	 cores int = 96
       """)                      # get code from a string
       env1 = dip.parse()        # parse the code

Parsed nodes, sources and units are stored in an environment object of class ``Environment``. This object can be easily transferred into a new instance of ``DIP`` and immediately used without additional parsing. 

.. code-block:: python

   with DIP(env1) as dip:              # pass environment to a new DIP instance
       dip.from_file("settings.dip")        # add new parameter
       env2 = dip.parse()              # parse new parameters

Getting parsed data
-------------------
       
Particular nodes can be selected using :doc:`references <../syntax/references>`.

.. code-block:: python
       
   nodes = env2.query("mpi.*")            # select nodes using a query method
   geom = env2.request("?box.geometry")   # select a node using a request method

In the example above, variable ``nodes`` is a list of two nodes: ``mpi.nodes`` and ``mpi.cores``.
The variable ``geom`` is a list with only one node ``box.geometry`` that was loaded from a file ``settings.dip``.

All environmental data can be parsed as a dictionary.

.. code-block::

   # Values are returned as Python datatypes
   data = env2.data()

   # data = {
   #     'mpi.nodes': 36,
   #     'mpi.cores': 96,
   #     'runtime.t_max': 10,
   #     'runtime.timestep': 0.01,
   #     'box.geometry': 3,
   #     'box.size.x': 10,
   #     'box.size.y': 3e7,
   #     'modules.heating': False,
   #     'modules.radiation': True,
   # }

   # Same as above, but umbers with units are returned as tuples
   data = env2.data(format=Format.TUPLE)

   # data = {
   #     'mpi.nodes': 36,
   #     'mpi.cores': 96,
   #     'runtime.t_max': (10, 'ns'),
   #     'runtime.timestep': (0.01, 'ns'),
   #     'box.geometry': 3,
   #     'box.size.x': (10, 'nm'),
   #     'box.size.y': (3e7,'nm'),
   #     'modules.heating': False,
   #     'modules.radiation': True,
   # }
   
   # Values are returned as DIP datatypes
   data = env2.data(format=Format.TYPE)

   # data = {
   #     'mpi.nodes': IntegerType(36),
   #     'mpi.cores': IntegerType(96),
   #     'runtime.t_max': FloatType(10, 'ns'),
   #     'runtime.timestep': FloatType(0.01, 'ns'),
   #     'box.geometry': IntegerType(3),
   #     'box.size.x': FloatType(10, 'nm'),
   #     'box.size.y': FloatType(3e7, 'nm'),
   #     'modules.heating': BooleanType(False),
   #     'modules.radiation': BooleanType(True),
   # }

Definitions
-----------

Often code users can modify initial settings in order to choose functionality of a code to what they currently need.
DIP gives code developers a tool to manage such input parameter lists and control what parameters are compulsory or mandatory and what is their format.
In the following example, we first create a definition file with description of all input parameter of a fictional numerical code:

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

Some nodes in ``definitions.dip`` are constant and some can be modified by user via ``settings.dip``.
Parsing of such DIP code will result in the following:

.. code-block::
   
   with DIP() as dip:
       dip.from_file('definitions.dip')
       env3 = dip.parse()
       data = env.data(format=Format.TYPE)

   # data = {
   #     'runtime.t_max':        FloatType(1e-08, 's'),
   #     'runtime.timestep':     FloatType(1e-11, 's'),
   #     'box.geometry':         IntegerType(3),
   #     'box.size.x':           FloatType(1e-06, 'cm'),
   #     'box.size.y':           FloatType(3.0, 'cm'),
   #     'box.size.z':           FloatType(23.0, 'cm'),
   #     'modules.hydrdynamics': BooleanType(True),
   #     'modules.heating':      BooleanType(False),
   #     'modules.radiation':    BooleanType(True)
   # }

.. note::

   An important feature of DIP is, that it automatically converts units from user modifications to definition units. E.g. user set ``box.size.x`` in ``nm``, but resulting value is given in definition units of ``cm``.
   
Templates
---------

Sometimes numerical codes require additional input parameter files with a special format or even defined in another programming language.

.. code-block:: rst
   :caption: template.txt

   Geometry: {{?box.geometry}}
   Box size: [{{?box.size.x}}, {{?box.size.y}}, {{?box.size.z}}]


Such files can be easily generated by processing of a DIP environment with a template solver.

.. code-block:: python

   from dipsl.solvers import TemplateSolver
   
   with TemplateSolver(env3) as ts:
       text = ts.template('template.txt','processed.txt')

Template solver in the example above will use the given environment ``env3``, reads template from ``template.txt`` and parses corresponding node values into file ``processed.txt``.

.. code-block:: rst
   :caption: processed.txt

   Geometry: 3
   Box size: [1e-06, 3.0, 23.0]

.. note::
   
   This is especially useful when using DIP with codes written in other programming languages, since DIP currently natively supports only programs written in Python.
   Nevertheless, support of other programming languages will be added later.
   
