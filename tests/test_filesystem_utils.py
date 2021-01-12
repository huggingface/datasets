import os

import boto3
import pytest
from moto import mock_s3

from datasets.utils import get_filesystem_from_dataset_path, is_remote_filesystem


@mock_s3
def test_get_filesystem_from_dataset_path():
    # Mocked AWS Credentials for moto.
    os.environ["AWS_ACCESS_KEY_ID"] = "fake_access_key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_secret_key"
    os.environ["AWS_SECURITY_TOKEN"] = "fake_secrurity_token"
    os.environ["AWS_SESSION_TOKEN"] = "fake_session_token"

    s3 = boto3.client("s3", region_name="us-east-1")
    mock_bucket = "moto-mock-s3-bucket"
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    s3.create_bucket(Bucket=mock_bucket)

    dataset_path = f"s3://{mock_bucket}"
    fs, dataset_path = get_filesystem_from_dataset_path(
        dataset_path, aws_access_key_id="fake_access_key", aws_secret_access_key="fake_secret_key"
    )
    assert "s3" in fs.protocol
    assert dataset_path.startswith("s3://") == False

    dataset_path = f"./local/path"
    fs, new_dataset_path = get_filesystem_from_dataset_path(
        dataset_path, aws_access_key_id="fake_access_key", aws_secret_access_key="fake_secret_key"
    )
    assert not "s3" in fs.protocol
    assert dataset_path == new_dataset_path


@mock_s3
def test_is_remote_filesystem():
    dataset_path = f"s3://moto-mock-s3-bucket"
    is_remote = is_remote_filesystem(dataset_path)
    assert is_remote == True

    dataset_path = f"./local/path"
    is_remote = is_remote_filesystem(dataset_path)
    assert is_remote == False
