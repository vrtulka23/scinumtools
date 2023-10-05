Integration with other libraries
================================

One of the advantage of this module is that it supports calculations with NumPy arrays and Decimal precision libraries.
In this section we describe the extent into which these libraries can be used and which operations are supported.

NumPy arrays
""""""""""""
   
As discussed in previous sections, ``Quantity`` and ``Magnitude`` classes can be initialized with scalar and list/array value.
The later are converted automatically into NumPy arrays, where all members of the array share common units.
Quantities with array magnitudes can be sliced in the same way as NumPy arrays.
   
.. code-block::

   >>> q = Quantity([1,2,3], 'm')
   >>> q[:2]
   Quantity([1. 2.] m)
   
Numpy ``np.nan`` type can be also used as a quantity with units.

.. code-block::

   >>> Quantity(np.nan, 'm')
   Quantity(nan m)
   >>> NaN('cm')
   Quantity(nan cm)
   
Basic arithmetic operations of array quantities with their modifications are summarized in the table below.

.. csv-table:: Operation with operators
   :widths: 30 80
   :header-rows: 1
   
   Operation,   Notes
   "+, -",      "Only quantities with the same units can be added/subtracted. Units of the first quantity is preserved."
   "\*, /",     "Quantity units are multiplied/divided and form new units."
   "\*\*",      "Both magnitude and units are raised on the dimensionless power."   

.. code-block::

   >>> from scinumtools.units import *
   >>> Quantity([2,3,4], 'm') + Quantity(2, 'cm')
   Quantity([2.02 3.02 4.02] m)
   >>> Quantity([2,3,4], 'm')**2
   Quantity([ 4.  9. 16.] m2)

Available NumPy universal functions ``ufunc`` that can be used with quantities are give below.

.. csv-table:: Operations with universal functions
   :widths: 30 80
   :header-rows: 1
   
   Operation,   Notes
   np.sqrt,     "Unit exponents are divided by 2."
   np.cbrt,     "Unit exponents are divided by 3."
   np.power,    "Unit exponents are raised on the given power."
   "np.sin, np.cos, np.tan", "Input quantity must be convertible to radians and output quantity is dimensionless."
   "np.arcsin, np.arccos, np.arctan", "Input quantity is dimensionless and output quantity is in radians."
   "np.isnan, np.isnat", "Returns booleans"
   
.. code-block::
   
   >>> import numpy as np
   >>> np.sqrt(Quantity([4, 9, 16], 'm3'))
   Quantity([2. 3. 4.] m3:2)
   >>> np.sin(Quantity([45, 60], "deg"))
   Quantity([0.707 0.866])
   
Several other important NumPy functions are also integrated.


.. csv-table:: Operations with functions
   :widths: 30 80
   :header-rows: 1
   
   Operation,   Notes
   np.linspace, "Units of the first quantity-argument are preserved"
   np.logspace, "Units of the first quantity-argument are preserved"
   "np.absolute, np.abs", "Units of an argument are preserved"
   "np.round, np.floor, np.ceil", "Units of an argument are preserved"
   "np.iscomplexobj", "Returns false"
   
.. code-block::

   >>> np.linspace(0,Quantity(23,'km'),3)
   Quantity([ 0.  11.5 23. ] km)
   >>> np.floor(Quantity(2.3,'m'))
   Quantity(2.000e+00 m)
   
More NumPy functions and operations can be implemented on demand. Please write an issue on GitHub and check out source code for new changes.
   
Decimal prescision
""""""""""""""""""

Quantity magnitudes have default precision of the Python's ``float`` type or that of a NumPy array.
Calculations with higher precision are possible in combination with ``Decimal`` library.
As required by the library, all subsequent calculations must be done using ``Decimal`` values.

.. code-block::

   >>> from decimal import Decimal
   >>> Quantity(Decimal(2.34234923498499399204), 'cm')
   Quantity(2.342e+0 cm)
   >>> a = Quantity(Decimal(3.3239840203948394e-3), 'cm')
   >>> b = Quantity(Decimal(9.9239000409020932894e6), 'cm')
   >>> a+b 
   Quantity(9.924e+6 cm)
   >>> (a+b).value() 
   Decimal('9923900.044226077073258914050')
   >>> a*b
   Quantity(3.299e+4 cm2)
   >>> (a*b).value()
   Decimal('32986.88515595424986253677220')
