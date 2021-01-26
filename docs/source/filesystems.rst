FileSystems Integration for cloud storages
====================================================================

Supported Filesystems
---------------------

Currenlty ``datasets`` offers an s3 filesystem implementation with :class:`datasets.filesystems.S3FileSystem`. ``S3FileSystem`` is a subclass of `s3fs.S3FileSystem <https://s3fs.readthedocs.io/en/latest/api.html>`_, which is a known implementation of ``fsspec``.

Furthermore ``datasets`` supports all ``fsspec`` implementations. Currently Known Implementations these are: 

- `s3fs <https://s3fs.readthedocs.io/en/latest/>`_  for Amazon S3 and other compatible stores
- `gcsfs <https://gcsfs.readthedocs.io/en/latest/>`_ for Google Cloud Storage
- `adl <https://github.com/dask/adlfs>`_ for Azure DataLake storage
- `abfs <https://github.com/dask/adlfs>`_ for Azure Blob service
- `dropbox <https://github.com/MarineChap/dropboxdrivefs>`_ for access to dropbox shares
- `gdrive <https://github.com/intake/gdrivefs>`_ to access Google Drive and shares (experimental)

These know implementations are going to be natively added in the near future within ``datasets``.

**Examples:**	

Example using :class:`datasets.filesystems.S3FileSystem` within ``datasets``.


.. code-block::

    >>> pip install datasets[s3]

Listing files from public s3 bucket.

.. code-block::

      >>> import datasets
      >>> s3 = datasets.filesystems.S3FileSystem(anon=True)  # doctest: +SKIP
      >>> s3.ls('public-datasets/imdb/train')  # doctest: +SKIP
      ['dataset_info.json.json','dataset.arrow','state.json']

Listing files from private s3 bucket using ``aws_access_key_id`` and ``aws_secret_access_key``.

.. code-block::

      >>> import datasets
      >>> s3 = datasets.filesystems.S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>> s3.ls('my-private-datasets/imdb/train')  # doctest: +SKIP
      ['dataset_info.json.json','dataset.arrow','state.json']

Using ``S3Filesystem`` with ``botocore.session.Session`` and custom ``aws_profile``.

.. code-block::

      >>> import botocore 
      >>> from datasets.filesystems import S3Filesystem
      >>> s3_session = botocore.session.Session(profile_name='my_profile_name')
      >>>
      >>> s3 = S3FileSystem(session=s3_session)  # doctest: +SKIP



Saving a processed dataset to s3
--------------------------------

Once you have your final dataset you can save it to s3 and reuse it later using :obj:`datasets.load_from_disk`.
Saving a dataset to s3 will upload various files to your bucket:

- ``arrow files.arrow``: they contain your dataset's data
- ``dataset_info.json``: contains the description, citations, etc. of the dataset
- ``state.json``: contains the list of the arrow files and other informations like the dataset format type, if any (torch or tensorflow for example)

Saving ``encoded_dataset`` to a private s3 bucket using ``aws_access_key_id`` and ``aws_secret_access_key``.

.. code-block::

      >>> from datasets.filesystems import S3FileSystem
      >>>
      >>> # create S3FileSystem instance with aws_access_key_id and aws_secret_access_key
      >>> s3 = S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>>
      >>> # saves encoded_dataset to your s3 bucket
      >>> encoded_dataset.save_to_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP

Saving ``encoded_dataset`` to a private s3 bucket using ``botocore.session.Session`` and custom ``aws_profile``.

.. code-block::

      >>> import botocore 
      >>> from datasets.filesystems import S3Filesystem
      >>>
      >>> # creates a botocore session with the provided aws_profile
      >>> s3_session = botocore.session.Session(profile_name='my_profile_name')
      >>>
      >>> # create S3FileSystem instance with s3_session
      >>> s3 = S3FileSystem(sessions=s3_session)  # doctest: +SKIP
      >>>
      >>> # saves encoded_dataset to your s3 bucket
      >>> encoded_dataset.save_to_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP


Loading a processed dataset from s3
-----------------------------------

After you have saved your processed dataset to s3 you can load it using :obj:`datasets.load_from_disk`.
You can only load datasets from s3, which are saved using :func:`datasets.Dataset.save_to_disk` 
and :func:`datasets.DatasetDict.save_to_disk`. 

Loading ``encoded_dataset`` from a public s3 bucket.

.. code-block::

      >>> from datasets import load_from_disk
      >>> from datasets.filesystems import S3Filesystem
      >>>
      >>> # create S3FileSystem without credentials
      >>> s3 = S3FileSystem(anon=True)  # doctest: +SKIP
      >>>
      >>> # load encoded_dataset to from s3 bucket
      >>> dataset = load_from_disk('s3://a-public-datasets/imdb/train',fs=s3)  # doctest: +SKIP
      >>>
      >>> print(len(dataset))
      >>> # 25000

Loading ``encoded_dataset`` from a private s3 bucket using ``aws_access_key_id`` and ``aws_secret_access_key``.

.. code-block::

      >>> from datasets import load_from_disk
      >>> from datasets.filesystems import S3Filesystem
      >>>
      >>> # create S3FileSystem instance with aws_access_key_id and aws_secret_access_key
      >>> s3 = S3FileSystem(key=aws_access_key_id, secret=aws_secret_access_key)  # doctest: +SKIP
      >>>
      >>> # load encoded_dataset to from s3 bucket
      >>> dataset = load_from_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP
      >>>
      >>> print(len(dataset))
      >>> # 25000

Loading ``encoded_dataset`` from a private s3 bucket using ``botocore.session.Session`` and custom ``aws_profile``.

.. code-block::

      >>> import botocore
      >>> from datasets.filesystems import S3Filesystem
      >>>
      >>> # create S3FileSystem instance with aws_access_key_id and aws_secret_access_key
      >>> s3_session = botocore.session.Session(profile_name='my_profile_name')
      >>>
      >>> # create S3FileSystem instance with s3_session
      >>> s3 = S3FileSystem(sessions=s3_session)  
      >>>
      >>> # load encoded_dataset to from s3 bucket
      >>> dataset = load_from_disk('s3://my-private-datasets/imdb/train',fs=s3)  # doctest: +SKIP
      >>>
      >>> print(len(dataset))
      >>> # 25000
