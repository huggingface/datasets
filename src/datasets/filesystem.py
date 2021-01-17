import fsspec
import s3fs


class S3FileSystem(s3fs.S3FileSystem):
    """
    ``datasets.S3FileSystem`` is a subclass of `s3fs.S3FileSystem <https://s3fs.readthedocs.io/en/latest/api.html>`_, which is a known
    implemenetation of ``fsspec``. `Filesystem Spec (FSSPEC) <https://filesystem-spec.readthedocs.io/en/latest/?badge=latest>`_  is a project to
    unify various projects and classes to work with remote filesystems
    and file-system-like abstractions using a standard pythonic interface.

    Examples:
      Listing files from public s3 bucket.

      >>> import datasets
      >>> s3 = datasets.S3FileSystem(anon=True)  # doctest: +SKIP
      >>> s3.ls('public-datasets/imdb/train')  # doctest: +SKIP
      ['dataset_info.json.json','dataset.arrow','state.json']

      Listing files from private s3 bucket using ``aws_access_key_id`` and ``aws_secret_access_key``.

      >>> import datasets
      >>> s3 = datasets.S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>> s3.ls('my-private-datasets/imdb/train')  # doctest: +SKIP
      ['dataset_info.json.json','dataset.arrow','state.json']

      Using ``S3Filesystem`` with ``boto3.Session`` and custom ``aws_profile``.

      >>> import boto3
      >>> from datasets import S3Filesystem
      >>> s3_session = boto3.session.Session(profile_name='my_profile_name')
      >>>
      >>> s3 = datasets.S3FileSystem(sessions=s3_session)  # doctest: +SKIP


      Loading dataset from s3 using ``S3Filesystem`` and ``load_from_disk()``.

      >>> from datasets import S3Filesystem, load_from_disk
      >>>
      >>> s3 = datasets.S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>>
      >>> dataset = load_from_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP
      >>>
      >>> print(len(dataset))
      25000

      Saving dataset to s3 using ``S3Filesystem`` and ``dataset.save_to_disk()``.

      >>> from datasets import S3Filesystem, load_dataset
      >>>
      >>> dataset = datasets.load_dataset("imdb")
      >>>
      >>> s3 = datasets.S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>>
      >>> dataset.save_to_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP



    """

    __doc__ = s3fs.S3FileSystem.__doc__.split("Examples")[0] + __doc__

    pass


def preproc_dataset_path(dataset_path: str) -> str:
    """
    preprocesses `dataset_path` and removes remote filesystem (e.g. removing ``s3://``)

    Args:
        dataset_path (``str``): path (e.g. ``dataset/train``) or remote uri (e.g. ``s3://my-bucket/dataset/train``) of the dataset directory
    """
    if "://" in dataset_path:
        dataset_path = dataset_path.split("://")[1]
    return dataset_path


def is_remote_filesystem(fs: fsspec.spec.AbstractFileSystem) -> bool:
    """
    Validates if filesystem has remote protocol.

    Args:
        fs (``fsspec.spec.AbstractFileSystem``): An abstract super-class for pythonic file-systems, e.g. :code:`fsspec.filesystem(\'file\')` or :class:`datasets.filesystem.S3FileSystem`
    """
    if fs is not None and fs.protocol != "file":
        return True
    else:
        return False
