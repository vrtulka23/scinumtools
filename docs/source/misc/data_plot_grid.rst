DataPlotGrid
============

.. code-block::

    >>> from scinumtools import DataPlotGrid
    >>> dpg = DataPlotGrid(list(range(5)), 2)
    >>> list(dpg.items())
    [(0, 0, 0, 0), (1, 0, 1, 1), (2, 1, 0, 2), (3, 1, 1, 3), (4, 2, 0, 4)]
    >>> list(dpg.items(missing=True))
    [(5, 2, 1)]
    >>> list(dpg.items(transpose=True))
    [(0, 0, 0, 0), (1, 1, 0, 1), (2, 2, 0, 2), (3, 0, 1, 3), (4, 1, 1, 4)]
    >>> list(dpg.items(transpose=True, missing=True))
    [(5, 2, 1)]

.. code-block::

    >>> dpg = snt.DataPlotGrid(dict(
    ...         a = 0,
    ...         b = 1,
    ...         c = 2,
    ...         d = 3,
    ...         e = 4
    ...     ), 2)
    >>> list(dpg.items())
    [(0, 0, 0, 'a', 0), (1, 0, 1, 'b', 1), (2, 1, 0, 'c', 2), (3, 1, 1, 'd', 3), (4, 2, 0, 'e', 4)]
    >>> list(dpg.items(missing=True))
    [(5, 2, 1)]
    >>> list(dpg.items(transpose=True))
    [(0, 0, 0, 'a', 0), (1, 1, 0, 'b', 1), (2, 2, 0, 'c', 2), (3, 0, 1, 'd', 3), (4, 1, 1, 'e', 4)]
    >>> list(dpg.items(transpose=True, missing=True))
    [(5, 2, 1)]

Example of use: Matplotlib
--------------------------

.. code-block:: python

    >>> from scinumtools import DataPlotGrid
    >>> import matplotlib.pyplot as plt
    >>> 
    >>> dpg = DataPlotGrid(['a','b','c','d','e'],ncols=3,axsize=(1,1))
    >>> 
    >>> fig, axes = plt.subplots(dpg.nrows, dpg.ncols, figsize=dpg.figsize, tight_layout=True)
    >>> for i, m, n, v in dpg.items():
    >>>     ax = axes[m,n]
    >>>     ax.text(0.5, 0.5, v)
    >>> for i, m, n in dpg.items(missing=True):
    >>>     ax = axes[m,n]
    >>>     ax.set_axis_off()
    >>> plt.show()

.. image:: ../_static/figures/data_plot_grid1.png

.. code-block:: python

    >>> fig, axes = plt.subplots(dpg.nrows, dpg.ncols, figsize=dpg.figsize, tight_layout=True)
    >>> for i, m, n, v in dpg.items(transpose=True):
    >>>     ax = axes[m,n]
    >>>     ax.text(0.5, 0.5, v)
    >>> for i, m, n in dpg.items(transpose=True, missing=True):
    >>>     ax = axes[m,n]
    >>>     ax.set_axis_off()
    >>> plt.show()

.. image:: ../_static/figures/data_plot_grid2.png
