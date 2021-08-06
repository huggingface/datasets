The Cache
=========

The cache is one of the reasons why 🤗 Datasets is so efficient. It stores previously downloaded and processed datasets so when you need to use them again, they are reloaded directly from the cache. This avoids having to download a dataset all over again, or reapplying processing functions. Even after you close and start another Python session, 🤗 Datasets will reload your dataset directly from the cache!

Fingerprint 
-----------

How does the cache keeps track of what transforms are applied to a dataset? Well, 🤗 Datasets assigns a fingerprint to the cache file. A fingerprint keeps track of the current state of a dataset. The initial fingerprint is computed using a hash from the Arrow table, or a hash of the Arrow files if the dataset is on disk. Subsequent fingerprints are computed by combining the fingerprint of the previous state, and a hash of the latest transform applied. 

.. tip::

    Transforms are any of the processing methods from the :doc:`How-to Process <./process>` guides such as :func:`datasets.Dataset.map` or :func:`datasets.Dataset.shuffle`.

Here are what the actual fingerprints look like:

.. code-block::

   >>> from datasets import Dataset
   >>> dataset1 = Dataset.from_dict({"a": [0, 1, 2]})
   >>> dataset2 = dataset1.map(lambda x: {"a": x["a"] + 1})
   >>> print(dataset1._fingerprint, dataset2._fingerprint)
   d19493523d95e2dc 5b86abacd4b42434

In order for a transform to be hashable, it needs to be picklable by `dill <https://dill.readthedocs.io/en/latest/>`_ or `pickle <https://docs.python.org/3/library/pickle.html>`_. 

When you use a non-hashable transform, 🤗 Datasets uses a random fingerprint instead and raises a warning. The non-hashable transform is considered different from the previous transforms. As a result, 🤗 Datasets will recompute all the transforms. Make sure your transforms are serializable with pickle or dill to avoid this!

An example of when 🤗 Datasets recomputes everything is when caching is disabled. When this happens, the cache files are generated everytime and they get written to a temporary directory. Once your Python session ends, the cache files in the temporary directory are deleted. A random hash is assigned to these cache files, instead of a fingerprint. 

.. tip::

   When caching is disabled, use :func:`datasets.Dataset.save_to_disk` to save your transformed dataset or it will be deleted once the session ends.

TO DO: Explain why it needs to be picklable to give the user more context. 

