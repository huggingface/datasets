Cache management
================

When you download a dataset, the processing scripts and data are stored locally. This avoids having to download the whole dataset every time you use it.

Cache directory
^^^^^^^^^^^^^^^

The default cache directory is ``~/.cache/huggingface/datasets``. You can change the cache location by setting the shell environment variavle, ``HF_DATASETS_CACHE`` to another directory:

.. code-block::

    $ export HF_DATASETS_CACHE="/path/to/another/directory"

When you load a dataset, you also have the option to control where the data is cached. Change the ``cache_dir`` parameter to the path you want:

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('LOADING_SCRIPT', cache_dir="PATH/TO/MY/CACHE/DIR")

Download mode
^^^^^^^^^^^^^

After you download a dataset, control how it is loaded by :func:`datasets.load_dataset` by setting the :obj:`download_mode` parameter. By default, Datasets will reuse a dataset if it exists. But if you need to use a fresh dataset, you can re-download the files:

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('squad', download_mode='force_redownload')

Refer to the `reference <https://huggingface.co/docs/datasets/package_reference/builder_classes.html#datasets.GenerateMode>`_ for a full list of download modes.

Cache files
^^^^^^^^^^^
 
You can clean up the cache files in the directory with :func:`datasets.Dataset.cleanup_cache_files`:

.. code-block::

    #Returns the number of removed cache files
    >>> dataset.cleanup_cache_files()
    2

Enable or disable caching
^^^^^^^^^^^^^^^^^^^^^^^^^

If you're using a cached file locally, it will automatically reload the dataset with any previous computations you applied to the dataset. You can disable this by setting the argument ``load_from_cache=False`` in :func:`datasets.Dataset.map`:

    >>> updated_dataset = small_dataset.map(add_prefix, load_from_cache=False)

In the example above, Datasets will compute the function ``add_prefix`` again instead of just loading it from it's previous state.

This can be applied on a global scale with :func:`datasets.set_caching_enabled`:

    >>> from datasets import set_caching_enabled
    >>> set_caching_enabled(False)

When you disable caching, Datasets will no longer reload cached files when applying transforms to datasets. Any computation you do on your dataset will be recomputed.

.. hint::

    If you want to regenerate a dataset from scratch, try using the ``download_mode`` parameter in :func:`datasets.load_dataset` instead. Disabling caching may decrease Datasets effficiency.