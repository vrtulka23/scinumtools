Data manipulation
=================

This part of the ``scinumtools`` package contains routines concerning data manipulation.

Function caching
""""""""""""""""

.. code-block:: python

   >>> from scinumtools.data import CachedFunction
   >>> 
   >>> @CachedFunction("data_file.npy")
   >>> def read_data(a, b):
   >>>     return dict(a=a, b=b)
   >>> 
   >>> read_data('foo','bar')    

   {'foo':'foo','bar':'bar'}

Image thumbnails
""""""""""""""""

.. code-block:: python

   >>> from scinumtools.data import ThumbnailImage
   >>>
   >>> nx, ny = 300, 200
   >>> data = np.zeros((nx,ny))
   >>> for i in range(nx):
   >>>     for j in range(ny):
   >>>         data[i,j] = (i-nx/2)**2 + (j-ny/2)**2
   >>> imold = ThumbnailImage(
   >>>     extent = (-30,30,-20,20),
   >>>     data = data
   >>> )

