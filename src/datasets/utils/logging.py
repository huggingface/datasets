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
""" Logging utilities."""

import logging
import os
import sys
from logging import CRITICAL  # NOQA
from logging import DEBUG  # NOQA
from logging import ERROR  # NOQA
from logging import FATAL  # NOQA
from logging import INFO  # NOQA
from logging import NOTSET  # NOQA
from logging import WARN  # NOQA
from logging import WARNING  # NOQA
from typing import Optional

from tqdm import auto as tqdm_lib


_default_handler: Optional[logging.Handler] = None

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

_default_log_level = logging.WARNING

_tqdm_active = True


def _get_default_logging_level():
    """
    If DATASETS_VERBOSITY env var is set to one of the valid choices return that as the new default level. If it is
    not - fall back to `_default_log_level`
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
    global _default_handler

    if _default_handler:
        # This library has already configured the library root logger.
        return
    _default_handler = logging.StreamHandler()  # Set sys.stderr as stream.
    _default_handler.flush = sys.stderr.flush

    # Apply our default configuration to the library root logger.
    library_root_logger = _get_library_root_logger()
    library_root_logger.addHandler(_default_handler)
    library_root_logger.setLevel(_get_default_logging_level())
    library_root_logger.propagate = False


def _reset_library_root_logger() -> None:
    global _default_handler

    if not _default_handler:
        return

    library_root_logger = _get_library_root_logger()
    library_root_logger.removeHandler(_default_handler)
    library_root_logger.setLevel(logging.NOTSET)
    _default_handler = None


def get_log_levels_dict():
    return log_levels


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger with the specified name.
    This function is not supposed to be directly accessed unless you are writing a custom datasets module.
    """
    if name is None:
        name = _get_library_name()

    return logging.getLogger(name)


def get_verbosity() -> int:
    """
    Return the current level for the 🤗 Datasets' root logger as an int.
    Returns:
        `int`: The logging level.
    <Tip>
    🤗 Datasets has following logging levels:
    - 50: `datasets.logging.CRITICAL` or `datasets.logging.FATAL`
    - 40: `datasets.logging.ERROR`
    - 30: `datasets.logging.WARNING` or `datasets.logging.WARN`
    - 20: `datasets.logging.INFO`
    - 10: `datasets.logging.DEBUG`
    </Tip>"""
    return _get_library_root_logger().getEffectiveLevel()


def set_verbosity(verbosity: int) -> None:
    """
    Set the verbosity level for the 🤗 Datasets' root logger.
    Args:
        verbosity (`int`):
            Logging level, e.g., one of:
            - `datasets.logging.CRITICAL` or `datasets.logging.FATAL`
            - `datasets.logging.ERROR`
            - `datasets.logging.WARNING` or `datasets.logging.WARN`
            - `datasets.logging.INFO`
            - `datasets.logging.DEBUG`
    """
    _get_library_root_logger().setLevel(verbosity)


def set_verbosity_info():
    """Set the verbosity to the `INFO` level."""
    return set_verbosity(INFO)


def set_verbosity_warning():
    """Set the verbosity to the `WARNING` level."""
    return set_verbosity(WARNING)


def set_verbosity_debug():
    """Set the verbosity to the `DEBUG` level."""
    return set_verbosity(DEBUG)


def set_verbosity_error():
    """Set the verbosity to the `ERROR` level."""
    return set_verbosity(ERROR)


def disable_default_handler() -> None:
    """Disable the default handler of the 🤗 Datasets' root logger."""
    assert _default_handler is not None
    _get_library_root_logger().removeHandler(_default_handler)


def enable_default_handler() -> None:
    """Enable the default handler of the 🤗 Datasets' root logger."""
    assert _default_handler is not None
    _get_library_root_logger().addHandler(_default_handler)


def add_handler(handler: logging.Handler) -> None:
    """adds a handler to the 🤗 Datasets' root logger."""
    assert handler is not None
    _get_library_root_logger().addHandler(handler)


def remove_handler(handler: logging.Handler) -> None:
    """removes given handler from the 🤗 Datasets' root logger."""
    assert handler is not None and handler not in _get_library_root_logger().handlers
    _get_library_root_logger().removeHandler(handler)


def disable_propagation() -> None:
    """
    Disable propagation of the library log outputs. Note that log propagation is disabled by default.
    """
    _get_library_root_logger().propagate = False


def enable_propagation() -> None:
    """
    Enable propagation of the library log outputs. Please disable the 🤗 Datasets' default handler to
    prevent double logging if the root logger has been configured.
    """
    _get_library_root_logger().propagate = True


def enable_explicit_format() -> None:
    """
    Enable explicit formatting for every 🤗 Datasets' logger. The explicit formatter is as follows:
    ```
        [LEVELNAME|FILENAME|LINE NUMBER] TIME >> MESSAGE
    ```
    All handlers currently bound to the root logger are affected by this method.
    """
    handlers = _get_library_root_logger().handlers

    for handler in handlers:
        formatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >> %(message)s")
        handler.setFormatter(formatter)


def reset_format() -> None:
    """
    Resets the formatting for 🤗 Datasets' loggers.
    All handlers currently bound to the root logger are affected by this method.
    """
    handlers = _get_library_root_logger().handlers

    for handler in handlers:
        handler.setFormatter(None)


# Configure the library root logger at the module level (singleton-like)
_configure_library_root_logger()


class EmptyTqdm:
    """Dummy tqdm which doesn't do anything."""

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        self._iterator = args[0] if args else None

    def __iter__(self):
        return iter(self._iterator)

    def __getattr__(self, _):
        """Return empty function."""

        def empty_fn(*args, **kwargs):  # pylint: disable=unused-argument
            return

        return empty_fn

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        return


_tqdm_active = True


class _tqdm_cls:
    def __call__(self, *args, **kwargs):
        if _tqdm_active:
            return tqdm_lib.tqdm(*args, **kwargs)
        else:
            return EmptyTqdm(*args, **kwargs)

    def set_lock(self, *args, **kwargs):
        self._lock = None
        if _tqdm_active:
            return tqdm_lib.tqdm.set_lock(*args, **kwargs)

    def get_lock(self):
        if _tqdm_active:
            return tqdm_lib.tqdm.get_lock()


tqdm = _tqdm_cls()


def is_progress_bar_enabled() -> bool:
    """Return a boolean indicating whether tqdm progress bars are enabled."""
    global _tqdm_active
    return bool(_tqdm_active)


def enable_progress_bar():
    """Enable tqdm progress bar."""
    global _tqdm_active
    _tqdm_active = True


def disable_progress_bar():
    """Disable tqdm progress bar."""
    global _tqdm_active
    _tqdm_active = False
