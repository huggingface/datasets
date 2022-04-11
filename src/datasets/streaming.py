import importlib
from functools import wraps
from typing import Optional, Union
from unittest.mock import patch

from .utils.logging import get_logger
from .utils.patching import patch_submodule
from .utils.streaming_download_manager import (
    xbasename,
    xdirname,
    xet_parse,
    xgetsize,
    xglob,
    xisdir,
    xisfile,
    xjoin,
    xlistdir,
    xopen,
    xpandas_read_csv,
    xpandas_read_excel,
    xpathglob,
    xpathjoin,
    xpathname,
    xpathopen,
    xpathparent,
    xpathrglob,
    xpathstem,
    xpathsuffix,
    xrelpath,
    xsio_loadmat,
    xsplitext,
    xwalk,
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

    if hasattr(module, "_patched_for_streaming") and module._patched_for_streaming:
        return

    def wrap_auth(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, use_auth_token=use_auth_token, **kwargs)

        wrapper._decorator_name_ = "wrap_auth"
        return wrapper

    # open files in a streaming fashion
    patch_submodule(module, "open", wrap_auth(xopen)).start()
    patch_submodule(module, "os.listdir", wrap_auth(xlistdir)).start()
    patch_submodule(module, "os.walk", wrap_auth(xwalk)).start()
    patch_submodule(module, "glob.glob", wrap_auth(xglob)).start()
    # allow to navigate in remote zip files
    patch_submodule(module, "os.path.join", xjoin).start()
    patch_submodule(module, "os.path.dirname", xdirname).start()
    patch_submodule(module, "os.path.basename", xbasename).start()
    patch_submodule(module, "os.path.relpath", xrelpath).start()
    patch_submodule(module, "os.path.splitext", xsplitext).start()
    # allow checks on paths
    patch_submodule(module, "os.path.isdir", wrap_auth(xisdir)).start()
    patch_submodule(module, "os.path.isfile", wrap_auth(xisfile)).start()
    patch_submodule(module, "os.path.getsize", wrap_auth(xgetsize)).start()
    if hasattr(module, "Path"):
        patch.object(module.Path, "joinpath", xpathjoin).start()
        patch.object(module.Path, "__truediv__", xpathjoin).start()
        patch.object(module.Path, "open", wrap_auth(xpathopen)).start()
        patch.object(module.Path, "glob", wrap_auth(xpathglob)).start()
        patch.object(module.Path, "rglob", wrap_auth(xpathrglob)).start()
        patch.object(module.Path, "parent", property(fget=xpathparent)).start()
        patch.object(module.Path, "name", property(fget=xpathname)).start()
        patch.object(module.Path, "stem", property(fget=xpathstem)).start()
        patch.object(module.Path, "suffix", property(fget=xpathsuffix)).start()
    patch_submodule(module, "pd.read_csv", wrap_auth(xpandas_read_csv), attrs=["__version__"]).start()
    patch_submodule(module, "pd.read_excel", xpandas_read_excel, attrs=["__version__"]).start()
    patch_submodule(module, "sio.loadmat", wrap_auth(xsio_loadmat), attrs=["__version__"]).start()
    # xml.etree.ElementTree
    for submodule in ["ElementTree", "ET"]:
        patch_submodule(module, f"{submodule}.parse", wrap_auth(xet_parse)).start()
    module._patched_for_streaming = True
