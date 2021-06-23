import os
from typing import Optional

import fsspec
from fsspec.archive import AbstractArchiveFileSystem
from fsspec.utils import DEFAULT_BLOCK_SIZE


class GZipFileSystem(AbstractArchiveFileSystem):
    """Read contents of GZIP archive as a file-system with one file inside."""

    root_marker = ""
    protocol = "gzip"

    def __init__(
        self,
        fo: str = "",
        mode: str = "rb",
        target_protocol: Optional[str] = None,
        target_options: Optional[dict] = None,
        block_size: int = DEFAULT_BLOCK_SIZE,
        **kwargs,
    ):
        """
        The GZipFileSystem can be instantiated from any gzip file.
        It read the contents of GZip archive as a file-system with one file inside.
        The single file inside the filesystem is named after the Gzip file, without ".gz" at the end.

        Args:
            fo (:obj:``str``): Path to file containing GZIP. Will fetch file using ``fsspec.open()``
            mode (:obj:``str``): Currently, only 'rb' accepted
            target_protocol(:obj:``str``, optional): To override the FS protocol inferred from a URL.
            target_options (:obj:``dict``, optional): Kwargs passed when instantiating the target FS.
        """
        super().__init__(self, **kwargs)
        if mode != "rb":
            raise ValueError("Only read from gzip files accepted")
        self.gzip = fsspec.open(fo, mode=mode, protocol=target_protocol, compression="gzip", **(target_options or {}))
        self.info = self.gzip.fs.info(self.gzip.path)
        self.compressed_name = os.path.basename(self.gzip.path.split("::")[0]).rstrip(".gz")
        self.uncompressed_name = self.compressed_name.rstrip(".gz")
        self.block_size = block_size
        self.dir_cache = None

    @classmethod
    def _strip_protocol(cls, path):
        # gzip file paths are always relative to the archive root
        return super()._strip_protocol(path).lstrip("/")

    def _get_dirs(self):
        if self.dir_cache is None:
            f = {**self.info, "name": self.uncompressed_name}
            self.dir_cache = {f["name"]: f}

    def cat(self, path: str):
        return self.gzip.open().read()

    def _open(
        self,
        path: str,
        mode: str = "rb",
        block_size: Optional[int] = None,
        autocommit: bool = True,
        cache_options: Optional[dict] = None,
        **kwargs,
    ):
        path = self._strip_protocol(path)
        if path != self.uncompressed_name:
            raise FileNotFoundError(f"Expected file {self.uncompressed_name} but got {path}")
        return self.gzip.open()
