import os

import boto3
import fsspec
import pytest
from moto import mock_s3

from datasets.filesystems import COMPRESSION_FILESYSTEMS, S3FileSystem, extract_path_from_uri, is_remote_filesystem

from .utils import require_lz4, require_zstandard


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "fake_access_key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_secret_key"
    os.environ["AWS_SECURITY_TOKEN"] = "fake_secrurity_token"
    os.environ["AWS_SESSION_TOKEN"] = "fake_session_token"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")


def test_extract_path_from_uri(s3):

    mock_bucket = "moto-mock-s3-bucket"
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    s3.create_bucket(Bucket=mock_bucket)

    dataset_path = f"s3://{mock_bucket}"

    dataset_path = extract_path_from_uri(dataset_path)
    assert dataset_path.startswith("s3://") is False

    dataset_path = "./local/path"
    new_dataset_path = extract_path_from_uri(dataset_path)
    assert dataset_path == new_dataset_path


def test_is_remote_filesystem():

    fs = S3FileSystem(key="fake_access_key", secret="fake_secret")

    is_remote = is_remote_filesystem(fs)
    assert is_remote is True

    fs = fsspec.filesystem("file")

    is_remote = is_remote_filesystem(fs)
    assert is_remote is False


@require_zstandard
@require_lz4
@pytest.mark.parametrize("compression_fs_class", COMPRESSION_FILESYSTEMS)
def test_compression_filesystems(compression_fs_class, gz_file, bz2_file, lz4_file, zstd_file, xz_file, text_file):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file, "bz2": bz2_file, "lz4": lz4_file}
    input_path = str(input_paths[compression_fs_class.protocol])
    fs = fsspec.filesystem(compression_fs_class.protocol, fo=input_path)
    assert isinstance(fs, compression_fs_class)
    expected_filename = os.path.basename(input_path)
    expected_filename = expected_filename[: expected_filename.rindex(".")]
    assert fs.ls("/") == [expected_filename]
    with fs.open(expected_filename, "r", encoding="utf-8") as f, open(text_file, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()
