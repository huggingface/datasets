Dataset Streaming
==============================================================

You can enable dataset streaming by passing ``streaming=True`` in the :func:`load_dataset` function to get an iterable dataset.
When a dataset is in streaming mode, you can iterate over it directly, without having to download the entire dataset.
The data are downloaded progressively as you iterate over the dataset.

This is useful if you don't have enough space on your disk to download the dataset, or if you don't want to wait hours for your dataset to be downloaded before using it.

Here is a demonstration:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> print(next(iter(dataset)))
    {'text': 'Mtendere Village was inspired by the vision of Chief Napoleon Dzombe, which he shared with John Blanchard during his first visit to Malawi. Chief Napoleon conveyed the desperate need for a program to intervene and care for the orphans and vulnerable children (OVC) in Malawi, and John committed to help...

.. note::

    The dataset that is returned in a :class:`datasets.IterableDataset`, not the classic map-style :class:`datasets.Dataset`. To get examples from an iterable dataset, you have to iterate over it using a for loop for example. To get the very last example of the dataset, you first have to iterate on all the previous examples.
    Therefore iterable datasets are mostly useful for iterative jobs like training a transformer model, but not for jobs that require random access of examples.


Shuffling the dataset: ``shuffle``
--------------------------------------------------

TODO

Processing data with ``map``
--------------------------------------------------

TODO

Mix several iterable datasets together with ``merge_datasets``
--------------------------------------------------

TODO

Working with NumPy, pandas, PyTorch and TensorFlow
--------------------------------------------------

TODO
