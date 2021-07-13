import importlib
from functools import partial
from typing import Optional, Union

from .utils.logging import get_logger
from .utils.patching import patch_submodule
from .utils.streaming_download_manager import xjoin, xopen


logger = get_logger(__name__)


def extend_module_for_streaming(module_path, use_auth_token: Optional[Union[str, bool]] = None):
    """
    Extend the `open` and `os.path.join` functions of the module to support data streaming.
    They rare replaced by `xopen` and `xjoin` defined to work with the StreamingDownloadManager.

    We use fsspec to extend `open` to be able to read remote files.
    To join paths and navigate in remote compressed archives, we use the "::" separator.
    """

    module = importlib.import_module(module_path)
    # open files in a streaming fashion
    if use_auth_token:
        patch_submodule(module, "open", partial(xopen, use_auth_token=use_auth_token)).start()
    else:
        patch_submodule(module, "open", xopen).start()
    # allow to navigate in remote zip files
    patch_submodule(module, "os.path.join", xjoin).start()
