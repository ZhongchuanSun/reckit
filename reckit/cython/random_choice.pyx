# distutils: language = c++
__author__ = "Zhongchuan Sun"
__email__ = "zhongchuansun@gmail.com"

from libcpp.unordered_set cimport unordered_set as cset
from libcpp.vector cimport vector as cvector
from libc.stdlib cimport rand, srand
import numpy as np
ctypedef cset[int] int_set


def _init_random_seed(seed):
    srand(seed)

cdef llrand():
    cdef unsigned long long r = 0
    cdef int i = 0
    for i in range(5):
        r = (r << 15) | (rand() & 0x7FFF)
    return r & 0xFFFFFFFFFFFFFFFFULL


def uniform_sample(high, size=1, replace=True, exclusion=None):
    cdef int_set omission
    if exclusion is not None:
        for elem in exclusion:
            omission.insert(elem)

    cdef cvector[int] c_arr
    cdef int a
    cdef int i = 0
    cdef int c_high = high
    cdef int c_replace = replace
    cdef int c_size = size

    while c_size - i:
            a = llrand() % c_high
            if not omission.count(a):
                c_arr.push_back(a)
                i += 1
                if not c_replace:
                    omission.insert(a)
    if size == 1:
        tmp = c_arr[0]
    else:
        tmp = c_arr
    return tmp


def distribution_choice(high, size=1, replace=True, p=None, exclusion=None):
    if p is None:
        raise ValueError("'p' cannot be None.")

    if exclusion is not None:
        for idx in exclusion:
            p[idx] = 0
    p = np.array(p, dtype=np.float32)
    p = p / np.sum(p)
    samples = np.random.choice(np.arange(high), size=size, replace=replace, p=p)

    if size == 1:
        tmp = int(samples)
    else:
        tmp = samples.tolist()
    return tmp


def _randint_choice(high, size=1, replace=True, p=None, exclusion=None):
    """Sample random integers from [0, high).

    Args:
        high (int): The largest integer (exclusive) to be drawn from the distribution.
        size (int): The number of samples to be drawn.
        replace (bool): Whether the sample is with or without replacement.
        p: 1-D array-like, optional. The probabilities associated with each entry in [0, high).
           If not given the sample assumes a uniform distribution.
        exclusion: 1-D array-like. The integers in exclusion will be excluded.

    Returns:

    """
    if size <= 0:
        raise ValueError("'size' must be a positive integer.")

    if not isinstance(replace, bool):
        raise TypeError("'replace' must be bool.")

    if p is not None and len(p)!=high:
        raise ValueError("The length of each 'p' must be equal with 'high'.")

    if exclusion is not None and high <= len(exclusion):
        raise ValueError("The number of 'exclusion' is greater than 'high'.")

    len_exclusion = len(exclusion) if exclusion is not None else 0
    if replace is False and (high-len_exclusion <= size):
        raise ValueError("There is not enough integers to be sampled.")


    if p is None:
        return uniform_sample(high, size=size, replace=replace, exclusion=exclusion)
    else:
        return distribution_choice(high, size=size, replace=replace, p=p, exclusion=exclusion)

def _batch_randint_choice(high, size, replace=True, p=None, exclusion=None):
    """Return random integers from `0` (inclusive) to `high` (exclusive).

    Args:
        high (int):
        size: 1-D array_like
        replace (bool):
        p: 2-D array_like
        exclusion: a list of 1-D array_like

    Returns:
        list: a list of 1-D array_like sample

    """
    if p is not None and len(p) != len(size):
        raise ValueError("If 'p' is not None, the lengths of 'p' and 'size' must be equal.")

    if exclusion is not None and len(size) != len(exclusion):
        raise ValueError("The shape of 'exclusion' is not compatible with the shape of 'size'!")

    results = []
    for idx in range(len(size)):
        p_tmp = p[idx] if p is not None else None
        exc = exclusion[idx] if exclusion is not None else None
        results.append(_randint_choice(high, size=size[idx], replace=replace, p=p_tmp, exclusion=exc))
    return results
