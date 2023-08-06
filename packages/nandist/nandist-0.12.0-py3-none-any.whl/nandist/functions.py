"""NA-ignoring distance functions for calculating the distance between two arrays"""

from functools import wraps
import numpy as np
import scipy

functions = [
    "braycurtis",
    "canberra",
    "chebyshev",
    "cityblock",
    "correlation",
    "cosine",
    "euclidean",
    "jensenshannon",
    "mahalanobis",
    "minkowski",
    "seuclidean",
    "sqeuclidean",
]


def ignore_na(f):
    """Ignore NaNs in input vectors to distance function f"""
    scipy_f = getattr(scipy.spatial.distance, f.__name__)

    @wraps(scipy_f)
    def inner(u, v, w=None, **kwargs):
        """Ignore the NaNs in input vectors u and v and optionally in w"""
        na_u = np.isnan(u)
        na_v = np.isnan(v)

        na_uv = na_u | na_v

        # if np.all(na_uv):
        #    return 0

        if w is not None:
            w = w[~na_uv]

        return scipy_f(u[~na_uv], v[~na_uv], w=w, **kwargs)

    return inner


@ignore_na
def braycurtis(*args, **kwargs):
    return


@ignore_na
def canberra(*args, **kwargs):
    return


@ignore_na
def chebyshev(u, v, w=None):
    return


@ignore_na
def cityblock(*args, **kwargs):
    return


@ignore_na
def correlation(*args, **kwargs):
    return


@ignore_na
def cosine(*args, **kwargs):
    return


@ignore_na
def euclidean(*args, **kwargs):
    return


@ignore_na
def jensenshannon(*args, **kwargs):
    return


@ignore_na
def mahalanobis(*args, **kwargs):
    return


@ignore_na
def minkowski(*args, **kwargs):
    return


@ignore_na
def seuclidean(*args, **kwargs):
    return


@ignore_na
def sqeuclidean(*args, **kwargs):
    return
