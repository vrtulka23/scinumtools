RowCollector
============

Scripts can often produce tabulated data row by row, but the amount of data does not require usage of overcomplicated libraries like ``pandas``. ``RowCollector`` is a simple and quick tool that can collect such data and manipulate it with a minimalistic and clean approach.

In the example below, we create a table with three columns ``['col1','col2','col3']``. Rows can be appended at the initialization ``[[1,2,3],[4,5,6]]``, and/or appended later ``[7,8,0]``. Individual columns can be accessed using selectors, or as object attributes.

.. code-block:: python

    >>> from scinumtools import RowCollector
    >>>
    >>> columns = ['col1','col2','col3']
    >>> rows = [[1,2,3],
    >>>         [4,5,6]]
    >>>
    >>> with RowCollector(columns,rows) as rc:
    >>>     rc.append([7,8,0])
    >>>     rc.size()
    3
    >>>     rc.shape()
    (3, 3)
    >>>     rc.col1
    [1, 4, 7]
    >>>     rc['col2']
    [2, 5, 8]

``RowCollector`` object can also be quickly converted into a dictionary, ``pandas`` DataFrame, or text.

.. code-block:: python
    
    >>> with RowCollector(columns,rows) as rc:
    >>>     rc.to_dict()
    {'col1': [1, 4], 'col2': [2, 5], 'col3': [3, 6]}
    >>>     rc.to_dataframe()
       col1  col2  col3
    0     1     2     3
    1     4     5     6
    >>>     rc.to_text()
    '   col1  col2  col3\n0     1     2     3\n1     4     5     6'
        

It is also possible to specify properties of individual columns using ``numpy`` arrays.

.. code-block::        

    >>> rows = [[0,1,2],[3,4,5]]
    >>> columns = {
    >>>     'col1':dict(dtype=bool),
    >>>     'col2':dict(dtype=str),
    >>>     'col3':dict(dtype=float),
    >>> }
    >>> with RowCollector(columns, rows, array=True) as rc:
    >>>     rc.to_dict()
    {'col1': array([False,  True]),
     'col2': array(['1', '4'], dtype='<U1'),
     'col3': array([2., 5.])}
     
One can also sort such table according to values in one of the columns.

.. code-block::

    >>> with RowCollector(columns, rows, array=True) as rc:
    >>>     rc.to_text()
        col1 col2  col3
    0  False    1   2.0
    1   True    4   5.0
    >>>     rc.sort('col1', reverse=True)
    >>>     rc.to_text()
        col1 col2  col3
    0   True    4   5.0
    1  False    1   2.0

    