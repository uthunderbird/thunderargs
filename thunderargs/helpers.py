from functools import wraps as orig_wraps, WRAPPER_ASSIGNMENTS

WRAPPER_ASSIGNMENTS += ('__annotations__',)


def wraps(func):
    return orig_wraps(func, WRAPPER_ASSIGNMENTS)
