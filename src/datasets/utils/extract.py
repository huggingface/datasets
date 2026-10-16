import bz2
import gzip
import hashlib
import lzma
import os
import shutil
import struct
import tarfile
import tempfile
import warnings
import zipfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

from .. import config
from ._filelock import FileLock
from .logging import get_logger


if TYPE_CHECKING:
    import py7zr
    import rarfile


logger = get_logger(__name__)


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

    def extract(self, input_path: str, force_extract: bool = False) -> str:
        """Return the extracted cache path, reusing it unless ``force_extract=True``.

        Complete final outputs can be reused without writing to the cache directory.
        Extraction and publication use a lock. Unrecognized formats are returned unchanged.
        """
        extractor_format = self.extractor.infer_extractor_format(input_path)
        if not extractor_format:
            return input_path
        output_path = self._get_output_path(input_path)
        self.extractor.extract(input_path, output_path, extractor_format, force_extract=force_extract)
        return output_path


class BaseExtractor(ABC):
    @classmethod
    @abstractmethod
    def is_extractable(cls, path: Union[Path, str], **kwargs) -> bool: ...

    @staticmethod
    @abstractmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None: ...


class MagicNumberBaseExtractor(BaseExtractor, ABC):
    magic_numbers: list[bytes] = []

    @staticmethod
    def read_magic_number(path: Union[Path, str], magic_number_length: int):
        with open(path, "rb") as f:
            return f.read(magic_number_length)

    @classmethod
    def is_extractable(cls, path: Union[Path, str], magic_number: bytes = b"") -> bool:
        if not magic_number:
            magic_number_length = max(len(cls_magic_number) for cls_magic_number in cls.magic_numbers)
            try:
                magic_number = cls.read_magic_number(path, magic_number_length)
            except OSError:
                return False
        return any(magic_number.startswith(cls_magic_number) for cls_magic_number in cls.magic_numbers)


class TarExtractor(BaseExtractor):
    @classmethod
    def is_extractable(cls, path: Union[Path, str], **kwargs) -> bool:
        return tarfile.is_tarfile(path)

    @staticmethod
    def safemembers(members: tarfile.TarFile, output_path: Union[Path, str]):
        """
        Fix for CVE-2007-4559
        Desc:
            Directory traversal vulnerability in the (1) extract and (2) extractall functions in the tarfile
            module in Python allows user-assisted remote attackers to overwrite arbitrary files via a .. (dot dot)
            sequence in filenames in a TAR archive, a related issue to CVE-2001-1267.
        See: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-4559
        From: https://stackoverflow.com/a/10077309
        """

        def resolved(path: Union[Path, str]) -> str:
            return os.path.realpath(os.path.abspath(path))

        def badpath(path: str, base: str) -> bool:
            # joinpath will ignore base if path is absolute
            # Also, a plain startswith(base) would still match sibling directories
            # whose name starts with the base name (e.g. "../base_evil/x" when
            # extracting into ".../base"), so require the base plus a separator
            target = resolved(os.path.join(base, path))
            return target != base and not target.startswith(base + os.sep)

        def badlink(info: tarfile.TarInfo, base: str) -> bool:
            # Links are interpreted relative to the directory containing the link
            tip = resolved(os.path.join(base, os.path.dirname(info.name)))
            return badpath(info.linkname, base=tip)

        base = resolved(output_path)

        for finfo in members:
            if badpath(finfo.name, base):
                logger.error(f"Extraction of {finfo.name} is blocked (illegal path)")
            elif finfo.issym() and badlink(finfo, base):
                logger.error(f"Extraction of {finfo.name} is blocked: Symlink to {finfo.linkname}")
            elif finfo.islnk() and badlink(finfo, base):
                logger.error(f"Extraction of {finfo.name} is blocked: Hard link to {finfo.linkname}")
            else:
                yield finfo

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        os.makedirs(output_path, exist_ok=True)
        tar_file = tarfile.open(input_path)
        tar_file.extractall(output_path, members=TarExtractor.safemembers(tar_file, output_path))
        tar_file.close()


class GzipExtractor(MagicNumberBaseExtractor):
    magic_numbers = [b"\x1f\x8b"]

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        with gzip.open(input_path, "rb") as gzip_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(gzip_file, extracted_file)


