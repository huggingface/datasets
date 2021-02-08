# coding=utf-8
# Copyright 2020 Optuna, Hugging Face
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Logging utilities. """

import logging
import os
import threading
from logging import CRITICAL  # NOQA
from logging import DEBUG  # NOQA
from logging import ERROR  # NOQA
from logging import FATAL  # NOQA
from logging import INFO  # NOQA
from logging import NOTSET  # NOQA
from logging import WARN  # NOQA
from logging import WARNING  # NOQA
from typing import Optional


_lock = threading.Lock()
_library_root_logger_configured = False

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

_default_log_level = logging.WARNING


def _get_default_logging_level():
    """
    If DATASETS_VERBOSITY env var is set to one of the valid choices return that as the new default level.
    If it is not - fall back to ``_default_log_level``
    """
    env_level_str = os.getenv("DATASETS_VERBOSITY", None)
    if env_level_str:
        if env_level_str in log_levels:
            return log_levels[env_level_str]
        else:
            logging.getLogger().warning(
                f"Unknown option DATASETS_VERBOSITY={env_level_str}, "
                f"has to be one of: { ', '.join(log_levels.keys()) }"
            )
    return _default_log_level


def _get_library_name() -> str:

    return __name__.split(".")[0]


def _get_library_root_logger() -> logging.Logger:

    return logging.getLogger(_get_library_name())


def _configure_library_root_logger() -> None:

    global _library_root_logger_configured

    with _lock:
        if _library_root_logger_configured:
            # This library has already configured the library root logger.
            return
        _library_root_logger_configured = True

        # Apply our default configuration to the library root logger.
        library_root_logger = _get_library_root_logger()
        library_root_logger.setLevel(_get_default_logging_level())


def _reset_library_root_logger() -> None:

    global _library_root_logger_configured

    with _lock:

        library_root_logger = _get_library_root_logger()
        library_root_logger.setLevel(logging.NOTSET)
        _library_root_logger_configured = False


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a logger with the specified name.
    This function can be used in dataset and metrics scripts.
    """

    if name is None:
        name = _get_library_name()

    _configure_library_root_logger()
    return logging.getLogger(name)


def get_verbosity() -> int:
    """Return the current level for the HuggingFace datasets library's root logger.
    Returns:
        Logging level, e.g., ``datasets.logging.DEBUG`` and ``datasets.logging.INFO``.
    .. note::
        HuggingFace datasets library has following logging levels:
        - ``datasets.logging.CRITICAL``, ``datasets.logging.FATAL``
        - ``datasets.logging.ERROR``
        - ``datasets.logging.WARNING``, ``datasets.logging.WARN``
        - ``datasets.logging.INFO``
        - ``datasets.logging.DEBUG``
    """

    _configure_library_root_logger()
    return _get_library_root_logger().getEffectiveLevel()


def set_verbosity(verbosity: int) -> None:
    """Set the level for the HuggingFace datasets library's root logger.
    Args:
        verbosity:
            Logging level, e.g., ``datasets.logging.DEBUG`` and ``datasets.logging.INFO``.
    """

    _configure_library_root_logger()
    _get_library_root_logger().setLevel(verbosity)


def set_verbosity_info():
    """Set the level for the HuggingFace datasets library's root logger to INFO.

    This will display most of the logging information and tqdm bars.

    Shortcut to ``datasets.logging.set_verbosity(datasets.logging.INFO)``
    """
    return set_verbosity(INFO)


def set_verbosity_warning():
    """Set the level for the HuggingFace datasets library's root logger to WARNING.

    This will display only the warning and errors logging information (no tqdm bars).

    Shortcut to ``datasets.logging.set_verbosity(datasets.logging.WARNING)``
    """
    return set_verbosity(WARNING)


def set_verbosity_debug():
    """Set the level for the HuggingFace datasets library's root logger to DEBUG.

    This will display all the logging information and tqdm bars.

    Shortcut to ``datasets.logging.set_verbosity(datasets.logging.DEBUG)``
    """
    return set_verbosity(DEBUG)


def set_verbosity_error():
    """Set the level for the HuggingFace datasets library's root logger to ERROR.

    This will display only the errors logging information (no tqdm bars).

    Shortcut to ``datasets.logging.set_verbosity(datasets.logging.ERROR)``
    """
    return set_verbosity(ERROR)


def disable_propagation() -> None:
    """Disable propagation of the library log outputs.
    Note that log propagation is disabled by default.
    """

    _configure_library_root_logger()
    _get_library_root_logger().propagate = False


def enable_propagation() -> None:
    """Enable propagation of the library log outputs.
    Please disable the HuggingFace datasets library's default handler to prevent double logging if the root logger has
    been configured.
    """

    _configure_library_root_logger()
    _get_library_root_logger().propagate = True
