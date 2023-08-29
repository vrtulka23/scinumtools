import numpy as np
import pandas as pd
from textwrap import dedent
import sys
sys.path.insert(0, 'src')

import scinumtools as snt

def test_row_collector_list():
    
    columns = ['col1','col2','col3']
    with snt.RowCollector(columns) as lc:
        lc.append([1,2,3])
        lc.append([4,5,6])
        lc.append([7,8,9])
        assert lc.size() == 3
        assert lc.col1 == [1,4,7]
        assert lc.col2 == [2,5,8]
        assert lc.col3 == [3,6,9]
        assert lc.to_dict() == dict(
            col1 = [1,4,7],
            col2 = [2,5,8],
            col3 = [3,6,9],
        )
        pd.testing.assert_frame_equal(
            lc.to_dataframe(),
            pd.DataFrame(dict(
                col1 = [1,4,7],
                col2 = [2,5,8],
                col3 = [3,6,9],
            ))
        )
        result = dedent("""\
               col1  col2  col3
            0     1     2     3
            1     4     5     6
            2     7     8     9
        """.rstrip())
        assert lc.to_text() == result
        assert str(lc) == result
        
def test_row_collector_array():
    
    with snt.RowCollector(['col1','col2','col3'], array=True) as ac:
        ac.append([1,2,3])
        ac.append([4,5,6])
        ac.append([7,8,0])
        assert ac.size() == 3
        np.testing.assert_equal(ac.col1, [1,4,7])
        np.testing.assert_equal(ac.col2, [2,5,8])
        np.testing.assert_equal(ac.col3, [3,6,0])
        np.testing.assert_equal(ac.to_dict(), dict(
            col1 = [1,4,7], 
            col2 = [2,5,8],
            col3 = [3,6,0],
        ))
        pd.testing.assert_frame_equal(
            ac.to_dataframe(),
            pd.DataFrame(dict(
                col1 = [1.,4.,7.],
                col2 = [2.,5.,8.],
                col3 = [3.,6.,0.],
            ))
        )
        result = dedent("""\
               col1  col2  col3
            0   1.0   2.0   3.0
            1   4.0   5.0   6.0
            2   7.0   8.0   0.0
        """.rstrip())
        assert ac.to_text() == result
        assert str(ac) == result
        
    columns = {'col1':dict(dtype=str),'col2':dict(dtype=float),'col3':dict(dtype=bool)}
    with snt.RowCollector(columns, array=True) as ac:
        ac.append([1,2,3])
        ac.append([4,5,6])
        ac.append([7,8,0])
        np.testing.assert_equal(ac.col1, ['1','4','7'])
        np.testing.assert_equal(ac.col2, [2,5,8])
        np.testing.assert_equal(ac.col3, [True,True,False])
        np.testing.assert_equal(ac.to_dict(), dict(
            col1 = ['1','4','7'], 
            col2 = [2,5,8],
            col3 = [True,True,False],
        ))
        pd.testing.assert_frame_equal(
            ac.to_dataframe(),
            pd.DataFrame(dict(
                col1 = ['1','4','7'],
                col2 = [2.,5.,8.],
                col3 = [True,True,False],
            ))
        )
        result = dedent("""\
              col1  col2   col3
            0    1   2.0   True
            1    4   5.0   True
            2    7   8.0  False
        """.rstrip())
        assert ac.to_text() == result
        assert str(ac) == result
