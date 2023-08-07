ThumbnailImage
==============

``ThumbnailImage`` is a class that can create thumbnails from images. The thumbnails preserve the image proportions and pad the rest of the new image with a predefined color.

.. code-block:: python

   >>> from scinumtools import ThumbnailImage
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
