import numpy as np
import os
import pytest
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

@pytest.fixture
def mock_data():
    xlen = 10
    ylen = 20
    data = np.linspace(1,xlen*ylen,xlen*ylen).reshape(xlen,ylen) - 10
    return xlen, ylen, data

def test_data_only(mock_data):
    xlen, ylen, data = mock_data

    # Test only data
    with snt.NormalizeData() as n:
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
    
def test_data_xaxis(mock_data):
    xlen, ylen, data = mock_data

    # Test data and x-axis
    with snt.NormalizeData(xaxis=True) as n:
        for r,row in enumerate(data):
            xdata = np.linspace(-r,r,xlen)
            n.append(row, xdata)
        xranges = n.xranges()

    assert xranges.minpos == 0.11111111111111116
    assert xranges.min == -9
    assert xranges.max == 9

def test_data_xyaxis(mock_data):
    xlen, ylen, data = mock_data

    # Test data and both axes
    with snt.NormalizeData(xaxis=True, yaxis=True) as n:
        for r,row in enumerate(data):
            xdata = np.linspace(-r,r,xlen)
            ydata = np.linspace(-r*2,r*2,ylen)
            n.append(row, xdata, ydata)
        xranges = n.xranges()
        yranges = n.yranges()
        extent = n.extent()

    assert xranges.minpos == 0.11111111111111116
    assert xranges.min == -9
    assert xranges.max == 9
    assert yranges.minpos == 0.10526315789473673
    assert yranges.min == -18
    assert yranges.max == 18
    
def test_iterator(mock_data):
    xlen, ylen, data = mock_data

    with snt.NormalizeData(xaxis='lin', yaxis='lin') as n:
        for r,row in enumerate(data):
            xdata = np.linspace(-r,r,xlen)
            ydata = np.linspace(-r*2,r*2,ylen)
            n.append(row, xdata, ydata)

        item, extent = n[0]
        assert extent == (0,0,0,0)

        for i, (item, extent) in enumerate(n.items()):
            assert extent == (-i,i,-i*2,i*2)
            assert np.all(data[i] == item)