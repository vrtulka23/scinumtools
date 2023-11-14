PDF documentation
=================

DIP package comes with an automatized PDF export of parameters.
As an example, we will parse following files:

*  `definitions.dip <../../_static/pdf/definitions.dip>`_
*  `settings.dip <../../_static/pdf/settings.dip>`_

Environment suitable for a documentation has to be parsed with a special method ``parse_pdf()``, that processes node differently as the standard ``parse()`` method.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.exports import ExportPDF
   >>> with DIP() as p:
   >>>     p.from_file('definitions.dip')
   >>>     env = p.parse_pdf()
   >>> with ExportPDF(env) as exp:
   >>>     title = "Example documentation"
   >>>     pageinfo = "DIP Documentation"
   >>>     exp.build('documentation.pdf', title, pageinfo)
   
Code above will generate the following `PDF documentation <../../_static/pdf/documentation.pdf>`_.
