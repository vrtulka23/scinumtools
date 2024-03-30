Materials
---------

Materials can be formed from one or more substances and their corresponding number (``x``, ``Norm.NUMBER_FRACTION``), or mass (``X``, ``Norm.MASS_FRACTION``) fractions.
If number fractions are given, mass fractions are calculated using substance masses, and vice versa.
Number and mass fraction values of components within a composite are automatically normalized.

Individual material components can be given in a form of a string (format ``fraction <substance> fraction <substance> ...``)

.. code-block:: python
   
   >>> from scinumtools.materials import Material, Norm
   >>> m = Material('0.2 <H2O> 0.3 <NaCl>', mass_density=Quantity(0.3,'g/cm3'), volume=Quantity(1,'l'))
   >>> m.print()
   Components:
   
   expr  fraction  mass[Da]    Z        N    e
    H2O       0.2 18.015286 10.0  8.00471 10.0
   NaCl       0.3 58.442707 28.0 30.48480 28.0
   
   Composit:
   
   expr  x[%]       X[%]
    H2O  40.0  17.047121
   NaCl  60.0  82.952879
    avg  50.0  50.000000
    sum 100.0 100.000000
   
   Matter:
   
   Mass density:   Quantity(3.000e-01 g*cm-3)
   Number density: Quantity(8.548e+21 cm-3)
   Volume:         Quantity(1.000e+00 l)
   Mass:           Quantity(3.000e+02 g)
   
   expr      n[cm-3]  rho[g/cm3]            N       M[g]
    H2O 1.709551e+21    0.051141 1.709551e+24  51.141364
   NaCl 2.564326e+21    0.248859 2.564326e+24 248.858636
    avg 2.136939e+21    0.150000 2.136939e+24 150.000000
    sum 4.273877e+21    0.300000 4.273877e+24 300.000000
    
or as a dictionary
    
.. code-block:: python

   >>> m = Material({
   >>>    'N2':  78.0840,  # given as percentage
   >>>    'O2':  20.9460,
   >>>    'Ar':  0.93400,
   >>>    'CO2': 0.03600,
   >>> }, norm_type=Norm.NUMBER_FRACTION)
   >>> m.print_components()
   expr  fraction  mass[Da]    Z         N    e
     N2    78.084 28.013406 14.0 14.007280 14.0
     O2    20.946 31.998810 16.0 16.008960 16.0
     Ar     0.934 39.947799 18.0 21.985398 18.0
    CO2     0.036 44.009546 22.0 22.019660 22.0
   >>> m.print_composite()
   expr    x[%]       X[%]
     N2  78.084  75.517607
     O2  20.946  23.139564
     Ar   0.934   1.288131
    CO2   0.036   0.054698
    avg  25.000  25.000000
    sum 100.000 100.000000
   
