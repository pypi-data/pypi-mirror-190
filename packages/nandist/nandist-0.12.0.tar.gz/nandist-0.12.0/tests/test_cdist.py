"""Test cdist functions. There is no need to test nandist.pdist because it calls cdist under the hood."""

from hypothesis.strategies import integers
from hypothesis import given
from .strategies.arrays import sized_normal_arrays, sized_nan_arrays
from .utils.weights import weights_from_array, pseudoweights_from_factor
from .strategies.parameters import minkowski_p
from .utils.constants import RELTOL, ZEROS_WITH_NAN, ONE_WITH_NAN

import pytest
import numpy as np
import scipy
import nandist

TEST_ARRAY_DIMENSION = 5


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(
    X=sized_nan_arrays(number_of_arrays=8, array_dimension=TEST_ARRAY_DIMENSION),
    W=sized_normal_arrays(number_of_arrays=1, array_dimension=TEST_ARRAY_DIMENSION),
    p=minkowski_p(),
)
def test_cdist_correct_with_nans(X, W, p, metric):
    """Tests whehter nandist.cdist gives correct results when NaNs are present in the arrays.
    This leverages the nandist.<metric> function and should thus only pass when all tests for nandist.<metric>
    functions have passed"""
    XA, XB = X[:3], X[3:]
    XA_n, XB_n = XA.shape[0], XB.shape[0]

    w = weights_from_array(W[0])

    kwargs = {"metric": metric, "w": w}
    kwargs_nandist = {"w": w}

    if metric == "minkowski":
        kwargs = {**kwargs, "p": p}
        kwargs_nandist = {**kwargs_nandist, "p": p}

    e_nandist = None
    e_scipy = None

    try:
        Y_expected = np.zeros(shape=(XA_n, XB_n))
        nandist_f = getattr(nandist, metric)
        for i in range(XA_n):
            for j in range(XB_n):
                try:
                    y = nandist_f(XA[i], XB[j], **kwargs_nandist)
                    Y_expected[i, j] = y
                except ZeroDivisionError:
                    if metric == "cosine":
                        # Ignore it
                        Y_expected[i, j] = 0
    except Exception as e:
        e_scipy = e

    try:
        Y_result = nandist.cdist(XA, XB, **kwargs)
    except Exception as e:
        e_nandist = e

    if e_scipy is not None or e_nandist is not None:
        assert type(e_scipy) == type(e_nandist)
        return

    try:
        assert np.allclose(Y_result, Y_expected, atol=1e-6)
    except AssertionError:
        raise AssertionError


@pytest.mark.parametrize("a", ZEROS_WITH_NAN)
@pytest.mark.parametrize("b", ONE_WITH_NAN)
@pytest.mark.parametrize("p", [0.1, 0.5, 1, 2, 3, 4])
@given(w_factor=integers(min_value=1, max_value=100))
def test_weighted_minkowski(a, b, w_factor, p):
    """Test weighted minkowski assuming vector a is 1 at position 0 and zero elsewhere; b is zero everywhere except for
    positions where it is NaN"""

    XA, XB = np.array([a]), np.array([b])

    # Construct weights array
    w = pseudoweights_from_factor(w_factor=w_factor, n=XA.shape[1])

    # Calculate distance
    Y = nandist.cdist(XA, XB, "minkowski", w=w, p=p)

    assert (Y[0][0] - w[0] ** (1 / p)) / Y[0][0] < RELTOL


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(
    X=sized_normal_arrays(number_of_arrays=8, array_dimension=TEST_ARRAY_DIMENSION),
    W=sized_normal_arrays(number_of_arrays=1, array_dimension=TEST_ARRAY_DIMENSION),
    p=minkowski_p(),
)
def test_cdist_equivalent_without_nans(X, W, p, metric):
    """Test whether nandist.cdist returns the same results as the scipy.spatial.distance.cdist when no NaNs are in the
    arrays"""
    XA, XB = X[:3], X[3:]

    w = weights_from_array(W[0])

    kwargs = {"metric": metric, "w": w}

    if metric == "minkowski":
        kwargs = {**kwargs, "p": p}

    try:
        Y_expected = scipy.spatial.distance.cdist(XA, XB, **kwargs)
    except ZeroDivisionError:
        assert True
        return

    Y_result = nandist.cdist(XA, XB, **kwargs)
    assert np.allclose(Y_result, Y_expected, equal_nan=True)
