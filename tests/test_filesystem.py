import importlib
import os

import fsspec
import pytest
from fsspec import register_implementation
from fsspec.registry import _registry as _fsspec_registry

from datasets.filesystems import COMPRESSION_FILESYSTEMS, extract_path_from_uri, is_remote_filesystem

from .utils import require_lz4, require_zstandard


def test_mockfs(mockfs):
    assert "mock" in _fsspec_registry
    assert "bz2" in _fsspec_registry


def test_non_mockfs():
    assert "mock" not in _fsspec_registry
    assert "bz2" in _fsspec_registry


def test_extract_path_from_uri():
    mock_bucket = "mock-s3-bucket"
    dataset_path = f"s3://{mock_bucket}"
    dataset_path = extract_path_from_uri(dataset_path)
    assert dataset_path.startswith("s3://") is False

    dataset_path = "./local/path"
    new_dataset_path = extract_path_from_uri(dataset_path)
    assert dataset_path == new_dataset_path


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
    assert isinstance(fs, compression_fs_class)
    expected_filename = os.path.basename(input_path)
    expected_filename = expected_filename[: expected_filename.rindex(".")]
    assert fs.glob("*") == [expected_filename]
    with fs.open(expected_filename, "r", encoding="utf-8") as f, open(text_file, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize("protocol", ["zip", "gzip"])
def test_fs_isfile(protocol, zip_jsonl_path, jsonl_gz_path):
    compressed_file_paths = {"zip": zip_jsonl_path, "gzip": jsonl_gz_path}
    compressed_file_path = compressed_file_paths[protocol]
    member_file_path = "dataset.jsonl"
    path = f"{protocol}://{member_file_path}::{compressed_file_path}"
    fs, *_ = fsspec.get_fs_token_paths(path)
    assert fs.isfile(member_file_path)
    assert not fs.isfile("non_existing_" + member_file_path)


def test_fs_overwrites():
    protocol = "bz2"

    # Import module
    import datasets.filesystems

    # Overwrite protocol and reload
    register_implementation(protocol, None, clobber=True)
    with pytest.warns(UserWarning) as warning_info:
        importlib.reload(datasets.filesystems)

    assert len(warning_info) == 1
    assert (
        str(warning_info[0].message)
        == f"A filesystem protocol was already set for {protocol} and will be overwritten."
    )
