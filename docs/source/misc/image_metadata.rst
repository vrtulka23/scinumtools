ImageMetadata
=============

Resolution studies often produce many generic figures, and one can easily lose track which figure belongs to which simulation setup. 
One way how to identify figures is to add some text information directly in a figure. 
This might be a disadvantage, especially, when figures are to be included in some presentations or documents.

Another approach is to hide such information directly into figure files using image EXIF Metadata. 
The class ``ImageMetadata`` implements a simple process that stores/retrieves metadata from the EXIF UserComment tag. 
The data is stored as a JSON string and contains the following categories:

.. csv-table:: Image metadata 
   :widths: 30 30 40
   :header-rows: 1
  
   Metadata,   Key,         Description
   DIR_SETUP,  "DirSetup",  "Simulation setup directory"
   DIR_DATA,   "DirData",   "Simulation output data directory"
   GIT_COMMIT, "GitCommit", "Git commit of a simulation code"
   GIT_BRANCH, "GitBranch", "Git branch of a simulation code"
   DATETIME,   "DateTime",  "Figure creation time"
   SETTINGS,   "Settings",  "Feature settings of a simulation setup"
   
Individual metadata can be easily added to a file,

.. code-block::

    >>> from scinumtools import ImageMetadata, Metadata
    >>> with ImageMetadata('figure.png') as im:
    >>>     im.set(Metadata.DATETIME,'2024-04-10 18:00:00')

or retrieved for further use.

.. code-block::

    >>> with ImageMetadata('figure.png') as im:
    >>>     im.get(Metadata.DATETIME)
    2024-04-10 18:00:00
    
All stored metadata can be also printed using ``print()`` method.

    >>> with ImageMetadata('figure.png') as im:
    >>>     im.print()
    DateTime: 2024-04-10 18:00:00