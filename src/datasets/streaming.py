import importlib
from functools import partial
from typing import Optional, Union
from unittest.mock import patch

from .utils.logging import get_logger
from .utils.patching import patch_submodule
from .utils.streaming_download_manager import (
    xdirname,
    xjoin,
    xopen,
    xpathglob,
    xpathjoin,
    xpathopen,
    xpathrglob,
    xpathstem,
    xpathsuffix,
)


logger = get_logger(__name__)


def extend_module_for_streaming(module_path, use_auth_token: Optional[Union[str, bool]] = None):
    """Extend the module to support streaming.

    We patch some functions in the module to use `fsspec` to support data streaming:
    - We use `fsspec.open` to open and read remote files. We patch the module function:
      - `open`
    - We use the "::" hop separator to join paths and navigate remote compressed/archive files. We patch the module
      functions:
      - `os.path.join`
      - `pathlib.Path.joinpath` and `pathlib.Path.__truediv__` (called when using the "/" operator)

    The patched functions are replaced with custom functions defined to work with the
    :class:`~utils.streaming_download_manager.StreamingDownloadManager`.

    Args:
        module_path: Path to the module to be extended.
        use_auth_token: Whether to use authentication token.
    """

    module = importlib.import_module(module_path)
    # open files in a streaming fashion
    if use_auth_token:
        patch_submodule(module, "open", partial(xopen, use_auth_token=use_auth_token)).start()
    else:
        patch_submodule(module, "open", xopen).start()
    # allow to navigate in remote zip files
    patch_submodule(module, "os.path.join", xjoin).start()
    patch_submodule(module, "os.path.dirname", xdirname).start()
    if hasattr(module, "Path"):
        patch.object(module.Path, "joinpath", xpathjoin).start()
        patch.object(module.Path, "__truediv__", xpathjoin).start()
        patch.object(module.Path, "open", xpathopen).start()
        patch.object(module.Path, "glob", xpathglob).start()
        patch.object(module.Path, "rglob", xpathrglob).start()
        patch.object(module.Path, "stem", property(fget=xpathstem)).start()
        patch.object(module.Path, "suffix", property(fget=xpathsuffix)).start()
