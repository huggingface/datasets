import warnings
from typing import Callable


def deprecated(deprecated_function: Callable):
    def wrapper(*args, **kwargs):
        warnings.warn(
            message=f"{deprecated_function.__name__} is deprecated and will be removed in the next major version of datasets.",
            category=DeprecationWarning,
        )
        return deprecated_function(*args, **kwargs)

    return wrapper
