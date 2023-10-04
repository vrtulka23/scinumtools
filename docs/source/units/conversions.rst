Unit conversions
================

Conversion of quantities from one units to another is and integral part of this module.
Currently, there are available three different types of unit conversion, standard, logarithmic and temperature, described in the text below.
Implementation of custom units and their conversions is described at the bottom of this section.

Quantities can be converted to other units (with the same dimensions) using ``to(<unit>)`` method.

.. code-block::

   >>> from scinumtools.units import *
   >>> distance = Quantity(2, 'km')
   >>> distance.to('m')
   Quantity(2.000e+03 m)

Values of quantities can be casted in different units as well, by specifying new base units.

.. code-block::

   >>> distance.value('cm')
   200000.0

Prefixes
""""""""

Many units listed below can be used in combination with :ref:`units/tables:unit prefixes`.
Information about allowed prefixes for individual units can be found in section :ref:`units/tables:tables and lists`.

.. code-block::

   >>> Quantity(84, 'm').to('cm')
   Quantity(8.400e+03 cm)
   >>> Quantity(193.3, 'eV').to('MJ')
   Quantity(3.097e-23 MJ)
   >>> Quantity(39, 'dBm').to('kW')
   Quantity(7.943e-03 kW)

Standard units
""""""""""""""

Standard units can be defined using multiplication, division and powers of :ref:`units/tables:base units` (``m``, ``g``, ``s``, ``K``, ``C``, ``cd``, ``mol`` and ``rad``) and some numerical value.
Most of the units fall into this cathegory and implement all default operations (``+``, ``-``, ``*``, ``/`` and ``**``).
Only quantities with same dimensionality can be added to, or subtracted from each other.
Power of an exponent should be always dimensionless. More numerical functions are implemented via :ref:`units/other:numpy arrays`.
A comprihensive list of all available named units and constants is in section :ref:`units/tables:tables and lists`.

.. code-block::

   >>> a = Quantity(4.34, 'kg*m2/s2')
   >>> b = Quantity(34.3, 'eV')
   >>> c = Quantity(29.2, 'J')
   >>> (a+b+c).to('erg')
   Quantity(3.354e+08 erg)
   >>> (a*b).to('nJ2')
   Quantity(2.385e+01 nJ2)
   >>> c**3
   Quantity(2.490e+04 J3)


   
Logarithmic units
"""""""""""""""""

:ref:`units/tables:logarithmic units` make an independent cathegory of units, because their logarithmic nature require special conversion functions and modification of basic operators (addition, substraction, ...).
Into this cathegory belong formost Bel (B, dB) and Nepers (Np) units, together with all their derived units and conversions to corresponding amplitude (AR), or power (PR) ratios and standard units (A, W, Ohm, V...).
Bel and Nepers units can be converted between each other and between power/amplitude ratios.
Other logarithmic units support conversions between their corresponding standard units.

.. code-block::

   >>> Quantity(39, 'dB').to('AR')
   Quantity(8.913e+01 AR)
   >>> Quantity(39, 'Np').to('PR')
   Quantity(7.498e+33 PR)
   >>> Quantity(39, 'dBOhm').to('Ohm')
   Quantity(8.913e+01 Ohm)
   >>> Quantity(39, 'dBSIL').to('W/m2')
   Quantity(7.943e-09 W*m-2)

Conversion of logarithmic units is also possible if the expression has a form of a fraction.
One example of such conversion is given below.

.. code-block::

   >>> q = Quantity(10, 'dBmW/Hz')
   >>> q.to('W/Hz')
   Quantity(1.000e-02 W*Hz-1)
   >>> q*Quantity(100, 'Hz')
   Quantity(1.000e+00 W)
   >>> (q*Quantity(100, 'Hz')).to('dBmW')
   Quantity(3.000e+01 dBmW)

Summation and subtraction operations work differently in case of logarithmic units.
These operations are implemented and can be used between logarithmic units of the same type.

.. code-block::

   >>> Quantity(1, 'dB')+Quantity(2, 'dB')
   Quantity(4.539e+00 dB)
   >>> Quantity(87, 'dBA')-Quantity(83, 'dBA')
   Quantity(8.480e+01 dBA)
   
Temperature units
"""""""""""""""""

This module uses Kelvins as a primary unit of temperature, but one can convert temperature also to other :ref:`units/tables:temperature units`.
These units can be used in unit expressions (e.g. ``erg/K``, ``erg/Cel``), however, temperatures can be converted only if there are no other units in an expression.

.. code-block::

   >>> Quantity(5, 'erg/K/s')*Quantity(10, 's')
   Quantity(5.000e+01 erg*K-1)
   >>> T = Quantity(1, 'eV')/Unit('[k_B]')
   >>> T.to('K')
   Quantity(1.160e+04 K)
   >>> T.to('Cel')
   Quantity(1.133e+04 Cel)

System of units
"""""""""""""""

Quantities in this module are defined in the internal :ref:`units/tables:base units` discussed earlier.
Nevertheless, it is also possible to perform calculations and do conversions with another standard systems of units.
Since not all units have dedicated names (e.g. atomic units) we cathegorize them according to their corresponding physical quantities.
Units of three major :ref:`units/tables:unit systems` are available in following lists: International System ``SI``, Centimeter-Gram-Second system ``CGS`` and Hartree Atomic Units ``AU``.
Unit symbols have a generic format ``#<sytem><abbreviation>``, where ``<system>`` specifies one of the unit systems (``S``\I, ``C``\GS, ``A``\U) and ``<abbreviation>`` is formed from corresponding quantity name.

.. code-block::

   >>> Unit(CGS.Energy)
   Quantity(1.000e+00 #CENE)
   >>> Quantity(1,AU.Length).to('m')
   Quantity(5.292e-11 m)
   >>> Quantity(23, '#ALEN/s').to(SI.Velocity)
   Quantity(1.217e-09 #SVEL)

Custom units
""""""""""""

Standardized units that are still not included in the default unit list should be requested in a GitHub issue and subsequently integrated into the core of this module.
Custom, or temporary units can be registered into current code release using helper class ``UnitEnvironment``.

.. code-block::

   >>> from scinumtools.units import Quantity, UnitEnvironment
   >>> units = {'x': {'magnitude':3, 'dimensions':[3,2,-1,0,0,1,0,0],'prefixes':['k','M','G']}}
   >>> with UnitEnvironment(units):
   >>>    Quantity(1, 'kx')
   Quantity(1.000e+00 kx)

Quantity objects can be also registered by ``UnitEnvironment`` as new units.
However, if one wants to specify also prefixes, the format above has to be used.

.. code-block::

   >>> units = {'x': Quantity(2, 'cm/g2')}
   >>> with UnitEnvironment(units):
   >>>     Quantity(1, 'x')
   Quantity(1.000e+00 x)

It is also possible to define a custom conversion class for the new units.
In such case the conversion class needs to be first defined and registered together with the new quantity.

.. code-block::

   >>> class CustomUnitType(UnitType):
   >>>      def convert(self, baseunits1, baseunits2):
   >>>          #... your implementation
   >>> units = {'x': {'magnitude':3, 'dimensions':[3,2,-1,0,0,1,0,0],'definition':CustomUnitType}}
   >>> env = UnitEnvironment(units)
   >>> Quantity(1, 'x')
   Quantity(1.000e+00 x)
   >>> env.close()
   
