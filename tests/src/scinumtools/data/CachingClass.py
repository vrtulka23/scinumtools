import os
import numpy as np

def CachedFunction(file_cache):
    """ Decorator function that cashes data produced by a function

    :param str file_cache: Name of the file that will store cached data
    """
    def wrapped(func):
        def inner(*args, **kwargs):
            if not os.path.isfile(file_cache):
                np.save(file_cache, func(*args, **kwargs))
            return np.load(file_cache, allow_pickle=True)
        return inner
    return wrapped
