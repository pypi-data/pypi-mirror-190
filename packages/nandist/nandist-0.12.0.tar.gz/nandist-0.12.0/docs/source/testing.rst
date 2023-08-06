Testing
=======

We test ``nandist`` using property-based testing using ``hypothesis``.


Functional equivalence
----------------------
We test functional equivalence to ``scipy.spatial.distance`` functions in the case that the vectors :math:`u` and :math:`v` (or collections thereof) do not have missing values.
In other words: ``nandist`` should return the same results as ``scipy.spatial.distance`` when passed vectors that do not have missing values.

Distance function testing
-------------------------
For distance functions, ``nandist`` is tested in the following way:

1. Create new vectors :math:`\hat{u}` and :math:`\hat{v}` from the original vectors :math:`u` and :math:`v` by removing all components that are missing in either :math:`u` or :math:`v`.
2. Calculate the distance between :math:`\hat{u}` and :math:`\hat{v}` using ``scipy.spatial.distance`` functions
3. Calculate the distance between :math:`u` and :math:`v` using ``nandist`` functions
4. Assert that both distances are equal.

Pairwise function testing
-------------------------
For pairwise distance calculations, ``nandist`` is tested in the following way:

1. Create new vectors :math:`\hat{u}` and :math:`\hat{v}` from the original vectors :math:`u` and :math:`v` by removing all components that are missing in either :math:`u` or :math:`v`.
2. Calculate each pairwise distance between :math:`\hat{u}` and :math:`\hat{v}` using ``scipy.spatial.distance`` functions
3. Calculate each pairwise distance between :math:`u` and :math:`v` using ``nandist`` functions ``cdist`` or ``pdist``.
4. Assert that each pairwise distance difference is close to zero.

We assert closeness to zero because the corrections may introduce numerical inaccuracies.
