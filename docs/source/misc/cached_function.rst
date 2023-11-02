CachedFunction
==============

``CachedFunction`` is a function decorator that stores the function output at its first evaluation into a data file.
Separate cache data files are created for each unique combination of arguments provided to the function.

In the example below, the function ``read_data()`` receives two arguments ``a`` and ``b`` and returns a dictionary.
Function arguments are automatically transformed into a hash string that is added to a corresponding cache file name.

.. code-block:: python

   >>> from scinumtools import CachedFunction
   >>> 
   >>> @CachedFunction("data_file.npy")
   >>> def read_data(a, b):
   >>>     return dict(a=a, b=b)
   >>> 
   >>> read_data('foo','bar')    

   {'foo':'foo','bar':'bar'}

The resulting cache file name will have the following form: 

``data_file.2d69f41a2db6f660f97556225b5a068fbfc6c6e7f7165cbc9ca3bb01e08cad07.npy``

Calling ``read_data()`` again with the same arguments will read cached data from the file above.
A different set of arguments will recalculate the function and store its value into a new cache file with a different hash.