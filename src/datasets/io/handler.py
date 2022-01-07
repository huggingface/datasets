import bz2
import gzip
import lzma


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

        return self._file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._file.close()
