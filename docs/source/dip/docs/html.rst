HTML documentation
==================

DIP package comes with an automatized HTML export of parameters.
As an example, we will parse following files:

*  `definitions.dip <../../_static/htmldocs/definitions.dip>`_
*  `settings.dip <../../_static/htmldocs/settings.dip>`_

Environment suitable for a documentation has to be parsed with a special method ``parse_docs()``, that processes node differently as the standard ``parse()`` method.

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.docs import ExportDocsHTML
   >>> with DIP() as p:
   >>>     p.add_file('definitions.dip')
   >>>     docs = p.parse_docs()
   >>> with ExportDocsHTML(docs) as exp:
   >>>     exp.build(
   >>>         './build', 
   >>>         "Example DIP documentation", 
   >>>         "In this document we want to demonstrate basic capabilities of a DIP documentation..... "
   >>>     )
   
``ExportDocsHTML`` class provided above can be used as it is, or as a template for your own personalized documentation.
When building your own documentation, you can simply take the `existing source code <https://github.com/vrtulka23/scinumtools/tree/main/src/scinumtools/dip/docs/html>`_ and modify it according to your needs.
For more information how to create and manipulate HTML content using Python see documentation of `Beautiful Soup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_ and `Bootstrap <https://getbootstrap.com/docs/5.3/getting-started/introduction/>`_.

Code above will generate the following default `HTML documentation <../../_static/htmldocs/build/index.html>`_.

.. raw:: html

    <iframe src="../../_static/htmldocs/build/index.html" height="800px" width="100%"></iframe>
