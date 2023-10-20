import numpy as np
import pytest
from math import isclose
import os
import pandas as pd
import sys
import time
import cProfile
import pstats
sys.path.insert(0, '../../../src')

from scinumtools.units import *
from scinumtools import RowCollector

if __name__ == '__main__':
    
    file_csv = "material_layers.csv"
    
    with RowCollector(['layer', 'dx', 'T_i', 'T_e', 'rho', 'v']) as rc:
        for i in range(100):
            rc.append(['Li',   20, 20e3, 20e3, 0.534, 0])
            rc.append(['Al',   20, 20e3, 20e3, 2.7,   0])
        for i in range(40):
            rc.append(['Au',   50, 3e-3, 3e-3, 19.32, 0])
        df = rc.to_dataframe()
    df.to_csv(file_csv)

    with cProfile.Profile() as pr:

        height  = quant(1, 'mm').value('cm')
        mass_Au  = quant(10.811, 'Da').value('g')
        mass_Al  = quant(1.0078, 'Da').value('g')
        mass_Li  = quant(2.01410177811, 'Da').value('g')

        csv = pd.read_csv(file_csv)
        rmin = quant(0, 'mm')
        numAu, numAl, numLi = 0, 0, 0
        for index, row in csv.iterrows():
            rmax = rmin + quant(row.dx, 'cm')
            volume = height * np.pi * (rmax**2 - rmin**2)
            mass = volume * quant(row.rho, 'g/cm3')
            layer = row.layer.strip()
            if layer.endswith('Al'):
                numAl = (mass/mass_Al).rebase().value()
            elif layer.endswith('Au'):
                numAu = (mass/mass_Au).rebase().value()
            elif layer.endswith('Li'):
                numLi += (mass/mass_Li).rebase().value()
            rmin = rmax

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(20)
