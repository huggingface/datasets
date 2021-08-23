Load a Dataset in Streaming mode
==============================================================

When a dataset is in streaming mode, you can iterate over it directly without having to download the entire dataset.
The data are downloaded progressively as you iterate over the dataset.
You can enable dataset streaming by passing ``streaming=True`` in the :func:`load_dataset` function to get an iterable dataset.

This is useful if you don't have enough space on your disk to download the dataset, or if you don't want to wait for your dataset to be downloaded before using it.

Here is a demonstration:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> print(next(iter(dataset)))
    {'text': 'Mtendere Village was inspired by the vision of Chief Napoleon Dzombe, which he shared with John Blanchard during his first visit to Malawi. Chief Napoleon conveyed the desperate need for a program to intervene and care for the orphans and vulnerable children (OVC) in Malawi, and John committed to help...

Even though the dataset is 1.2 terabytes of data, you can start using it right away. Under the hood, it downloaded only the first examples of the dataset for buffering, and returned the first example.

.. note::

    The dataset that is returned is a :class:`datasets.IterableDataset`, not the classic map-style :class:`datasets.Dataset`. To get examples from an iterable dataset, you have to iterate over it using a for loop for example. To get the very last example of the dataset, you first have to iterate on all the previous examples.
    Therefore iterable datasets are mostly useful for iterative jobs like training a model, but not for jobs that require random access of examples.

.. _iterable-dataset-shuffling:

Shuffling the dataset: ``shuffle``
--------------------------------------------------

Shuffle the dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To shuffle your dataset, the :func:`datasets.IterableDataset.shuffle` method fills a buffer of size ``buffer_size`` and randomly samples examples from this buffer.
The selected examples in the buffer are replaced by new examples.

For instance, if your dataset contains 1,000,000 examples but ``buffer_size`` is set to 1,000, then shuffle will initially select a random examples from only the first 1,000 examples in the buffer.
Once an example is selected, its space in the buffer is replaced by the next (i.e. 1,001-st) example, maintaining the 1,000 example buffer.

.. note::
    For perfect shuffling, you need to set ``buffer_size`` to be greater than the size of your dataset. But in this case it will download the full dataset in the buffer.

Moreover, for larger datasets that are sharded into multiple files, :func:`datasets.IterableDataset.shuffle` also shuffles the order of the shards.

.. code-block::

    >>> shuffled_dataset = dataset.shuffle(buffer_size=10_000, seed=42)
    >>> print(next(iter(shuffled_dataset)))
    {text': 'In this role, she oversees the day-to-day operations of the agency’s motoring services divisions (Vehicle Titles & Registration, Motor Vehicles, Motor Carrier, Enforcement, Consumer Relations and the Automobile Burglary & Theft Prevention Authority) to ensure they are constantly improving and identifying opportunities to become more efficient and effective in service delivery...
    >>> print(dataset.n_shards)
    670

In this example, the shuffle buffer contains 10,000 examples that were downloaded from one random shard of the dataset (here it actually comes from the 480-th shard out of 670).
The example was selected randomly from this buffer, and replaced by the 10,001-st example of the dataset shard.

Note that if the order of the shards has been fixed by using :func:`datasets.IterableDataset.skip` or :func:`datasets.IterableDataset.take` then the order of the shards is kept unchanged.


Reshuffle the dataset at each epoch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The seed used to shuffle the dataset is the one you specify in :func:`datasets.IterableDataset.shuffle`. But often we want to use another seed after each epoch to reshuffle the dataset.
Therefore between epochs you can simply tell the dataset at what epoch you're at, and the data will be shuffled using an effective seed of ``seed + epoch``.

For example your training loop can look like this:

.. code-block::

    >>> for epoch in range(epochs):
    ...     shuffled_dataset.set_epoch(epoch)
    ...     for example in shuffled_dataset:
    ...         ...

In this case in the first epoch, the dataset is shuffled with ``seed + 0`` and in the second epoch it is shuffled with ``seed + 1``, making your dataset reshuffled at each epoch. It randomizes both the shuffle buffer and the shards order.


Processing data with ``map``
--------------------------------------------------

As for :class:`datasets.Dataset` objects, you can process your data using ``map``. This is useful if you want to transform the data or rename/remove columns.
Since the examples of an :class:`datasets.IterableDataset` are downloaded progressively, the :func:`datasets.IterableDataset.map` method processes the examples on-the-fly when you are iterating over the dataset (contrary to :func:`datasets.Dataset.map` which processes all the examples directly).

This example shows how to tokenize your dataset:

.. code-block::

    >>> from transformers import AutoTokenizer
    >>> tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    >>> tokenized_dataset = dataset.map(lambda x: tokenizer(x["text"]))
    >>> print(next(iter(tokenized_dataset)))
    {'input_ids': [101, 11047, 10497, 7869, 2352...], 'token_type_ids': [0, 0, 0, 0, 0...], 'attention_mask': [1, 1, 1, 1, 1...]}

Tokenizers are written in Rust and use parallelism to speed up tokenization. To leverage parallelism, you can process the examples batch by batch. Note that the output examples are still returned one by one.

    >>> tokenized_dataset = dataset.map(lambda x: tokenizer(x["text"]), batched=True)  # default batch_size is 1000 but you can specify another batch_size if needed
    >>> print(next(iter(tokenized_dataset)))
    {'input_ids': [101, 11047, 10497, 7869, 2352...], 'token_type_ids': [0, 0, 0, 0, 0...], 'attention_mask': [1, 1, 1, 1, 1...]}


Split your dataset with ``take`` and ``skip``
--------------------------------------------------

You can split your dataset by taking or skipping the first ``n`` examples.

You can create a new dataset with the first ``n`` examples by using :func:`datasets.IterableDataset.take`, or you can create a dataset with the rest of the examples by skipping the first ``n`` examples with :func:`datasets.IterableDataset.skip`:


.. code-block::

    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> dataset_head = dataset.take(2)
    >>> list(dataset_head)
    [{'id': 0, 'text': 'Mtendere Village was...'}, '{id': 1, 'text': 'Lily James cannot fight the music...'}]
    >>> # You can also create splits from a shuffled dataset
    >>> train_dataset = shuffled_dataset.skip(1000)
    >>> eval_dataset = shuffled_dataset.take(1000)

Some things to keep in mind:

- When you apply ``skip`` to a dataset, iterating on the new dataset will take some time to start. This is because under the hood it has to iterate over the skipped examples first.
- Using ``take`` (or ``skip``) prevents future calls to ``shuffle`` from shuffling the dataset shards order, otherwise the taken examples could come from other shards. In this case it only uses the shuffle buffer. Therefore it is advised to shuffle the dataset before splitting using ``take`` or ``skip``. See more details in the :ref:`iterable-dataset-shuffling` section.


Mix several iterable datasets together with ``interleave_datasets``
----------------------------------------------------------------------------------------------------

It is common to use several datasets to use a model. For example BERT was trained on a mix of Wikipedia and BookCorpus.
You can mix several iterable datasets together using :func:`datasets.interleave_datasets`.

By default, the resulting dataset alternates between the original datasets, but can also define sampling probabilities to sample randomly from the different datasets.

For example if you want a dataset in several languages:

.. code-block::

    >>> from datasets import interleave_datasets
    >>> from itertools import islice
    >>> en_dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> fr_dataset = load_dataset('oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)
    >>>
    >>> multilingual_dataset = interleave_datasets([en_dataset, fr_dataset])
    >>> print(list(islice(multilingual_dataset, 2)))
    [{'text': 'Mtendere Village was inspired by the vision...}, {'text': "Média de débat d'idées, de culture et de littérature....}]
    >>>
    >>> multilingual_dataset_with_oversampling = interleave_datasets([en_dataset, fr_dataset], probabilities=[0.8, 0.2], seed=42)
    >>> print(list(islice(multilingual_dataset_with_oversampling, 2)))
    [{'text': 'Mtendere Village was inspired by the vision...}, {'text': 'Lily James cannot fight the music...}]


Working with NumPy, pandas, PyTorch and TensorFlow
--------------------------------------------------

This part is still experimental and breaking changes may happen in the near future.

It is possible to get a ``torch.utils.data.IterableDataset`` from a :class:`datasets.IterableDataset` by setting the dataset format to "torch", as for a :class:`datasets.Dataset`:

.. code-block::

    >>> import torch
    >>> tokenized_dataset = dataset.map(lambda x: tokenizer(x["text"], return_tensors="pt"))
    >>> torch_tokenized_dataset = tokenized_dataset.with_format("torch")
    >>> assert isinstance(torch_tokenized_dataset, torch.utils.data.IterableDataset)
    >>> print(next(iter(torch_tokenized_dataset)))
    {'input_ids': tensor([[101, 11047, 10497, 7869, 2352...]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0...]]), 'attention_mask': tensor([[1, 1, 1, 1, 1...]])}

For now, only the PyTorch format is supported but support for TensorFlow and others will be added soon.


How does dataset streaming work ?
--------------------------------------------------

The StreamingDownloadManager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The standard (i.e. non-streaming) way of loading a dataset has two steps:

1. download and extract the raw data files of the dataset by using the :class:`datasets.DownloadManager`
2. process the data files to generate the Arrow file used to load the :class:`datasets.Dataset` object.

For example, in non-streaming mode a file is simply downloaded like this:

.. code-block::

    >>> from datasets import DownloadManager
    >>> url = "https://huggingface.co/datasets/lhoestq/test/resolve/main/some_text.txt"
    >>> filepath = DownloadManager().download(url)  # the file is downloaded here
    >>> print(filepath)
    '/Users/user/.cache/huggingface/datasets/downloads/16b702620cad8d485bafea59b1d2ed69e796196e6f2c73f005dee935a413aa19.ab631f60c6cb31a079ecf1ad910005a7c009ef0f1e4905b69d489fb2bd162683'
    >>> with open(filepath) as f:
    ...     print(f.read())

When you load a dataset in streaming mode, the download manager that is used instead is the :class:`datasets.StreamingDownloadManager`.
Instead of actually downloading and extracting all the data when you load the dataset, it is done lazily.
The file starts to be downloaded and extracted only when ``open`` is called.
This is made possible by extending ``open`` to support opening remote files via HTTP.
In each dataset script, ``open`` is replaced by our function ``xopen`` that extends ``open`` to be able to stream data from remote files.

Here is a sample code that shows what is done under the hood:

.. code-block::

    >>> from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen
    >>> url = "https://huggingface.co/datasets/lhoestq/test/resolve/main/some_text.txt"
    >>> urlpath = StreamingDownloadManager().download(url)
    >>> print(urlpath)
    'https://huggingface.co/datasets/lhoestq/test/resolve/main/some_text.txt'
    >>> with xopen(urlpath) as f:
    ...     print(f.read())  # the file is actually downloaded here

As you can see, since it's possible to open remote files via an URL, the streaming download manager just returns the URL instead of the path to the local downloaded file.

Then the file is downloaded in a streaming fashion: it is downloaded progessively as you iterate over the data file.
This is made possible because it is based on ``fsspec``, a library that allows to open and iterate on remote files.
You can find more information about ``fsspec`` in `its documentation <https://filesystem-spec.readthedocs.io/>`_

Compressed files and archives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may have noticed that the streaming download manager returns the exact same URL that was given as input for a text file.
However if you use ``download_and_extract`` on a compressed file instead, then the output url will be a chained URL.
Chained URLs are used by ``fsspec`` to navigate in remote compressed archives.

Some examples of chained URL are:

.. code-block::

    >>> from datasets.utils.streaming_download_manager import xopen
    >>> chained_url = "zip://combined/train.json::https://adversarialqa.github.io/data/aqa_v1.0.zip"
    >>> with xopen(chained_url) as f:
    ...     print(f.read()[:100])
    '{"data": [{"title": "Brain", "paragraphs": [{"context": "Another approach to brain function is to ex'
    >>> chained_url2 = "gzip://mkqa.jsonl::https://github.com/apple/ml-mkqa/raw/master/dataset/mkqa.jsonl.gz"
    >>> with xopen(chained_url2) as f:
    ...     print(f.readline()[:100])
    '{"query": "how long did it take the twin towers to be built", "answers": {"en": [{"type": "number_wi'

We also extended some functions from ``os.path`` to work with chained URLs.
For example ``os.path.join`` is replaced by our function ``xjoin`` that extends ``os.path.join`` to work with chained URLs:

.. code-block::

    >>> from datasets.utils.streaming_download_manager import StreamingDownloadManager, xopen, xjoin
    >>> url = "https://adversarialqa.github.io/data/aqa_v1.0.zip"
    >>> archive_path = StreamingDownloadManager().download_and_extract(url)
    >>> print(archive_path)
    'zip://::https://adversarialqa.github.io/data/aqa_v1.0.zip'
    >>> filepath = xjoin(archive_path, "combined", "train.json")
    >>> print(filepath)
    'zip://combined/train.json::https://adversarialqa.github.io/data/aqa_v1.0.zip'
    >>> with xopen(filepath) as f:
    ...     print(f.read()[:100])
    '{"data": [{"title": "Brain", "paragraphs": [{"context": "Another approach to brain function is to ex'

You can also take a look at the ``fsspec`` documentation about URL chaining `here <https://filesystem-spec.readthedocs.io/en/latest/features.html#url-chaining>`_

.. note::

    Streaming data from TAR archives is currently highly inefficient and requires a lot of bandwidth. We are working on optimizing this to offer you the best performance, stay tuned !

Dataset script compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that you are aware of how dataset streaming works, you can make sure your dataset script work in streaming mode:

1. make sure you use ``open`` to open the data files: it is extended to work with remote files
2. if you have to deal with archives like ZIP files, make sure you use ``os.path.join`` to navigate in the archive

Currently a few python functions or classes are not supported for dataset streaming:

- ``pathlib.Path`` and all its methods are not supported, please use ``os.path.join`` and string objects
- ``os.walk``, ``os.listdir``, ``glob.glob`` are not supported yet
