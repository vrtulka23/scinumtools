Installation
============

Source code of this project is available in a `DIP GitHub repository <https://github.com/dipsl/pydipsl>`_.
One can use this library directly from a source code by including the source code directory in a ``$PYTHONPATH``:

.. code-block:: bash
		
   cd ~
   git clone https://github.com/dipsl/pydipsl.git
   export PYTHONPATH=$PYTHONPATH:$HOME/pydipsl/src/

One can also import it directly from a python script:

.. code-block:: python

   import sys
   sys.path.append("~/pydipsl/src")

   
Nevertheless, it is recommended to install it from a PyPi repository:

.. code-block:: bash

   pip3 install dipsl

   
The main DIP module can be imported into your Python project as follows:

.. code-block:: python

   import dipsl
   
More :doc:`examples of use <example>` are in the following section.
