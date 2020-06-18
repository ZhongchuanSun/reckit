import hashlib
import os
import sys

__all__ = ["md5sum"]


def md5sum(*args):
    """Compute and check MD5 message
    Args:
        *args: one or more file paths

    Returns: a list of MD5 message
    """
    md5_list = []
    for filename in args:
        if not os.path.isfile(filename):
            sys.stderr.write("There is not file named '%s'!" % filename)
            md5_list.append(None)
            continue
        with open(filename, "rb") as fin:
            readable_hash = hashlib.md5(fin.read()).hexdigest()
            md5_list.append(readable_hash)
    md5_list = md5_list[0] if len(args) == 1 else md5_list
    return md5_list