class ZipExtractor(MagicNumberBaseExtractor):
    magic_numbers = [
        b"PK\x03\x04",
        b"PK\x05\x06",  # empty archive
        b"PK\x07\x08",  # spanned archive
    ]

    @classmethod
    def is_extractable(cls, path: Union[Path, str], magic_number: bytes = b"") -> bool:
        if super().is_extractable(path, magic_number=magic_number):
            return True
        try:
            # Alternative version of zipfile.is_zipfile that has less false positives, but misses executable zip archives.
            # From: https://github.com/python/cpython/pull/5053
            from zipfile import (
                _CD_SIGNATURE,
                _ECD_DISK_NUMBER,
                _ECD_DISK_START,
                _ECD_ENTRIES_TOTAL,
                _ECD_OFFSET,
                _ECD_SIZE,
                _EndRecData,
                sizeCentralDir,
                stringCentralDir,
                structCentralDir,
            )

            with open(path, "rb") as fp:
                endrec = _EndRecData(fp)
                if endrec:
                    if endrec[_ECD_ENTRIES_TOTAL] == 0 and endrec[_ECD_SIZE] == 0 and endrec[_ECD_OFFSET] == 0:
                        return True  # Empty zipfiles are still zipfiles
                    elif endrec[_ECD_DISK_NUMBER] == endrec[_ECD_DISK_START]:
                        fp.seek(endrec[_ECD_OFFSET])  # Central directory is on the same disk
                        if fp.tell() == endrec[_ECD_OFFSET] and endrec[_ECD_SIZE] >= sizeCentralDir:
                            data = fp.read(sizeCentralDir)  # CD is where we expect it to be
                            if len(data) == sizeCentralDir:
                                centdir = struct.unpack(structCentralDir, data)  # CD is the right size
                                if centdir[_CD_SIGNATURE] == stringCentralDir:
                                    return True  # First central directory entry  has correct magic number
            return False
        except Exception:  # catch all errors in case future python versions change the zipfile internals
            return False

    @staticmethod
    def safemembers(members: list[zipfile.ZipInfo], output_path: Union[Path, str]):
        """
        Fix for CVE-2007-4559
        Desc:
            Directory traversal vulnerability in the (1) extract and (2) extractall functions in the tarfile
            module in Python allows user-assisted remote attackers to overwrite arbitrary files via a .. (dot dot)
            sequence in filenames in a TAR archive, a related issue to CVE-2001-1267.
        See: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-4559
        From: https://stackoverflow.com/a/10077309

        This additional mitigation is applied for zipfile as well.
        """

        def resolved(path: Union[Path, str]) -> str:
            return os.path.realpath(os.path.abspath(path))

        def badpath(path: str, base: str) -> bool:
            # joinpath will ignore base if path is absolute
            # Also, a plain startswith(base) would still match sibling directories
            # whose name starts with the base name (e.g. "../base_evil/x" when
            # extracting into ".../base"), so require the base plus a separator
            target = resolved(os.path.join(base, path))
            return target != base and not target.startswith(base + os.sep)

        base = resolved(output_path)

        for finfo in members:
            if badpath(finfo.filename, base):
                logger.error(f"Extraction of {finfo.filename} is blocked (illegal path)")
            # zipfile doesn't support symlinks
            # elif finfo.is_symlink and badlink(finfo, base):
            #     logger.error(f"Extraction of {finfo.name} is blocked: Symlink to {finfo.linkname}")
            else:
                yield finfo

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        os.makedirs(output_path, exist_ok=True)
        with zipfile.ZipFile(input_path, "r") as zip_file:
            zip_file.extractall(output_path, members=ZipExtractor.safemembers(zip_file.filelist, output_path))
            zip_file.close()


class XzExtractor(MagicNumberBaseExtractor):
    magic_numbers = [b"\xfd\x37\x7a\x58\x5a\x00"]

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        with lzma.open(input_path) as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class RarExtractor(MagicNumberBaseExtractor):
    magic_numbers = [b"Rar!\x1a\x07\x00", b"Rar!\x1a\x07\x01\x00"]  # RAR_ID  # RAR5_ID

    @staticmethod
    def safemembers(members: list["rarfile.RarInfo"], output_path: Union[Path, str]):
        """
        Fix for CVE-2007-4559
        Desc:
            Directory traversal vulnerability in the (1) extract and (2) extractall functions in the tarfile
            module in Python allows user-assisted remote attackers to overwrite arbitrary files via a .. (dot dot)
            sequence in filenames in a TAR archive, a related issue to CVE-2001-1267.
        See: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-4559
        From: https://stackoverflow.com/a/10077309

        This additional mitigation is applied for rarfile as well.
        """

        def resolved(path: Union[Path, str]) -> str:
            return os.path.realpath(os.path.abspath(path))

        def badpath(path: str, base: str) -> bool:
            # joinpath will ignore base if path is absolute
            # Also, a plain startswith(base) would still match sibling directories
            # whose name starts with the base name (e.g. "../base_evil/x" when
            # extracting into ".../base"), so require the base plus a separator
            target = resolved(os.path.join(base, path))
            return target != base and not target.startswith(base + os.sep)

        def badlink(info: "rarfile.RarInfo", base: str) -> bool:
            # Links are interpreted relative to the directory containing the link
            tip = resolved(os.path.join(base, os.path.dirname(info.filename)))
            redir_type, redir_flags, link_name = info.file_redir
            return badpath(link_name, base=tip)

        base = resolved(output_path)

        for finfo in members:
            if badpath(finfo.filename, base):
                logger.error(f"Extraction of {finfo.filename} is blocked (illegal path)")
            elif finfo.is_symlink() and badlink(finfo, base):
                logger.error(f"Extraction of {finfo.filename} is blocked: Symlink to {finfo.file_redir}")
            else:
                yield finfo

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        if not config.RARFILE_AVAILABLE:
            raise ImportError("Please pip install rarfile")
        import rarfile

        os.makedirs(output_path, exist_ok=True)
        rf = rarfile.RarFile(input_path)
        rf.extractall(output_path, members=RarExtractor.safemembers(rf.infolist(), output_path))
        rf.close()


