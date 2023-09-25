import os
import zipfile

import pytest

from datasets.utils.extract import (
    Bzip2Extractor,
    Extractor,
    GzipExtractor,
    Lz4Extractor,
    SevenZipExtractor,
    TarExtractor,
    XzExtractor,
    ZipExtractor,
    ZstdExtractor,
)

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


@pytest.mark.parametrize(
    "insecure_tar_file, error_log",
    [("tar_file_with_dot_dot", "illegal path"), ("tar_file_with_sym_link", "Symlink")],
)
def test_tar_extract_insecure_files(
    insecure_tar_file, error_log, tar_file_with_dot_dot, tar_file_with_sym_link, tmp_path, caplog
):
    insecure_tar_files = {
        "tar_file_with_dot_dot": tar_file_with_dot_dot,
        "tar_file_with_sym_link": tar_file_with_sym_link,
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
    assert zipfile.is_zipfile(str(not_a_zip_file))  # is a false positive for `zipfile`
    assert not ZipExtractor.is_extractable(not_a_zip_file)  # but we're right
