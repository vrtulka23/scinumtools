Stopwatch
=========

.. code-block:: python

    # Using as a normal object
    sw = Stopwatch()
    sw.start('part1')
    time.sleep(.001)
    sw.start('part2')
    time.sleep(.001)
    sw.stop('part2')
    sw.stop('part1')
    sw.start('part3')
    time.sleep(.003)
    sw.stop('part3')
    result = sw.report().to_dict()
    assert result['Laps'] == [6, 1, 1, 1]
    assert result['Node'] == ['stopwatch', 'part1/part2', 'part1', 'part3']

.. code-block:: python

    with Stopwatch() as sw:
        with sw.observer('part1'):
            time.sleep(.001)
            with sw.observer('part2'):
                time.sleep(.001)
        with sw.observer('part3'):
            time.sleep(.003)
        result = sw.report().to_dict()
        assert result['Laps'] == [6, 1, 1, 1]
        assert result['Node'] == ['stopwatch', 'part1/part2', 'part1', 'part3']
