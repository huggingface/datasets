Main classes
----------------------------------------------------


``DatasetInfo``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: nlp.DatasetInfo
    :members: 

``Dataset``
~~~~~~~~~~~~~~~~~~~~~

The base class :class:`nlp.Dataset` implements a Dataset backed by an Apache Arrow table.

.. autoclass:: nlp.Dataset
    :members: from_file, from_buffer,
        drop, unique, dictionary_encode_column, flatten,
        __len__, __iter__, formated_as, set_format, reset_format,
        __getitem__, cleanup_cache_files,
        map, filter, select, sort, shuffle, train_test_split, shard,
        add_faiss_index, add_faiss_index_from_external_arrays, save_faiss_index, load_faiss_index,
        add_elasticsearch_index,
        list_indexes, get_index, drop_index, search, search_batch, get_nearest_examples, get_nearest_examples_batch,
        info, split, builder_name, citation, config_name, dataset_size,
        description, download_checksums, download_size, features, homepage,
        license, size_in_bytes, supervised_keys, version

``Features``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: nlp.Features
    :members:

.. autoclass:: nlp.Sequence
    :members:

.. autoclass:: nlp.ClassLabel
    :members:

.. autoclass:: nlp.Value
    :members:

.. autoclass:: nlp.Tensor
    :members:

.. autoclass:: nlp.Translation
    :members:

.. autoclass:: nlp.TranslationVariableLanguages
    :members:


``MetricInfo``
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: nlp.MetricInfo
    :members: 

``Metric``
~~~~~~~~~~~~~~~~~~~~~

The base class ``Metric`` implements a Metric backed by one or several :class:`nlp.Dataset`.

.. autoclass:: nlp.Metric
    :members:
