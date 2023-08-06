import pytest
import numpy as np
import scipy
import nandist
from hypothesis import given

from .strategies.arrays import normal_arrays, sized_normal_arrays, sized_nan_arrays
from .strategies.parameters import minkowski_p
from .utils.weights import weights_from_array


@pytest.mark.parametrize("metric", nandist.functions.functions)
@given(X=normal_arrays(), p=minkowski_p())
def test_equivalent_without_nans(X, metric, p):
    """Test whether nandist.<metric> is equivalent to scipy.spatial.distance.<metric> when passed normal arrays without
    NaNs. Asserts True if they return the same result or when they raise the same error"""

    # Unpack matrix with arrays
    u, v, w = X
    w = weights_from_array(w)

    nandist_f = getattr(nandist, metric)
    scipy_f = getattr(scipy.spatial.distance, metric)

    kwargs = {"u": u, "v": v, "w": w}

    # Add Minkowski's "p" parameter if the metric is "minkowski"
    if metric == "minkowski":
        kwargs = {**kwargs, "p": p}

    e_scipy = None
    e_nandist = None

    # Attempt to call the scipy.spatial.distance.<metric> function; store error if one is raised
    try:
        y_scipy = scipy_f(**kwargs)
    except Exception as e:
        e_scipy = e

    # Attempt to call the nandist.<metric> function; store error if one is raised
    try:
        y_nandist = nandist_f(**kwargs)
    except Exception as e:
        e_nandist = e

    # If an error was raised in either implementation; assert whether the same error was raised.
    # Return early
    if e_nandist is not None or e_scipy is not None:
        assert type(e_scipy) == type(e_nandist)
        return

    # If no error was raised but one of the results is NaN, assert whether both results are NaN.
    # Return early
    if np.isnan(y_scipy) or np.isnan(y_nandist):
        assert np.isnan(y_scipy) and np.isnan(y_nandist)
        return

    # In all other cases: assert whether the returned value is the same
    try:
        assert y_scipy == y_nandist
    except AssertionError:
        print("uh-oh")


@pytest.mark.parametrize("metric", nandist.functions.functions)
@given(X=sized_nan_arrays(2, 6), w=sized_normal_arrays(1, 6), p=minkowski_p())
def test_equivalent_with_nans(X, w, metric, p):
    """Test whether distance between u, v with weights w calculated with nandist.<metric> is equivalent to distance uh,
    vh with weights wh calculated with scipy.spatial.distance.<metric> when uh, vh the vectors u, v with components
    removed if they are NaN in either u or v. The weights vector wh is also adapted in a similar way."""
    u, v = X
    w = weights_from_array(w[0])

    nandist_f = getattr(nandist, metric)
    scipy_f = getattr(scipy.spatial.distance, metric)

    # Determine inputs to scipy
    idx_nan = np.isnan(u) | np.isnan(v)
    uh, vh = u[~idx_nan], v[~idx_nan]
    wh = w[~idx_nan] if w is not None else None

    kwargs_nandist = {"u": u, "v": v, "w": w}
    kwargs_scipy = {"u": uh, "v": vh, "w": wh}

    if metric == "minkowski":
        kwargs_nandist = {**kwargs_nandist, "p": p}
        kwargs_scipy = {**kwargs_scipy, "p": p}

    # Initialize errors
    e_nandist = None
    e_scipy = None

    try:
        y_nandist = nandist_f(**kwargs_nandist)
    except Exception as e:
        e_nandist = e

    try:
        y_scipy = scipy_f(**kwargs_scipy)
    except Exception as e:
        e_scipy = e

    # If an error was raised in either implementation; assert whether the same error was raised.
    # Return early
    if e_nandist is not None or e_scipy is not None:
        assert type(e_scipy) == type(e_nandist)
        return

    # If no error was raised but one of the results is NaN, assert whether both results are NaN.
    # Return early
    if np.isnan(y_scipy) or np.isnan(y_nandist):
        assert np.isnan(y_scipy) and np.isnan(y_nandist)
        return

    # In all other cases: assert whether the returned value is the same
    assert y_scipy == y_nandist
