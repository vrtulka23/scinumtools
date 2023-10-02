Physical Units
==============

Class ``Quantity`` and its derivates, ``Unit`` and ``Constant``, can be used in many scientific applications, because they enable easy manipulation and calculations with physical quantities. Among the most interesting features are:

* Concise and regularized unit notation with arbitrary unit prefixes.
* Conversion of units with the same, or inverse dimensionality (SI, CGS, natural units and more...).
* Conversion of temperatures (K, degR, degC, degF).
* Conversion of logarithmic units (dB, Np, dBmW,...).
* Integration with ``numpy`` arrays and functions.
* Usage of float or ``Decimal`` precision.
* ``Quantity`` is a self-content class that does not need initialization in a header, or use of registries. Quantities can be pickled and are compatible when created in different parts of the code.
* Support of fractional powers

All available units, constants and prefixes with their corresponding symbols and definitions are listed in `settings.py <https://github.com/vrtulka23/scinumtools/blob/main/src/scinumtools/units/settings.py>`_. In this text, we will refer to them without extensive introduction. A list of available units and constants can also be printed using the following python command:

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

All units used by ``Quantity`` are based on 8 fundamental ``dimensions``. These are not identical with any standard metric system (SI, CGS) but conveniently selected for ease of implementation and internal calculations. Six units are physical (``m`` meter, ``g`` gram, ``s`` second, ``K`` Kelvin, ``C`` Coulomb, ``cd`` candela) and two are numerical (``mol`` mole, ``rad`` radian). Derived units use combinations of these dimensions and a numerical value, magnitude.

Units can be used individually, or combined using basic mathematical operations. Multiplication is denoted using asterisk symbol ``m*m``, division using slash symbol ``m/s``, integer powers are indicated with a number after the unit ``m2`` (or ``m-2``) and fractional powers are denoted using two numbers separated by a colon ``s3:3`` (or ``s-3:3``). Units can also have a numerical part ``60*s`` (or ``365.25*day``, or ``1.67e-24*g``) and can use parenthesis ``m3/(kg*s2)``. No empty spaces in unit expressions are allowed.

* Units without prefixes: ``g``, ``J``, ``ly``
* Units with prefixes: ``mg``, ``MJ``, ``kly``
* Unit expressions: ``kg*m2/s2``, ``V/(C/s)``, ``1/Hz1:2``

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quantities
   conversions
   other
   tables
