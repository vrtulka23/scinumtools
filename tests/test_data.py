import numpy as np
import os
import sys
sys.path.insert(0, 'src')

from scinumtools.data import *

def test_caching():

    file_cache = "tests/cached_data.npy"
    
    if os.path.isfile(file_cache):
        os.remove(file_cache)
    assert not os.path.isfile(file_cache)
    
    @CachedFunction(file_cache)
    def read_data(a, b):
        return dict(a=a, b=b)

    data = read_data('foo','bar')    
    assert data == dict(a='foo', b='bar')

    data = read_data('foo2','bar2')
    assert os.path.isfile(file_cache)
    assert data == dict(a='foo', b='bar')
    
    if os.path.isfile(file_cache):
        os.remove(file_cache)
    assert not os.path.isfile(file_cache)

    @CachedFunction(file_cache)
    def read_data():
        return {
            'array': np.linspace(1,100,100),
            'scalar': 34,
            'string': 'foo',
        }
    
    data = read_data()
    np.testing.assert_equal(data, dict(
        array=np.linspace(1,100,100),
        scalar=34,
        string='foo',
    ))
    
def test_normalizing():

    xlen = 10
    ylen = 20
    data = np.linspace(1,xlen*ylen,xlen*ylen).reshape(xlen,ylen) - 10

    # Test only data
    with NormalizeData() as n:
        for row in data:
            n.append(row)
        linnorm = n.linnorm()
        lognorm = n.lognorm()
        zranges = n.zranges()

    assert linnorm.vmin == -9.
    assert linnorm.vmax == 190.0
    assert lognorm.vmin == 0
    assert lognorm.vmax == 2.278753600952829
    assert zranges.minpos == 1
    assert zranges.min == -9
    assert zranges.max == 190.0
    
    # Test data and x-axis
    with NormalizeData(xaxis=True) as n:
        for r,row in enumerate(data):
            xdata = np.linspace(-r,r,xlen)
            n.append(row, xdata)
        xranges = n.xranges()

    assert xranges.minpos == 0.11111111111111116
    assert xranges.min == -9
    assert xranges.max == 9

    # Test data and both axes
    with NormalizeData(xaxis=True, yaxis=True) as n:
        for r,row in enumerate(data):
            xdata = np.linspace(-r,r,xlen)
            ydata = np.linspace(-r*2,r*2,ylen)
            n.append(row, xdata, ydata)
        xranges = n.xranges()
        yranges = n.yranges()

    assert xranges.minpos == 0.11111111111111116
    assert xranges.min == -9
    assert xranges.max == 9
    assert yranges.minpos == 0.10526315789473673
    assert yranges.min == -18
    assert yranges.max == 18
    
def test_list_to_grid():

    data = range(5)
    ncols = 2
    
    # List all defined grid points
    grid = [
        (0, 0, 0, 0),
        (1, 0, 1, 1),
        (2, 1, 0, 2),
        (3, 1, 1, 3),
        (4, 2, 0, 4),
    ]
    for r,row in enumerate(ListToGrid(data,ncols)):
        assert grid[r] == row

    # List all missing grid points
    for r,row in enumerate(ListToGrid(data,ncols,missing=True)):
        assert (5, 2, 1) == row

    # List transposed grid points
    grid = [
        (0, 0, 0, 0),
        (1, 1, 0, 1),
        (2, 2, 0, 2),
        (3, 0, 1, 3),
        (4, 1, 1, 4),
    ]
    for r,row in enumerate(ListToGrid(data,ncols,transpose=True)):
        assert grid[r] == row
        
    # List all missing transposed grid points
    for r,row in enumerate(ListToGrid(data,ncols,transpose=True,missing=True)):
        assert (5, 2, 1) == row
        
def test_dict_to_grid():

    data = dict(
        a = 0,
        b = 1,
        c = 2,
        d = 3,
        e = 4
    )
    ncols = 2
    
    # List all defined grid points
    grid = [
        (0, 0, 0, 'a', 0),
        (1, 0, 1, 'b', 1),
        (2, 1, 0, 'c', 2),
        (3, 1, 1, 'd', 3),
        (4, 2, 0, 'e', 4),
    ]
    for r,row in enumerate(DictToGrid(data,ncols)):
        assert grid[r] == row

    # List all missing grid points
    grid = [
        (5, 2, 1)
    ]
    for r,row in enumerate(DictToGrid(data,ncols,missing=True)):
        assert grid[r] == row
        
    # List all transposed grid points
    grid = [
        (0, 0, 0, 'a', 0),
        (1, 1, 0, 'b', 1),
        (2, 2, 0, 'c', 2),
        (3, 0, 1, 'd', 3),
        (4, 1, 1, 'e', 4),
    ]
    for r,row in enumerate(DictToGrid(data,ncols,transpose=True)):
        assert grid[r] == row

    # List all missing transposed grid points
    grid = [
        (5, 2, 1)
    ]
    for r,row in enumerate(DictToGrid(data,ncols,transpose=True,missing=True)):
        assert grid[r] == row
        
def test_thumbnail():

    # Test grayscale case
    nx, ny = 300, 200
    data = np.zeros((nx,ny))
    for i in range(nx):
        for j in range(ny):
            data[i,j] = (i-nx/2)**2 + (j-ny/2)**2
            imold = ThumbnailImage(
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
    imold = ThumbnailImage(
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
    
