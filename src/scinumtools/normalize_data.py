from matplotlib.colors import Normalize, LogNorm
from dataclasses import dataclass
import numpy as np

from .row_collector import RowCollector

@dataclass
class Ranges:
    """ Dataclass that contains data ranges
    """
    minpos: float
    min: float
    max: float

class NormalizeData:
    """ Normalize numerical data across multiple plots
    """

    xaxis: str
    yaxis: str
    _collector: RowCollector

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass

    def __init__(self, xaxis=None, yaxis=None):
        self.xaxis = xaxis
        self.yaxis = yaxis
        columns = ['zdata','zminpos','zmin','zmax']
        if xaxis: columns += ['xminpos','xmin','xmax']
        if yaxis: columns += ['yminpos','ymin','ymax']
        self._collector = RowCollector(columns)

    def __getitem__(self, idx: int):
        data = self._collector.zdata[idx]
        if self.xaxis and self.yaxis:
            if self.xaxis=='lin' and self.yaxis=='lin':
                extent = (self._collector.xmin[idx], self._collector.xmax[idx], self._collector.ymin[idx], self._collector.ymax[idx])
            elif self.xaxis=='log' and self.yaxis=='lin':
                extent = (self._collector.xminpos[idx], self._collector.xmax[idx], self._collector.ymin[idx], self._collector.ymax[idx])
            elif self.xaxis=='lin' and self.yaxis=='log':
                extent = (self._collector.xmin[idx], self._collector.xmax[idx], self._collector.yminpos[idx], self._collector.ymax[idx])
            elif self.xaxis=='log' and self.yaxis=='log':
                extent = (self._collector.xminpos[idx], self._collector.xmax[idx], self._collector.yminpos[idx], self._collector.ymax[idx])
            return data, extent
        else:
            return data
            
    def items(self):
        for i in range(len(self._collector)):
            yield self[i]

    def append(self, vdata, xdata=None, ydata=None):
        """ Append data to the range collector
        
        Statistics of x and y axes is optional

        :param vdata: Numerical data
        :param xdata: X-axis points
        :param ydata: Y-axis points
        """
        zminpos = np.nanmin(vdata[vdata>0]) if np.sum(vdata>0) else np.nan
        ranges = [vdata,zminpos,np.min(vdata), np.max(vdata)]
        if self.xaxis:
            if xdata is None:
                raise Exception("Missing x-axes values")
            xminpos = np.nanmin(xdata[xdata>0]) if np.sum(xdata>0) else np.nan
            ranges += [xminpos,np.min(xdata),np.max(xdata)]
        if self.yaxis:
            if ydata is None:
                raise Exception("Missing y-axes values")
            yminpos = np.nanmin(ydata[ydata>0]) if np.sum(ydata>0) else np.nan
            ranges += [yminpos,np.min(ydata),np.max(ydata)]
        self._collector.append(ranges)

    def data(self):
        """ Return collected ranges as a dictionary
        """
        return self._collector.to_dict()

    def xranges(self):
        """ Return x-axis ranges
        """
        return Ranges(
            minpos = np.nanmin(self._collector.xminpos),
            min = np.nanmin(self._collector.xmin),
            max = np.nanmax(self._collector.xmax)
        )
    
    def yranges(self):
        """ Return y-axis ranges
        """
        return Ranges(
            minpos = np.nanmin(self._collector.yminpos),
            min = np.nanmin(self._collector.ymin),
            max = np.nanmax(self._collector.ymax)
        )
        
    def zranges(self):
        """ Return data ranges
        """
        return Ranges(
            minpos = np.nanmin(self._collector.zminpos),
            min = np.nanmin(self._collector.zmin),
            max = np.nanmax(self._collector.zmax)
        )
    
    def linnorm(self):
        """ Return linear norm from ranges
        """
        return Normalize(
            vmin=np.nanmin(self._collector.zmin), 
            vmax=np.nanmax(self._collector.zmax)
        )

    def lognorm(self):
        """ Return logarithmic norm from ranges
        """
        return LogNorm(
            vmin=np.log10(np.nanmin(self._collector.zminpos)), 
            vmax=np.log10(np.nanmax(self._collector.zmax))
        )

    def extent(self, xlog=False, ylog=False):
        xranges = self.xranges()
        yranges = self.yranges()
        if xlog and ylog:
            return (xranges.minpos, xranges.max, yranges.minpos, yranges.max)
        elif xlog:
            return (xranges.minpos, xranges.max, yranges.min, yranges.max)
        elif ylog:
            return (xranges.min, xranges.max, yranges.minpos, yranges.max)            
        else:
            return (xranges.min, xranges.max, yranges.min, yranges.max)     