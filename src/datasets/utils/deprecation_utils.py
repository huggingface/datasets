import logging
import warnings
from typing import Callable


_emitted_deprecation_warnings = set()
logger = logging.getLogger(__name__)


def deprecated(deprecated_function: Callable):
    global _emitted_deprecation_warnings

    def wrapper(*args, **kwargs):
        func_hash = hash(deprecated_function)
        if func_hash not in _emitted_deprecation_warnings:
            warning_msg = (
                f"{deprecated_function.__name__} is deprecated and will be removed "
                "in the next major version of datasets."
            )
            warnings.warn(message=warning_msg, category=DeprecationWarning)
            logger.warning(warning_msg)
            _emitted_deprecation_warnings.add(func_hash)
        return deprecated_function(*args, **kwargs)

    return wrapper
