HTML documentation
==================

DIP package comes with an automatized HTML export of parameters.
As an example, we will parse following files:

*  `definitions.dip <../../_static/htmldocs/definitions.dip>`_
*  `settings.dip <../../_static/htmldocs/settings.dip>`_

Environment suitable for a documentation has to be parsed with a special method ``parse_docs()``, that processes node differently as the standard ``parse()`` method.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.docs import ExportHTML
   >>> with DIP() as p:
   >>>     p.from_file('definitions.dip')
   >>>     docs = p.parse_docs()
   >>> with ExportHTML(docs) as exp:
   >>>     exp.build(
   >>>         './build', 
   >>>         "Example DIP documentation", 
   >>>         "In this document we want to demonstrate basic capabilities of a DIP documentation..... "
   >>>     )
   
Code above will generate the following `HTML documentation <../../_static/html/build/index.html>`_.

.. raw:: html

    <iframe src="../../_static/htmldocs/build/index.html" height="800px" width="100%"></iframe>
