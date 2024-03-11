Material Properties
===================

In this section, we describe an application of the :ref:`solver/index:expression solver` that calculates atomic properties from molecular formulas.
This should serve as a quick tool when one needs to count number of nucleons, or material masses and densities.

Expression syntax
-----------------

The syntax of molecular formulas used in this solver is based on standard molecular formulas known from chemistry.
The most basic part of formulas, an element symbol, carries information about element type, isotope number and ionisation state.
A comprehensive list of all available :ref:`elements <materials/index:list of elements>` and their isotopes is given at the end of this section.
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

Several element expressions can be combined into a more complex molecular formula.
The expression solver currently supports the following 3 basic operations:

.. csv-table:: Operations in molecular formulas
   :widths: 30, 30, 30
   :header-rows: 1
   
   Operation,      "Explicit notation", "Short notation"
   addition,       "``Na{23} + Cl``",   "``Na{23}Cl``"            
   multiplication, "``O{17-1} * 3``",   "``O{17-1}3``"            
   parentheses,    "``Ca(OH)2``",       ""
   
.. note::

   Symbols of explicit addition and multiplication need to be separated from element symbols with an empty space.

Elements
--------

Properties of individual :ref:`elements <materials/index:list of elements>` are managed by ``Element`` class.

.. code-block:: python

   >>> from scinumtools.materials import Element
   >>> e = Element('O')
   >>> print(e)
   Element(O Z=8.0 N=8.004 e=8.0 A=15.999)
   >>> e.Z, e.N, e.e, e.A
   8.0, 8.00448, 8.0, Quantity(1.600e+01 Da)
   >>> Element('O{17-2}')
   Element(O{17-2} Z=8 N=9.000 e=6 A=16.998)

The option ``natural`` determines how element properties are calculated if isotope number is not specified.
By default, its value is set to ``True``. 
In this case, element values are calculated as a weighted average of all isotopes according to their natural abundances.
If set to ``False``, an isotope with the highest abundance is used.

.. note::

   The number of neutrons in naturally abundant elements is not always an integer.
   This is due to calculation of averages over all element isotopes.

.. code-block:: python

   >>> from scinumtools.materials import Element
   >>> Element('O', natural=False)
   Element(O Z=8 N=8.000 e=8 A=15.995)

The option ``count`` is by default set to one, but it can also hold multiple elements of the same type, e.g. in a substance.
If its value is higher than one, all element properties are multiplied correspondingly by this number.

.. code-block:: python

   >>> from scinumtools.materials import Element
   >>> Element('O', count=2, natural=False)
   Element(O2 Z=16 N=1.600e+01 e=16 A=31.990)
   >>> e.count, e.element, e.isotope, e.ionisation
   2, 'O', 16, 0

Substances
---------

Substances consist of several elements.
In this context, we consider as substances pure elements, chemical compounds and molecules.
Class ``Substance`` can solve a molecular formula, break it into individual elements and calculate their collective atomic properties.
Similarly, as for ``Element`` class, it has an option to switch between natural and most abundant elements when isotopes are not specified.
In this case, the option applies to all elements in a substance.

.. code-block:: python

   >>> from scinumtools.materials import Substance
   >>> Substance('DT')
   Substance(p=2 n=3.000 e=2 A=5.030)
   >>> Substance('H2O', natural=False)
   Substance(p=10 n=8.000 e=10 A=18.011)

A substance can also be initialised from an explicit dictionary of element expressions and counts.

.. code-block:: python

   >>> Substance({
   >>>     "B{11}": 1,
   >>>     "N{14}": 1,
   >>>     "H{1}":  6,
   >>> })
   Substance(p=18 n=13.000 e=18 A=31.059)

Besides information about elements and nucleon, every substance calculate also other parameters.
In the example below, we show an example for the substance of water ``H2O``.
A concise overview of all its properties can be printed using its ``print()`` method.
Here the ``A`` is an atomic mass, ``Z`` proton number, ``N`` number of neutrons, ``e`` number of electrons, ``x`` number fraction and ``X`` is a mass fraction.

