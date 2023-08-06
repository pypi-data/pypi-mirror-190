"""NA-ignoring replacement for scipy.spatial.distance.cdist"""
import itertools

from .functions import chebyshev as _chebyshev

import scipy
import numpy as np
from functools import wraps


def ignore_na_cdist(*args, **kwargs):
    @wraps(scipy.spatial.distance.cdist)
    def inner(XA, XB, metric="euclidean", *, out=None, **kwargs):
        """The arguments are taken from the scipy API"""
        # No NANs present? Do nothing
        nans_in_A, nans_in_B = np.any(np.isnan(XA)), np.any(np.isnan(XB))
        if not nans_in_A and not nans_in_B:
            return scipy.spatial.distance.cdist(XA, XB, metric, out=out, **kwargs)

        if metric == "cityblock":
            return minkowski(XA, XB, out=out, p=1, **kwargs)
        elif metric == "euclidean":
            return minkowski(XA, XB, out=out, p=2, **kwargs)
        elif metric == "minkowski":
            return minkowski(XA, XB, out=out, **kwargs)
        elif metric == "cosine":
            return cosine(XA, XB, out=out, **kwargs)
        elif metric == "chebyshev":
            return chebyshev(XA, XB, out=out, **kwargs)
        else:
            raise NotImplementedError(
                f"NA-ignored distance {metric =} not implemented."
            )

    return inner


@ignore_na_cdist
def cdist(*args, **kwargs):
    return


def minkowski(XA, XB, **kwargs):
    """NA-ignoring Minkowski variant returning a square form distance matrix"""
    if np.all(np.isnan(XA)) | np.all(np.isnan(XB)):
        return np.zeros(shape=(XA.shape[0], XB.shape[0]))

    p = kwargs.get("p", 2.0)  # get 'p' from kwargs, otherwise default to 2
    w = kwargs.get("w")
    out = kwargs.get("out")

    XA0 = np.nan_to_num(XA, nan=0)
    XB0 = np.nan_to_num(XB, nan=0)

    Dp = scipy.spatial.distance.cdist(XA0, XB0, "minkowski", out=out, w=w, p=p) ** p

    if w is None:
        w = np.ones_like(XA[0])

    Dp -= np.matmul(np.isnan(XA), (w * (np.abs(XB0) ** p)).T)
    Dp -= np.matmul(w * (np.abs(XA0) ** p), np.isnan(XB).T)

    # Hack: set very small values to zero to prevent inflation by ** (1/p) for larger values of p
    Dp[Dp / np.average(Dp) < 1e-10] = 0

    return np.nan_to_num(Dp ** (1 / p))


def zero_check(X, w=None):
    """Return whether the average weighted squared elements of vectors in X are zero"""
    return np.average(np.square(np.nan_to_num(X)), weights=w, axis=1, keepdims=1) == 0


def _correct_norms(XA, XB, w=None):
    """Correct norms ||u||*||v|| to use with cosine similarity normalizatation when XA or XB contain NaNs"""
    if w is None:
        w = np.ones(shape=(1, XA.shape[1]))
    else:
        w = np.array([w])
    return np.sqrt(
        np.matmul(np.square(np.nan_to_num(XA)), w.T * ~np.isnan(XB).T)
    ) * np.sqrt(np.dot(w * ~np.isnan(XA), np.square(np.nan_to_num(XB).T)))


def _uncorrected_norms(XA, XB, w=None):
    """Uncorrected norms ||u0||*||v0|| that were used with cosine similarity normalization when NaNs in XA and XB were
    zero-filled"""
    if w is None:
        w = np.ones(shape=(1, XA.shape[1]))
    return np.sqrt(
        np.matmul(np.square(np.nan_to_num(XA)), (w * np.ones_like(XB)).T)
    ) * np.sqrt(np.dot(w * np.ones_like(XA), np.square(np.nan_to_num(XB)).T))


def cosine(XA, XB, **kwargs):
    """NA-ignoring cosine distance variant returning a square form distance matrix"""

    XA0 = np.nan_to_num(XA, nan=0)
    XB0 = np.nan_to_num(XB, nan=0)

    # Cosine similarity calculated with XA0 and XB0 are incorrect due to an inflation of the normalization factor
    # We must correct for this factor
    w = kwargs.get("w", None)

    uuvv = _correct_norms(XA, XB, w=w)
    uu0vv0 = _uncorrected_norms(XA, XB, w=w)

    # Cosine may return nan when the vectors are all zeros, so convert before returning
    D = np.nan_to_num(scipy.spatial.distance.cdist(XA0, XB0, "cosine", **kwargs))

    # Corrections may cause division by zero, so also convert NaNs to zero in corrected distance
    return np.nan_to_num(1 - (uu0vv0 / uuvv) * (1 - D))


def chebyshev(XA, XB, **kwargs):
    """NA-ignoring chebyshev distance variant returning a square form distance matrix"""

    # Unfortunately, we need to loop because the Chebyshev distance takes the maximum distance and hence there is no
    # algebraic way to correct for overestimations when NaNs are replaced with zero.
    Y = np.zeros(shape=(XA.shape[0], XB.shape[0]))
    i = -1
    for x, (u, v) in enumerate(itertools.product(XA, XB)):
        # Call nandist.chebyshev
        y = _chebyshev(u, v, w=kwargs.get("w", None))

        # Index to distance matrix
        j = x % XB.shape[0]
        # Increment
        if j == 0:
            i += 1

        Y[i, j] = y

    return Y
