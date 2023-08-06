"""Compute distances in numpy arrays with nans"""
__version__ = "0.12.0"

from .cdist import cdist  # noqa: F401
from .pdist import pdist  # noqa: F401
from .functions import (
    braycurtis,  # noqa: F401
    canberra,  # noqa: F401
    chebyshev,  # noqa: F401
    cityblock,  # noqa: F401
    correlation,  # noqa: F401
    cosine,  # noqa: F401
    euclidean,  # noqa: F401
    jensenshannon,  # noqa: F401
    mahalanobis,  # noqa: F401
    minkowski,  # noqa: F401
    seuclidean,  # noqa: F401
    sqeuclidean,  # noqa: F401
)

SUPPORTED_METRICS = [
    "chebyshev",
    "cityblock",
    "cosine",
    "euclidean",
    "minkowski",
]
