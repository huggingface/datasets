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
    :members: from_file, from_buffer, from_pandas, from_dict,
        data, cache_files, num_columns, num_rows, column_names, shape,
        unique, flatten_,
        cast_, remove_columns_, rename_column_,
        __len__, __iter__, formatted_as, set_format, reset_format,
        __getitem__, cleanup_cache_files,
        map, filter, select, sort, shuffle, train_test_split, shard, export,
        save_to_disk, load_from_disk, flatten_indices,
        add_faiss_index, add_faiss_index_from_external_arrays, save_faiss_index, load_faiss_index,
        add_elasticsearch_index, load_elasticsearch_index,
        list_indexes, get_index, drop_index, search, search_batch, get_nearest_examples, get_nearest_examples_batch,
        info, split, builder_name, citation, config_name, dataset_size,
        description, download_checksums, download_size, features, homepage,
        license, size_in_bytes, supervised_keys, version

.. autofunction:: datasets.concatenate_datasets

``DatasetDict``
~~~~~~~~~~~~~~~~~~~~~

Dictionary with split names as keys ('train', 'test' for example), and :obj:`datasets.Dataset` objects as values.
It also has dataset transform methods like map or filter, to process all the splits at once.

.. autoclass:: datasets.DatasetDict
    :members: data, cache_files, num_columns, num_rows, column_names, shape,
        unique, flatten_,
        cleanup_cache_files,
        map, filter, sort, shuffle, set_format, reset_format, formatted_as,
        cast_, remove_columns_, rename_column_,
        save_to_disk, load_from_disk,


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
