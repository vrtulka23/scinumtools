Data types
==========

In this section we describe standard and derived data types that can be used in DIP code.

Standard data types
-------------------

DIP uses defaultly a set of 4 basic data types.
Below is an overview of possible scalar values for each of them:

**Boolean** (``bool``)

.. code-block:: DIP 

   day bool = true
   night bool = false

**Integer** (``int``, signed 32-bit)

.. code-block:: DIP

 year int = 2023
     
**Float** (``float``, 64-bit)

.. code-block:: DIP

   duration float = 10              # integer form
   weight float = 23.3              # floating form
   distance float = 2.3e20          # scientific form
  
**String** (``str``)

.. code-block:: DIP

   name str = John                  # single word
   city str = 'New York'            # multiple words
   country str = "United Kingdoms"  # multiple words
   
Derived data types
------------------

When DIP is parsing parameters for low level programming languages (e.g. C/C++ and Fotran), it is sometimes necessary to closely specify which precision float and integer values have.
This can be done using derived data types.
Such data types are internally identical to their standard counterparts, however, they carry additional information about their sign (``int``) and precision (both ``int`` and ``float``).
The table below gives a list of all standard and corresponding derived data types that can be used in DIP.

.. csv-table:: List of standard and derived data types
   :widths: 20 60
   :header-rows: 1
   
   Standard, Derived
   "``int``",      "``int16``, ``int32``, ``int64``, ``uint16``, ``uint32``, ``uint64``"
   "``float``",    "``float32``, ``float64``, ``float128``"
   
Information about sign and precision is stored both in DIP node and type objects.

.. code-block::

    >>> with DIP() as p:
    >>>     p.add_string("""
    >>>     unsignedLongInteger uint64 = 29349850209348495020394849
    >>>     """)
    >>>     env = p.parse()
    >>> data = env.data(Format.TYPE)
    >>> data['unsignedLongInteger'].unsigned
    true
    >>> data['unsignedLongInteger'].precision
    64