class ZstdExtractor(MagicNumberBaseExtractor):
    magic_numbers = [b"\x28\xb5\x2f\xfd"]

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        if not config.ZSTANDARD_AVAILABLE:
            raise ImportError("Please pip install zstandard")
        import zstandard as zstd

        dctx = zstd.ZstdDecompressor()
        with open(input_path, "rb") as ifh, open(output_path, "wb") as ofh:
            dctx.copy_stream(ifh, ofh)


class Bzip2Extractor(MagicNumberBaseExtractor):
    magic_numbers = [b"\x42\x5a\x68"]

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        with bz2.open(input_path, "rb") as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class SevenZipExtractor(MagicNumberBaseExtractor):
    magic_numbers = [b"\x37\x7a\xbc\xaf\x27\x1c"]

    @staticmethod
    def safemembers(members: list["py7zr.FileInfo"], output_path: Union[Path, str]):
        """
        Fix for CVE-2007-4559
        Desc:
            Directory traversal vulnerability in the (1) extract and (2) extractall functions in the tarfile
            module in Python allows user-assisted remote attackers to overwrite arbitrary files via a .. (dot dot)
            sequence in filenames in a TAR archive, a related issue to CVE-2001-1267.
        See: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-4559
        From: https://stackoverflow.com/a/10077309

        This additional mitigation is applied for py7zr as well.
        """

        def resolved(path: Union[Path, str]) -> str:
            return os.path.realpath(os.path.abspath(path))

        def badpath(path: str, base: str) -> bool:
            # joinpath will ignore base if path is absolute
            # Also, a plain startswith(base) would still match sibling directories
            # whose name starts with the base name (e.g. "../base_evil/x" when
            # extracting into ".../base"), so require the base plus a separator
            target = resolved(os.path.join(base, path))
            return target != base and not target.startswith(base + os.sep)

        def badlink(info: "py7zr.FileInfo", base: str) -> bool:
            # Links are interpreted relative to the directory containing the link
            tip = resolved(os.path.join(base, os.path.dirname(info.filename)))
            return badpath(os.path.basename(info.filename), base=tip)

        base = resolved(output_path)

        for finfo in members:
            if badpath(finfo.filename, base):
                logger.error(f"Extraction of {finfo.filename} is blocked (illegal path)")
            # py7zr already checks symlinks validity
            # elif finfo.is_symlink and badlink(finfo, base):
            #     logger.error(f"Extraction of {finfo.name} is blocked: Symlink to {finfo.linkname}")
            else:
                yield finfo

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        if not config.PY7ZR_AVAILABLE:
            raise ImportError("Please pip install py7zr")
        import py7zr

        os.makedirs(output_path, exist_ok=True)
        with py7zr.SevenZipFile(input_path, "r") as archive:
            targets = [finfo.filename for finfo in SevenZipExtractor.safemembers(archive.list(), output_path)]
            archive.extract(output_path, targets=targets)


class Lz4Extractor(MagicNumberBaseExtractor):
    magic_numbers = [b"\x04\x22\x4d\x18"]

    @staticmethod
    def extract(input_path: Union[Path, str], output_path: Union[Path, str]) -> None:
        if not config.LZ4_AVAILABLE:
            raise ImportError("Please pip install lz4")
        import lz4.frame

        with lz4.frame.open(input_path, "rb") as compressed_file:
            with open(output_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)


