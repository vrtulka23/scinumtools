Material properties
===================

In this section we describe an application of the :ref:`solver/index:expression solver` that calculates atomic properties from molecular formulas.
This should serve as a quick tool when one needs to count number of nucleons, or material masses and densities.

Expression syntax
-----------------

The syntax of the molecular formulas used in this solver is based on standard molecular formulas known from chemistry.
The most basic part of formulas, an element symbol, carries information about element type, isotope number and ionisation state.
A comprehensive list of all available :ref:`elements <materials/index:elements>` and their isotopes is given at the end of this section.
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
The expression solver currently supports following 3 basic operations:

.. csv-table:: Operations in molecular formulas
   :widths: 30, 30, 30
   :header-rows: 1
   
   Operation,      "Explicit notation", "Short notation"
   addition,       "``Na{23} + Cl``",   "``Na{23}Cl``"            
   multiplication, "``O{17-1} * 3``",   "``O{17-1}3``"            
   parentheses,    "``Ca(OH)2``",       ""
   
.. note::

   Symbols of explicit addition and multiplication need to be separated from element symbols with an empty space.

Example of use
--------------

   
   
Elements
--------

Individual nucleons can be used in formulas and have the following properties:

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

Below is a list of elements and their corresponding isotopes that can be used with this module. The data was taken from the `NIST <https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl>`_ database.
More elements and isotopes can be added on request.

.. csv-table:: List of available elements
   :file: ../_static/tables/elements.csv
   :widths: 10 10 10 30 30
   :header-rows: 1
