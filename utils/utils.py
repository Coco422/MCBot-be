# utils.py
import warnings
from functools import wraps

def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"'{func.__name__}' is deprecated and will be removed in a future version.",
            FutureWarning,
            stacklevel=2
        )
        return func(*args, **kwargs)
    return wrapper
