ParameterTable
==============

``ParameterTable`` can be used as a quick tool for constant parameter set definitons.
The main advantage of this structure is, that one does not have to repeat parameter names every time a new parameter is created.
Parameter names are defined only once at the beginning and afterward one needs to input only their values.

In the example below we append one row of parameters after another.
First we define parameter keys ``['a','b','c']`` and then we input values independently using ``append()`` method.

.. code-block:: python

    >>> from scinumtools import ParameterTable
    >>>
    >>> with ParameterTable(['a','b','c']) as pt:
    >>>     pt.append([1, 2, 3])
    >>>     pt.append([4, 5, 6])
    >>>
    >>>     print(pt[0])
    ParameterSettings(a=1 b=2 c=3)
    >>>     pt[1].a
    4
    >>>     pt[1]['b']
    5
    >>>     pt.shape()
    (2, 3)

Parameters can also be defined at once as a nested list/tuples of values.
This is especially useful for static parameter definitions, because one does not need to repeat parameter names.
Definition of parameters thus stay clean and concise.

.. code-block:: python

    >>> pt = ParameterTable(['row','column','width','height','log','name','unit'],[
    >>>     [ 2, 5, 23.3, 25.2, True,  'Density',     'g/cm3' ],
    >>>     [ 3, 2, 49.2, 55.2, False, 'Temperature', 'K'     ],
    >>>     [ 5, 3, 24.2, 83.2, False, 'Velocity',    'km/s'  ],
    >>> ])
    >>>
    >>> pt[1].log
    False

Parameter sets defined above used simple lists, but it is also possible to define and access associative parameter lists using string keys.
Sets of parameters and individual values can be accessed both as list selectors, or objects.

.. code-block:: python

    >>> names = ['a','b','c']
    >>> params = {'d':[1,2,3]}
    >>> with ParameterTable(names, params, keys=True) as pt:
    >>>     pt.append('e', [4, 5, 6])
    >>>     pt['f'] = [7, 8, 9]
    >>>
    >>>     pt['d']
    ParameterSettings(a=1 b=2 c=3)
    >>>     pt.e.b
    5
    
If needed, parameter sets can be deleted similarly as standard list, or dictionary items.

.. code-block:: python

    >>> with ParameterTable(['a','b','c']) as pt:
    >>>     pt.append([1, 2, 3])
    >>>     pt.append([4, 5, 6])
    >>>     
    >>>     del pt[0]
    >>>     pt.shape()
    (1, 3)

    >>> with ParameterTable(['a','b','c'], keys=True) as pt:
    >>>     pt['d'] = [1, 2, 3]
    >>>     pt.append( 'e', [4, 5, 6] )
    >>>     
    >>>     del pt['d']
    >>>     pt.shape()
    (1, 3)

Parameter table object can also be easily converted into a Pandas DataFrame, or casted as a text. If rows in parameter table have keys, it is possible to set a name for the parameter key column. By default symbol ``#`` is used.

.. code-block::

    >>> with snt.ParameterTable(['a','b','c'], keys=True, keyname='x') as pt:
    >>>     pt['d'] = [1, 2, 3]
    >>>     pt['e'] = [4, 5, 6]
    >>>     df = pt.to_dataframe()
    >>>     pt.to_text()
       x  a  b  c
    0  d  1  2  3
    1  e  4  5  6
