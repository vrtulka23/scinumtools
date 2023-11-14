Templates
=========

Template solver was already introduced in previous sections concerning general DIP syntax.
Class ``TemplateSolver`` can be, however, used also separately as a template parser.

Let's take an example of a template file below:

.. code-block:: rst
   :caption: template.txt

   Geometry: {{?box.geometry}}
   Box size: [{{?box.size.x}}, {{?box.size.y}}, {{?box.size.z}}]

This file can be easily processed using ``TemplateSolver`` class

.. code-block:: python

   >>> from scinumtools import DIP
   >>> from scinumtools.dip.solvers import TemplateSolver
   >>> 
   >>> with DIP() as dip:
   >>>     dip.from_file('definitions.dip')
   >>>     env = dip.parse()
   >>> with TemplateSolver(env) as ts:
   >>>     text = ts.template('template.txt','processed.txt')

and exported as following text file:

.. code-block:: rst
   :caption: processed.txt

   Geometry: 3
   Box size: [1e-06, 3.0, 23.0]
