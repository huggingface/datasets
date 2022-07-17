import bz2
import gzip
import lzma
import os
import shutil
import tarfile
import zipfile
from abc import ABC, abstractmethod

from .. import config
from .filelock import FileLock


class ExtractManager:
    def __init__(self, cache_dir=None):
        self.extract_dir = (
            os.path.join(cache_dir, config.EXTRACTED_DATASETS_DIR) if cache_dir else config.EXTRACTED_DATASETS_PATH
        )
        self.extractor = Extractor

    def _get_output_path(self, path):
        from .file_utils import hash_url_to_filename

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


class BaseExtractor(ABC):
    magic_number = b""

    @staticmethod
    def read_magic_number(path: str, magic_number_length: int):
        with open(path, "rb") as f:
            return f.read(magic_number_length)

    @classmethod
    @abstractmethod
    def is_extractable(cls, path: str, magic_number: bytes = b"") -> bool:
        if not magic_number:
            try:
                magic_number = cls.read_magic_number(path, len(cls.magic_number))
            except OSError:
                return False
        return magic_number.startswith(cls.magic_number)

    @staticmethod
    @abstractmethod
    def extract(input_path: str, output_path: str) -> None:
        ...


class TarExtractor(BaseExtractor):
    @classmethod
    def is_extractable(cls, path: str, **kwargs) -> bool:
        return tarfile.is_tarfile(path)

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        os.makedirs(output_path, exist_ok=True)
        tar_file = tarfile.open(input_path)
        tar_file.extractall(output_path)
        tar_file.close()


class GzipExtractor(BaseExtractor):
    magic_number = b"\x1F\x8B"

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        with gzip.open(input_path, "rb") as gzip_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(gzip_file, extracted_file)


class ZipExtractor(BaseExtractor):
    @classmethod
    def is_extractable(cls, path: str, **kwargs) -> bool:
        return zipfile.is_zipfile(path)

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        os.makedirs(output_path, exist_ok=True)
        with zipfile.ZipFile(input_path, "r") as zip_file:
            zip_file.extractall(output_path)
            zip_file.close()


class XzExtractor(BaseExtractor):
    magic_number = b"\xFD\x37\x7A\x58\x5A\x00"

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        with lzma.open(input_path) as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class RarExtractor(BaseExtractor):
    RAR_ID = b"Rar!\x1a\x07\x00"
    RAR5_ID = b"Rar!\x1a\x07\x01\x00"

    @classmethod
    def is_extractable(cls, path: str, **kwargs) -> bool:
        """https://github.com/markokr/rarfile/blob/master/rarfile.py"""
        with open(path, "rb") as f:
            magic_number = f.read(len(cls.RAR5_ID))
        return magic_number == cls.RAR5_ID or magic_number.startswith(cls.RAR_ID)

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        if not config.RARFILE_AVAILABLE:
            raise OSError("Please pip install rarfile")
        import rarfile

        os.makedirs(output_path, exist_ok=True)
        rf = rarfile.RarFile(input_path)
        rf.extractall(output_path)
        rf.close()


class ZstdExtractor(BaseExtractor):
    magic_number = b"\x28\xb5\x2F\xFD"

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        if not config.ZSTANDARD_AVAILABLE:
            raise OSError("Please pip install zstandard")
        import zstandard as zstd

        dctx = zstd.ZstdDecompressor()
        with open(input_path, "rb") as ifh, open(output_path, "wb") as ofh:
            dctx.copy_stream(ifh, ofh)


class Bzip2Extractor(BaseExtractor):
    magic_number = b"\x42\x5A\x68"

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        with bz2.open(input_path, "rb") as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class SevenZipExtractor(BaseExtractor):
    magic_number = b"\x37\x7A\xBC\xAF\x27\x1C"

    @staticmethod
    def extract(input_path: str, output_path: str) -> None:
        if not config.PY7ZR_AVAILABLE:
            raise OSError("Please pip install py7zr")
        import py7zr

        os.makedirs(output_path, exist_ok=True)
        with py7zr.SevenZipFile(input_path, "r") as archive:
            archive.extractall(output_path)


class Extractor:
    #  Put zip file to the last, b/c it is possible wrongly detected as zip (I guess it means: as tar or gzip)
    extractors = [
        TarExtractor,
        GzipExtractor,
        ZipExtractor,
        XzExtractor,
        RarExtractor,
        ZstdExtractor,
        Bzip2Extractor,
        SevenZipExtractor,
    ]

    @classmethod
    def _get_magic_number_max_length(cls):
        magic_number_max_length = 0
        for extractor in cls.extractors:
            if hasattr(extractor, "magic_number"):
                magic_number_length = len(extractor.magic_number)
                magic_number_max_length = (
                    magic_number_length if magic_number_length > magic_number_max_length else magic_number_max_length
                )
        return magic_number_max_length

    @staticmethod
    def _read_magic_number(path: str, magic_number_length: int):
        try:
            return BaseExtractor.read_magic_number(path, magic_number_length=magic_number_length)
        except OSError:
            return b""

    @classmethod
    def is_extractable(cls, path, return_extractor=False):
        magic_number_max_length = cls._get_magic_number_max_length()
        magic_number = cls._read_magic_number(path, magic_number_max_length)
        for extractor in cls.extractors:
            if extractor.is_extractable(path, magic_number=magic_number):
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
