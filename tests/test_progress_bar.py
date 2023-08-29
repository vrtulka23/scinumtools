import numpy as np
import pandas as pd
from textwrap import dedent
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

def test_progressbar():

    nsteps = 200
    pb = snt.ProgressBar(nsteps)
    for i in range(nsteps):
        pb.step()
    pb.close()

    with snt.ProgressBar(nsteps) as pb:
        pb.step()
        