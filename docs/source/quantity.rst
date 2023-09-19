Physical quantities
===================

Class ``Quantity`` and its derivates, ``Unit`` and ``Constant``, can be used in many scientific applications, because they enable easy manipulation and calculations with physical quantities. Among the most interesting features are:

* Concise and regularized unit notation with arbitrary unit prefixes.
* Conversion of units with the same, or inversed dimensionality (SI, CGS, natural units and more...).
* Conversion of temperatures (K, degR, degC, degF).
* Conversion of logarithmic units (dB, Np, dBmW,...).
* Integration with ``numpy`` arrays and functions.
* Usage of float or ``Decimal`` precision.
* ``Quantity`` is a self-content class that does not need initialization in a header, or use of registries. Quantities can be pickled and are compatible when created in different parts of the code.
* Support of fractional powers

All available units, constants and prefixes with their corresponding symbols and definitions are listed in `settings.py <https://github.com/vrtulka23/scinumtools/blob/main/src/scinumtools/units/settings.py>`_. In this text we will refer to them without extensive introduction. List of available units and constants can be also printed using following python command:

.. code-block::

   >>> import scinumtools.units as su
   >>> print(su.Unit())
   Units

   Prefixes:
   
   Symbol   | Prefix               | Definition          
   ---------+----------------------+---------------------
   Y        | yotta                | 1e24                
   Z        | zetta                | 1e21                
   E        | exa                  | 1e18                
   P        | peta                 | 1e15                
   ...
   
   >>> print(su.Constant())
   Constants
   
   Symbol   | Unit                 | Definition          
   ---------+----------------------+---------------------
   [c]      | velocity of light    | 299792458*m/s       
   [h]      | Planck const.        | 6.6260755e-34*J*s   
   [k]      | Boltzmann const.     | 1.380658e-23*J/K    
   [eps_0]  | permit. of vac.      | 8.854187817e-12*F/m 
   ...

All units used by ``Quantity`` are based on 8 fundamental ``dimensions``. These are not identical with any standard metric system (SI, CGS) but conveniently selected for ease of implementation and internal calculations. Six units are physical (``m`` meter, ``g`` gramm, ``s`` second, ``K`` Kelvin, ``C`` Coulomb, ``cd`` candela) and two are numerical (``mol`` mole, ``rad`` radian). Derived units use combinations of these dimensions and a numerical value, magnitude.

Units can be used individually, or combined together using basic mathematical operations. Multiplication is denoted using asterisk symbol ``m*m``, division using slash symbol ``m/s``, integer powers are indicated with a number after the unit ``m2`` (or ``m-2``) and fractional powers are denoted using two numbers separated by a colon ``s3:3`` (or ``s-3:3``). Units can also have a numerical part ``60*s`` (or ``365.25*day``, or ``1.67e-24*g``) and can use parenthesis ``m3/(kg*s2)``. No empty spaces in unit expressions are alowed.

* Units without prefixes: ``g``, ``J``, ``ly``
* Units with prefixes: ``mg``, ``MJ``, ``kly``
* Unit expressions: ``kg*m2/s2``, ``V/(C/s)``, ``1/Hz1:2``

Quantities
^^^^^^^^^^

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
   
In the above example classes ``Unit`` and ``Constant`` are called as functions that return correspondent quantities. 
They can be also initialized as objects, and one can access individual qantities via its parameters.

.. code-block::

   >>> u, c = Unit(), Constant()
   >>> distance = 1.2 * u.au
   >>> velocity = np.array([1,2,3]) * c.c
   >>> distance, velocity

   (Quantity(1.200e+00 au), Quantity([1. 2. 3.] [c]))

In the rest of this documentation we will give only examples that use the direct quantity initialization using ``Quantity`` class.
Every quantity contains ``magnitude`` and ``baseunits`` part, that can be accessed in a following way:

.. code-block::

   >>> distance = Quantity(2, 'km')
   >>> distance.magnitude             # numerical value in base dimensions (meters)
   2000.0 
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

Numerical value of ``Quantity`` is managed by class ``Magnitude`` that can be initialized with a numerical value and optionally a measurement error.

Values
------

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

Corresponding quantities can be initiallized in the following way:

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

