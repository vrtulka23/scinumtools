PDF documentation
=================

DIP package comes with an automatized PDF export of parameters.
As an example, we will parse following files:

*  `definitions.dip <../../_static/pdf/definitions.dip>`_
*  `settings.dip <../../_static/pdf/settings.dip>`_

Environment suitable for a documentation has to be parsed with a special method ``parse_docs()``, that processes node differently as the standard ``parse()`` method.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.docs import ExportPDF
   >>> with DIP() as p:
   >>>     p.from_file('definitions.dip')
   >>>     docs = p.parse_docs()
   >>> with ExportPDF(docs) as exp:
   >>>     exp.build(
   >>>         'documentation.pdf', 
   >>>         "Example DIP documentation", 
   >>>         "In this document we want to demonstrate basic capabilities of a DIP documentation..... "
   >>>     )
   
Code above will generate the following `PDF documentation <../../_static/pdf/documentation.pdf>`_.

.. pdf-include:: ../../_static/pdf/documentation.pdf
   :height: 800px