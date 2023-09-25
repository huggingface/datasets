import importlib
import shutil
import threading
import warnings
from typing import List

import fsspec
import fsspec.asyn

from . import compression


_has_s3fs = importlib.util.find_spec("s3fs") is not None

if _has_s3fs:
    from .s3filesystem import S3FileSystem  # noqa: F401

COMPRESSION_FILESYSTEMS: List[compression.BaseCompressedFileFileSystem] = [
    compression.Bz2FileSystem,
    compression.GzipFileSystem,
    compression.Lz4FileSystem,
    compression.XzFileSystem,
    compression.ZstdFileSystem,
]

# Register custom filesystems
for fs_class in COMPRESSION_FILESYSTEMS:
    if fs_class.protocol in fsspec.registry and fsspec.registry[fs_class.protocol] is not fs_class:
        warnings.warn(f"A filesystem protocol was already set for {fs_class.protocol} and will be overwritten.")
    fsspec.register_implementation(fs_class.protocol, fs_class, clobber=True)


def extract_path_from_uri(dataset_path: str) -> str:
    """
    Preprocesses `dataset_path` and removes remote filesystem (e.g. removing `s3://`).

    Args:
        dataset_path (`str`):
            Path (e.g. `dataset/train`) or remote uri (e.g. `s3://my-bucket/dataset/train`) of the dataset directory.
    """
    if "://" in dataset_path:
        dataset_path = dataset_path.split("://")[1]
    return dataset_path


def is_remote_filesystem(fs: fsspec.AbstractFileSystem) -> bool:
    """
    Validates if filesystem has remote protocol.

    Args:
        fs (`fsspec.spec.AbstractFileSystem`):
            An abstract super-class for pythonic file-systems, e.g. `fsspec.filesystem(\'file\')` or [`datasets.filesystems.S3FileSystem`].
    """
    if fs is not None and fs.protocol != "file":
        return True
    else:
        return False


def rename(fs: fsspec.AbstractFileSystem, src: str, dst: str):
    """
    Renames the file `src` in `fs` to `dst`.
    """
    is_local = not is_remote_filesystem(fs)
    if is_local:
        # LocalFileSystem.mv does copy + rm, it is more efficient to simply move a local directory
        shutil.move(fs._strip_protocol(src), fs._strip_protocol(dst))
    else:
        fs.mv(src, dst, recursive=True)


def _reset_fsspec_lock() -> None:
    """
    Clear reference to the loop and thread.
    This is necessary otherwise HTTPFileSystem hangs in the ML training loop.
    Only required for fsspec >= 0.9.0
    See https://github.com/fsspec/gcsfs/issues/379
    """
    if hasattr(fsspec.asyn, "reset_lock"):
        # for future fsspec>2022.05.0
        fsspec.asyn.reset_lock()
    else:
        fsspec.asyn.iothread[0] = None
        fsspec.asyn.loop[0] = None
        fsspec.asyn.lock = threading.Lock()
