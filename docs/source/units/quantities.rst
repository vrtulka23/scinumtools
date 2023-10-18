Quantities
==========

Working with quantities is fairly straightforward and follows similar patters as other Python unit modules:

.. code-block::

   >>> from scinumtools.units import Quantity, Unit, Constant
   >>> 
   >>> height = Quantity(1.85, 'm')
   >>> height

   Quantity(1.850e+00 m)

Units and constants can be used directly in operations with scalar values or ``numpy`` arrays.

.. code-block::

   >>> import numpy as np
   >>> 
   >>> distance = 1.2 * Unit('au')
   >>> velocity = np.array([1,2,3]) * Constant('c')
   >>> distance, velocity

   (Quantity(1.200e+00 au), Quantity([1. 2. 3.] [c]))
   
In the above example, classes ``Unit`` and ``Constant`` are called as functions that return correspondent quantities. 
They can also be initialized as objects, and one can access individual quantities via its parameters.

.. code-block::

   >>> u, c = Unit(), Constant()
   >>> distance = 1.2 * u.au
   >>> velocity = np.array([1,2,3]) * c.c
   >>> distance, velocity

   (Quantity(1.200e+00 au), Quantity([1. 2. 3.] [c]))

In the rest of this documentation, we will give only examples that use the direct quantity initialization using ``Quantity`` class.
Every quantity contains ``magnitude`` and ``baseunits`` part, that can be accessed in a following way:

.. code-block::

   >>> distance = Quantity(2, 'km')
   >>> distance.magnitude             # magnitude in base dimensions (kilometers)
   2.0 
   >>> distance.baseunits             # exponents of base units
   BaseUnits(km=1)

Further on, numerical value of quantity in any base units can be accessed using ``value()`` method:

.. code-block::

   >>> distance.value()               # numerical value in base units (kilometers)
   2.0
   >>> distance.value('cm')           # numerical value in other units (centimeters)
   200000.0

Magnitude
"""""""""

Numerical value of ``Quantity`` is managed by a class ``Magnitude`` that can be initialized with a numerical value and optionally a measurement error.

Values
------

Magnitude values can be initialized from the following three inputs:

* Scalar values (integers or floats).
  Note that all calculations in this case are converted to float precision

  .. code-block::
  
     >>> Magnitude(1)
     1.000e+00
     >>> Magnitude(1).value()
     1.0

* Decimal values
  As in the above case, all subsequent calculations are converted to Decimal precision
  
  .. code-block::
  
     >>> from decimal import Decimal
     >>> Magnitude(Decimal(3))
     3.000e+0

* Lists of values or NumPy arrays.
  In both cases, the values are converted into NumPy arrays and can be used accordingly.

  .. code-block::
  
     >>> Magnitude([1.3, 4.53455, 23.3])           
     [ 1.3    4.535 23.3  ]
     >>> import numpy as np
     >>> Magnitude(np.array([1.3, 4.53455, 23.3]))     
     [ [ [ 1.3    4.535 23.3  ]

Corresponding quantities can be initialized in the following way:

.. code-block::

   >>> Quantity(1, 'cm')
   Quantity(1.000e+00 cm)                                                                                                                              
   >>> Quantity(Decimal(3), 'cm')
   Quantity(3.000e+0 cm)
   >>> Quantity([1.3, 4.53455, 23.3], 'cm')
   Quantity([ 1.3    4.535 23.3  ] cm)
   
Numerical values of quantities are retrieved as:

.. code-block::

   >>> Quantity(1, 'cm').value()
   1.0

Errors
------

``Magnitude`` class can be initialized with either absolute, or relative uncertainties.
Relative uncertainties are converted into their absolute equivalents, and errors are propagated in this form in all subsequent calculations.
Currently, errors are propagated only during addition, subtraction, multiplication, division and power operations.
Propagation of errors in other mathematical functions may be implemented in the future versions of ``scinumtools``.

* Absolute errors are given as numerical values

  .. code-block::

     >>> Magnitude(23, 0.34)
     2.300(34)e+01
     >>> Magnitude(23, abse=0.34)
     2.300(34)e+01

* Relative errors are given in percentages

  .. code-block::
  
     >>> Magnitude(23, rele=10)
     2.30(23)e+01

Corresponding quantities can be initialized in the following way:

.. code-block::

   >>> Quantity(23, 'cm', abse=0.34)
   Quantity(2.300(34)e+01 cm)
   >>> Quantity(23, 'cm', rele=10)        
   Quantity(2.30(23)e+01 cm)
   
Errors can be additionally obtained from, and set to ``Magnitude`` and ``Quantity`` objects using ``rele()`` and ``abse()`` methods:

.. code-block::

   >>> Magnitude(23).rele(10)
   2.30(23)e+01
   >>> Magnitude(23, rele=10).rele()
   10.0
   >>> Quantity(23, 'cm').abse(0.34)
   Quantity(2.300(34)e+01 cm)
   >>> Quantity(23, 'cm', abse=0.34).abse()
   0.34

Base units
""""""""""

