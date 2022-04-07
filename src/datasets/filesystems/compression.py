import os
from typing import Optional

import fsspec
from fsspec.archive import AbstractArchiveFileSystem
from fsspec.utils import DEFAULT_BLOCK_SIZE


class BaseCompressedFileFileSystem(AbstractArchiveFileSystem):
    """Read contents of compressed file as a filesystem with one file inside."""

    root_marker = ""
    protocol: str = (
        None  # protocol passed in prefix to the url. ex: "gzip", for gzip://file.txt::http://foo.bar/file.txt.gz
    )
    compression: str = None  # compression type in fsspec. ex: "gzip"
    extension: str = None  # extension of the filename to strip. ex: "".gz" to get file.txt from file.txt.gz

    def __init__(
        self, fo: str = "", target_protocol: Optional[str] = None, target_options: Optional[dict] = None, **kwargs
    ):
        """
        The compressed file system can be instantiated from any compressed file.
        It reads the contents of compressed file as a filesystem with one file inside, as if it was an archive.

        The single file inside the filesystem is named after the compresssed file,
        without the compression extension at the end of the filename.

        Args:
            fo (:obj:``str``): Path to compressed file. Will fetch file using ``fsspec.open()``
            mode (:obj:``str``): Currently, only 'rb' accepted
            target_protocol(:obj:``str``, optional): To override the FS protocol inferred from a URL.
            target_options (:obj:``dict``, optional): Kwargs passed when instantiating the target FS.
        """
        super().__init__(self, **kwargs)
        # always open as "rb" since fsspec can then use the TextIOWrapper to make it work for "r" mode
        self.file = fsspec.open(
            fo, mode="rb", protocol=target_protocol, compression=self.compression, **(target_options or {})
        )
        self.compressed_name = os.path.basename(self.file.path.split("::")[0])
        self.uncompressed_name = (
            self.compressed_name[: self.compressed_name.rindex(".")]
            if "." in self.compressed_name
            else self.compressed_name
        )
        self.dir_cache = None

    @classmethod
    def _strip_protocol(cls, path):
        # compressed file paths are always relative to the archive root
        return super()._strip_protocol(path).lstrip("/")

    def _get_dirs(self):
        if self.dir_cache is None:
            f = {**self.file.fs.info(self.file.path), "name": self.uncompressed_name}
            self.dir_cache = {f["name"]: f}

    def cat(self, path: str):
        return self.file.open().read()

    def _open(
        self,
        path: str,
        mode: str = "rb",
        block_size=None,
        autocommit=True,
        cache_options=None,
        **kwargs,
    ):
        path = self._strip_protocol(path)
        if mode != "rb":
            raise ValueError(f"Tried to read with mode {mode} on file {self.file.path} opened with mode 'rb'")
        return self.file.open()


class Bz2FileSystem(BaseCompressedFileFileSystem):
    """Read contents of BZ2 file as a filesystem with one file inside."""

    protocol = "bz2"
    compression = "bz2"
    extension = ".bz2"


class GzipFileSystem(BaseCompressedFileFileSystem):
    """Read contents of GZIP file as a filesystem with one file inside."""

    protocol = "gzip"
    compression = "gzip"
    extension = ".gz"


class Lz4FileSystem(BaseCompressedFileFileSystem):
    """Read contents of LZ4 file as a filesystem with one file inside."""

    protocol = "lz4"
    compression = "lz4"
    extension = ".lz4"


class XzFileSystem(BaseCompressedFileFileSystem):
    """Read contents of .xz (LZMA) file as a filesystem with one file inside."""

    protocol = "xz"
    compression = "xz"
    extension = ".xz"


class ZstdFileSystem(BaseCompressedFileFileSystem):
    """
    Read contents of zstd file as a filesystem with one file inside.

    Note that reading in binary mode with fsspec isn't supported yet:
    https://github.com/indygreg/python-zstandard/issues/136
    """

    protocol = "zstd"
    compression = "zstd"
    extension = ".zst"

    def __init__(
        self,
        fo: str,
        mode: str = "rb",
        target_protocol: Optional[str] = None,
        target_options: Optional[dict] = None,
        block_size: int = DEFAULT_BLOCK_SIZE,
        **kwargs,
    ):
        super().__init__(
            fo=fo,
            mode=mode,
            target_protocol=target_protocol,
            target_options=target_options,
            block_size=block_size,
            **kwargs,
        )
        # We need to wrap the zstd decompressor to avoid this error in fsspec==2021.7.0 and zstandard==0.15.2:
        #
        # File "/Users/user/.virtualenvs/hf-datasets/lib/python3.7/site-packages/fsspec/core.py", line 145, in open
        #     out.close = close
        # AttributeError: 'zstd.ZstdDecompressionReader' object attribute 'close' is read-only
        #
        # see https://github.com/intake/filesystem_spec/issues/725
        _enter = self.file.__enter__

        class WrappedFile:
            def __init__(self, file_):
                self._file = file_

            def __enter__(self):
                self._file.__enter__()
                return self

            def __exit__(self, *args, **kwargs):
                self._file.__exit__(*args, **kwargs)

            def __iter__(self):
                return iter(self._file)

            def __next__(self):
                return next(self._file)

            def __getattr__(self, attr):
                return getattr(self._file, attr)

        def fixed_enter(*args, **kwargs):
            return WrappedFile(_enter(*args, **kwargs))

        self.file.__enter__ = fixed_enter
