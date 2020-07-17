__author__ = "Zhongchuan Sun"
__email__ = "zhongchuansun@gmail.com"

__all__ = ["randint_choice"]

from reckit.cython import _randint_choice
import numpy as np


def randint_choice(high, size=1, replace=True, p=None, exclusion=None):
    """Sample random integers from [0, high).

    Args:
        high (int): The largest integer (exclusive) to be drawn from the distribution.
        size (int): The number of samples to be drawn.
        replace (bool): Whether the sample is with or without replacement.
        p: 1-D array-like, optional. The probabilities associated with each entry in [0, high).
           If not given the sample assumes a uniform distribution.
        exclusion: 1-D array-like. The integers in exclusion will be excluded.

    Returns:
        int or ndarray
    """
    samples = _randint_choice(high, size, replace, p, exclusion)
    return np.int32(samples)
