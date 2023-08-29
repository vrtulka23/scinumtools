import time
from textwrap import dedent
import sys
sys.path.insert(0, 'src')

from scinumtools import Stopwatch

def test_stopwatch():
    # Using as a normal object
    sw = Stopwatch()
    sw.start('part1')
    time.sleep(.1)
    sw.start('part2')
    time.sleep(.1)
    sw.stop('part2')
    sw.stop('part1')
    sw.start('part3')
    time.sleep(.3)
    sw.stop('part3')
    result = sw.report().to_dict()
    assert result['Laps'] == [6, 1, 1, 1]
    assert result['Node'] == ['stopwatch', 'part1/part2', 'part1', 'part3']

    # Using 'with' statement
    with Stopwatch() as sw:
        with sw.observer('part1'):
            time.sleep(.1)
            with sw.observer('part2'):
                time.sleep(.1)
        with sw.observer('part3'):
            time.sleep(.3)
        result = sw.report().to_dict()
        assert result['Laps'] == [6, 1, 1, 1]
        assert result['Node'] == ['stopwatch', 'part1/part2', 'part1', 'part3']
