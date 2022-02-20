import importlib
from typing import List

import fsspec

from . import compression
from .hffilesystem import HfFileSystem


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
for fs_class in COMPRESSION_FILESYSTEMS + [HfFileSystem]:
    fsspec.register_implementation(fs_class.protocol, fs_class)


def extract_path_from_uri(dataset_path: str) -> str:
    """
    preprocesses `dataset_path` and removes remote filesystem (e.g. removing ``s3://``)

    Args:
        dataset_path (``str``): path (e.g. ``dataset/train``) or remote uri (e.g. ``s3://my-bucket/dataset/train``) of the dataset directory
    """
    if "://" in dataset_path:
        dataset_path = dataset_path.split("://")[1]
    return dataset_path


def is_remote_filesystem(fs: fsspec.AbstractFileSystem) -> bool:
    """
    Validates if filesystem has remote protocol.

    Args:
        fs (``fsspec.spec.AbstractFileSystem``): An abstract super-class for pythonic file-systems, e.g. :code:`fsspec.filesystem(\'file\')` or :class:`datasets.filesystems.S3FileSystem`
    """
    if fs is not None and fs.protocol != "file":
        return True
    else:
        return False
