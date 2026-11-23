import gzip
import io
import os
import tarfile
from pathlib import Path
from unittest.mock import patch

import pytest

from datasets.utils.extract import (
    Bzip2Extractor,
    ExtractManager,
    Extractor,
    GzipExtractor,
    Lz4Extractor,
    SevenZipExtractor,
    TarExtractor,
    XzExtractor,
    ZipExtractor,
    ZstdExtractor,
)
from datasets.utils.file_utils import hash_url_to_filename

from .utils import require_lz4, require_py7zr, require_zstandard


@pytest.mark.parametrize(
    "compression_format, is_archive",
    [
        ("7z", True),
        ("bz2", False),
        ("gzip", False),
        ("lz4", False),
        ("tar", True),
        ("xz", False),
        ("zip", True),
        ("zstd", False),
    ],
)
def test_base_extractors(
    compression_format,
    is_archive,
    bz2_file,
    gz_file,
    lz4_file,
    seven_zip_file,
    tar_file,
    xz_file,
    zip_file,
    zstd_file,
    tmp_path,
    text_file,
):
    input_paths_and_base_extractors = {
        "7z": (seven_zip_file, SevenZipExtractor),
        "bz2": (bz2_file, Bzip2Extractor),
        "gzip": (gz_file, GzipExtractor),
        "lz4": (lz4_file, Lz4Extractor),
        "tar": (tar_file, TarExtractor),
        "xz": (xz_file, XzExtractor),
        "zip": (zip_file, ZipExtractor),
        "zstd": (zstd_file, ZstdExtractor),
    }
    input_path, base_extractor = input_paths_and_base_extractors[compression_format]
    if input_path is None:
        reason = f"for '{compression_format}' compression_format, "
        if compression_format == "7z":
            reason += require_py7zr.kwargs["reason"]
        elif compression_format == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_format == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    assert base_extractor.is_extractable(input_path)
    output_path = tmp_path / ("extracted" if is_archive else "extracted.txt")
    base_extractor.extract(input_path, output_path)
    if is_archive:
        assert output_path.is_dir()
        for file_path in output_path.iterdir():
            assert file_path.name == text_file.name
            extracted_file_content = file_path.read_text(encoding="utf-8")
    else:
        extracted_file_content = output_path.read_text(encoding="utf-8")
    expected_file_content = text_file.read_text(encoding="utf-8")
    assert extracted_file_content == expected_file_content


@pytest.mark.parametrize(
    "compression_format, is_archive",
    [
        ("7z", True),
        ("bz2", False),
        ("gzip", False),
        ("lz4", False),
        ("tar", True),
        ("xz", False),
        ("zip", True),
        ("zstd", False),
    ],
)
def test_extractor(
    compression_format,
    is_archive,
    bz2_file,
    gz_file,
    lz4_file,
    seven_zip_file,
    tar_file,
    xz_file,
    zip_file,
    zstd_file,
    tmp_path,
    text_file,
):
    input_paths = {
        "7z": seven_zip_file,
        "bz2": bz2_file,
        "gzip": gz_file,
        "lz4": lz4_file,
        "tar": tar_file,
        "xz": xz_file,
        "zip": zip_file,
        "zstd": zstd_file,
    }
    input_path = input_paths[compression_format]
    if input_path is None:
        reason = f"for '{compression_format}' compression_format, "
        if compression_format == "7z":
            reason += require_py7zr.kwargs["reason"]
        elif compression_format == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_format == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    extractor_format = Extractor.infer_extractor_format(input_path)
    assert extractor_format is not None
    output_path = tmp_path / ("extracted" if is_archive else "extracted.txt")
    Extractor.extract(input_path, output_path, extractor_format)
    if is_archive:
        assert output_path.is_dir()
        for file_path in output_path.iterdir():
            assert file_path.name == text_file.name
            extracted_file_content = file_path.read_text(encoding="utf-8")
    else:
        extracted_file_content = output_path.read_text(encoding="utf-8")
    expected_file_content = text_file.read_text(encoding="utf-8")
    assert extracted_file_content == expected_file_content


