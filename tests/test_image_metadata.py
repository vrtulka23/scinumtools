import numpy as np
import os
import pytest
from PIL import Image
import piexif
import sys
sys.path.insert(0, 'src')

from scinumtools import ImageMetadata, Metadata

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
        im.set(Metadata.DATETIME,'World')

    with ImageMetadata(temp_file) as im:
        assert im.get(Metadata.DATETIME) == 'World'
