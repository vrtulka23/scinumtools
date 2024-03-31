Elements
========

Properties of individual elements are managed by ``Element`` class.
Expressions of different elements carry information about their element types, isotope numbers and ionisation states.
A comprehensive list of all available elements and their isotopes is given at the end of this section.
Examples of element symbols of a carbon atom are given below:

.. csv-table:: Notation of element symbols
   :widths: 20, 20, 20, 40
   :header-rows: 1

   Symbol,    Abundance,  Ionisation, Note
   "``C``",       natural,    neutral,    "naturally occuring carbon"
   "``C{-3}``",   natural,    cation,     "positive natural ion"
   "``C{+3}``",   natural,    anion,      "negative natural ion"
   "``C{13}``",   isotope,    neutral,    "carbon-13 isotope"
   "``C{13-3}``", isotope,    cation,     "positive isotope ion"
   "``C{13+3}``", isotope,    anion,      "negative isotope ion"

The ``Element`` class can be used in the following way.

.. code-block:: python

   >>> from scinumtools.materials import Element
   >>> e = Element('O')
   >>> print(e)
   Element(O mass=15.999 Z=8.0 N=8.004 e=8.0)
   >>> e.Z, e.N, e.e, e.mass
   8.0, 8.00448, 8.0, Quantity(1.600e+01 Da)
   >>> Element('O{17-2}')
   Element(O{17-2} mass=16.998 Z=8 N=9.000 e=6)

The option ``natural`` determines how element properties are calculated if isotope number is not specified.
By default, its value is set to ``True``. 
In this case, element values are calculated as a weighted average of all isotopes according to their natural abundances.
If set to ``False``, an isotope with the highest abundance is used.

.. note::

   The number of neutrons in naturally abundant elements is not always an integer.
   This is due to the calculation of averages over all element isotopes.

.. code-block:: python

   >>> from scinumtools.materials import Element
   >>> Element('O', natural=False)
   Element(O mass=15.995 Z=8 N=8.000 e=8)

The option ``proportion`` is by default set to one, but it can also hold multiple elements of the same type, e.g. in a substance.
If its value is higher than one, all element properties are multiplied correspondingly by this number.

.. code-block:: python

   >>> from scinumtools.materials import Element
   >>> e = Element('O', proportion=2, natural=False)
   >>> print(e)
   Element(O2 mass=31.990 Z=16 N=16.000 e=16)
   >>> e.proportion, e.element, e.isotope, e.ionisation
   2, 'O', 16, 0

Elements can also have properties of matter by adding a density and volume.
All properties can be previewed using ``print()`` method.

.. code-block:: python

   >>> e = Element('B', mass_density=Quantity(997,'kg/m3'), volume=Quantity(1,'l'))
   >>> e.print()
   Element:
    
   Expression: B
   Mass:       10.811
   Protons:    5.0
   Neutrons:   5.801
   Electrons:  5.0
    
   Matter:
   
   Mass density:   Quantity(9.970e-01 g*cm-3)
   Number density: Quantity(5.554e+22 cm-3)
   Volume:         Quantity(1.000e+00 l)
   Mass:           Quantity(9.970e+02 g)
    
   expr      n[cm-3]  rho[g/cm3]            N  M[g]
      B 5.553657e+22       0.997 5.553657e+25 997.0

Individual nucleons can be used in formulas in the same way as elements and have the following properties:

.. csv-table:: Nucleon properties
   :widths: 20, 20, 10, 10, 10, 30
   :header-rows: 1

   Nucleon,    Symbol,     Z, N, e, "Relative atomic mass (Da)"
   Proton,     ``[p]``,    1, 0, 0, 1.007276
   Neutron,    ``[n]``,    0, 1, 0, 1.008664
   Electron,   ``[e]``,    0, 0, 1, 5.48579e-4


Symbols of the elements conform to a standard element notation. 
In the case of named Hydrogen isotopes, it is also possible to use the following short notation:

.. csv-table:: Special symbols of hydrogen isotopes
   :widths: 20, 20, 20
   :header-rows: 1
   
   Isotope,     Symbol,    Equivalent 
   Proton,      ``[p]``,   ``H{1-1}``
   Deuterium,   ``D``,     ``H{2}``    
   Tritium,     ``T``,     ``H{3}``     

Below is a list of elements and their corresponding isotopes that can be used with this module. 
The data was taken from `NIST <https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl>`_ database.

.. csv-table:: List of available elements
   :file: ../_static/tables/elements.csv
   :widths: 10 10 10 30 30
   :header-rows: 1