@pytest.fixture
def tar_file_with_dot_dot(tmp_path, text_file):
    import tarfile

    directory = tmp_path / "data_dot_dot"
    directory.mkdir()
    path = directory / "tar_file_with_dot_dot.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(text_file, arcname=os.path.join("..", text_file.name))
    return path


@pytest.fixture
def tar_file_with_sym_link(tmp_path):
    import tarfile

    directory = tmp_path / "data_sym_link"
    directory.mkdir()
    path = directory / "tar_file_with_sym_link.tar"
    os.symlink("..", directory / "subdir", target_is_directory=True)
    with tarfile.TarFile(path, "w") as f:
        f.add(str(directory / "subdir"), arcname="subdir")  # str required by os.readlink on Windows and Python < 3.8
    return path


@pytest.fixture
def tar_file_with_sibling_prefix(tmp_path, text_file):
    # A member like "../extracted_evil/x" escapes into a *sibling* of the output
    # directory whose name starts with the output directory's name, which a plain
    # startswith(base) check used to allow.
    import tarfile

    directory = tmp_path / "data_sibling_prefix"
    directory.mkdir()
    path = directory / "tar_file_with_sibling_prefix.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(text_file, arcname="../extracted_evil/" + text_file.name)
    return path


@pytest.mark.parametrize(
    "insecure_tar_file, error_log",
    [
        ("tar_file_with_dot_dot", "illegal path"),
        ("tar_file_with_sym_link", "Symlink"),
        ("tar_file_with_sibling_prefix", "illegal path"),
    ],
)
def test_tar_extract_insecure_files(
    insecure_tar_file,
    error_log,
    tar_file_with_dot_dot,
    tar_file_with_sym_link,
    tar_file_with_sibling_prefix,
    tmp_path,
    caplog,
):
    insecure_tar_files = {
        "tar_file_with_dot_dot": tar_file_with_dot_dot,
        "tar_file_with_sym_link": tar_file_with_sym_link,
        "tar_file_with_sibling_prefix": tar_file_with_sibling_prefix,
    }
    input_path = insecure_tar_files[insecure_tar_file]
    output_path = tmp_path / "extracted"
    TarExtractor.extract(input_path, output_path)
    assert caplog.text
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert error_log in record.msg


def test_is_zipfile_false_positive(tmpdir):
    # We should have less false positives than zipfile.is_zipfile
    # We do that by checking only the magic number
    not_a_zip_file = tmpdir / "not_a_zip_file"
    # From: https://github.com/python/cpython/pull/5053
    data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x02\x08\x06\x00\x00\x00\x99\x81\xb6'\x00\x00\x00\x15I"
        b"DATx\x01\x01\n\x00\xf5\xff\x00PK\x05\x06\x00PK\x06\x06\x07"
        b"\xac\x01N\xc6|a\r\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    with not_a_zip_file.open("wb") as f:
        f.write(data)
    # zipfile.is_zipfile(str(not_a_zip_file)) could be a false positive for `zipfile`
    assert not ZipExtractor.is_extractable(not_a_zip_file)  # but we're right


ORIGINAL_TEXT = "original-content\n"
REPLACEMENT_TEXT = "replacement-with-more-characters\n"
SAME_SIZE_A = "AAAAAAAAAA"
SAME_SIZE_B = "BBBBBBBBBB"
STALE_LEGACY_TEXT = "stale-legacy\n"


def _write_gzip_archive(path, text):
    Path(path).write_bytes(gzip.compress(text.encode("utf-8"), mtime=0))


def _write_tar_archive(path, members):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        for name, text in members.items():
            payload = text.encode("utf-8")
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
    Path(path).write_bytes(gzip.compress(buffer.getvalue(), mtime=0))


def _write_archive(path, kind, text, member_name="member.txt"):
    if kind == "gzip":
        _write_gzip_archive(path, text)
    else:
        _write_tar_archive(path, {member_name: text})


def _read_extracted(path):
    path = Path(path)
    if path.is_dir():
        files = sorted(child for child in path.rglob("*") if child.is_file())
        return {child.name: child.read_text(encoding="utf-8") for child in files}
    return path.read_text(encoding="utf-8")


