Functions
=========

Use these functions to calculate distances between two arrays ``u`` and ``v``.

.. admonition:: warning

    Note: The documentation is exactly the same as the documentation from ``scipy.spatial`` but is included here
    for completeness.


.. autofunction:: nandist.braycurtis
.. autofunction:: nandist.canberra
.. autofunction:: nandist.chebyshev
.. autofunction:: nandist.cityblock
.. autofunction:: nandist.correlation
.. autofunction:: nandist.cosine
.. autofunction:: nandist.euclidean
.. autofunction:: nandist.jensenshannon
.. autofunction:: nandist.mahalanobis
.. autofunction:: nandist.minkowski
.. autofunction:: nandist.seuclidean
.. autofunction:: nandist.sqeuclidean

Pairwise (single input)
=======================

Use ``pdist`` to calculate all pairwise distances between vectors in a matrix ``X``.

.. autofunction:: nandist.pdist

Pairwise (two inputs)
=====================

Use ``cdist`` to calculate all pairwise distances between vectors in matrices ``XA`` and ``XB``.


.. autofunction:: nandist.cdist
