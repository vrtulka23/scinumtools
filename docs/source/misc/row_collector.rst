RowCollector
============

.. code-block:: python

    rows = [[1,2,3],
            [4,5,6],
            [7,8,0]]
            
    columns = ['col1','col2','col3']

.. code-block:: python

    def check_values(rc):
        assert rc.size() == len(rows)
        assert rc.col1 == [1,4,7]
        assert rc.col2 == [2,5,8]
        assert rc.col3 == [3,6,0]

    with snt.RowCollector(columns) as rc:
        for row in rows:
            rc.append(row)
        check_values(rc)
    with snt.RowCollector(columns,rows) as rc:
        check_values(rc)

.. code-block:: python

    with snt.RowCollector(columns) as rc:
        for row in rows:
            rc.append(row)
        assert rc['col1'] == [1,4,7]
        
.. code-block:: python

    with snt.RowCollector(columns) as rc:
        for row in rows:
            rc.append(row)
        rc.append(row)
        assert rc.shape() == (3,4)

.. code-block:: python
    
    with snt.RowCollector(columns,rows) as rc:
        assert rc.to_dict() == dict(
            col1 = [1,4,7],
            col2 = [2,5,8],
            col3 = [3,6,0],
        )
        pd.testing.assert_frame_equal(
            rc.to_dataframe(),
            pd.DataFrame(dict(
                col1 = [1,4,7],
                col2 = [2,5,8],
                col3 = [3,6,0],
            ))
        )
        result = dedent("""\
               col1  col2  col3
            0     1     2     3
            1     4     5     6
            2     7     8     0
        """.rstrip())
        assert rc.to_text() == result
        assert str(rc) == result

.. code-block:: python
    
    def check_values(rc):
        assert rc.size() == len(rows)
        np.testing.assert_equal(rc.col1, [1,4,7])
        np.testing.assert_equal(rc.col2, [2,5,8])
        np.testing.assert_equal(rc.col3, [3,6,0])
        
    with snt.RowCollector(columns, array=True) as rc:
        for row in rows:
            rc.append(row)
        check_values(rc)
    with snt.RowCollector(columns, rows, array=True) as rc:
        check_values(rc)

.. code-block:: python
    
    with snt.RowCollector(columns, rows, array=True) as rc:
        np.testing.assert_equal(rc.to_dict(), dict(
            col1 = [1,4,7], 
            col2 = [2,5,8],
            col3 = [3,6,0],
        ))
        pd.testing.assert_frame_equal(
            rc.to_dataframe(),
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
        assert rc.to_text() == result
        assert str(rc) == result
        
    columns = {'col1':dict(dtype=str),'col2':dict(dtype=float),'col3':dict(dtype=bool)}
    with snt.RowCollector(columns, rows, array=True) as rc:
        np.testing.assert_equal(rc.col1, ['1','4','7'])
        np.testing.assert_equal(rc.col2, [2,5,8])
        np.testing.assert_equal(rc.col3, [True,True,False])
        np.testing.assert_equal(rc.to_dict(), dict(
            col1 = ['1','4','7'], 
            col2 = [2,5,8],
            col3 = [True,True,False],
        ))
        pd.testing.assert_frame_equal(
            rc.to_dataframe(),
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
        assert rc.to_text() == result
        assert str(rc) == result
