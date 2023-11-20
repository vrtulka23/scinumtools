import time
from textwrap import dedent
import sys
sys.path.insert(0, 'src')

from scinumtools import Stopwatch

def test_normal_object():
    # Using as a normal object
    sw = Stopwatch()
    sw.start('part1')
    time.sleep(.01)
    sw.start('part2')
    time.sleep(.02)
    sw.stop('part2')
    sw.stop('part1')
    sw.start('part3')
    time.sleep(.05)
    sw.stop('part3')
    result = sw.report().to_dict()
    assert result['Laps'] == [6, 1, 1, 1]
    assert result['Node'] == ['stopwatch', 'part1/part2', 'part1', 'part3']

def test_with_statement():
    with Stopwatch() as sw:
        with sw.observer('part1'):
            time.sleep(.01)
            with sw.observer('part2'):
                time.sleep(.02)
        with sw.observer('part3'):
            time.sleep(.05)
        result = sw.report().to_dict()
        assert result['Laps'] == [6, 1, 1, 1]
        assert result['Node'] == ['stopwatch', 'part1/part2', 'part1', 'part3']
