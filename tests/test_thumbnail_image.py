import numpy as np
import os
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

def test_thumbnail():

    # Test grayscale case
    nx, ny = 300, 200
    data = np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            data[i,j] = (i-nx/2)**2 + (j-ny/2)**2
    imold = snt.ThumbnailImage(
        extent = (-30,30,-20,20),
        data = data
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
    imnew = imold.resize((-35,35,-25,25), (5,5))
    np.testing.assert_almost_equal(np.asarray(imnew.im), data_resized, decimal=3)

    # Test RGB case
    nx, ny = 300, 200
    data = np.zeros((nx,ny,3), dtype=float)
    for i in range(nx):
        for j in range(ny):
            data[i,j] = [(i-nx/2)**2 + (j-ny/2)**2]*3
    data = (255*data/data.max()).astype(np.uint8)
    imold = snt.ThumbnailImage(
        extent = (-30,30,-20,20),
        data = data,
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
    imnew = imold.resize((-35,35,-25,25), (5,5))
    np.testing.assert_equal(np.asarray(imnew.im), data_resized)
    