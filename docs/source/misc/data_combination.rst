DataCombination
===============

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
