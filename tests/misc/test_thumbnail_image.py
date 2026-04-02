import numpy as np
import pytest
import os
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

@pytest.fixture()
def temp_file():
    dir_temp = "tmp"
    name_temp = "thumbnail.png"
    if os.path.isdir(dir_temp):
        if os.path.isdir(f"{dir_temp}/{name_temp}"):
            os.remove()
    else:
        os.mkdir(dir_temp)
    return f"{dir_temp}/{name_temp}"

def test_grayscale():

    # Test grayscale case
    nx, ny = 300, 200
    data = np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            data[i,j] = (i-nx/2)**2 + (j-ny/2)**2
    imold = snt.ThumbnailImage(
        data = data,
        extent = (-30,30,-20,20),
    )
    np.testing.assert_equal(np.asarray(imold.im), data)

    # Test grayscale resizing
    data_resized = [
        [9.6480850e+03, 1.1210736e+04, 9.5458672e+03, 1.1227712e+04, 9.3136709e+03],
        [1.0238771e+04, 9.7449180e+03, 6.8944453e+03, 9.7642842e+03, 9.8572793e+03],
        [5.1896011e+03, 2.6150837e+03, 1.7226636e-03, 2.6263579e+03, 4.9675088e+03],
        [1.0238771e+04, 9.7449180e+03, 6.8944453e+03, 9.7642842e+03, 9.8572793e+03],
        [9.3407617e+03, 1.0838822e+04, 9.2195254e+03, 1.0855267e+04, 9.0168174e+03],
    ]    
    imnew = imold.crop((-35,35,-25,25)).resize((5,5))   # input tuples
    np.testing.assert_almost_equal(np.asarray(imnew.im), data_resized, decimal=3)

def test_rgb():

    # Test RGB case
    nx, ny = 300, 200
    data = np.zeros((nx,ny,3), dtype=float)
    for i in range(nx):
        for j in range(ny):
            data[i,j] = [(i-nx/2)**2 + (j-ny/2)**2]*3
    data = (255*data/data.max()).astype(np.uint8)
    imold = snt.ThumbnailImage(
        data = data,
        extent = (-30,30,-20,20),
        mode = 'RGB'
    )
    np.testing.assert_equal(np.asarray(imold.im), data)

    # Test RGB resizing
    data_resized = [
        [[76, 76, 76],
         [88, 88, 88],
         [75, 75, 75],
         [88, 88, 88],
         [73, 73, 73]],
        [[80, 80, 80],
         [76, 76, 76],
         [54, 54, 54],
         [76, 76, 76],
         [77, 77, 77]],
        [[40, 40, 40],
         [20, 20, 20],
         [ 0,  0,  0],
         [20, 20, 20],
         [39, 39, 39]],
        [[80, 80, 80],
         [76, 76, 76],
         [54, 54, 54],
         [76, 76, 76],
         [77, 77, 77]],
        [[73, 73, 73],
         [85, 85, 85],
         [72, 72, 72],
         [85, 85, 85],
         [71, 71, 71]],
    ]
    imnew = imold.crop(-35,35,-25,25).resize(5,5)     # input individual values
    np.testing.assert_equal(np.asarray(imnew.im), data_resized)
    
def test_read_save_file(temp_file):
    
    # Test grayscale case
    nx, ny = 300, 200
    data = np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            data[i,j] = (i-nx/2)**2 + (j-ny/2)**2
            
    # Save image into a temporary file
    snt.ThumbnailImage(data).save(temp_file)
    
    # Load image from a temporary file
    image = snt.ThumbnailImage(temp_file, mode='F')
    
    # Resize image
    image.resize(5, 5)
    
    np.testing.assert_almost_equal(np.asarray(image.im), [
        [254.99962, 255.00188, 255.09755, 255.00336, 254.9995, ],
        [255.00157, 254.99255, 254.54832, 254.98578, 255.0021, ],
        [255.20503, 253.91243, 215.97983, 253.3033,  255.2591, ],
        [255.00352, 254.98228, 254.17003, 254.96962, 255.00458,],
        [254.9995,  255.00252, 255.12416, 255.0044,  254.99934,],
    ], decimal=4)

def test_default_extent(temp_file):
    
    # Test grayscale case
    nx, ny = 300, 150
    data = np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            data[i,j] = (i-nx/2)**2 + (j-ny/2)**2
            
    # Save image into a temporary file
    thumb = snt.ThumbnailImage(data)
    assert thumb.extent == [0, 1, 0, 2.0]
    thumb.crop([0, 2, 0, 2])
    assert thumb.im.size == (300, 300)
    thumb.save(temp_file)
    