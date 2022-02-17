import gzip
import lzma
import os
import shutil
import struct
import tarfile
from zipfile import ZipFile
from zipfile import is_zipfile as _is_zipfile

from datasets import config
from datasets.utils.filelock import FileLock


class ExtractManager:
    def __init__(self, cache_dir=None):
        self.extract_dir = (
            os.path.join(cache_dir, config.EXTRACTED_DATASETS_DIR) if cache_dir else config.EXTRACTED_DATASETS_PATH
        )
        self.extractor = Extractor

    def _get_output_path(self, path):
        from datasets.utils.file_utils import hash_url_to_filename

        # Path where we extract compressed archives
        # We extract in the cache dir, and get the extracted path name by hashing the original path"
        abs_path = os.path.abspath(path)
        return os.path.join(self.extract_dir, hash_url_to_filename(abs_path))

    def _do_extract(self, output_path, force_extract):
        return force_extract or (
            not os.path.isfile(output_path) and not (os.path.isdir(output_path) and os.listdir(output_path))
        )

    def extract(self, input_path, force_extract=False):
        is_extractable, extractor = self.extractor.is_extractable(input_path, return_extractor=True)
        if not is_extractable:
            return input_path
        output_path = self._get_output_path(input_path)
        if self._do_extract(output_path, force_extract):
            self.extractor.extract(input_path, output_path, extractor=extractor)
        return output_path


class TarExtractor:
    @staticmethod
    def is_extractable(path):
        return tarfile.is_tarfile(path)

    @staticmethod
    def extract(input_path, output_path):
        os.makedirs(output_path, exist_ok=True)
        tar_file = tarfile.open(input_path)
        tar_file.extractall(output_path)
        tar_file.close()


class GzipExtractor:
    @staticmethod
    def is_extractable(path: str) -> bool:
        """from https://stackoverflow.com/a/60634210"""
        with gzip.open(path, "r") as fh:
            try:
                fh.read(1)
                return True
            except OSError:
                return False

    @staticmethod
    def extract(input_path, output_path):
        with gzip.open(input_path, "rb") as gzip_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(gzip_file, extracted_file)


class ZipExtractor:
    @staticmethod
    def is_extractable(path):
        return _is_zipfile(path)

    @staticmethod
    def extract(input_path, output_path):
        os.makedirs(output_path, exist_ok=True)
        with ZipFile(input_path, "r") as zip_file:
            zip_file.extractall(output_path)
            zip_file.close()


class XzExtractor:
    @staticmethod
    def is_extractable(path: str) -> bool:
        """https://tukaani.org/xz/xz-file-format-1.0.4.txt"""
        with open(path, "rb") as f:
            try:
                header_magic_bytes = f.read(6)
            except OSError:
                return False
            if header_magic_bytes == b"\xfd7zXZ\x00":
                return True
            else:
                return False

    @staticmethod
    def extract(input_path, output_path):
        with lzma.open(input_path) as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class RarExtractor:
    @staticmethod
    def is_extractable(path: str) -> bool:
        """https://github.com/markokr/rarfile/blob/master/rarfile.py"""
        RAR_ID = b"Rar!\x1a\x07\x00"
        RAR5_ID = b"Rar!\x1a\x07\x01\x00"

        with open(path, "rb", 1024) as fd:
            buf = fd.read(len(RAR5_ID))
        if buf.startswith(RAR_ID) or buf.startswith(RAR5_ID):
            return True
        else:
            return False

    @staticmethod
    def extract(input_path, output_path):
        if not config.RARFILE_AVAILABLE:
            raise OSError("Please pip install rarfile")
        import rarfile

        os.makedirs(output_path, exist_ok=True)
        rf = rarfile.RarFile(input_path)
        rf.extractall(output_path)
        rf.close()


class ZstdExtractor:
    @staticmethod
    def is_extractable(path: str) -> bool:
        """https://datatracker.ietf.org/doc/html/rfc8878

        Magic_Number:  4 bytes, little-endian format.  Value: 0xFD2FB528.
        """
        with open(path, "rb") as f:
            try:
                magic_number = f.read(4)
            except OSError:
                return False
        return True if magic_number == struct.pack("<I", 0xFD2FB528) else False

    @staticmethod
    def extract(input_path: str, output_path: str):
        if not config.ZSTANDARD_AVAILABLE:
            raise OSError("Please pip install zstandard")
        import zstandard as zstd

        dctx = zstd.ZstdDecompressor()
        with open(input_path, "rb") as ifh, open(output_path, "wb") as ofh:
            dctx.copy_stream(ifh, ofh)


class Extractor:
    #  Put zip file to the last, b/c it is possible wrongly detected as zip (I guess it means: as tar or gzip)
    extractors = [TarExtractor, GzipExtractor, ZipExtractor, XzExtractor, RarExtractor, ZstdExtractor]

    @classmethod
    def is_extractable(cls, path, return_extractor=False):
        for extractor in cls.extractors:
            if extractor.is_extractable(path):
                return True if not return_extractor else (True, extractor)
        return False if not return_extractor else (False, None)

    @classmethod
    def extract(cls, input_path, output_path, extractor=None):
        # Prevent parallel extractions
        lock_path = input_path + ".lock"
        with FileLock(lock_path):
            shutil.rmtree(output_path, ignore_errors=True)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if extractor:
                return extractor.extract(input_path, output_path)
            for extractor in cls.extractors:
                if extractor.is_extractable(input_path):
                    return extractor.extract(input_path, output_path)
