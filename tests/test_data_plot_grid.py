import numpy as np
import os
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

def test_data_plot_grid_list():
    # test lists
    grid = [
        (0, 0, 0, 0),
        (1, 0, 1, 1),
        (2, 1, 0, 2),
        (3, 1, 1, 3),
        (4, 2, 0, 4),
    ]
    dpg = snt.DataPlotGrid(list(range(5)), 2)
    for i, m, n, v in dpg.items():
        assert grid[i] == (i, m, n, v)
    for i, m, n in dpg.items(missing=True):
        assert (i, m, n) == (5, 2, 1)
    grid = [
        (0, 0, 0, 0),
        (1, 1, 0, 1),
        (2, 2, 0, 2),
        (3, 0, 1, 3),
        (4, 1, 1, 4),
    ]
    for i, m, n, v in dpg.items(transpose=True):
        assert grid[i] == (i, m, n, v)
    for i, m, n in dpg.items(transpose=True, missing=True):
        assert (i, m, n) == (5, 2, 1)

def test_data_plot_grid_dict():        
    # test dictionaries
    dpg = snt.DataPlotGrid(dict(
        a = 0,
        b = 1,
        c = 2,
        d = 3,
        e = 4
    ), 2)
    grid = [
        (0, 0, 0, 'a', 0),
        (1, 0, 1, 'b', 1),
        (2, 1, 0, 'c', 2),
        (3, 1, 1, 'd', 3),
        (4, 2, 0, 'e', 4),
    ]
    for i,m,n,k,v in dpg.items():
        assert grid[i] == (i,m,n,k,v)
    for i,m,n in dpg.items(missing=True):
        assert (5, 2, 1) == (i,m,n)
    grid = [
        (0, 0, 0, 'a', 0),
        (1, 1, 0, 'b', 1),
        (2, 2, 0, 'c', 2),
        (3, 0, 1, 'd', 3),
        (4, 1, 1, 'e', 4),
    ]
    for i,m,n,k,v in dpg.items(transpose=True):
        assert grid[i] == (i,m,n,k,v)
    for i,m,n in dpg.items(transpose=True,missing=True):
        assert (5, 2, 1) == (i,m,n)
        