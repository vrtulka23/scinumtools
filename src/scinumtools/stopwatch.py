import time
import numpy as np

from .row_collector import RowCollector

class Stopwatch:
    """ Helper class that measures time of various processes in the code

    All nodes have to be closed in an oposite order as started.
    """

    _watches: dict
    _nodes: list

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass
    
    def __init__(self):
        self._nodes = []
        self._watches = {
            'stopwatch': {'laps':0, 'time': 0}
        }
    
    def start(self, name:str):
        """ Start a new measuring node

        :param str name: Name of a node
        """
        start = time.time()
        self._nodes.append(name)
        node = '/'.join(self._nodes)
        if node not in self._watches:
            self._watches[node] = {
                'start': 0.,
                'laps': 0,
                'time': 0.
            }
        self._watches[node]['start'] = time.time()
        self._watches[node]['laps'] += 1
        self._watches['stopwatch']['time'] += time.time()-start
        self._watches['stopwatch']['laps'] += 1

    def stop(self, name:str):
        """ Stop existing node

        :param str name: Name of a node
        """
        start = time.time()
        if self._nodes[-1]!=name:
            raise Exception(f"Stopwatch node '{self._nodes[-1]}' was not closed!")
        node = '/'.join(self._nodes)
        self._watches[node]['time'] += time.time()-self._watches[node]['start']
        self._watches[node]['start'] = 0.
        self._watches['stopwatch']['time'] += time.time()-start
        self._watches['stopwatch']['laps'] += 1
        self._nodes.pop()

    def observer(self, name:str):
        """ Start an observer

        :param str name: Name of a node
        """
        return StopwatchObserver(name,self)
        
    def report(self):
        """ Print time report for all nodes
        """        
        lc = RowCollector(['Laps','Time','Time/Lap','Node'])
        for name,watch in self._watches.items():
            lc.append([
                watch['laps'],
                watch['time'],
                watch['time']/watch['laps'],
                name
            ])
        lc.sort('Time')
        return lc

class StopwatchObserver:

    name: str
    _stopwatch: Stopwatch
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        self._stopwatch.stop(self.name)
        pass

    def __init__(self, name, stopwatch):
        self.name = name
        self._stopwatch = stopwatch
        self._stopwatch.start(self.name)