class Extractor:
    #  Put zip file to the last, b/c it is possible wrongly detected as zip (I guess it means: as tar or gzip)
    extractors: dict[str, type[BaseExtractor]] = {
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
        return max(
            len(extractor_magic_number)
            for extractor in cls.extractors.values()
            if issubclass(extractor, MagicNumberBaseExtractor)
            for extractor_magic_number in extractor.magic_numbers
        )

    @staticmethod
    def _read_magic_number(path: Union[Path, str], magic_number_length: int):
        try:
            return MagicNumberBaseExtractor.read_magic_number(path, magic_number_length=magic_number_length)
        except OSError:
            return b""

    @classmethod
    def is_extractable(cls, path: Union[Path, str], return_extractor: bool = False) -> bool:
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
    def infer_extractor_format(cls, path: Union[Path, str]) -> Optional[str]:  # <Added version="2.4.0"/>
        magic_number_max_length = cls._get_magic_number_max_length()
        magic_number = cls._read_magic_number(path, magic_number_max_length)
        for extractor_format, extractor in cls.extractors.items():
            if extractor.is_extractable(path, magic_number=magic_number):
                return extractor_format

    @classmethod
    def extract(
        cls,
        input_path: Union[Path, str],
        output_path: Union[Path, str],
        extractor_format: str,
        force_extract: bool = True,
    ) -> None:
        """Extract into a staging path and publish the completed output under a lock.

        Direct callers rebuild by default for backward compatibility. Pass
        ``force_extract=False`` to reuse a final cached file or nonempty directory,
        as :class:`ExtractManager` does by default. Failed extractions leave only
        staging data and preserve any previously published output.

        Temporary siblings use the reserved prefix ``.tmp-extract-<sha256>-``, where
        the digest identifies the normalized output basename, followed by tempfile's
        random component. Only this output's temporary namespace is cleaned under its
        lock; arbitrary ``.old`` and ``.incomplete`` siblings are never touched.

        Replacing directories requires renaming the old output aside first, including
        on Windows. The final path is briefly absent between renames; readers of a
        previously returned path do not hold the extraction lock during this interval.
        """

        def remove_path(path):
            if os.path.islink(path) or os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

        def is_cached():
            try:
                return os.path.isfile(output_path) or (os.path.isdir(output_path) and os.listdir(output_path))
            except (FileNotFoundError, NotADirectoryError):
                # A forced rebuild may rename the final output during this check.
                return False

        # Strip trailing separators without resolving symlinks or collapsing "..":
        # the OS must resolve the output and its temporary siblings the same way.
        drive, tail = os.path.splitdrive(os.fspath(output_path))
        output_path = drive + (tail.rstrip(os.sep + (os.altsep or "")) or tail)
        # Atomic publication makes a final cache hit safe without opening a writable lock.
        if not force_extract and is_cached():
            return
        output_dir = os.path.dirname(output_path) or "."
        os.makedirs(output_dir, exist_ok=True)
        # Canonicalize only the lock filename so aliases share a lock before
        # FileLock applies abspath. Output and temporary paths stay uncollapsed.
        lock_path = os.path.realpath(str(Path(output_path).with_suffix(".lock")))
        with FileLock(lock_path):
            # Only the final path is a cache hit: partial extractions are never published.
            if not force_extract and is_cached():
                return
            output_id = hashlib.sha256(os.fsencode(os.path.normcase(os.path.basename(output_path)))).hexdigest()
            tmp_prefix = f".tmp-extract-{output_id}-"
            try:
                temporary_names = os.listdir(output_dir)
            except PermissionError:
                # A writable/searchable parent need not be readable. Fresh unique
                # staging is still safe; defer garbage collection in that case.
                temporary_names = []
            for name in temporary_names:
                if name.startswith(tmp_prefix):
                    remove_path(os.path.join(output_dir, name))

            def temporary_path():
                path = tempfile.mkdtemp(prefix=tmp_prefix, dir=output_dir)
                # mkdtemp may return an abspath that collapses "..". Keep the
                # allocated basename in the caller's uncollapsed parent instead.
                path = os.path.join(output_dir, os.path.basename(path))
                # Remove only our empty reservation so either a file or directory can
                # take its place, with the extractor's usual permissions. The lock
                # protects this output's temporary namespace until publication.
                os.rmdir(path)
                return path

            incomplete_path = temporary_path()
            extractor = cls.extractors[extractor_format]
            extractor.extract(input_path, incomplete_path)

            # Retire directories before deleting them so an interrupted removal
            # cannot leave a partial final cache. Also handle file/directory changes.
            old_path = None
            if os.path.isdir(output_path) or (os.path.isdir(incomplete_path) and os.path.lexists(output_path)):
                old_path = temporary_path()
                os.replace(output_path, old_path)
            # Staging is on the same filesystem; never fall back to copying in place.
            os.replace(incomplete_path, output_path)
            if old_path is not None:
                remove_path(old_path)
