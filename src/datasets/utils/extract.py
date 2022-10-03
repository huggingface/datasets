import bz2
import gzip
import lzma
import os
import shutil
import tarfile
import warnings
import zipfile
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Union

from .. import config
from .filelock import FileLock
from .logging import get_logger


logger = get_logger(__name__)


if TYPE_CHECKING:
    import pathlib


class ExtractManager:
    def __init__(self, cache_dir: Optional[str] = None):
        self.extract_dir = (
            os.path.join(cache_dir, config.EXTRACTED_DATASETS_DIR) if cache_dir else config.EXTRACTED_DATASETS_PATH
        )
        self.extractor = Extractor

    def _get_output_path(self, path: str) -> str:
        from .file_utils import hash_url_to_filename

        # Path where we extract compressed archives
        # We extract in the cache dir, and get the extracted path name by hashing the original path"
        abs_path = os.path.abspath(path)
        return os.path.join(self.extract_dir, hash_url_to_filename(abs_path))

    def _do_extract(self, output_path: str, force_extract: bool) -> bool:
        return force_extract or (
            not os.path.isfile(output_path) and not (os.path.isdir(output_path) and os.listdir(output_path))
        )

    def extract(self, input_path: str, force_extract: bool = False) -> str:
        extractor_format = self.extractor.infer_extractor_format(input_path)
        if not extractor_format:
            return input_path
        output_path = self._get_output_path(input_path)
        if self._do_extract(output_path, force_extract):
            self.extractor.extract(input_path, output_path, extractor_format)
        return output_path


class BaseExtractor(ABC):
    @classmethod
    @abstractmethod
    def is_extractable(cls, path: Union["pathlib.Path", str], **kwargs) -> bool:
        ...

    @staticmethod
    @abstractmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        ...


class MagicNumberBaseExtractor(BaseExtractor, ABC):
    magic_number = b""

    @staticmethod
    def read_magic_number(path: Union["pathlib.Path", str], magic_number_length: int):
        with open(path, "rb") as f:
            return f.read(magic_number_length)

    @classmethod
    def is_extractable(cls, path: Union["pathlib.Path", str], magic_number: bytes = b"") -> bool:
        if not magic_number:
            try:
                magic_number = cls.read_magic_number(path, len(cls.magic_number))
            except OSError:
                return False
        return magic_number.startswith(cls.magic_number)


class TarExtractor(BaseExtractor):
    @classmethod
    def is_extractable(cls, path: Union["pathlib.Path", str], **kwargs) -> bool:
        return tarfile.is_tarfile(path)

    @staticmethod
    def safemembers(members):
        """
        Fix for CVE-2007-4559
        Desc:
            Directory traversal vulnerability in the (1) extract and (2) extractall functions in the tarfile
            module in Python allows user-assisted remote attackers to overwrite arbitrary files via a .. (dot dot)
            sequence in filenames in a TAR archive, a related issue to CVE-2001-1267.
        See: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-4559
        From: https://stackoverflow.com/a/10077309
        """

        def resolved(path: str) -> str:
            return os.path.realpath(os.path.abspath(path))

        def badpath(path: str, base: str) -> bool:
            # joinpath will ignore base if path is absolute
            return not resolved(os.path.join(base, path)).startswith(base)

        def badlink(info, base: str) -> bool:
            # Links are interpreted relative to the directory containing the link
            tip = resolved(os.path.join(base, os.path.dirname(info.name)))
            return badpath(info.linkname, base=tip)

        base = resolved(".")

        for finfo in members:
            if badpath(finfo.name, base):
                logger.error(f"Extraction of {finfo.name} is blocked (illegal path)")
            elif finfo.issym() and badlink(finfo, base):
                logger.error(f"Extraction of {finfo.name} is blocked: Hard link to {finfo.linkname}")
            elif finfo.islnk() and badlink(finfo, base):
                logger.error(f"Extraction of {finfo.name} is blocked: Symlink to {finfo.linkname}")
            else:
                yield finfo

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        os.makedirs(output_path, exist_ok=True)
        tar_file = tarfile.open(input_path)
        tar_file.extractall(output_path, members=TarExtractor.safemembers(tar_file))
        tar_file.close()


class GzipExtractor(MagicNumberBaseExtractor):
    magic_number = b"\x1F\x8B"

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        with gzip.open(input_path, "rb") as gzip_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(gzip_file, extracted_file)


class ZipExtractor(BaseExtractor):
    @classmethod
    def is_extractable(cls, path: Union["pathlib.Path", str], **kwargs) -> bool:
        return zipfile.is_zipfile(path)

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        os.makedirs(output_path, exist_ok=True)
        with zipfile.ZipFile(input_path, "r") as zip_file:
            zip_file.extractall(output_path)
            zip_file.close()


class XzExtractor(MagicNumberBaseExtractor):
    magic_number = b"\xFD\x37\x7A\x58\x5A\x00"

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        with lzma.open(input_path) as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class RarExtractor(BaseExtractor):
    RAR_ID = b"Rar!\x1a\x07\x00"
    RAR5_ID = b"Rar!\x1a\x07\x01\x00"

    @classmethod
    def is_extractable(cls, path: Union["pathlib.Path", str], **kwargs) -> bool:
        """https://github.com/markokr/rarfile/blob/master/rarfile.py"""
        with open(path, "rb") as f:
            magic_number = f.read(len(cls.RAR5_ID))
        return magic_number == cls.RAR5_ID or magic_number.startswith(cls.RAR_ID)

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        if not config.RARFILE_AVAILABLE:
            raise OSError("Please pip install rarfile")
        import rarfile

        os.makedirs(output_path, exist_ok=True)
        rf = rarfile.RarFile(input_path)
        rf.extractall(output_path)
        rf.close()


