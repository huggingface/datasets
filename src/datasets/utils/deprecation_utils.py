import warnings
from functools import wraps
from typing import Callable, Optional

from .logging import get_logger


_emitted_deprecation_warnings = set()
logger = get_logger(__name__)


def deprecated(help_message: Optional[str] = None):
    """Decorator to mark a function as deprecated.

    Args:
        help_message (`Optional[str]`): An optional message to guide the user on how to
            switch to non-deprecated usage of the library.
    """

    def decorator(deprecated_function: Callable):
        global _emitted_deprecation_warnings
        warning_msg = (
            (
                f"{deprecated_function.__name__} is deprecated and will be removed "
                "in the next major version of datasets."
            )
            + f" {help_message}"
            if help_message
            else ""
        )

        @wraps(deprecated_function)
        def wrapper(*args, **kwargs):
            func_hash = hash(deprecated_function)
            if func_hash not in _emitted_deprecation_warnings:
                warnings.warn(warning_msg, category=FutureWarning, stacklevel=2)
                _emitted_deprecation_warnings.add(func_hash)
            return deprecated_function(*args, **kwargs)

        wrapper._decorator_name_ = "deprecated"
        return wrapper

    return decorator
