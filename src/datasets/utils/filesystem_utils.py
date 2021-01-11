import boto3
import fsspec


def get_filesystem_from_dataset_path(
    dataset_path: str, aws_profile="default", aws_access_key_id=None, aws_secret_access_key=None, anon=False
):
    """
    identifies the filesystem from dataset path and returns an `fsspec` instance of together with the adjusted `dataset_path` (e.g. removing `s3://`)

    Args:
        dataset_path (``str``): path or s3 uri of the dataset directory where the dataset will be saved to
        aws_profile (:obj:`str`,  `optional`, defaults to :obj:``default``): the aws profile used to create the `boto_session` for uploading the data to s3
        aws_access_key_id (:obj:`str`,  `optional`, defaults to :obj:``None``): the aws access key id used to create the `boto_session` for uploading the data to s3
        aws_secret_access_key (:obj:`str`,  `optional`, defaults to :obj:``None``): the aws secret access key used to create the `boto_session` for uploading the data to s3
        anon (:obj:`boolean`,  `optional`, defaults to :obj:``False``): The connection can be anonymous - in which case only publicly-available, read-only buckets are accessible, for anonymous connection use `anon=True`
    """
    # checks if dataset_path is s3 uri
    if is_remote_filesystem(dataset_path):
        dataset_path = dataset_path.replace("s3://", "")
        if aws_secret_access_key is not None and aws_secret_access_key is not None:
            fs = fsspec.filesystem("s3", anon=False, key=aws_access_key_id, secret=aws_secret_access_key)
        elif anon == True:
            # The connection can be anonymous - in which case only publicly-available, read-only buckets are accessible
            fs = fsspec.filesystem("s3", anon=True)
        else:
            from boto3 import Session

            # Credentials are refreshable, so accessing your access key / secret key
            # separately can lead to a race condition. Use this to get an actual matched
            # set.
            credentials = Session(profile_name=aws_profile).get_credentials().get_frozen_credentials()
            fs = fsspec.filesystem("s3", anon=False, key=credentials.access_key, secret=credentials.secret_key)

    else:
        fs = fsspec.filesystem("file")
    return fs, dataset_path


def is_remote_filesystem(dataset_path: str) -> bool:
    """
    Checks if filesystem is remote filesystem

    Args:
        dataset_path (``str``): path or s3 uri of the dataset directory where the dataset will be saved to
    """
    if dataset_path.startswith("s3://"):
        return True
    else:
        return False
