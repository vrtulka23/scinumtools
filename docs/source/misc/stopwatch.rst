Stopwatch
=========

``Stopwatch`` class is similar to other profiling tools like ``cProfile``, but it focuses on profiling of individual code parts rather than functions. Method ``report()`` collects and composes the final report in a form of a ``RowCollector`` object.

.. code-block:: python

    >>> sw = Stopwatch()
    >>> sw.start('part1')
    >>> time.sleep(.001)
    >>> sw.start('part2')
    >>> time.sleep(.001)
    >>> sw.stop('part2')
    >>> sw.stop('part1')
    >>> sw.start('part3')
    >>> time.sleep(.003)
    >>> sw.stop('part3')
    >>> report = sw.report()
    >>> report['Node']
    ['stopwatch', 'part1/part2', 'part1', 'part3']
    >>> report.to_text()
       Laps      Time  Time/Lap         Node
    0     6  0.000035  0.000006    stopwatch
    1     1  0.001389  0.001389  part1/part2
    2     1  0.002804  0.002804        part1
    3     1  0.003863  0.003863        part3
    
The same effect as above can also be achieved using ``with`` statements.

.. code-block:: python

    >>> with Stopwatch() as sw:
    >>>     with sw.observer('part1'):
    >>>         time.sleep(.001)
    >>>         with sw.observer('part2'):
    >>>             time.sleep(.001)
    >>>     with sw.observer('part3'):
    >>>         time.sleep(.003)
    >>>     sw.report().to_text()
       Laps      Time  Time/Lap         Node
    0     6  0.000033  0.000006    stopwatch
    1     1  0.001301  0.001301  part1/part2
    2     1  0.002698  0.002698        part1
    3     1  0.003781  0.003781        part3
