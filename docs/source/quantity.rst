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
They can be also initialized as objects, and one can access corresponding quantities as parameters.

.. code-block::

   >>> u, c = Unit(), Constant()
   >>> distance = 1.2 * u.au
   >>> velocity = np.array([1,2,3]) * c.c
   >>> distance, velocity

   (Quantity(1.200e+00 au), Quantity([1. 2. 3.] [c]))

In the rest of this documentation we will give only examples that use the direct quantity initialization using ``Quantity`` class.
Every quantity contains following data:

``magnitude``

  numerical value of a quantity in base units

``baseunits`` 

  unit base of a quantity.

Both data can be accessed in a following way:

.. code-block::

   >>> distance = Quantity(2, 'km')
   >>> distance.magnitude             # numerical value in base dimensions (meters)
   2000.0 
   >>> distance.baseunits             # exponents of base units
   BaseUnits(km=1)

Further on, numerical value of quantity in base units, dimension and baseunits can be accessed using ``value()`` methods:

.. code-block::

   >>> distance.value()               # numerical value in base units (kilometers)
   2.0
   >>> distance.value('cm')
   200000.0
   >>> distance.baseunits.value()     # dictionary of base units exponents
   {'k:m': 1}
   
Note that value of the quantity is given in units of ``baseunits``. Value of ``basunits`` object are expressed as a Python dictionary, where dictionary keys are individual unit symbols and dictionary values are corresponding exponents. For conveinence, unit prefixes are separated from unit symbols with a colon.
   
Magnitude
"""""""""

Numerical value of ``Quantity`` are encapsuled by a special class ``Magnitude`` that is initialized by some numerical value and optionally an error.

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

Fractional exponents
--------------------

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