def _set_mtime_ns(path, mtime_ns):
    os.utime(path, ns=(os.stat(path).st_atime_ns, mtime_ns))
    return os.stat(path).st_mtime_ns


@pytest.mark.parametrize("kind", ["gzip", "tar"])
def test_extract_manager_reuses_unchanged_archive(kind, tmp_path):
    archive = tmp_path / ("archive.gz" if kind == "gzip" else "archive.tar.gz")
    _write_archive(archive, kind, ORIGINAL_TEXT)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    with patch.object(Extractor, "extract", wraps=Extractor.extract) as extract:
        first = manager.extract(str(archive))
        second = manager.extract(str(archive))
    assert extract.call_count == 1
    assert first == second
    expected = ORIGINAL_TEXT if kind == "gzip" else {"member.txt": ORIGINAL_TEXT}
    assert _read_extracted(first) == expected


@pytest.mark.parametrize("kind", ["gzip", "tar"])
def test_extract_manager_returns_fresh_content_after_source_replacement(kind, tmp_path):
    archive = tmp_path / ("archive.gz" if kind == "gzip" else "archive.tar.gz")
    _write_archive(archive, kind, ORIGINAL_TEXT)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    first = manager.extract(str(archive))
    before = os.stat(archive)
    _write_archive(archive, kind, REPLACEMENT_TEXT)
    applied_mtime = _set_mtime_ns(archive, before.st_mtime_ns + 2_000_000_000)
    after = os.stat(archive)
    assert after.st_size != before.st_size
    assert after.st_mtime_ns == applied_mtime != before.st_mtime_ns
    rewritten = manager.extract(str(archive))
    expected_original = ORIGINAL_TEXT if kind == "gzip" else {"member.txt": ORIGINAL_TEXT}
    expected_replacement = REPLACEMENT_TEXT if kind == "gzip" else {"member.txt": REPLACEMENT_TEXT}
    assert rewritten != first
    assert _read_extracted(rewritten) == expected_replacement
    assert Path(first).exists()
    assert _read_extracted(first) == expected_original


def test_extract_manager_invalidates_size_only_change_with_preserved_mtime(tmp_path):
    archive = tmp_path / "archive.gz"
    _write_gzip_archive(archive, ORIGINAL_TEXT)
    _set_mtime_ns(archive, 1_700_000_000_000_000_000)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    first = manager.extract(str(archive))
    before = os.stat(archive)
    _write_gzip_archive(archive, REPLACEMENT_TEXT)
    applied_mtime = _set_mtime_ns(archive, before.st_mtime_ns)
    after = os.stat(archive)
    assert after.st_size != before.st_size
    assert after.st_mtime_ns == applied_mtime == before.st_mtime_ns
    rewritten = manager.extract(str(archive))
    assert rewritten != first
    assert _read_extracted(rewritten) == REPLACEMENT_TEXT
    assert _read_extracted(first) == ORIGINAL_TEXT


def test_extract_manager_invalidates_same_size_change_with_subsecond_mtime(tmp_path):
    archive = tmp_path / "archive.gz"
    original_bytes = gzip.compress(SAME_SIZE_A.encode("utf-8"), mtime=0)
    replacement_bytes = gzip.compress(SAME_SIZE_B.encode("utf-8"), mtime=0)
    assert len(original_bytes) == len(replacement_bytes)
    archive.write_bytes(original_bytes)
    _set_mtime_ns(archive, 1_700_000_000_000_000_000)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    first = manager.extract(str(archive))
    before = os.stat(archive)
    archive.write_bytes(replacement_bytes)
    requested_mtime = before.st_mtime_ns + 100
    applied_mtime = _set_mtime_ns(archive, requested_mtime)
    after = os.stat(archive)
    assert after.st_size == before.st_size
    if applied_mtime == before.st_mtime_ns:
        pytest.skip("filesystem cannot represent a 100ns mtime increment")
    assert after.st_mtime_ns == applied_mtime != before.st_mtime_ns
    rewritten = manager.extract(str(archive))
    assert rewritten != first
    assert _read_extracted(rewritten) == SAME_SIZE_B
    assert _read_extracted(first) == SAME_SIZE_A


