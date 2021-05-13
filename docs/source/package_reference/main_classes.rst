Main classes
----------------------------------------------------


``DatasetInfo``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: datasets.DatasetInfo
    :members:

``Dataset``
~~~~~~~~~~~~~~~~~~~~~

The base class :class:`datasets.Dataset` implements a Dataset backed by an Apache Arrow table.

.. autoclass:: datasets.Dataset
    :members:
        add_column, add_item,
        from_file, from_buffer, from_pandas, from_dict,
        data, cache_files, num_columns, num_rows, column_names, shape,
        unique,
        flatten_, cast_, remove_columns_, rename_column_,
        flatten, cast, remove_columns, rename_column, class_encode_column,
        __len__, __iter__, formatted_as, set_format, set_transform, reset_format, with_format, with_transform,
        __getitem__, cleanup_cache_files,
        map, filter, select, sort, shuffle, train_test_split, shard, export,
        save_to_disk, load_from_disk, flatten_indices,
        to_csv, to_pandas, to_dict,
        add_faiss_index, add_faiss_index_from_external_arrays, save_faiss_index, load_faiss_index,
        add_elasticsearch_index, load_elasticsearch_index,
        list_indexes, get_index, drop_index, search, search_batch, get_nearest_examples, get_nearest_examples_batch,
        info, split, builder_name, citation, config_name, dataset_size,
        description, download_checksums, download_size, features, homepage,
        license, size_in_bytes, supervised_keys, version,
        from_csv, from_json, from_text,

.. autofunction:: datasets.concatenate_datasets

.. autofunction:: datasets.set_caching_enabled

.. autofunction:: datasets.is_caching_enabled

``DatasetDict``
~~~~~~~~~~~~~~~~~~~~~

Dictionary with split names as keys ('train', 'test' for example), and :obj:`datasets.Dataset` objects as values.
It also has dataset transform methods like map or filter, to process all the splits at once.

.. autoclass:: datasets.DatasetDict
    :members: data, cache_files, num_columns, num_rows, column_names, shape,
        unique,
        cleanup_cache_files,
        map, filter, sort, shuffle, set_format, reset_format, formatted_as, with_format, with_transform,
        flatten_, cast_, remove_columns_, rename_column_,
        flatten, cast, remove_columns, rename_column, class_encode_column,
        save_to_disk, load_from_disk,
        from_csv, from_json, from_text,


``Features``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: datasets.Features
    :members:

.. autoclass:: datasets.Sequence
    :members:

.. autoclass:: datasets.ClassLabel
    :members:

.. autoclass:: datasets.Value
    :members:

.. autoclass:: datasets.Translation
    :members:

.. autoclass:: datasets.TranslationVariableLanguages
    :members:

.. autoclass:: datasets.Array2D
    :members:

.. autoclass:: datasets.Array3D
    :members:

.. autoclass:: datasets.Array4D
    :members:

.. autoclass:: datasets.Array5D
    :members:

``MetricInfo``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: datasets.MetricInfo
    :members:

``Metric``
~~~~~~~~~~~~~~~~~~~~~

The base class ``Metric`` implements a Metric backed by one or several :class:`datasets.Dataset`.

.. autoclass:: datasets.Metric
    :members:


``Filesystems``
~~~~~~~~~~~~~~~~~~~~~


.. autoclass:: datasets.filesystems.S3FileSystem(anon=False, key=None, secret=None, token=None, use_ssl=True, client_kwargs=None, requester_pays=False, default_block_size=None, default_fill_cache=True, default_cache_type='bytes', version_aware=False, config_kwargs=None, s3_additional_kwargs=None, session=None, username=None, password=None, asynchronous=False, loop=None, **kwargs)

.. autofunction:: datasets.filesystems.extract_path_from_uri

.. autofunction:: datasets.filesystems.is_remote_filesystem
