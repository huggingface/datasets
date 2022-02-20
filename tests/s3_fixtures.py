import os
import time

import pytest
import requests


# From: https://github.com/dask/s3fs/blob/ffe3a5293524869df56e74973af0d2c204ae9cbf/s3fs/tests/test_s3fs.py#L25-L141

s3_test_bucket_name = "test"
s3_port = 5555
s3_endpoint_uri = f"http://127.0.0.1:{s3_port}/"

S3_FAKE_ENV_VARS = {
    "AWS_ACCESS_KEY_ID": "fake_access_key",
    "AWS_SECRET_ACCESS_KEY": "fake_secret_key",
    "AWS_SECURITY_TOKEN": "fake_secrurity_token",
    "AWS_SESSION_TOKEN": "fake_session_token",
}


@pytest.fixture()
def s3_base():
    # writable local S3 system
    import shlex
    import subprocess

    # Mocked AWS Credentials for moto.
    old_environ = os.environ.copy()
    os.environ.update(S3_FAKE_ENV_VARS)

    proc = subprocess.Popen(shlex.split(f"moto_server s3 -p {s3_port}"))

    timeout = 5
    while timeout > 0:
        try:
            r = requests.get(s3_endpoint_uri)
            if r.ok:
                break
        except:  # noqa
            pass
        timeout -= 0.1
        time.sleep(0.1)
    yield
    proc.terminate()
    proc.wait()
    os.environ.clear()
    os.environ.update(old_environ)


def get_boto3_client():
    from botocore.session import Session

    # NB: we use the sync botocore client for setup
    session = Session()
    return session.create_client("s3", endpoint_url=s3_endpoint_uri)


@pytest.fixture()
def s3(s3_base):
    client = get_boto3_client()
    client.create_bucket(Bucket=s3_test_bucket_name, ACL="public-read")

    from s3fs.core import S3FileSystem

    S3FileSystem.clear_instance_cache()
    s3 = S3FileSystem(anon=False, client_kwargs={"endpoint_url": s3_endpoint_uri})
    s3.invalidate_cache()
    yield s3
