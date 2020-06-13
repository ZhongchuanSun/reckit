import numpy as np

__all__ = ["pad_sequences"]


def pad_sequences(sequences, value=0., max_len=None,
                  padding='post', truncating='post', dtype=np.int32):
    """Pads sequences to the same length.

    Args:
        sequences (list): A list of lists, where each element is a sequence.
        value (int or float): Padding value. Defaults to `0.`.
        max_len (int or None): Maximum length of all sequences.
        padding (str): `"pre"` or `"post"`: pad either before or after each
            sequence. Defaults to `post`.
        truncating (str): `"pre"` or `"post"`: remove values from sequences
            larger than `max_len`, either at the beginning or at the end of
            the sequences. Defaults to `post`.
        dtype (int or float): Type of the output sequences. Defaults to `np.int32`.

    Returns:
        np.ndarray: Numpy array with shape `(len(sequences), max_len)`.

    Raises:
        ValueError: If `padding` or `truncating` is not understood.
    """
    lengths = []
    for x in sequences:
        try:
            lengths.append(len(x))
        except TypeError:
            raise ValueError('`sequences` must be a list of iterables. '
                             'Found non-iterable: ' + str(x))

    if max_len is None:
        max_len = np.max(lengths)

    x = np.full([len(sequences), max_len], value, dtype=dtype)
    for idx, s in enumerate(sequences):
        if not len(s):
            continue  # empty list/array was found
        if truncating == 'pre':
            trunc = s[-max_len:]
        elif truncating == 'post':
            trunc = s[:max_len]
        else:
            raise ValueError('Truncating type "%s" not understood' % truncating)

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x
