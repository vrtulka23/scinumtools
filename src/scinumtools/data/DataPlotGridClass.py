import numpy as np
from typing import Union

class DataPlotGrid:
    data: Union[list,dict]
    ndata: int
    ncols: int
    nrows: int
    figsize: tuple

    def __init__(self, data: Union[list,dict], ncols:int=2, axsize:tuple=(4,2)):
        self.data = data
        self.ndata = len(data)
        self.ncols = ncols
        self.nrows = int(np.ceil(self.ndata/self.ncols))
        self.figsize = (self.ncols*axsize[0], self.nrows*axsize[1])

    def items(self, missing:bool=None, transpose:bool=False):
        if missing:
            for i in range(self.ndata, self.ncols*self.nrows):
                if transpose:
                    yield (i,int(i%self.nrows),int(i/self.nrows))
                else:
                    yield (i,int(i/self.ncols),int(i%self.ncols))
        else:
            if isinstance(self.data, list):
                for i,d in enumerate(self.data):
                    if transpose:
                        yield (i,int(i%self.nrows),int(i/self.nrows),d)
                    else:
                        yield (i,int(i/self.ncols),int(i%self.ncols),d)
            elif isinstance(self.data, dict):
                for i,(k,v) in enumerate(self.data.items()):
                    if transpose:
                        yield (i,int(i%self.nrows),int(i/self.nrows),k,v)
                    else:
                        yield (i,int(i/self.ncols),int(i%self.ncols),k,v)
            else:
                raise Exception('Wrong data type:', self.data)