``baseunits`` determine units of the quantity magnitude. If no base units are provided, the quantity is dimensionless.
Base units and their corresponding exponents are managed by ``BaseUnits`` class.
This can be initialized using:

* String expressions

  .. code-block::
  
     >>> BaseUnits('kg*m2/s2')
     BaseUnits(kg=1 m=2 s=-2)
     
* Dictionary with pairs of ``unitid`` and exponents.
  Note that unit prefixes in ``unitid`` need to be separated from the unit symbol by a colon sign.
     
  .. code-block::
  
     >>> BaseUnits({'k:g':1, 'm':2, 's':-2})
     BaseUnits(kg=1 m=2 s=-2)
     
* List/array of dimension exponents.
  Note that this type of initialization can be used only on units that consist of basic dimensions.
  More complex units and their derivates need to be initialized by the other two methods.

  .. code-block::
  
     >>> BaseUnits([2,1,-2,0,0,0,0,0])
     BaseUnits(m=2 g=1 s=-2)
     >>> BaseUnits(Dimensions(m=Fraction(2),g=Fraction(1),s=Fraction(-2)))
     BaseUnits(m=2 g=1 s=-2)
     
Values of ``BaseUnits`` can be obtained in three different forms:

* String expression

  .. code-block::

     >>> bu = BaseUnits('kg*m2/s2')     
     >>> bu.expression
     'kg*m2*s-2'

* Dictionary with pairs of ``unitid`` and exponents

  .. code-block::
  
     >>> bu.value()
     {'k:g': 1, 'm': 2, 's': -2}

* Combination of total dimension and magnitude

  .. code-block::
  
     >>> bu.dimensions
     Dimensions(m=Fraction(2) g=Fraction(1) s=Fraction(-2))
     >>> bu.magnitude
     1000.0
     
Corresponding initialization of ``Quantity`` class is:

.. code-block::

   >>> Quantity(23, 'km*m2/s2')
   Quantity(2.300e+01 km*m2*s-2)
   >>> Quantity(23, [2,1,-2,0,0,0,0,0])
   Quantity(2.300e+01 m2*g*s-2)
   >>> Quantity(23, {'k:g':1, 'm':2, 's':-2})
   Quantity(2.300e+01 kg*m2*s-2)

One can also get values of base units directly from the ``Quantity`` object:

.. code-block::

   >>> q = Quantity(23, 'km*m2/s2') 
   >>> q.baseunits.expression
   'km*m2*s-2'
   >>> q.baseunits.value()
   {'k:m': 1, 'm': 2, 's': -2}
   >>> q.baseunits.magnitude
   1000.0
   >>> q.baseunits.dimensions
   Dimensions(m=Fraction(3) s=Fraction(-2))

Fractional exponents
--------------------

Exponents stored both in ``BaseUnits`` and ``Dimensions`` classes do not need to be only integers.
In fact, all exponents are converted automatically into a fractional form using class ``Fraction``.
Fraction objects store nominator and denominator and the expressions are automatically displayed in the most basic form:

.. code-block::

   >>> Fraction(1)      # setting only numerator   
   1
   >>> Fraction(4,8)    # setting both numerator and denominator
   1:2
   >>> Fraction.from_tuple((0,3))   # setting as a tuple
   0
   >>> Fraction.from_string('2:3')  # setting as a string
   2:3

As seen above, values of fractions are printed in a textual form, where the colon sign divides nominator and denominator part of the fraction value.
Fractions with a unit denominator display only their nominator.
Fractions with a zero nominator are displayed as zero and their denominator is set automatically to unity.

Tuple notation of fractions is used as a shorthand during ``Quantity``, ``BaseUnits``, or ``Dimensions`` initialization.

.. code-block::

   >>> Quantity(3, {'k:g':(1,2)})
   Quantity(3.000e+00 kg1:2)
   >>> BaseUnits([(2,3),1,-2,0,0,0,0,0])
   BaseUnits(m=2:3 g=1 s=-2)
   >>> Dimensions(m=Fraction(2,3))
   Dimensions(m=2:3)

Dimensions
----------

Class ``Dimensions`` used above stores exponents of the unit dimensions (i.e. ``m``, ``g``, ``s``, ``K``, ``C``, ``cd``, ``mol`` and ``rad``).
Manipulation with this class is straightforward:

.. code-block::

   >>> d = Dimensions(m=Fraction(2), g=Fraction(1,2), s=Fraction(-2))
   >>> d.value()
   [2, (1,2), -2, 0, 0, 0, 0, 0]
   >>> Dimensions.from_list([3, (3,2), 0, 0, 0, 0, 0, 0])
   Dimensions(m=3 g=3:2)
   
