Supported distances
===================

Distance functions
------------------

The library ``nandist`` supports all distance functions that calculate the distance between two input arrays ``u`` and ``v``.
The supported distance functions are:

- ``braycurtis``
- ``canberra``
- ``chebyshev``
- ``cityblock``
- ``cityblock``
- ``correlation``
- ``cosine``
- ``euclidean``
- ``jensenshannon``
- ``mahalanobis``
- ``minkowski``
- ``seuclidean``
- ``sqeuclidean``

Pairwise functions
------------------

The library ``nandist`` supports pairwise distance calculating functions ``cdist`` and ``pdist``, but only a limited
number of distance metrics can be used.

Supported metrics
^^^^^^^^^^^^^^^^^

Both functions ``cdist`` and ``pdist`` accept a ``"metric"`` argument that determines the distance metric to be used.
Supported metrics are:

-  ``"chebyshev"``
-  ``"cityblock"``
-  ``"cosine"``
-  ``"euclidean"``
-  ``"minkowski"``

Unsupported metrics
^^^^^^^^^^^^^^^^^^^

Metrics that are not supported by ``nandist.cdist`` and ``nandist.pdist`` are:

- ``"braycurtis"``
- ``"canberra"``
- ``"correlation"``
- ``"jensenshannon"``
- ``"mahalanobis"``
- ``"seuclidean"``
- ``"sqeuclidean"``
