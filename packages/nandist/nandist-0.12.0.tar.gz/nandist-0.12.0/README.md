![](https://img.shields.io/pypi/l/nandist) ![](https://img.shields.io/pypi/v/nandist) ![](https://img.shields.io/pypi/pyversions/nandist)

# Nandist: Calculating distances in arrays with missing values

The python library `nandist` enables (fast) computation of various distances in numpy arrays containing missing (NaN) values.
These distances are implemented as a drop-in replacement for distance functions in the `scipy.spatial.distance` module.

The distance functions in `nandist` can be used as a drop-in replacement for the distance functions in `scipy.spatial.distance`.
The library `nandist` offers replacements for _all_ standalone distance functions in scipy and _partial_ support for the fast pairwise distance calculating functions `cdist` and `pdist`.

## Supported functions between two vectors
Supported "standalone" distance functions for calculating distances between two arrays (complete):

- `braycurtis`
- `canberra`
- `chebyshev`
- `cityblock`
- `cityblock`
- `correlation`
- `cosine`
- `euclidean`
- `jensenshannon`
- `mahalanobis`
- `minkowski`
- `seuclidean`
- `sqeuclidean`

## Supported functions between arrays of vectors

Supported functions for fast calculation of (pairwise) distances between multiple arrays (partial support for metrics):

- `cdist`
- `pdist`

Supported distance measures in `cdist` and `pdist` (passed as `metric` argument):

-  `"chebyshev"`
-  `"cityblock"`
-  `"cosine"`
-  `"euclidean"`
-  `"minkowski"`

# Installation
Using pip:
```bash
pip install nandist
```

# Usage
A simple example for calculating the cityblock distance between (0, 1) and (NaN, 0) is shown below.

```python
>>> import nandist
>>> import scipy
>>> import numpy as np
>>>
>>> # City-block distance between  (0, 1) and (NaN, 0)
>>> u, v = np.array([0, 1]), np.array([np.nan, 0])
>>> scipy.spatial.distance.cityblock(u, v)
nan
>>> nandist.cityblock(u, v)
1.0
```
You can replace the function `cityblock` by any of the supported distance functions.

You can get pairwise distances between arrays in two matrices using `cdist`.
The NaNs do not need to be in the same component.

```python
>>> import nandist
>>> import numpy as np

>>> # City-block distances between vectors A = [(0, 0), (1, NaN)] and vectors B=[(1, NaN) and (1, 1)]
>>> XA, XB = np.array([[0, 0], [1, np.nan]]), np.array([[1, np.nan], [1, 1]])
>>> Y = nandist.cdist(XA, XB, metric="cityblock")
array([[1., 2.],
       [0., 0.]])
```


# Supported metrics
Supported distance metrics are:

- Chebyshev: `chebyshev`, `metric="chebyshev"`
- Cityblock: `cityblock`, `metric="cityblock"`
- Cosine: `cosine`, `metric="cosine"`
- Euclidean: `euclidean`, `metric="euclidean"`
- Minkowski: `minkowski`, `metric="minkowski"`

If you require support for additional distance metrics, please submit an Issue or Merge Request.

# How does it work
In `nandist`, the components where a vector is NaN will be ignored (interpreted as "any number") in the distance metric.
This is achieved by replacing NaN values with zeros and correcting the resulting overestimated distance value.
Under the hood, `nandist` calls functions from `scipy.spatial.distance` and then applies the corrections using `numpy` linear algebra.
This ensures that the outcomes of `nandist` functions are equivalent to `scipy.spatial.distance` distance functions when arrays are passed without NaNs in them.
In addition, all heavy computational lifting is done through `scipy`, requiring only the additional computational cost of applying the corrections.

# Does it _always_ work?
No. The package `nandist` performs a correction on an overestimation of the distances when missing values are imputed as zero.
It is possible that this correction runs into the limits of floating point arithmetic.
In that case, `nandist` will raise an appropriate error.
However, you don't often run into these edge cases in typical usage.
