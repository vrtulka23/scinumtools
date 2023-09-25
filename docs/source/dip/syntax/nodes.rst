Nodes
=====

Definition
----------

.. code-block:: DIPSchema
   :caption: Node definition schema

   <indent><name> <type> = <value> <unit> 
   <indent><name> <type> = <value> 

All members of definition are separated with at least one empty space, and their order is not interchangeable.

**Indentation** is at the beginning of a line and it determines node :ref:`hierarchy`.
It can consist of zero or more empty spaces.

Node **names** are formed from letters, numbers, underscores, hyphens and dots.
Dots have a special function, because they separate parent and child node names.

There are four main **data types** in DIP that are based on data types used in Python language: boolean (``bool``), integer (``int``), float (``float``) and string (``str``).
Nevertheless, one can in principle extend the number of data types to match those of e.g. C-language.

Node **values** are separated from left members by an equal sign.
Values without quotes consists only from non-empty characters.
If values consists of empty spaces, it must be wrapped into single or double quotes.
If node value spans over multiple lines, one can use :ref:`blocks`.

The two data types that support **units** are integers and floats.
Units are written directly after a node value and are separated with an empty space.
More detailed description of units is given in a chapter about :doc:`units`.
In this subsection, we only describe basic syntax with respect to the nodes.

**Comments** are always at the end of lines and start with a hash sign.
It is also possible to use comments on empty lines to describe the code.


Modification
------------

.. code-block:: DIPSchema
   :caption: Node modification schema
	     
   <indent><name> <type> = <value> <unit> 
   <indent><name> <type> = <value> 
   <indent><name> = <value> <unit> 
   <indent><name> = <value> 

The first occurrence of a node is called definition.
All subsequent occurrences of a node with the same name are called modifications.
The data type of node needs to be set in each definition, however it can be omitted in subsequent modifications.
If node is a dimensional parameter, units have to be set in a definition.
One can use different units of the same dimension in modifications, however, the final value of the node will always be converted into units set by the definition.

.. code-block:: DIP

   size float = 70 cm    # definition
   size float = 80 cm    # modifying only value
   size = 90 cm          # omitting datatype
   size = 100            # omitting units
   size = 1 pc           # using different units of length

   # size = 3.086e18 cm  # final value

Declaration
-----------

.. code-block:: DIPSchema
   :caption: Node declaration schema
	     
   <indent><name> <type> <unit> 
   <indent><name> <type> 

Declaration in DIP is a special case of definition where equal sign and value is not specified.
The value must be later set in subsequent DIP code using modifications, otherwise code will not be valid.

.. code-block:: DIP

   weight float kg  # declaration
   weight = 88      # modification

.. _hierarchy:

Hierarchy
---------

DIP nodes are organized in a hierarchical way using indentation, i.e. number of empty spaces before nodes.
**Parent** nodes have lower indentation as their **children** nodes.
**Siblings** are nodes which share a common parent and indentation level.
Multiple levels of hierarchy are also allowed, and there can be empty lines between the nodes.
The number of empty spaces for each indentation level can vary, as long as indentation of all children nodes is consistent.

.. code-block:: DIP

   grandfather str = 'John'   # parent of Peter and Cintia
     father str = 'Peter'     # John's child, Cintia's sibling
                              # Ben's and Lucia's parent
       son str = 'Benjamin'   # Peter's child
       daughter str = 'Lucia' # Peter's child
     aunt str = 'Cintia'      # John's child, Peter's sibling

Both parent and children nodes can be either definitions, modifications or declarations.
Besides that, nodes can be arranged using another type of node called *group* node.

.. code-block:: DIPSchema
   :caption: Group node schema
	     
   <indent><name> 

Group nodes do not carry any value, nor do they declare any parameter for further use.
Their function is to group multiple child nodes into a logical structure and their name enters the final node path.

After parsing of nodes, their names are transformed into a path that consists of the original name plus all parent names in the hierarchy separated by a dot.
The original node name can already be a path and will be parsed accordingly.

.. code-block:: DIP

   family                          # group is not parsed
     father str = 'Peter'          
       son str = 'Benjamin'        # normal notation
     father.daughter str = 'Lucia' # using both normal and path notation
   family.aunt.dog str = 'Lassie'  # using only path notation
   
The example above will result in the following final parameters:

.. code-block:: DIP
   
   family.father = 'Peter'
   family.father.son = 'Benjamin'
   family.father.daughter = 'Lucia'
   family.aunt.dog = 'Lassie'
