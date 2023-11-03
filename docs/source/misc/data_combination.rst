DataCombination
===============

``DataCombination`` class is designed to quickly iterate over all combination of data in multiple lists.
Under the hood, it utilizes ``itertools`` module and calculate product of inputted lists.

.. code-block:: python

    >>> from scinumtools import DataCombinations
    >>> pc = DataCombination([
    >>>     ['a','b'],
    >>>     ['c','d','e']
    >>> ])
    >>> list(pc.keys())
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    >>> list(pc.values())
    [('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'c'), ('b', 'd'), ('b', 'e')]
    >>> list(pc.items())
    [((0, 0), ('a', 'c')), ((0, 1), ('a', 'd')), ((0, 2), ('a', 'e')), ((1, 0), ('b', 'c')), ((1, 1), ('b', 'd')), ((1, 2), ('b', 'e'))]

Similarily as a standard Python dictionary, ``DataCombination`` can iterate over list indexes (``keys()``), values (``values()``), or both (``items()``). This is especially useful for parameter studies, where one needs to produce large sets of initial conditions.

.. code-block:: python

   >>> radius = [2,4,6,8]
   >>> temperature = [12, 24, 48]
   >>> pc = DataCombination([radius, temperature])
   >>> ics = []
   >>> for (r,t), (rval, tval) in pc.items():
   >>>     ics.append({
   >>>         "simulation": f"sim-{r:02d}-{t:02d}",
   >>>         "radius": rval,
   >>>         "temperature": tval,
   >>>     })
   [{'simulation': 'sim-00-00', 'radius': 2, 'temperature': 12},
    {'simulation': 'sim-00-01', 'radius': 2, 'temperature': 24},
    {'simulation': 'sim-00-02', 'radius': 2, 'temperature': 48},
    {'simulation': 'sim-01-00', 'radius': 4, 'temperature': 12},
    {'simulation': 'sim-01-01', 'radius': 4, 'temperature': 24},
    {'simulation': 'sim-01-02', 'radius': 4, 'temperature': 48},
    {'simulation': 'sim-02-00', 'radius': 6, 'temperature': 12},
    {'simulation': 'sim-02-01', 'radius': 6, 'temperature': 24},
    {'simulation': 'sim-02-02', 'radius': 6, 'temperature': 48},
    {'simulation': 'sim-03-00', 'radius': 8, 'temperature': 12},
    {'simulation': 'sim-03-01', 'radius': 8, 'temperature': 24},
    {'simulation': 'sim-03-02', 'radius': 8, 'temperature': 48}]