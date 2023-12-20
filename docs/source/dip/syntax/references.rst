References
==========

Node referencing is an important feature of DIP, because it enables to create reusable parts of a code.
Reference is similar to a standard URL **requests**.
It consist of a source name (path to a file) and a query (node path) part, separated by a question mark.
Sources are defined once using ``$source`` definition and can be referenced multiple times.

.. code-block:: DIPSchema
   :caption: Schema of a source definition

   <indent>$source <name> = <path>

It is also possible to define sources outside a DIP code using ``DIP::add_source()`` method before code parsing:

.. code-block:: python

   >>> with DIP() as dip:
   >>>     dip.add_source("settings", 'settings.dip')
   >>>     dip.add_string("""
   >>>     x_size float = {settings?box.size.x}
   >>>     """)
   >>>     env = dip.parse()

Source paths are relative to the calling script if code is parsed using ``DIP::add_string()``, or ``DIP::add_source()``. Sources defined in DIP files have path relative to the corresponding DIP file.
   
Depending on a context, **sources** can be either simple text files (references without query) or DIP files (references with, or without query).
A local domain contains all nodes that were already parsed in the current DIP file.
Remote domain is a completely separate DIP file that is processed independently.
   
**Query** part specifies which nodes from local or remote DIP files will be selected.
A single node is queried by its full hierarchy path.
An asterix at the end of the query selects children nodes:

.. code-block:: DIPSchema
   :caption: Schema of reference requests

   # content of a source is returned
   {<source>}                     # remote
	     
   # single node is returned
   {?<query>}                     # local
   {<source>?<query>}             # remote

   # children nodes are returned
   {?<query>.*}                   # local
   {<source>?<query>.*}           # remote

   # all nodes are returned
   {?*}                           # local
   {<source>?*}                   # remote

   # node self-reference
   {?}                            # local
   
.. note::
   
   The last reference type ``{?}`` is used only in :doc:`condition properties <properties>` to reference the node's own value.  
   
References have two main applications.
One can either import some already parsed DIP nodes into a new location, or inject other node values or contents of text files into a new node.
Besides the two cases, references are also used in :doc:`conditions <conditions>` that are explained in a separate chapter.
		      
Imports
-------

Imports can be used to insert referenced nodes directly into the current DIP hierarchy.

.. code-block:: DIPSchema
   :caption: Schema of node imports

   <indent>{<request>}
   <indent><name> {<request>}

Name paths of imported nodes are embedded into the current node hierarchy as shown in the following examples.


.. code-block:: DIP

   icecream 
     waffle str = 'standard'
     scoops
       strawberry int = 1
       chocolate int = 2

   bowl
     {?icecream.scoops.*}      # select children nodes
   plate {?icecream.waffle}    # select specific node

Code above will result in the following final nodes

.. code-block:: DIP

  icecream.waffle = 'standard'
  icecream.scoops.strawberry = 1
  icecream.scoops.chocolate = 2
  bowl.strawberry = 1
  bowl.chocolate = 2
  plate.waffle = 'standard'

In the example above we import local nodes, however, it works the same also for external DIP files.
One has to just add a source name in front of the question mark.

.. code-block:: DIP
   
   $source nodes = nodes.dip
   
   bag {nodes?*}                # import all
   bowl 
     {nodes?fruits}             # selecting a specific node
     {nodes?vegies.potato}      # selecting a specific subnode
   plate {nodes?vegies.*}       # selecting all subnodes   

So far, we have shown how to import regular nodes from a local or remote source.
It is, however, also possible to import sources and custom :doc:`units` in the similar way.
The request can select either one ``{<source>?<query>}`` or all ``{<source>?*}`` sources/units.

.. code-block:: DIPSchema
   :caption: Schema for importing sources and units
	     
   <indent>$source {<request>}
   <indent>$unit {<request>}

.. note::
   
   Request query is in this case not a node path but name of a source/unit.

Importing sources/units enables users to dynamically modify numerical code units and setting scripts via their DIP.

.. code-block:: DIP

   $source init = initial/settings.dip
   $source {init?*}           # all sources of 'init' are imported
   $unit {units?*}            # all units are imported from an imported source 'units'
   weight float = 23 [mass]   # using imported unit

Injections
----------

Injections do not insert whole nodes.
They are used in node definitions and modifications instead of values.

.. code-block:: DIPSchema
   :caption: Schema of node value injections

   <indent><name> <type> = {<request>} <unit>	     
   <indent><name> <type> = {<request>}
   <indent><name> = {<request>} <unit>	     
   <indent><name> = {<request>}

A valid injection can reference only a single node or a text content of a file.

.. code-block:: DIP

   size1 float = 34 cm       # standard definition
   size2 float = {?size1} m  # definition using import with other units
   size3 float = {?size2}    # definition using import with same units
   size1 = {?size2}          # modifying by import

   # Nodes above will have the following values:
   #
   # size1 = 3400 cm
   # size2 = 34 m
   # size3 = 34 m

It is also possible to inject values from remote DIP files:

.. code-block:: DIP
   
   $source pressure = pressures.dip
   
   pressure float = {pressure?magnetic}
   
Arrays can be imported either directly or can be sliced to match dimensions of a host node using the following schemas:

.. code-block:: DIPSchema
   :caption: Schema of an array slice reference

   {?<query>}[<slice>]            # node query from a local domain
   {<source>?<query>}[<slice>]    # node query from a remote domain

Slicing of arrays and also strings adopts the same notation as used in Python.
An example of sliced injected arrays is below:

.. code-block:: DIP

   person str = "Will Smith"
   surname str = {?person}[5:]   # slicing a string

   # selecting a single value
   sizes float[3] = [34,23.34,1e34] cm      
   mysize float = {?sizes}[1]  
   
   # selecting range of values
   masses float[2,2] = [[34,23.34],[1,1e34]] cm    
   mymass float[2] = {?masses}[:,1]              

   # Above nodes will have values:
   #
   # person = "Will Smith"
   # surname = "Smith"
   # sizes = [3.400e+01, 2.334e+01, 1.000e+34]
   # mysize = [2.334e+01]
   # masses = [[34,23.34],[1,1e34]]
   # mymass = [23.34,1e34]


Value injection can also be used to keep large text blocks in external files.
This makes both the code and text data more readable and easily editable.
Note that when requests do not include a question mark with a query, DIP imports files as a text and not as a node list.

.. code-block:: DIP
   
   $source velocity = velocity.txt
   $source outputs = outputs.txt
   $source message = message.txt
   
   velocity int[3,4] = {velocity} km/s   # import an array
   outputs table = {outputs}             # import a table
   message str = {message}               # import a text

Values of source and unit definitions can also be injected from other nodes.

.. code-block:: DIPSchema
   :caption: Schema of node value injections

   <indent>$unit <name> = {<request>}
   <indent>$source <name> = {<request>}
   
.. note::
   In comparison to imports, request query in injections is always path of a node.

This adds an additional scalability to the code.
Referenced nodes by sources have to be strings and referenced nodes by units have to be floats or integers.

.. code-block:: DIP

   refs str = "path/to/sources.dip"  # node named 'refs'
   $source refs = {?refs}            # source named 'refs'

   mass float = 1 kg                 # node named 'mass'
   $unit mass = {?mass}              # unit named 'mass'