``Magnitude`` class can be initialized with both absolute and relative uncertainities.
Relative uncertainities are converted into their absolute equivalents and errors are propagated in this form in all subsequent calculations.
Currently, errors are propagated only during addition, substraction, multiplication, division and power operations.
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
   
Errors can be additionally get from and set to ``Magnitude`` and ``Quantity`` objects using ``rele()`` and ``abse()`` methods:

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
  Note that this type of initialization can be used only on units that consist of basic dimenssions.
  More complex units and their derivates need to be initialized by the other two methods.

  .. code-block::
  
     >>> BaseUnits([2,1,-2,0,0,0,0,0])
     BaseUnits(m=2 g=1 s=-2)
     
Values of ``BaseUnits`` can be obtained in three different forms:

* String expression

  .. code-block::

     >>> bu = BaseUnits('kg*m2/s2')     
     >>> bu.expression()
     'kg*m2*s-2'

* Dictionary with pairs of ``unitid`` and exponents

  .. code-block::
  
     >>> bu.value()
     {'k:g': 1, 'm': 2, 's': -2}

* Base object with dimensions.
  Note that in order to express arbitrary ``BaseUnits`` in terms of unit dimensions, one has to also express its corresponding numerical magnitude.

  .. code-block::
  
     >>> base = bu.base()
     >>> base
     Base(magnitude=1000.0, dimensions=Dimensions(m=2 g=1 s=-2))
     >>> base.dimensions
     Dimensions(m=2 g=1 s=-2)
     >>> base.magnitude
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
   >>> q.baseunits.expression()
   'km*m2*s-2'
   >>> q.baseunits.value()
   {'k:m': 1, 'm': 2, 's': -2}
   >>> q.baseunits.base()
   Base(magnitude=1000.0, dimensions=Dimensions(m=3 s=-2))

Dimensions
----------

Class ``Dimensions`` used above stores exponents of the unit dimensions (i.e. ``m``, ``g``, ``s``, ``K``, ``C``, ``cd``, ``mol`` and ``rad``).
Manimpulation with this class is straightforward:

.. code-block::

   >>> d = Dimensions(m=2, g=1, s=-2)
   >>> d.value()
   [2, 1, -2, 0, 0, 0, 0, 0]

Fractional exponents
--------------------

Exponents stored both in ``BaseUnits`` and ``Dimensions`` classes do not need to be only integers.
In fact, all exponents are converted automatically into a fractional form using class ``Fraction``.
Fraction objects store nominator and denominator and are automatically reduced to the most basic form at the initialization:

.. code-block::

   >>> Fraction(1)      # setting only numerator   
   1
   >>> Fraction(4,8)    # setting both numerator and denominator
   1:2
   >>> Fraction((0,3))  # setting as a tuple
   0

As seen above, values of fractions are printed in a textual form, where colon sign divides nominator and denominator part of the fraction value.
Fractions with a unit denominator display only their nominator.
Fractions with a zero nominator are displayied as zero and their denominator is set automatically to unity.

Tuple notation of fractions is used as a shorthand during ``Quantity``, ``BaseUnits``, or ``Dimensions`` initialization.

.. code-block::

   >>> Quantity(3, {'k:g':(1,2)})
   Quantity(3.000e+00 kg1:2)
   >>> BaseUnits([(2,3),1,-2,0,0,0,0,0])
   BaseUnits(m=2:3 g=1 s=-2)
   >>> Dimensions(m=(2,3))
   Dimensions(m=2:3)

Unit conversions
^^^^^^^^^^^^^^^^

Linear units
""""""""""""

Unit conversion is an integral part of this package. Every quantity can be converted to other units (with the same dimensions) using ``to(<unit>)`` method.

.. code-block::

   >>> distance = Quantity(2, 'km')
   >>> distance.to('m')
   Quantity(2.000e+03 m)

Values of quantities can be casted in different units as well, by specifying new base units.

.. code-block::

   >>> distance.value('cm')
   200000.0
   
Logarithmic units
"""""""""""""""""

Temperature units
"""""""""""""""""

Integration with 3rd party libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NumPy arrays
""""""""""""
   
Decimal prescision
""""""""""""""""""
