import os
from pathlib import Path
from unittest.mock import patch

import pytest
import zstandard as zstd

from datasets.download.download_config import DownloadConfig
from datasets.utils.file_utils import (
    OfflineModeIsEnabled,
    cached_path,
    fsspec_get,
    fsspec_head,
    ftp_get,
    ftp_head,
    get_from_cache,
    http_get,
    http_head,
)


FILE_CONTENT = """\
    Text data.
    Second line of data."""

FILE_PATH = "file"


@pytest.fixture(scope="session")
def zstd_path(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / (FILE_PATH + ".zstd")
    data = bytes(FILE_CONTENT, "utf-8")
    with zstd.open(path, "wb") as f:
        f.write(data)
    return path


@pytest.fixture
def tmpfs_file(tmpfs):
    with open(os.path.join(tmpfs.local_root_dir, FILE_PATH), "w") as f:
        f.write(FILE_CONTENT)
    return FILE_PATH


@pytest.mark.parametrize("compression_format", ["gzip", "xz", "zstd"])
def test_cached_path_extract(compression_format, gz_file, xz_file, zstd_path, tmp_path, text_file):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_path}
    input_path = input_paths[compression_format]
    cache_dir = tmp_path / "cache"
    download_config = DownloadConfig(cache_dir=cache_dir, extract_compressed_file=True)
    extracted_path = cached_path(input_path, download_config=download_config)
    with open(extracted_path) as f:
        extracted_file_content = f.read()
    with open(text_file) as f:
        expected_file_content = f.read()
    assert extracted_file_content == expected_file_content


@pytest.mark.parametrize("default_extracted", [True, False])
@pytest.mark.parametrize("default_cache_dir", [True, False])
def test_extracted_datasets_path(default_extracted, default_cache_dir, xz_file, tmp_path, monkeypatch):
    custom_cache_dir = "custom_cache"
    custom_extracted_dir = "custom_extracted_dir"
    custom_extracted_path = tmp_path / "custom_extracted_path"
    if default_extracted:
        expected = ("downloads" if default_cache_dir else custom_cache_dir, "extracted")
    else:
        monkeypatch.setattr("datasets.config.EXTRACTED_DATASETS_DIR", custom_extracted_dir)
        monkeypatch.setattr("datasets.config.EXTRACTED_DATASETS_PATH", str(custom_extracted_path))
        expected = custom_extracted_path.parts[-2:] if default_cache_dir else (custom_cache_dir, custom_extracted_dir)

    filename = xz_file
    download_config = (
        DownloadConfig(extract_compressed_file=True)
        if default_cache_dir
        else DownloadConfig(cache_dir=tmp_path / custom_cache_dir, extract_compressed_file=True)
    )
    extracted_file_path = cached_path(filename, download_config=download_config)
    assert Path(extracted_file_path).parent.parts[-2:] == expected


def test_cached_path_local(text_file):
    # absolute path
    text_file = str(Path(text_file).resolve())
    assert cached_path(text_file) == text_file
    # relative path
    text_file = str(Path(__file__).resolve().relative_to(Path(os.getcwd())))
    assert cached_path(text_file) == text_file


def test_cached_path_missing_local(tmp_path):
    # absolute path
    missing_file = str(tmp_path.resolve() / "__missing_file__.txt")
    with pytest.raises(FileNotFoundError):
        cached_path(missing_file)
    # relative path
    missing_file = "./__missing_file__.txt"
    with pytest.raises(FileNotFoundError):
        cached_path(missing_file)


def test_get_from_cache_fsspec(tmpfs_file):
    output_path = get_from_cache(f"tmp://{tmpfs_file}")
    with open(output_path) as f:
        output_file_content = f.read()
    assert output_file_content == FILE_CONTENT


@patch("datasets.config.HF_DATASETS_OFFLINE", True)
def test_cached_path_offline():
    with pytest.raises(OfflineModeIsEnabled):
        cached_path("https://huggingface.co")


@patch("datasets.config.HF_DATASETS_OFFLINE", True)
def test_http_offline(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.html"
    with pytest.raises(OfflineModeIsEnabled):
        http_get("https://huggingface.co", temp_file=filename)
    with pytest.raises(OfflineModeIsEnabled):
        http_head("https://huggingface.co")


@patch("datasets.config.HF_DATASETS_OFFLINE", True)
def test_ftp_offline(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.html"
    with pytest.raises(OfflineModeIsEnabled):
        ftp_get("ftp://huggingface.co", temp_file=filename)
    with pytest.raises(OfflineModeIsEnabled):
        ftp_head("ftp://huggingface.co")


@patch("datasets.config.HF_DATASETS_OFFLINE", True)
def test_fsspec_offline(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.html"
    with pytest.raises(OfflineModeIsEnabled):
        fsspec_get("s3://huggingface.co", temp_file=filename)
    with pytest.raises(OfflineModeIsEnabled):
        fsspec_head("s3://huggingface.co")
