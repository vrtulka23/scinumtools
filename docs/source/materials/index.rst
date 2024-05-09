Material Properties
===================

In this section, we describe an application of the :ref:`solver/index:expression solver` that calculates atomic properties from molecular formulas.
This should serve as a quick tool when one needs to count the number of nucleons and molecules, or material masses and densities.

Classes in this module are grouped into the following categories. 

.. csv-table:: Material cathegories
   :widths: 20, 20, 20, 20, 30
   :header-rows: 1

   "Class",       Matter,  Composite, Component, Note
   "Element",     "✔",     "",        "✔",       "atoms and homoatomic molecules"
   "Substance",   "✔",     "✔",       "✔",       "compounds and molecules"
   "Material",    "✔",     "✔",       "",        "mixtures"

Exact terminology for categories used in this code is given below.

.. note::
   Categories used here are based on the standard chemical terminology, nevertheless, they might differ in some nuances that simplify their numerical implementation.

Element
   A single or multiple atoms of the same kind (e.g. O, H2).

Substance
   The smallest form of matter with constant chemical composition made of single atoms (e.g. O), or multiple atoms connected by covalent, ionic, or metallic bonds.

Material
   It is a substance, or a mixture of substances, that constitutes an object (e.g. Air, Seawater). Substances in a material are not bound chemically, but rather blended mechanically and retain their chemical properties.

Matter
   A physical material that occupies space (volume) and possesses some rest mass.

Component
   An elementary part of a composite that has a specific proportion (number, or a fraction).
   In substances, proportions are numbers (count) of individual atoms.
   In materials, proportions are number, or mass fractions of individual substances.
   
Composite
   A chemical structure composed of several components. 

Further description of the Element, Substance and Material classes is given in the following sections.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   elements
   substances
   materials