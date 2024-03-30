Substances
----------

Several element expressions can be combined into a more complex molecular formula.
In this context, we consider as substances pure elements, chemical compounds and molecules.
The syntax of molecular formulas used in this solver is based on standard molecular formulas known from chemistry.
The substance expression solver currently supports the following 3 basic operations:

.. csv-table:: Operations in molecular formulas
   :widths: 30, 30, 30
   :header-rows: 1
   
   Operation,      "Explicit notation", "Short notation"
   addition,       "``Na{23} + Cl``",   "``Na{23}Cl``"            
   multiplication, "``O{17-1} * 3``",   "``O{17-1}3``"            
   parentheses,    "``Ca(OH)2``",       ""
   
.. note::

   Symbols of explicit addition and multiplication need to be separated from element symbols with an empty space.

Class ``Substance`` can solve a molecular formula, break it into individual elements and calculate their collective atomic properties.
Similarly, as for ``Element`` class, it has an option to switch between natural and most abundant elements when isotopes are not specified.
In this case, the option applies to all elements in a substance.

.. code-block:: python

   >>> from scinumtools.materials import Substance
   >>> Substance('DT')
   Substance(mass=5.030 Z=2 N=3.000 e=2)
   >>> Substance('H2O', natural=False)
   Substance(mass=18.011 Z=10 N=8.000 e=10)

A substance can also be initialized from an explicit dictionary of element expressions and corresponding proportions.

.. code-block:: python

   >>> Substance({
   >>>     "B{11}": 1,
   >>>     "N{14}": 1,
   >>>     "H{1}":  6,
   >>> })
   Substance(mass=31.059 Z=18 N=13.000 e=18)

Besides information about elements and nucleons, every substance calculates also other parameters.
In the example below, we show an example of the substance of water ``H2O``.
A concise overview of all its properties can be printed using its ``print()`` method.
Here the ``mass`` is an atomic mass, ``Z`` proton number, ``N`` number of neutrons, ``e`` number of electrons, ``x`` number fraction and ``X`` is a mass fraction.

.. code-block:: python

   >>> with Substance('H2O', natural=False, mass_density=Quantity(997,'kg/m3'), volume=Quantity(1,'l')) as c:
   >>>     c.print()
   Components:
   
   expr element  isotope  ionisation  mass[Da]  count  Z  N  e
      H       H        1           0  1.007825    2.0  1  0  1
      O       O       16           0 15.994915    1.0  8  8  8
   
   Composite:
   
   Total mass:     Quantity(1.801e+01 Da)
   Total number:   3.0
   
   expr  mass[Da]         Z        N         e       x[%]       X[%]
      H  2.015650  2.000000 0.000000  2.000000  66.666667  11.191487
      O 15.994915  8.000000 8.000000  8.000000  33.333333  88.808513
    avg  6.003522  3.333333 2.666667  3.333333  33.333333  33.333333
    sum 18.010565 10.000000 8.000000 10.000000 100.000000 100.000000
   
   Matter:
   
   Mass density:   Quantity(9.970e-01 g*cm-3)
   Number density: Quantity(3.334e+22 cm-3)
   Volume:         Quantity(1.000e+00 l)
   Mass:           Quantity(9.970e+02 g)
   
   expr      n[cm-3]  rho[g/cm3]            N       M[g]
      H 6.667280e+22    0.111579 6.667280e+25 111.579129
      O 3.333640e+22    0.885421 3.333640e+25 885.420871
    avg 3.333640e+22    0.332333 3.333640e+25 332.333333
    sum 1.000092e+23    0.997000 1.000092e+26 997.000000

In the example above, we additionally set substance density ``rho`` and its volume ``V``.
Density is used for calculation of number ``n`` and mass ``rho`` densities.
If volume is also set, the total number of species ``N`` and total mass ``M`` are added.

Individual substance parameters can be accessed directly using ``data_components()``, ``data_composite()`` and ``data_matter()``.
Both methods return a :ref:`ParameterTable <misc/parameter_table:parametertable>` object with corresponding values.
Corresponding tabular values can be printed using method ``print_components()``, ``print_composite()`` and ``print_matter()``.

.. code-block:: python

   >>> with Substance('H2O', natural=False) as c:
   >>>     data = c.data_components()
   >>>     data.O['N']
   8
   >>>     data.H.count
   2
   >>>     data = c.data_composite()
   >>>     data['sum'].e
   10
   >>>     data.H.mass
   Quantity(2.015650, 'Da')

In both cases, dimensional parameters are returned as ``Quantity`` objects.
If needed, simple numerical values can be requested by setting the following option: ``quantity=False``.
Sometimes it is required to know information about part of a substance.
In this case, one can specify which elements (``H``) should be returned.

.. code-block:: python

   >>> with Substance('H2O', natural=False) as c:
   >>>     c.data_substance(['H'], quantity=False).to_text()
     expr      mass    Z    N    e          x          X
   0    H  2.015650  2.0  0.0  2.0  66.666667  11.191487
   1  avg  1.007825  1.0  0.0  1.0  33.333333   5.595744
   2  sum  2.015650  2.0  0.0  2.0  66.666667  11.191487

