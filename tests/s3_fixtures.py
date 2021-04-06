import json
import time

import pytest
import requests


# From: https://github.com/dask/s3fs/blob/ffe3a5293524869df56e74973af0d2c204ae9cbf/s3fs/tests/test_s3fs.py#L25-L141

s3_test_bucket_name = "test"
s3_secure_bucket_name = "test-secure"
s3_versioned_bucket_name = "test-versioned"
s3_files = {
    "test/accounts.1.json": (
        b'{"amount": 100, "name": "Alice"}\n'
        b'{"amount": 200, "name": "Bob"}\n'
        b'{"amount": 300, "name": "Charlie"}\n'
        b'{"amount": 400, "name": "Dennis"}\n'
    ),
    "test/accounts.2.json": (
        b'{"amount": 500, "name": "Alice"}\n'
        b'{"amount": 600, "name": "Bob"}\n'
        b'{"amount": 700, "name": "Charlie"}\n'
        b'{"amount": 800, "name": "Dennis"}\n'
    ),
}

s3_csv_files = {
    "2014-01-01.csv": (b"name,amount,id\n" b"Alice,100,1\n" b"Bob,200,2\n" b"Charlie,300,3\n"),
    "2014-01-02.csv": (b"name,amount,id\n"),
    "2014-01-03.csv": (b"name,amount,id\n" b"Dennis,400,4\n" b"Edith,500,5\n" b"Frank,600,6\n"),
}
s3_text_files = {
    "nested/file1": b"hello\n",
    "nested/file2": b"world",
    "nested/nested2/file1": b"hello\n",
    "nested/nested2/file2": b"world",
}
s3_glob_files = {"file.dat": b"", "filexdat": b""}
s3_a = s3_test_bucket_name + "/tmp/test/a"
s3_b = s3_test_bucket_name + "/tmp/test/b"
s3_c = s3_test_bucket_name + "/tmp/test/c"
s3_d = s3_test_bucket_name + "/tmp/test/d"
s3_port = 5555
s3_endpoint_uri = "http://127.0.0.1:%s/" % s3_port


@pytest.fixture()
def s3_base():
    # writable local S3 system
    import shlex
    import subprocess

    proc = subprocess.Popen(shlex.split("moto_server s3 -p %s" % s3_port))

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


def get_boto3_client():
    from botocore.session import Session

    # NB: we use the sync botocore client for setup
    session = Session()
    return session.create_client("s3", endpoint_url=s3_endpoint_uri)


@pytest.fixture()
def s3(s3_base):
    client = get_boto3_client()
    client.create_bucket(Bucket=s3_test_bucket_name, ACL="public-read")

    client.create_bucket(Bucket=s3_versioned_bucket_name, ACL="public-read")
    client.put_bucket_versioning(Bucket=s3_versioned_bucket_name, VersioningConfiguration={"Status": "Enabled"})

    # initialize secure bucket
    client.create_bucket(Bucket=s3_secure_bucket_name, ACL="public-read")
    policy = json.dumps(
        {
            "Version": "2012-10-17",
            "Id": "PutObjPolicy",
            "Statement": [
                {
                    "Sid": "DenyUnEncryptedObjectUploads",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::{bucket_name}/*".format(bucket_name=s3_secure_bucket_name),
                    "Condition": {"StringNotEquals": {"s3:x-amz-server-side-encryption": "aws:kms"}},
                }
            ],
        }
    )
    client.put_bucket_policy(Bucket=s3_secure_bucket_name, Policy=policy)
    for flist in [s3_files, s3_csv_files, s3_text_files, s3_glob_files]:
        for f, data in flist.items():
            client.put_object(Bucket=s3_test_bucket_name, Key=f, Body=data)

    from s3fs.core import S3FileSystem

    S3FileSystem.clear_instance_cache()
    s3 = S3FileSystem(anon=False, client_kwargs={"endpoint_url": s3_endpoint_uri})
    s3.invalidate_cache()
    yield s3
