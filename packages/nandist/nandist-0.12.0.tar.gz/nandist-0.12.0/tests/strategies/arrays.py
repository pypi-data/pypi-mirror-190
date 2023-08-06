from hypothesis.extra.numpy import arrays, from_dtype
from hypothesis.strategies import integers, composite, booleans
import numpy as np


# Array lengths
MIN_LENGTH = 1
MAX_LENGTH = 1_000

# We test using 32-bit floats because testing with 64-bit floats can lead to infinities and accumulation of inaccuracies
# when extreme values (like the maximum float) are involved; breaking the tests.
# The goal of the tests is to test the validity of the corrections, and not the robustness of nandist for extreme inputs
TEST_DTYPE = "int32"


@composite
def array_elements(draw, nan: bool = True):
    """Strategy for generating values to be used in testing. These are integer values between -10 and 10 and can
    sometimes be nan"""

    # Are we returning a NaN?
    if nan:
        if draw(booleans()):
            return np.nan

    i = draw(integers(min_value=-10, max_value=10))
    return float(i)


@composite
def normal_arrays(draw, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
    """Hypothesis strategy for returning a matrix with shape = (3, length), with random length between min_length and
    max_length"""
    length = draw(integers(min_value=min_length, max_value=max_length))

    # Draw random array, ensure that the sum of elements is less than the max float to prevent testing errors
    return draw(
        arrays(
            np.dtype("float"),
            shape=(3, length),
            elements=from_dtype(
                np.dtype(TEST_DTYPE), allow_nan=False, allow_infinity=False
            ),
        ).filter(lambda x: np.sum(x) < np.finfo("float").max)
    )


@composite
def nan_arrays(draw, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
    """Hypothesis strategy for returning a matrix with shape = (3, length), with random length between min_length and
    max_length. The matrix consists of vectors a, b, and w.
    The filter ensures that either a or b contains at least one NAN value"""
    length = draw(integers(min_value=min_length, max_value=max_length))

    # Draw random array, filter such that:
    # 1: there is at least one NaN in the first two arrays
    # 2: the sum of all elements is smaller than the maximum float

    # The reason for (2) is that we will be testing whether the nandist calculated distance is equal to the scipy
    # distance alculated for an array where NaN elements are removed. In our implementation, we might overestimate the
    # distance and then correct for this overestimation. However, the overestimation can lead to infinite values.
    # To prevent these infinities, the sum of elements of each vector cannot exceed the maximum float value.
    return draw(
        arrays(
            np.dtype("float"),
            shape=(3, length),
            elements=from_dtype(
                np.dtype(TEST_DTYPE),
                allow_nan=True,
                allow_infinity=False,
            ),
        )
        .filter(lambda x: np.any(np.isnan(x[:2])))  # filter (1)
        .filter(
            lambda x: np.all(np.sum(np.nan_to_num(x, 0), 1) < np.finfo("float").max)
        )  # filter (2)
    )


@composite
def sized_normal_arrays(draw, number_of_arrays: int, array_dimension: int):
    """Return a NaN-free matrix with shape = (number_of_arrays, array_dimension)"""
    # Draw random array, ensure that the sum of elements is less than the max float to prevent testing errors
    return draw(
        arrays(
            np.dtype("float"),
            shape=(number_of_arrays, array_dimension),
            elements=array_elements(nan=False),
        )
        .filter(lambda x: np.sum(x) < np.finfo("float").max)
        .filter(lambda x: np.any(np.sum(x) > 0))
    )


@composite
def sized_nan_arrays(draw, number_of_arrays: int, array_dimension: int):
    """Return a NaN-containing matrix with shape (number_of_arrays, array_dimensions)"""
    return draw(
        arrays(
            np.dtype("float"),
            shape=(number_of_arrays, array_dimension),
            elements=array_elements(nan=True),
        ).filter(lambda x: np.any(np.isnan(x)))
    )
