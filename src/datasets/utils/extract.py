import bisect
import bz2
import gzip
import lzma
import os
import shutil
import struct
import tarfile
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

        # Members seen so far, in archive order, with whether each was yielded;
        # plus, per normalized name, the positions at which it occurred. A hard
        # link is only safe to yield when the archive member it resolves to was
        # itself extracted: when the link target is not already on disk,
        # tarfile's link fallback re-extracts the target member at the link
        # path without re-applying this filter, so a link to a skipped
        # device/FIFO would materialise that member anyway. Resolution must
        # be position-limited exactly like tarfile._getmember: each link
        # resolves against the members preceding *that* link (last occurrence
        # wins), so a later regular file sharing a name with an earlier
        # special member must not whitewash a chain that tarfile resolves to
        # the earlier member.
        seen_members: list[tuple[tarfile.TarInfo, bool]] = []
        positions_by_name: dict[str, list[int]] = {}
        # Resolved safety verdict per hard-link position (True/False, or None
        # when a target is missing from the archive). Every link in one chain
        # shares the verdict of the chain's terminal member, so memoizing it
        # keeps validation linear: without it, a chain a0, a1 -> a0,
        # a2 -> a1, ... would re-walk the whole chain for every new link.
        link_safety: dict[int, Optional[bool]] = {}

        def resolve_before(name: str, limit: int) -> Optional[tuple[int, tarfile.TarInfo, bool]]:
            """Last member named `name` among the first `limit` seen members."""
            positions = positions_by_name.get(os.path.normpath(name))
            if not positions:
                return None
            index = bisect.bisect_left(positions, limit) - 1
            if index < 0:
                return None
            position = positions[index]
            member, yielded = seen_members[position]
            return position, member, yielded

        def safe_link_target(info: tarfile.TarInfo, position: int) -> Optional[bool]:
            """Follow a hard-link chain, resolving each step against the
            members preceding that link.

            Returns True if the chain ends at a yielded regular file or a
            yielded (in-bounds) symlink, False if it ends at any other
            member type, and None if a target is not in the archive at all,
            in which case tarfile's own behaviour for such links (KeyError)
            is preserved. No cycle check is needed: each step resolves to a
            strictly earlier member position, so the chain must terminate.
            """
            current = info
            limit = position
            yielded = False
            trail: list[int] = []
            while current.islnk():
                if limit in link_safety:
                    verdict = link_safety[limit]
                    for trail_position in trail:
                        link_safety[trail_position] = verdict
                    return verdict
                trail.append(limit)
                target_name = os.path.normpath(current.linkname)
                resolved = resolve_before(target_name, limit)
                if resolved is None:
                    for trail_position in trail:
                        link_safety[trail_position] = None
                    return None
                limit, current, yielded = resolved
            verdict = (current.isreg() or current.issym()) and yielded
            for trail_position in trail:
                link_safety[trail_position] = verdict
            return verdict

        for finfo in members:
            was_yielded = False
            if badpath(finfo.name, base):
                logger.error(f"Extraction of {finfo.name} is blocked (illegal path)")
            elif finfo.issym() and badlink(finfo, base):
                logger.error(f"Extraction of {finfo.name} is blocked: Symlink to {finfo.linkname}")
            elif finfo.islnk() and badlink(finfo, base):
                logger.error(f"Extraction of {finfo.name} is blocked: Hard link to {finfo.linkname}")
            elif finfo.islnk() and safe_link_target(finfo, len(seen_members)) is False:
                logger.error(f"Extraction of {finfo.name} is blocked (unsupported file type)")
            elif not (finfo.isreg() or finfo.isdir() or finfo.issym() or finfo.islnk()):
                # Device nodes, FIFOs, sockets and any other non-regular member can never be
                # legitimate dataset content: a device aborts the whole extraction and a FIFO
                # is materialised in the cache dir. Skip them like ArchiveIterable._iter_tar does.
                logger.error(f"Extraction of {finfo.name} is blocked (unsupported file type)")
            else:
                was_yielded = True
                yield finfo
            seen_members.append((finfo, was_yielded))
            positions_by_name.setdefault(os.path.normpath(finfo.name), []).append(len(seen_members) - 1)

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
    ) -> None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Prevent parallel extractions
        lock_path = str(Path(output_path).with_suffix(".lock"))
        with FileLock(lock_path):
            if os.path.islink(output_path):
                os.unlink(output_path)
            shutil.rmtree(output_path, ignore_errors=True)
            extractor = cls.extractors[extractor_format]
            return extractor.extract(input_path, output_path)
