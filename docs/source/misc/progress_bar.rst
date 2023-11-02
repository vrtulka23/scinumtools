ProgressBar
===========

.. code-block:: python

    nsteps = 200
    pb = snt.ProgressBar(nsteps)
    for i in range(nsteps):
        pb.step()
    pb.close()

    with snt.ProgressBar(nsteps) as pb:
        pb.step()
        