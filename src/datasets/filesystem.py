# from s3fs import S3FileSystem


class extend_docstring:
    def __init__(self, method):
        self.doc = method.__doc__

    def __call__(self, function):
        if self.doc is not None:
            doc = function.__doc__
            function.__doc__ = self.doc
            if doc is not None:
                function.__doc__ += doc
        return function


import s3fs

#  @extend_docstring(s3fs.S3FileSystem)
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

      Loading dataset from s3 using ``S3Filesystem`` and ``load_from_disk()``.

      >>> from datasets import S3Filesystem, load_from_disk
      >>>
      >>> s3 = datasets.S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>>
      >>> dataset = load_from_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP
      >>>
      >>> print(len(dataset))
      25000


    """

    __doc__ = s3fs.S3FileSystem.__doc__.split("Examples")[0] + __doc__

    pass
