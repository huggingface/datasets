import gzip
import os
from unittest.mock import patch

import fsspec
import pytest
from fsspec.core import url_to_fs
from fsspec.registry import _registry as _fsspec_registry

from datasets import load_dataset
from datasets.filesystems import COMPRESSION_FILESYSTEMS, is_remote_filesystem
from datasets.filesystems.compression import GzipFileSystem

from .fixtures.fsspec import MockFileSystem
from .utils import require_lz4, require_zstandard


def test_mockfs(mockfs):
    assert "mock" in _fsspec_registry
    assert "bz2" in _fsspec_registry


def test_non_mockfs():
    assert "mock" not in _fsspec_registry
    assert "bz2" in _fsspec_registry


def test_is_remote_filesystem(mockfs):
    is_remote = is_remote_filesystem(mockfs)
    assert is_remote is True

    fs = fsspec.filesystem("file")

    is_remote = is_remote_filesystem(fs)
    assert is_remote is False


@pytest.mark.parametrize("compression_fs_class", COMPRESSION_FILESYSTEMS)
def test_compression_filesystems(compression_fs_class, gz_file, bz2_file, lz4_file, zstd_file, xz_file, text_file):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file, "bz2": bz2_file, "lz4": lz4_file}
    input_path = input_paths[compression_fs_class.protocol]
    if input_path is None:
        reason = f"for '{compression_fs_class.protocol}' compression protocol, "
        if compression_fs_class.protocol == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_fs_class.protocol == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    fs = fsspec.filesystem(compression_fs_class.protocol, fo=input_path)
    expected_filename = os.path.basename(input_path)
    expected_filename = expected_filename[: expected_filename.rindex(".")]
    assert fs.glob("*") == [expected_filename]
    with fs.open(expected_filename, "r", encoding="utf-8") as f, open(text_file, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize("client_kwargs", [None, {"region_name": "us-east-1"}])
def test_streaming_gzip_preserves_s3_client_options(tmp_path, monkeypatch, client_kwargs):
    class S3FileSystem(MockFileSystem):
        protocol = "s3"

        def __init__(self, *args, client_kwargs=None, **kwargs):
            assert client_kwargs == expected_client_kwargs
            super().__init__(*args, **kwargs)

        @classmethod
        def _strip_protocol(cls, path):
            return super()._strip_protocol(path).removeprefix("s3://")

    expected_client_kwargs = client_kwargs
    monkeypatch.setitem(_fsspec_registry, "s3", S3FileSystem)
    (tmp_path / "bucket").mkdir()
    with gzip.open(tmp_path / "bucket" / "data.jsonl.gz", "wt", encoding="utf-8") as f:
        f.write('{"id": 1}\n{"id": 2}\n')

    s3_options = {"local_root_dir": tmp_path}
    if client_kwargs is not None:
        s3_options["client_kwargs"] = client_kwargs
    dataset = load_dataset(
        "json",
        data_files="s3://bucket/data.jsonl.gz",
        streaming=True,
        split="train",
        storage_options={"s3": s3_options},
    )
    assert list(dataset) == [{"id": 1}, {"id": 2}]


@pytest.mark.parametrize(("url", "target_protocol"), [("https://example.com/data.gz", None), ("data.gz", "http")])
def test_gzip_preserves_http_client_defaults_and_overrides(url, target_protocol):
    target_options = {"client_kwargs": {"trust_env": False}}
    with patch("datasets.filesystems.compression.fsspec.open") as opener:
        fs = GzipFileSystem(fo=url, target_protocol=target_protocol, target_options=target_options)
        fs.cat("data")
        opener.assert_called_once_with(
            url,
            mode="rb",
            protocol=target_protocol,
            compression="gzip",
            client_kwargs={"requote_redirect_url": False, "trust_env": False},
        )
    assert target_options == {"client_kwargs": {"trust_env": False}}


@pytest.mark.parametrize("protocol", ["zip", "gzip"])
def test_fs_isfile(protocol, zip_jsonl_path, jsonl_gz_path):
    compressed_file_paths = {"zip": zip_jsonl_path, "gzip": jsonl_gz_path}
    compressed_file_path = compressed_file_paths[protocol]
    member_file_path = "dataset.jsonl"
    path = f"{protocol}://{member_file_path}::{compressed_file_path}"
    fs, *_ = url_to_fs(path)
    assert fs.isfile(member_file_path)
    assert not fs.isfile("non_existing_" + member_file_path)
