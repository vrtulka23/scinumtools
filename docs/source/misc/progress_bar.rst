ProgressBar
===========

``ProgressBar`` is a minimalistic implementation of a command line progress bar. It can be used in any loop with known number of steps to track the current progress of the code.

.. code-block:: python

    >>> from scinumtools import *
    >>> import time
    >>> 
    >>> nsteps = 10
    >>> with ProgressBar(nsteps) as pb:
    >>>     for i in range(nsteps):
    >>>         time.sleep(1)
    >>>         pb.step()
    |Step 0/10 Time 0.0s/0.0s                                              |
    ...
    |Step 5/10 Time 5.0s/10.0s                                             |
    ...
    |Step 10/10 Time 10.0s/10.0s                                           |

``ProgressBar`` can also be used as a standard object. However, at the end of the loop, one has to explicitly close the progress session by calling ``close()`` method.

.. code-block:: python
    
    >>> pb = ProgressBar(nsteps)
    >>> for i in range(nsteps):
    >>>     time.sleep(1)
    >>>     pb.step()
    >>> pb.close()
