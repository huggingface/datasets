Cache management
================

When you download a dataset, the processing scripts and data are stored locally on your computer. The cache allows 🤗 Datasets to avoid re-downloading or processing the entire dataset every time you use it. 

This guide will show you how to:

* Change the cache directory.
* Control how a dataset is loaded from the cache.
* Clean up cache files in the directory.
* Enable or disable caching.

Cache directory
---------------

The default cache directory is ``~/.cache/huggingface/datasets``. Change the cache location by setting the shell environment variable, ``HF_DATASETS_CACHE`` to another directory:

.. code::

   $ export HF_DATASETS_CACHE="/path/to/another/directory"

When you load a dataset, you also have the option to change where the data is cached. Change the ``cache_dir`` parameter to the path you want:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('LOADING_SCRIPT', cache_dir="PATH/TO/MY/CACHE/DIR")

Similarly, you can change where a metric is cached with the ``cache_dir`` parameter:

.. code-block::

   >>> from datasets import load_metric
   >>> metric = load_metric('glue', 'mrpc', cache_dir="MY/CACHE/DIRECTORY")

Download mode
-------------

After you download a dataset, control how it is loaded by :func:`datasets.load_dataset` with the :obj:`download_mode` parameter. By default, 🤗 Datasets will reuse a dataset if it exists. But if you need the original dataset without any processing functions applied, re-download the files as shown below:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('squad', download_mode='force_redownload')

Refer to :class:`datasets.DownloadMode` for a full list of download modes.

Cache files
-----------
 
Clean up the cache files in the directory with :func:`datasets.Dataset.cleanup_cache_files`:

.. code-block::

   #Returns the number of removed cache files
   >>> dataset.cleanup_cache_files()
   2

Enable or disable caching
-------------------------

If you're using a cached file locally, it will automatically reload the dataset with any previous transforms you applied to the dataset. Disable this behavior by setting the argument ``load_from_cache=False`` in :func:`datasets.Dataset.map`:

.. code::

   >>> updated_dataset = small_dataset.map(add_prefix, load_from_cache=False)

In the example above, 🤗 Datasets will execute the function ``add_prefix`` over the entire dataset again instead of loading the dataset from its previous state.

Disable caching on a global scale with :func:`datasets.set_caching_enabled`:

.. code-block::

   >>> from datasets import set_caching_enabled
   >>> set_caching_enabled(False)

When you disable caching, 🤗 Datasets will no longer reload cached files when applying transforms to datasets. Any transform you apply on your dataset will be need to be reapplied.

.. tip::

   If you want to reuse a dataset from scratch, try setting the ``download_mode`` parameter in :func:`datasets.load_dataset` instead.

You can also avoid caching your metric entirely, and keep it in CPU memory instead:

.. code-block::

   >>> from datasets import load_metric
   >>> metric = load_metric('glue', 'mrpc', keep_in_memory=True)

.. caution::

   Keeping the predictions in-memory is not possible in a distributed setting since the CPU memory spaces of the various processes are not shared.

.. _load_dataset_enhancing_performance:

Improve performance
-------------------

Disabling the cache and copying the dataset in-memory will speed up dataset operations. There are two options for copying the dataset in-memory:

1. Set ``datasets.config.IN_MEMORY_MAX_SIZE`` to a nonzero value (in bytes) that fits in your RAM memory. 

2. Set the environment variable ``HF_DATASETS_IN_MEMORY_MAX_SIZE`` to a nonzero value. Note that the first method takes higher precedence.