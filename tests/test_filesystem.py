import os

import boto3
import fsspec
import pytest
from moto import mock_s3

from datasets.filesystem import S3FileSystem, is_remote_filesystem, preproc_dataset_path


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


@mock_s3
def test_preproc_dataset_path(s3):

    mock_bucket = "moto-mock-s3-bucket"
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    s3.create_bucket(Bucket=mock_bucket)

    dataset_path = f"s3://{mock_bucket}"

    dataset_path = preproc_dataset_path(dataset_path)
    assert dataset_path.startswith("s3://") is False

    dataset_path = f"./local/path"
    new_dataset_path = preproc_dataset_path(dataset_path)
    assert dataset_path == new_dataset_path


@mock_s3
def test_is_remote_filesystem():

    fs = S3FileSystem(key="fake_access_key", secret="fake_secret")

    is_remote = is_remote_filesystem(fs)
    assert is_remote is True

    fs = fsspec.filesystem("file")

    is_remote = is_remote_filesystem(fs)
    assert is_remote is False
