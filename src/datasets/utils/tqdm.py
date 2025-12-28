"""Utility helpers to handle progress bars in `datasets`.

Example:
    1. Use `datasets.utils.tqdm` as you would use `tqdm.tqdm` or `tqdm.auto.tqdm`.
    2. To disable progress bars, either use `disable_progress_bars()` helper or set the
       environment variable `HF_DATASETS_DISABLE_PROGRESS_BARS` to 1.
    3. To re-enable progress bars, use `enable_progress_bars()`.
    4. To check whether progress bars are disabled, use `are_progress_bars_disabled()`.
    5. To emit machine-readable JSON progress, use `set_progress_format("json")`.

NOTE: Environment variable `HF_DATASETS_DISABLE_PROGRESS_BARS` has the priority.

Example:
    ```py
    from datasets.utils import (
        are_progress_bars_disabled,
        disable_progress_bars,
        enable_progress_bars,
        set_progress_format,
        get_progress_format,
        tqdm,
    )

    # Disable progress bars globally
    disable_progress_bars()

    # Use as normal `tqdm`
    for _ in tqdm(range(5)):
       do_something()

    # Still not showing progress bars, as `disable=False` is overwritten to `True`.
    for _ in tqdm(range(5), disable=False):
       do_something()

    are_progress_bars_disabled() # True

    # Re-enable progress bars globally
    enable_progress_bars()

    # Progress bar will be shown !
    for _ in tqdm(range(5)):
       do_something()

    # Emit JSON progress (machine-readable)
    set_progress_format("json")
    for i in tqdm(range(100)):
       do_something()
    # Outputs: {"stage":"","current":50,"total":100,"percent":50.0}
    ```
"""

import json
import sys
import warnings

from tqdm.auto import tqdm as old_tqdm

from ..config import HF_DATASETS_DISABLE_PROGRESS_BARS


# `HF_DATASETS_DISABLE_PROGRESS_BARS` is `Optional[bool]` while `_hf_datasets_progress_bars_disabled`
# is a `bool`. If `HF_DATASETS_DISABLE_PROGRESS_BARS` is set to True or False, it has priority.
# If `HF_DATASETS_DISABLE_PROGRESS_BARS` is None, it means the user have not set the
# environment variable and is free to enable/disable progress bars programmatically.
# TL;DR: env variable has priority over code.
#
# By default, progress bars are enabled.
_hf_datasets_progress_bars_disabled: bool = HF_DATASETS_DISABLE_PROGRESS_BARS or False

# Progress format: "tqdm" (default), "json", or "silent"
# Similar to huggingface/tokenizers#1921
_hf_datasets_progress_format: str = "tqdm"


def disable_progress_bars() -> None:
    """
    Disable globally progress bars used in `datasets` except if `HF_DATASETS_DISABLE_PROGRESS_BAR` environment
    variable has been set.

    Use [`~utils.enable_progress_bars`] to re-enable them.
    """
    if HF_DATASETS_DISABLE_PROGRESS_BARS is False:
        warnings.warn(
            "Cannot disable progress bars: environment variable `HF_DATASETS_DISABLE_PROGRESS_BAR=0` is set and has"
            " priority."
        )
        return
    global _hf_datasets_progress_bars_disabled
    _hf_datasets_progress_bars_disabled = True


def enable_progress_bars() -> None:
    """
    Enable globally progress bars used in `datasets` except if `HF_DATASETS_DISABLE_PROGRESS_BAR` environment
    variable has been set.

    Use [`~utils.disable_progress_bars`] to disable them.
    """
    if HF_DATASETS_DISABLE_PROGRESS_BARS is True:
        warnings.warn(
            "Cannot enable progress bars: environment variable `HF_DATASETS_DISABLE_PROGRESS_BAR=1` is set and has"
            " priority."
        )
        return
    global _hf_datasets_progress_bars_disabled
    _hf_datasets_progress_bars_disabled = False


def are_progress_bars_disabled() -> bool:
    """Return whether progress bars are globally disabled or not.

    Progress bars used in `datasets` can be enable or disabled globally using [`~utils.enable_progress_bars`]
    and [`~utils.disable_progress_bars`] or by setting `HF_DATASETS_DISABLE_PROGRESS_BAR` as environment variable.
    """
    global _hf_datasets_progress_bars_disabled
    return _hf_datasets_progress_bars_disabled


def set_progress_format(format: str) -> None:
    """
    Set the global progress format for `datasets`.

    Similar to huggingface/tokenizers#1921 progress_format option.

    Args:
        format: One of "tqdm" (default interactive bars), "json" (machine-readable JSON lines), or "silent" (no output).

    Example:
        ```py
        from datasets.utils import set_progress_format, tqdm

        # Enable JSON output for programmatic consumption
        set_progress_format("json")

        for i in tqdm(range(100), desc="Processing"):
            do_something()
        # Outputs: {"stage":"Processing","current":50,"total":100,"percent":50.0}
        ```
    """
    if format not in ("tqdm", "json", "silent"):
        raise ValueError(f"Invalid progress format: {format}. Must be 'tqdm', 'json', or 'silent'.")
    global _hf_datasets_progress_format
    _hf_datasets_progress_format = format


def get_progress_format() -> str:
    """
    Get the current global progress format.

    Returns:
        Current progress format ("tqdm", "json", or "silent").
    """
    global _hf_datasets_progress_format
    return _hf_datasets_progress_format


class tqdm(old_tqdm):
    """
    Class to override `disable` argument in case progress bars are globally disabled
    and to emit JSON progress when format is "json".

    Taken from https://github.com/tqdm/tqdm/issues/619#issuecomment-619639324
    and enhanced with progress_format support (similar to huggingface/tokenizers#1921).
    """

    def __init__(self, *args, **kwargs):
        if are_progress_bars_disabled():
            kwargs["disable"] = True
        elif get_progress_format() == "silent":
            kwargs["disable"] = True
        elif get_progress_format() == "json":
            # Suppress tqdm visual output but keep tracking active
            import io
            kwargs["file"] = io.StringIO()  # Suppress output to invisible stream
            kwargs["disable"] = False  # Keep tracking active

        super().__init__(*args, **kwargs)

        # Store description for JSON output
        self._json_stage = kwargs.get("desc", "")
        self._last_json_percent = -1

    def update(self, n=1):
        """Override update to emit JSON progress when format is 'json'."""
        super().update(n)

        if get_progress_format() == "json" and self.total:
            current_percent = round((self.n / self.total) * 100, 1) if self.total > 0 else 0

            # Emit JSON every 5% or at completion
            if current_percent - self._last_json_percent >= 5.0 or self.n == self.total:
                progress_data = {
                    "stage": self._json_stage,
                    "current": self.n,
                    "total": self.total,
                    "percent": current_percent
                }
                print(json.dumps(progress_data, ensure_ascii=False), file=sys.stderr, flush=True)
                self._last_json_percent = current_percent

    def __delattr__(self, attr: str) -> None:
        """Fix for https://github.com/huggingface/datasets/issues/6066"""
        try:
            super().__delattr__(attr)
        except AttributeError:
            if attr != "_lock":
                raise


# backward compatibility
enable_progress_bar = enable_progress_bars
disable_progress_bar = disable_progress_bars


def is_progress_bar_enabled():
    return not are_progress_bars_disabled()
