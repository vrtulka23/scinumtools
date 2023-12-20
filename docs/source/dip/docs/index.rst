Documentation
=============

Documentations of DIP parameters can be easily generated using a special `Documentation <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/docs/documentation.py>`_ environment.
Environment from ``parse_docs()`` method differs from a standard data environment returned by ``parse()``, because it contains detailed information about parameter nodes, references, custom units and sources.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> with DIP() as p:
   >>>     p.add_file('definitions.dip')
   >>>     docs = p.parse_docs()

The ``Documentation`` class returned by ``parse_docs()`` method contains the following:

- List of node types
- List of parameters with corresponding node definitions, declarations and modifications
- Information about node value injections and node imports
- List of custom units and sources
- Corresponding links between parameters, nodes, injections, imports and sources

Below, we provide several export examples for the most used documentation formats.
They can be used as such, or modified to your personal needs.

.. toctree::
   :maxdepth: 2

   pdf
   html
   rst/build/index

For more information, please see the `source code <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/docs/>`_ of ``Documentation`` class and export examples given above.