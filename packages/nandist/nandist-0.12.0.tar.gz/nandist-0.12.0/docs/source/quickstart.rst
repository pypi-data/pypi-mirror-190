Quickstart
==========

You can use ``nandist`` as a drop-in replacement for functions from ``scipy.spatial.distance``:

.. code-block:: python
    :caption: Simple example using nan-ignoring ``euclidean`` replacement

    from nandist import euclidean
    import numpy as np

    u, v = np.array([0, 0, 0]), np.array([1, np.nan, np.nan])
    euclidean(u, v)



.. automodule:: nandist
    :members:
