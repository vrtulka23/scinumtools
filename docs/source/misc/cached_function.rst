CachedFunction
==============

``CachedFunction`` is a simple function decorator that stores the function output at its first evaluation into a file provided as an argument.

.. code-block:: python

   >>> from scinumtools import CachedFunction
   >>> 
   >>> @CachedFunction("data_file.npy")
   >>> def read_data(a, b):
   >>>     return dict(a=a, b=b)
   >>> 
   >>> read_data('foo','bar')    

   {'foo':'foo','bar':'bar'}