.. code-block:: python

   >>> with Substance('H2O', natural=False, rho=Quantity(997,'kg/m3'), V=Quantity(1,'l')) as c:
   >>>     c.print()
   Properties:
   
   Molecular mass: Quantity(1.801e+01 Da)
   Mass density: Quantity(9.970e+02 kg*m-3)
   Molecular density: Quantity(3.334e+28 m-3)
   Volume: Quantity(1.000e+00 l)
   
   Elements:
   
   expression element  isotope  ionisation     A[Da]  Z  N  e
            H       H        1           0  1.007825  1  0  1
            O       O       16           0 15.994915  8  8  8
   
   Substance:
   
   expression  count     A[Da]         Z        N         e       x[%]       X[%]      n[cm-3]  rho[g/cm3]          n_V     M_V[g]
            H    2.0  2.015650  2.000000 0.000000  2.000000  66.666667  11.191487 6.667280e+22    0.111579 6.667280e+25 111.579129 
            O    1.0 15.994915  8.000000 8.000000  8.000000  33.333333  88.808513 3.333640e+22    0.885421 3.333640e+25 885.420871 
          avg    1.5  6.003522  3.333333 2.666667  3.333333  33.333333  33.333333 3.333640e+22    0.332333 3.333640e+25 332.333333 
          sum    3.0 18.010565 10.000000 8.000000 10.000000 100.000000 100.000000 1.000092e+23    0.997000 1.000092e+26 997.000000

In the example above, we additionally set substance density ``rho`` and its volume ``V``.
Density is used for calculation of number ``n`` and mass ``rho`` densities.
If volume is also set, total number of species ``n_V`` and total mass ``m_V`` are added.

Individual substance parameters can be accessed directly using ``data_elements()`` and ``data_substance()``.
Both methods return a :ref:`ParameterTable <misc/parameter_table:parametertable>` object with corresponding values.
Corresponding tabular values can be printed using method ``print_elements()`` and ``print_substance()``.

.. code-block:: python

   >>> with Substance('H2O', natural=False) as c:
   >>>     data = c.data_elements()
   >>>     data.O['N']
   8
   >>>     data = c.data_substance()
   >>>     data['sum'].e
   10
   >>>     data.H.count
   2
   >>>     data.H.A
   Quantity(2.015650, 'Da')

In both cases, dimensional parameters are returned as ``Quantity`` objects.
If needed, simple numerical values can be requested by setting the following option: ``quantity=False``.
Sometimes it is required to know information about part of a substance.
In this case, one can specify which elements (``H``) should be returned.

.. code-block:: python

   >>> with Substance('H2O', natural=False) as c:
   >>>     c.data_substance(['H'], quantity=False).to_text()
     expression  count         A    Z    N    e          x          X
   0          H    2.0  2.015650  2.0  0.0  2.0  66.666667  11.191487
   1        avg    2.0  1.007825  1.0  0.0  1.0  33.333333   5.595744
   2        sum    2.0  2.015650  2.0  0.0  2.0  66.666667  11.191487

Materails
---------

Materials can be formed from one or more substances and their corresponding number (``x``, ``FracType.NUMBER``), or mass (``X``, ``FracType.MASS``) fractions.
If number fractions are given, mass fractions are calculated using substance masses, and vice versa.
Number and mass fraction values are always normalized to unity.

.. code-block:: python

   >>> from scinumtools.materials import Material, FracType
   >>> m = Material({
   >>>    'N2':  78.0840,  # given as percentage
   >>>    'O2':  20.9460,
   >>>    'Ar':  0.93400,
   >>>    'CO2': 0.03600,
   >>> }, fractype=FracType.NUMBER)
   >>> m.print_substances()
   expression  fraction          M
          N2    78.084   28.013406
          O2    20.946   31.998810
          Ar     0.934   39.947799
         CO2     0.036   44.009546
         avg    25.000   35.992390
         sum   100.000  143.969561
   >>> m.print_material()
   expression        x         X
           N2  0.78084  0.755176
           O2  0.20946  0.231396
           Ar  0.00934  0.012881
          CO2  0.00036  0.000547
          avg  0.25000  0.250000
          sum  1.00000  1.000000
   
List of elements
----------------

Individual nucleons can be used in formulas in the same way as elements and have the following properties:

.. csv-table:: Nucleon properties
   :widths: 20, 20, 10, 10, 10, 30
   :header-rows: 1

   Nucleon,    Symbol,     Z, N, e, "Relative atomic mass (Da)"
   Proton,     ``[p]``,    1, 0, 0, 1.007276
   Neutron,    ``[n]``,    0, 1, 0, 1.008664
   Electron,   ``[e]``,    0, 0, 1, 5.48579e-4


Symbols of the elements conform to a standard element notation. 
In case of named Hydrogen isotopes, it is also possible to use the following short notation:

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
