Physical quantities
===================

Class ``Quantity`` and its derivates, ``Unit`` and ``Constant``, can be used in many scientific applications, because they enable easy manipulation and calculations with physical quantities. Among the most interesting features of ``Quantity`` are:

* Concise and regularized unit notation with arbitrary unit prefixes.
* Conversion of units with the same, or inversed dimensionality (SI, CGS, natural units and more...).
* Conversion of temperatures (K, degR, degC, degF).
* Integration with ``numpy`` functions.
* ``Quantity`` is a self-content class that does not need initialization in a header, or use of registries. Quantities can be pickled and are compatible when created in different parts of the code.
* Support of fractional powers

All available units, constants and prefixes with their corresponding symbols and definitions are listed in `UnitList.py <https://github.com/vrtulka23/scinumtools/blob/main/src/scinumtools/units/UnitList.py>`_. In this text we will use them without extensive introduction. List of available units and constants can be printed using following python command:

.. code-block::

   >>> import scinumtools as snt
   >>> print(snt.Unit())
   Units

   Prefixes:
   
   Symbol   | Prefix               | Definition          
   ---------+----------------------+---------------------
   Y        | yotta                | 1e24                
   Z        | zetta                | 1e21                
   E        | exa                  | 1e18                
   P        | peta                 | 1e15                
   ...
   
   >>> print(snt.Constant())
   Constants
   
   Symbol   | Unit                 | Definition          
   ---------+----------------------+---------------------
   [c]      | velocity of light    | 299792458*m/s       
   [h]      | Planck const.        | 6.6260755e-34*J*s   
   [k]      | Boltzmann const.     | 1.380658e-23*J/K    
   [eps_0]  | permit. of vac.      | 8.854187817e-12*F/m 

All units used by ``Quantity`` are based on 8 fundamental ``base units``, also called ``dimensions``. These are not identical with any standard metric system (SI, CGS) but conveniently selected for ease of implementation and internal calculations. Six units are physical (``m`` meter, ``g`` gramm, ``s`` second, ``K`` Kelvin, ``C`` Coulomb, ``cd`` candela) and two are numerical (``mol`` mole, ``rad`` radian). Derived units use combinations of these dimensions.

Units can be used individually, or combined together using basic mathematical operations. Multiplication is denoted using asterisk symbol ``m*m``, division using slash symbol ``m/s``, integer powers are indicated with a number after the unit ``m2`` (or ``m-2``) and fractional powers are denoted using two numbers separated by a colon ``s3:3`` (or ``s-3:3``). Units can also have a numerical part ``60*s`` (or ``365.25*day``, or ``1.67e-24*g``) and can use parenthesis ``m3/(kg*s2)``. No empty spaces in unit expressions are alowed.

* Units without prefixes: ``g``, ``J``, ``ly``
* Units with prefixes: ``mg``, ``MJ``, ``kly``
* Unit expressions: ``kg*m2/s2``, ``V/(C/s)``, ``1/Hz1:2``

Quantity definitions
^^^^^^^^^^^^^^^^^^^^

Working with quantities is fairly straightforward and follows similar patters as other Python unit modules:

.. code-block::

   >>> from scinumtools.units import Quantity, Unit, Constant
   >>> 
   >>> height = Quantity(1.85, 'm')
   >>> height

   Quantity(1.850e+00 m)

Units and constants can be used directly in operations with a scalar values or ``numpy`` arrays:

.. code-block::

   >>> import numpy as np
   >>> 
   >>> distance = 1.2 * Unit('au')
   >>> velocity = np.array([1,2,3]) * Constant('c')
   >>> distance, velocity

   (Quantity(1.200e+00 au), Quantity([1. 2. 3.] [c]))
   
In the above example classes ``Unit`` and ``Constant`` are called as functions that return correspondent quantities. They can be also initialized as objects, and one can access corresponding quantities as parameters.

.. code-block::

   >>> u, c = Unit(), Constant()
   >>> distance = 1.2 * u.au
   >>> velocity = np.array([1,2,3]) * c.c
   >>> distance, velocity

   (Quantity(1.200e+00 au), Quantity([1. 2. 3.] [c]))

Every quantity object contains following data:

``dimensions`` (aka. base dimensions)

  exponents of 8 base dimensions (i.e. ``m``, ``g``, ``s``, ``K``, ``C``, ``cd``, ``mol`` and ``rad``)

``magnitude``

  numerical value of a quantity in base dimensions

``baseunits`` (aka. base units, or quantity units)

  actual units of a quantity

This data can be accessed in a following way:

.. code-block::

   >>> distance = Quantity(2, 'km')
   >>> distance.dimensions            # exponents of base dimension
   Dimensions(m=1)
   >>> distance.magnitude             # numerical value in base dimensions (meters)
   2000.0 
   >>> distance.baseunits             # exponents of base units
   BaseUnits(km=1)

Further on, numerical value of quantity in base units, dimension and baseunits can be accessed using ``value()`` methods:

.. code-block::

   >>> distance.value()               # numerical value in base units (kilometers)
   2.0
   >>> distance.dimensions.value()    # list of base dimensions exponents
   [1, 0, 0, 0, 0, 0, 0, 0]
   >>> distance.baseunits.value()     # dictionary of base units exponents
   {'k:m': 1}
   
Note that value of the quantity is given in units of ``baseunits`` instead of ``dimensions``. Value of ``dimensions`` object is represented as a Python list, where integers are exponents of individual base units, respectively. Value of ``basunits`` object are expressed as a Python dictionary, where dictionary keys are individual unit symbols and dictionary values are corresponding exponents. For conveinence, unit prefixes are separated from unit symbols with a colon.
   
Conversion between units
^^^^^^^^^^^^^^^^^^^^^^^^

Unit conversion is an integral part of this package. Every quantity can be converted to other units (with the same dimensions) using ``to(<unit>)`` method.

.. code-block::

   >>> distance = Quantity(2, 'km')
   >>> distance.to('m')
   Quantity(2.000e+03 m)

Values of quantities can be casted in different units as well, by specifying new base units.

.. code-block::

   >>> distance.value('cm')
   200000.0