class ZstdExtractor(MagicNumberBaseExtractor):
    magic_number = b"\x28\xb5\x2F\xFD"

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        if not config.ZSTANDARD_AVAILABLE:
            raise OSError("Please pip install zstandard")
        import zstandard as zstd

        dctx = zstd.ZstdDecompressor()
        with open(input_path, "rb") as ifh, open(output_path, "wb") as ofh:
            dctx.copy_stream(ifh, ofh)


class Bzip2Extractor(MagicNumberBaseExtractor):
    magic_number = b"\x42\x5A\x68"

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        with bz2.open(input_path, "rb") as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class SevenZipExtractor(MagicNumberBaseExtractor):
    magic_number = b"\x37\x7A\xBC\xAF\x27\x1C"

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        if not config.PY7ZR_AVAILABLE:
            raise OSError("Please pip install py7zr")
        import py7zr

        os.makedirs(output_path, exist_ok=True)
        with py7zr.SevenZipFile(input_path, "r") as archive:
            archive.extractall(output_path)


class Lz4Extractor(MagicNumberBaseExtractor):
    magic_number = b"\x04\x22\x4D\x18"

    @staticmethod
    def extract(input_path: Union["pathlib.Path", str], output_path: Union["pathlib.Path", str]) -> None:
        if not config.LZ4_AVAILABLE:
            raise OSError("Please pip install lz4")
        import lz4.frame

        with lz4.frame.open(input_path, "rb") as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class Extractor:
    #  Put zip file to the last, b/c it is possible wrongly detected as zip (I guess it means: as tar or gzip)
    extractors = {
        "tar": TarExtractor,
        "gzip": GzipExtractor,
        "zip": ZipExtractor,
        "xz": XzExtractor,
        "rar": RarExtractor,
        "zstd": ZstdExtractor,
        "bz2": Bzip2Extractor,
        "7z": SevenZipExtractor,  # <Added version="2.4.0"/>
        "lz4": Lz4Extractor,  # <Added version="2.4.0"/>
    }

    @classmethod
    def _get_magic_number_max_length(cls):
        magic_number_max_length = 0
        for extractor in cls.extractors.values():
            if hasattr(extractor, "magic_number"):
                magic_number_length = len(extractor.magic_number)
                magic_number_max_length = (
                    magic_number_length if magic_number_length > magic_number_max_length else magic_number_max_length
                )
        return magic_number_max_length

    @staticmethod
    def _read_magic_number(path: Union["pathlib.Path", str], magic_number_length: int):
        try:
            return MagicNumberBaseExtractor.read_magic_number(path, magic_number_length=magic_number_length)
        except OSError:
            return b""

    @classmethod
    def is_extractable(cls, path: Union["pathlib.Path", str], return_extractor: bool = False) -> bool:
        warnings.warn(
            "Method 'is_extractable' was deprecated in version 2.4.0 and will be removed in 3.0.0. "
            "Use 'infer_extractor_format' instead.",
            category=FutureWarning,
        )
        extractor_format = cls.infer_extractor_format(path)
        if extractor_format:
            return True if not return_extractor else (True, cls.extractors[extractor_format])
        return False if not return_extractor else (False, None)

    @classmethod
    def infer_extractor_format(cls, path: Union["pathlib.Path", str]) -> str:  # <Added version="2.4.0"/>
        magic_number_max_length = cls._get_magic_number_max_length()
        magic_number = cls._read_magic_number(path, magic_number_max_length)
        for extractor_format, extractor in cls.extractors.items():
            if extractor.is_extractable(path, magic_number=magic_number):
                return extractor_format

    @classmethod
    def extract(
        cls,
        input_path: Union["pathlib.Path", str],
        output_path: Union["pathlib.Path", str],
        extractor_format: Optional[str] = None,  # <Added version="2.4.0"/>
        extractor: Optional[BaseExtractor] = "deprecated",
    ) -> None:
        # Prevent parallel extractions
        lock_path = str(input_path) + ".lock"
        with FileLock(lock_path):
            shutil.rmtree(output_path, ignore_errors=True)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if extractor_format or extractor != "deprecated":
                if extractor != "deprecated" or not isinstance(extractor_format, str):  # passed as positional arg
                    warnings.warn(
                        "Parameter 'extractor' was deprecated in version 2.4.0 and will be removed in 3.0.0. "
                        "Use 'extractor_format' instead.",
                        category=FutureWarning,
                    )
                    extractor = extractor if extractor != "deprecated" else extractor_format
                else:
                    extractor = cls.extractors[extractor_format]
                return extractor.extract(input_path, output_path)
            else:
                warnings.warn(
                    "Parameter 'extractor_format' was made required in version 2.4.0 and not passing it will raise an "
                    "exception in 3.0.0.",
                    category=FutureWarning,
                )
                for extractor in cls.extractors.values():
                    if extractor.is_extractable(input_path):
                        return extractor.extract(input_path, output_path)