def test_extract_manager_output_path_uses_nanosecond_mtime(tmp_path):
    archive = tmp_path / "archive.gz"
    _write_gzip_archive(archive, ORIGINAL_TEXT)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    size = os.stat(archive).st_size
    mtime_ns = 1_700_000_000_000_000_000
    with patch("datasets.utils.extract.os.stat") as mocked_stat:
        mocked_stat.return_value = type("StatResult", (), {"st_size": size, "st_mtime_ns": mtime_ns})()
        first = manager._get_output_path(str(archive))
        mocked_stat.return_value = type("StatResult", (), {"st_size": size, "st_mtime_ns": mtime_ns + 1})()
        second = manager._get_output_path(str(archive))
    assert first != second
    assert "." not in Path(first).name
    assert "." not in Path(second).name


def test_extract_manager_ignores_and_preserves_legacy_path_only_output(tmp_path):
    gzip_archive = tmp_path / "archive.gz"
    tar_archive = tmp_path / "archive.tar.gz"
    _write_gzip_archive(gzip_archive, ORIGINAL_TEXT)
    _write_tar_archive(tar_archive, {"train.jsonl": ORIGINAL_TEXT, "remove.jsonl": "removed-member\n"})
    gzip_manager = ExtractManager(cache_dir=str(tmp_path / "cache-gzip"))
    tar_manager = ExtractManager(cache_dir=str(tmp_path / "cache-tar"))

    gzip_legacy = Path(gzip_manager.extract_dir) / hash_url_to_filename(os.path.abspath(gzip_archive))
    gzip_legacy.parent.mkdir(parents=True, exist_ok=True)
    gzip_legacy.write_text(STALE_LEGACY_TEXT, encoding="utf-8")
    gzip_output = gzip_manager.extract(str(gzip_archive))
    assert gzip_output != str(gzip_legacy)
    assert _read_extracted(gzip_output) == ORIGINAL_TEXT
    assert gzip_legacy.read_text(encoding="utf-8") == STALE_LEGACY_TEXT

    tar_legacy = Path(tar_manager.extract_dir) / hash_url_to_filename(os.path.abspath(tar_archive))
    tar_legacy.mkdir(parents=True)
    (tar_legacy / "stale.jsonl").write_text(STALE_LEGACY_TEXT, encoding="utf-8")
    tar_output = tar_manager.extract(str(tar_archive))
    assert tar_output != str(tar_legacy)
    assert _read_extracted(tar_output) == {"train.jsonl": ORIGINAL_TEXT, "remove.jsonl": "removed-member\n"}
    assert (tar_legacy / "stale.jsonl").read_text(encoding="utf-8") == STALE_LEGACY_TEXT


def test_extract_manager_versioned_cache_hit_does_not_extract_or_mkdir(tmp_path):
    archive = tmp_path / "archive.gz"
    _write_gzip_archive(archive, ORIGINAL_TEXT)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    first = manager.extract(str(archive))
    with patch.object(Extractor, "extract", side_effect=AssertionError("cache hit attempted extraction")):
        with patch("datasets.utils.extract.os.makedirs", side_effect=AssertionError("cache hit attempted mkdir")):
            second = manager.extract(str(archive))
            assert second == first
            assert manager.extract(archive) == first
    assert _read_extracted(first) == ORIGINAL_TEXT


def test_extract_manager_force_extract_reextracts_existing_output(tmp_path):
    archive = tmp_path / "archive.gz"
    _write_gzip_archive(archive, ORIGINAL_TEXT)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    first = manager.extract(str(archive))
    with patch.object(Extractor, "extract", wraps=Extractor.extract) as extract:
        forced = manager.extract(str(archive), force_extract=True)
    assert extract.call_count == 1
    assert forced == first
    assert _read_extracted(forced) == ORIGINAL_TEXT


def test_extract_manager_output_path_propagates_missing_source(tmp_path):
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    with pytest.raises(OSError):
        manager._get_output_path(str(tmp_path / "missing.gz"))
