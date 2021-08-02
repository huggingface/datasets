Stream
======

Streaming a dataset is useful when you want to start using the dataset without having to wait to download the entire dataset. It also allows you to work with datasets that exceed the amount of disk space on your computer. The data is downloaded progressively as you iterate over the dataset. 

The English split of the `OSCAR <https://huggingface.co/datasets/oscar>`_ is 1.2 terabytes, but you can use it instantly with streaming. Stream a dataset by setting ``streaming=True`` in ``load_dataset()`` as shown below:

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> print(next(iter(dataset)))
    {'text': 'Mtendere Village was inspired by the vision of Chief Napoleon Dzombe, which he shared with John Blanchard during his first visit to Malawi. Chief Napoleon conveyed the desperate need for a program to intervene and care for the orphans and vulnerable children (OVC) in Malawi, and John committed to help...

Loading a dataset in streaming mode creates a unique instance of the classic :class:`datasets.Dataset` object, known as an :class:`datasets.IterableDataset`. This special type of dataset has it's own set of processing methods shown below:

.. note::

    This type of Dataset is useful for iterative jobs such as training a model. You shouldn't use an iterable Dataset for jobs that require random access to examples because you have to iterate over it using a for loop. To get the last example in a dataset would require you to iterate over all the previous examples.

``Shuffle``
^^^^^^^^^^^

As with a regular Dataset object, you can also shuffle an iterable Dataset with :func:`datasets.IterableDataset.shuffle`. The ``buffer_size`` argument controls the size of the buffer to randomly sample examples from. For example, if your dataset has one million examples and you set the ``buffer_size`` to ten thousand, :func:`datasets.IterableDataset.shuffle` will randomly select examples from the first ten thousand examples in the buffer. Selected examples in the buffer are replaced by new examples.

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> shuffled_dataset = dataset.shuffle(buffer_size=10_000, seed=42)

.. tip::

    For datasets that are sharded into multiple files, :func:`datasets.IterableDataset.shuffle` will also shuffle the order of the shards.

Reshuffle
^^^^^^^^^

Sometimes you may want to reshuffle the dataset after each epoch, so you will need to set a different seed. Use ``set_epoch()`` in between epochs to tell the dataset what epoch you're on. This way, the data will be shuffled using a seed of ``initial seed + current epoch``:

    >>> for epoch in range(epochs):
    ...     shuffled_dataset.set_epoch(epoch)
    ...     for example in shuffled_dataset:
    ...         ...

Split dataset
^^^^^^^^^^^^^

You can split your dataset one of two ways: :func:`datasets.IterableDataset.take`, or :func:`datasets.IterableDataset.skip`.

* :func:`datasets.IterableDataset.take` returns the first ``n`` examples in a dataset:

    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> dataset_head = dataset.take(2)
    >>> list(dataset_head)
    [{'id': 0, 'text': 'Mtendere Village was...'}, '{id': 1, 'text': 'Lily James cannot fight the music...'}]

* :func:`datasets.IterableDataset.skip` omits the first ``n`` examples in a dataset and returns the remaining examples:

    >>> train_dataset = shuffled_dataset.skip(1000)

.. important::

    ``take`` and ``skip`` prevents future calls to ``shuffle`` because they lock in the order of the shards. You should ``shuffle`` your dataset before splitting it.

``Interleave``
^^^^^^^^^^^^^^

Iterable Datasets can also be mixed together with :func:`datasets.interleave_datasets`. The mixed dataset returns alternating examples from each of the original datasets. 

    >>> from datasets import interleave_datasets
    >>> from itertools import islice
    >>> en_dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> fr_dataset = load_dataset('oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)
    >>>
    >>> multilingual_dataset = interleave_datasets([en_dataset, fr_dataset])
    >>> print(list(islice(multilingual_dataset, 2)))
    [{'text': 'Mtendere Village was inspired by the vision...}, {'text': "Média de débat d'idées, de culture et de littérature....}]

For more control over how each of the original datasets are sampled and mixed, define sampling probabilities for each of the original datasets. In the following example, 80% of the final mixed dataset is in English and 20% is in French:

    >>> multilingual_dataset_with_oversampling = interleave_datasets([en_dataset, fr_dataset], probabilities=[0.8, 0.2], seed=42)
    >>> print(list(islice(multilingual_dataset_with_oversampling, 2)))
    [{'text': 'Mtendere Village was inspired by the vision...}, {'text': 'Lily James cannot fight the music...}]