PDF documentation
=================

DIP package comes with an automatized PDF export of parameters.
As an example, we will parse following files:

*  `pdf_definitions.dip <https://github.com/vrtulka23/scinumtools/blob/main/tests/dip/examples/pdf_definitions.dip>`_
*  `pdf_settings.dip <https://github.com/vrtulka23/scinumtools/blob/main/tests/dip/examples/pdf_settings.dip>`_

Environment suitable for a documentation has to be parsed with a special method ``parse_pdf()``, that processes node differently as the standard ``parse()`` method.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.exports import ExportPDF
   >>> with DIP(docs=True) as p:
   >>>     p.from_file('pdf_definitions.dip')
   >>>     env = p.parse_pdf()
   >>> with ExportPDF(env) as exp:
   >>>     title = "Example documentation"
   >>>     pageinfo = "DIP Documentation"
   >>>     exp.build('documentation.pdf', title, pageinfo)
   
Code above will generate the following `PDF documentation <https://github.com/vrtulka23/scinumtools/blob/main/docs/source/_static/pdf/documentation.pdf>`_.
