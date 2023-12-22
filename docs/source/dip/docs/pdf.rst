PDF documentation
=================

DIP package comes with an automatized PDF export of parameters.
As an example, we will parse following files:

*  `definitions.dip <../../_static/pdf/definitions.dip>`_
*  `settings.dip <../../_static/pdf/settings.dip>`_

Environment suitable for a documentation has to be parsed with a special method ``parse_docs()``, that processes node differently as the standard ``parse()`` method.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.docs import ExportDocsPDF
   >>> with DIP() as p:
   >>>     p.add_file('definitions.dip')
   >>>     docs = p.parse_docs()
   >>> with ExportDocsPDF(docs) as exp:
   >>>     exp.build(
   >>>         'documentation.pdf', 
   >>>         "Example DIP documentation", 
   >>>         "In this document we want to demonstrate basic capabilities of a DIP documentation..... "
   >>>     )
   
``ExportDocsPDF`` class provided above can be used as it is, or as a template for your own personalized documentation.
When building your own documentation, you can simply take the `existing source code <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/docs/pdf>`_ and modify it according to your needs.
For more information how to create PDF content using Python see documentation of `ReportLab <https://docs.reportlab.com/>`_.

Code above will generate the following `PDF documentation <../../_static/pdf/documentation.pdf>`_.

.. pdf-include:: ../../_static/pdf/documentation.pdf
   :height: 800px