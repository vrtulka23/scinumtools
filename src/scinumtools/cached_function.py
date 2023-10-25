import os
import numpy as np
import hashlib
import json

def hash_file_name(file_cache, args, kwargs):
    json_string = json.dumps({'args':args,'kwargs':kwargs}, sort_keys=True)
    hash_object = hashlib.sha256()
    hash_object.update(json_string.encode())
    hash_value = hash_object.hexdigest()
    file_name, file_extension = os.path.splitext(file_cache)
    return f"{file_name}.{hash_value}{file_extension}"

def CachedFunction(file_cache):
    """ Decorator function that cashes data produced by a function

    :param str file_cache: Name of the file that will store cached data
    """
    def wrapped(func):
        def inner(*args, **kwargs):
            file_data = hash_file_name(file_cache, args, kwargs)
            if not os.path.isfile(file_data):
                np.save(file_data, func(*args, **kwargs))
            data = np.load(file_data, allow_pickle=True)
            return data.item() if data.ndim==0 else data
        return inner
    return wrapped
