import bz2
import gzip
import lzma
import os
import zipfile
from io import BytesIO, StringIO
from pathlib import Path


class FileWriteHandler:
    def __init__(self, file_name, file_mode, compression):
        self._file_name = file_name
        self._file_mode = file_mode
        self._compression = compression

    def __enter__(self):
        if self._compression is None:
            self._file = open(self._file_name, self._file_mode)
        elif self._compression == "gzip":
            self._file = gzip.open(self._file_name, self._file_mode)
        elif self._compression == "bz2":
            self._file = bz2.open(self._file_name, self._file_mode)
        elif self._compression == "xz":
            self._file = lzma.open(self._file_name, self._file_mode)
        elif self._compression == "zip":
            self._file = _BytesZipFile(self._file_name, self._file_mode)

        return self._file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._file.close()


class _BytesZipFile(zipfile.ZipFile, BytesIO):
    """
    Adapted from https://github.com/pandas-dev/pandas/blob/main/pandas/io/common.py
    Wrapper for standard library class ZipFile and allow the returned file-like
    handle to accept byte strings via `write` method.
    BytesIO provides attributes of file-like object and ZipFile.writestr writes
    bytes strings into a member of the archive.
    """

    def __init__(
        self,
        file,
        mode: str,
        **kwargs,
    ):
        mode = mode.replace("b", "")
        self.multiple_write_buffer = None

        kwargs_zip = {"compression": zipfile.ZIP_DEFLATED}
        kwargs_zip.update(kwargs)

        super().__init__(file, mode, **kwargs_zip)

    def infer_filename(self):
        if isinstance(self.filename, (os.PathLike, str)):
            filename = Path(self.filename)
            if filename.suffix == ".zip":
                return filename.with_suffix("").name
            return filename.name
        return None

    def write(self, data):
        # buffer multiple write calls, write on flush
        if self.multiple_write_buffer is None:
            self.multiple_write_buffer = BytesIO() if isinstance(data, bytes) else StringIO()
        self.multiple_write_buffer.write(data)
        return len(self.multiple_write_buffer.getvalue())

    def flush(self) -> None:
        # write to actual handle and close write buffer
        if self.multiple_write_buffer is None or self.multiple_write_buffer.closed:
            return

        # ZipFile needs a non-empty string
        archive_name = self.infer_filename()
        with self.multiple_write_buffer:
            super().writestr(archive_name, self.multiple_write_buffer.getvalue())

    def close(self):
        self.flush()
        super().close()

    @property
    def closed(self):
        return self.fp is None
