import s3fs


class S3FileSystem(s3fs.S3FileSystem):
    """
    ``datasets.filesystems.S3FileSystem`` is a subclass of `s3fs.S3FileSystem <https://s3fs.readthedocs.io/en/latest/api.html>`_, which is a known
    implementation of ``fsspec``. `Filesystem Spec (FSSPEC) <https://filesystem-spec.readthedocs.io/en/latest/?badge=latest>`_  is a project to
    unify various projects and classes to work with remote filesystems
    and file-system-like abstractions using a standard pythonic interface.

    Examples:
      Listing files from public s3 bucket.

      >>> import datasets
      >>> s3 = datasets.filesystems.S3FileSystem(anon=True)  # doctest: +SKIP
      >>> s3.ls('public-datasets/imdb/train')  # doctest: +SKIP
      ['dataset_info.json.json','dataset.arrow','state.json']

      Listing files from private s3 bucket using ``aws_access_key_id`` and ``aws_secret_access_key``.

      >>> import datasets
      >>> s3 = datasets.filesystems.S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>> s3.ls('my-private-datasets/imdb/train')  # doctest: +SKIP
      ['dataset_info.json.json','dataset.arrow','state.json']

      Using ``S3Filesystem`` with ``botocore.session.Session`` and custom ``aws_profile``.

      >>> import botocore
      >>> from datasets.filesystems import S3Filesystem
      >>> s3_session = botocore.session.Session(profile_name='my_profile_name')
      >>>
      >>> s3 = S3FileSystem(session=s3_session)  # doctest: +SKIP


      Loading dataset from s3 using ``S3Filesystem`` and ``load_from_disk()``.

      >>> from datasets import load_from_disk
      >>> from datasets.filesystems import S3Filesystem
      >>>
      >>> s3 = S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>>
      >>> dataset = load_from_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP
      >>>
      >>> print(len(dataset))
      25000

      Saving dataset to s3 using ``S3Filesystem`` and ``dataset.save_to_disk()``.

      >>> from datasets import load_dataset
      >>> from datasets.filesystems import S3Filesystem
      >>>
      >>> dataset = load_dataset("imdb")
      >>>
      >>> s3 = S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>>
      >>> dataset.save_to_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP



    """

    __doc__ = s3fs.S3FileSystem.__doc__.split("Examples")[0] + __doc__

    pass
