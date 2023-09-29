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

System of units
"""""""""""""""

Quantities in this module are defined in the custom unit base (``m`` meter, ``g`` gramm, ``s`` second, ``K`` Kelvin, ``C`` Coulomb, ``cd`` candela, ``mol`` mole, ``rad`` radian) discussed earlier.
Nevertheless, it is straightforward to use another standard unit systems.
Since not all units have a dedicated name (e.g. atomic units) we cathegorize them according to their corresponding quantities.
Units of three major unit systems are available in following lists: International System ``SI``, Centimeter-Gram-Second system ``CGS`` and atomic units ``AU``.
Names and definitions of quantities are available in `settings <https://github.com/vrtulka23/scinumtools/blob/main/src/scinumtools/units/settings.py>`_.

Custom units
""""""""""""

Standardized units that are still not included in the default unit list should be requested in a GitHub issue and subsequently integrated into the core of this module.
Custom, or temporary units can be registered into current code release using helper class ``UnitEnvironment`` defined in `settings <https://github.com/vrtulka23/scinumtools/blob/main/src/scinumtools/units/settings.py>`_.

.. code-block::

   >>> from scinumtools.units import *
   >>> from scinumtools.units.settings import UnitEnvironment
   >>> units = {'x': {'magnitude':3, 'dimensions':[3,2,-1,0,0,1,0,0],'prefixes':['k','M','G']}}
   >>> with UnitEnvironment(units):
   >>>    Quantity(1, 'kx')
   Quantity(1.000e+00 kx)

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