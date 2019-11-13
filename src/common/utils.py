# Universally useful utilities
#
# src.common.utils
#

from itertools import islice

def first_filter(pred, iterable):
    f = list(islice(filter(pred, iterable), 1))
    if f:
        return f[0]
    else:
        return None
