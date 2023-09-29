Unit conversions
================

Conversion of quantities from one units to another is and integral part of this module.
Currently, there are available three different types of unit conversion, standard, logarithmic and temperature, described in the text below.
Implementation of custom units and their conversions is described at the bottom of this section.

Quantities can be converted to other units (with the same dimensions) using ``to(<unit>)`` method.

.. code-block::

   >>> distance = Quantity(2, 'km')
   >>> distance.to('m')
   Quantity(2.000e+03 m)

Values of quantities can be casted in different units as well, by specifying new base units.

.. code-block::

   >>> distance.value('cm')
   200000.0

Standard units
""""""""""""""

Standard units can be defined using multiplication, division and powers of base dimensions (``m``, ``g``, ``s``, ``K``, ``C``, ``cd``, ``mol`` and ``rad``) and some numerical value.
Most of the units fall into this cathegory and implement all default operations.

.. code-block::

   >>> from scinumtools.units import *
   >>> a = Quantity(4.34, 'kg*m2/s2')
   >>> b = Quantity(34.3, 'eV')
   >>> c = Quantity(29.2, 'J')
   >>> (a+b+c).to('erg')
   Quantity(3.354e+08 erg)

Logarithmic units
"""""""""""""""""

Logarithmic units make an independent cathegory of units, because their logarithmic nature require special conversion functions and modification of basic operators (addition, substraction, ...).
Into this cathegory belong formost Bel (B, dB) and Nepers (Np) units, together with all their derived units and conversions to corresponding amplitude, or power ratios and standard units.
List of available conversions is given in the table below.

 .. csv-table:: Logarithmic unit conversions
   :widths: 40 40
   :header-rows: 1

   Logarithmic,          Standard
   Np,                   "PR, AR"       
   B,                    "PR, AR"
   "Bm, BmW, BW, BSWL",  W
   "BV, BuV",            V
   BuA,                  A
   BOhm,                 Ohm
   BSPL,                 Pa
   BSIL,                 W/m2

Temperature units
"""""""""""""""""

Currently, one can convert between following temperature units: Kelvin ``K``, Rankine ``degR``, Celsius ``Cel`` and Farenheit ``degF``.
These units can be used in complex unit expressions (e.g. ``erg/K``), however, units of temperature can be converted only between each other.

.. code-block::

   >>> from scinumtools.units import * 
   >>> T = Quantity(1, 'eV')/Unit('[k_B]')
   >>> T.to('K')
   Quantity(1.160e+04 K)
   >>> T.to('Cel')
   Quantity(1.133e+04 Cel)

System of units
"""""""""""""""

Quantities in this module are defined in the custom unit base (``m`` meter, ``g`` gramm, ``s`` second, ``K`` Kelvin, ``C`` Coulomb, ``cd`` candela, ``mol`` mole, ``rad`` radian) discussed earlier.
Nevertheless, it is also possible to calculate in another standard systems of units.
Since not all units have a dedicated name (e.g. atomic units) we cathegorize them according to their corresponding physical quantities.
Units of three major unit systems are available in following lists: International System ``SI``, Centimeter-Gram-Second system ``CGS`` and Hartree Atomic Units ``AU``.
Names and definitions of quantities are available in `settings <https://github.com/vrtulka23/scinumtools/blob/main/src/scinumtools/units/settings.py>`_.
Unit symbols have a generic format ``#<sytem><abbreviation>``, where ``<system>`` specifies one of the unit systems (``S``\I, ``C``\GS, ``A``\U) and ``<abbreviation>`` is formed from corresponding quantity name.

.. code-block::

   >>> from scinumtools.units import *
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
   
