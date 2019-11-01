# Universally useful utilities
#
# src.common.utils
#

from itertools import islice

def firstFilter(pred, iterable):
    f = list(islice(filter(pred, iterable), 1))
    if f:
        return f[0]
    else:
        return None
