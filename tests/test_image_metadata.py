import numpy as np
import os
import pytest
from PIL import Image
from io import StringIO 
import sys
sys.path.insert(0, 'src')

from scinumtools import ImageMetadata, Metadata

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
        
@pytest.fixture()
def temp_file():
    dir_temp = "tmp"
    name_temp = "thumbnail.png"
    file_name = f"{dir_temp}/{name_temp}"
    if not os.path.isdir(dir_temp):
        os.mkdir(dir_temp)
    data = np.full((10,10),1)
    with Image.fromarray(data.astype('uint8')) as im:
        im.save(file_name)
    return file_name
    
def test_read_exif(temp_file):
    assert os.path.isfile(temp_file)
    
    with ImageMetadata(temp_file) as im:
        im.set(Metadata.DATETIME,'2024-04-10 18:00:00')

    with ImageMetadata(temp_file) as im:
        assert im.get(Metadata.DATETIME) == '2024-04-10 18:00:00'

def test_print(temp_file):
    assert os.path.isfile(temp_file)
    
    with Capturing() as output:
        with ImageMetadata(temp_file) as im:
            im.set(Metadata.DATETIME,'2024-04-10 18:00:00')
            im.print()
    assert output == [
        'DateTime: 2024-04-10 18:00:00'
    ]