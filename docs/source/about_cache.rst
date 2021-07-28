The Cache
=========

One of the reasons why Datasets is so efficient is because of the cache. It stores previously downloaded and processed datasets so when you need to use them again, Datasets will reload it straight from the cache. This avoids having to download a dataset all over again, or recomputing all the processing functions you applied.

Fingerprint 
-----------

How does the cache keeps track of what transforms you applied to your dataset? Well, Datasets assigns a fingerprint to the cache file. This keeps track of the current state of a dataset. The initial fingerprint is computed using a hash from the Arrow table, or a hash of the Arrow files if the dataset is on disk. Subsequent fingerprints are computed by combining the fingerprint of the previous state, and a hash of the latest transform applied. 

.. tip::

    Transforms are any of the processing methods from the :doc:`How-to Process <./process>` guides such as :func:`datasets.Dataset.map` or :func:`datasets.Dataset.shuffle`.

Here are what the actual fingerprints look like:

    >>> from datasets import Dataset
    >>> dataset1 = Dataset.from_dict({"a": [0, 1, 2]})
    >>> dataset2 = dataset1.map(lambda x: {"a": x["a"] + 1})
    >>> print(dataset1._fingerprint, dataset2._fingerprint)
    d19493523d95e2dc 5b86abacd4b42434

In order for a transform to be hashable, it needs to be picklable using `dill <https://dill.readthedocs.io/en/latest/>`_ or `pickle <https://docs.python.org/3/library/pickle.html>`_. When you use a non-hashable transform, Datasets uses a random fingerprint instead and raises a warning. The non-hashable transform is considered different from the previous transforms, so Datasets will recompute everything. Make sure your transforms are serializable with pickle or dill to avoid this!

An example of when Datasets recomputes everything is when caching is disabled. When this happens, the cache files are always created. The cache files are written to a temporary directory, and gets deleted once the session ends. A random hash is assigned to these cache files, instead of a fingerprint. 

.. tip::

    If caching is disabled, use :func:`datasets.Dataset.save_to_disk` to save your transformed dataset or it will be deleted once the session ends.

TO DO: Explain why it needs to be picklable to give the user more context. 

