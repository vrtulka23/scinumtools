from dataclasses import dataclass
import numpy as np
import pandas as pd
from typing import Union

@dataclass
class RowCollector:
    """ RowCollector class collect table rows and transform them into one of available formats

    Example of use:

    .. code-block::
    
        import scinumtools as snt
        
        with snt.structs.RowCollector(['col1','col2','col3']) as rc:
             rc.append([1,2,3])
             rc.append([4,5,6])
             data = rc.to_dict()
    
    :param columns: This can be either a list of column names or a dictionary with column array settings
    :param bool array: Stores values as numpy arrays if 'True', otherwise store data in lists
    """
    _columns: list
    _array: bool
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass
    
    def __init__(self, columns: Union[list,dict], rows: list = None, array: bool = False):
        self._columns = []
        self._array = array
        if self._array is False:
            self._columns = []
            for column in columns:      
                setattr(self,column,[])
                self._columns.append(column)
        else:
            if isinstance(columns,dict):
                for column, kwargs in columns.items():
                    setattr(self,column,np.array([],**kwargs))
                    self._columns.append(column)
            else:
                for column in columns:
                    setattr(self,column,np.array([]))
                    self._columns.append(column)
        if rows:
            for row in rows:
                self.append(row)

    def __str__(self):
        return self.to_text()
    
    def __len__(self):
        return self.size()
        
    def __getitem__(self, key: Union[int, str]):
        return getattr(self, key)
        
    def shape(self):
        return (len(self._columns), self.size())

    def append(self, values: list):
        """ Append a single row

        :param values: List of values for each column
        """
        if self._array:
            for n, name in enumerate(self._columns):
                data = getattr(self,name)
                new = np.array(values[n],dtype=data.dtype)
                setattr(self,name, np.append(data,new) )
        else:
            for n, name in enumerate(self._columns):
                getattr(self,name).append(values[n])
            
    def sort(self, name: str, reverse=False):
        """ Sort all columns according to one

        :param str name: name of the sorting column
        """
        ids = np.argsort(getattr(self, name))
        if reverse: ids = ids[::-1]
        if self._array:
            for n, name in enumerate(self._columns):
                setattr(self,name,getattr(self, name)[ids])
        else:
            for n, name in enumerate(self._columns):
                setattr(self,name,list(np.array(getattr(self, name))[ids]))
            
    def size(self):
        """ Get number of items in columns
        """
        if self._columns:
            return len(getattr(self, self._columns[0]))
        else:
            return 0
        
    def to_dict(self):
        """ Convert class data to a dictionary of lists/arrays
        """
        data = {}
        for name in self._columns:
            data[name] = getattr(self,name)
        return data
    
    def to_dataframe(self, columns: Union[list,dict]=None):
        """ Convert class data to a pandas data frame

        :param columns: This can be either a list of columns or a dictionary of column:title pairs. If not set, all coumns are being taken.
        """
        if isinstance(columns,dict):
            return pd.DataFrame({title:getattr(self,name) for name,title in columns.items()})
        elif isinstance(columns,list):
            return pd.DataFrame({name:getattr(self,name) for name in columns})
        else:
            return pd.DataFrame({name:getattr(self,name) for name in self._columns})
        
    def to_text(self, **kwargs):
        """ Convert class data to a text using pandas dataframe

        :param kwargs: kwargs of DataFrame's to_string() method
        """
        return self.to_dataframe().to_string(**kwargs)
