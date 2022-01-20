Stream
======

Dataset streaming lets you get started with a dataset without waiting for the entire dataset to download. The data is downloaded progressively as you iterate over the dataset. This is especially helpful when:

* You don't want to wait for an extremely large dataset to download.
* The dataset size exceeds the amount of disk space on your computer.

.. image:: /imgs/stream.gif
   :align: center

For example, the English split of the `OSCAR <https://huggingface.co/datasets/oscar>`_ dataset is 1.2 terabytes, but you can use it instantly with streaming. Stream a dataset by setting ``streaming=True`` in :func:`datasets.load_dataset` as shown below:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
   >>> print(next(iter(dataset)))
   {'text': 'Mtendere Village was inspired by the vision of Chief Napoleon Dzombe, which he shared with John Blanchard during his first visit to Malawi. Chief Napoleon conveyed the desperate need for a program to intervene and care for the orphans and vulnerable children (OVC) in Malawi, and John committed to help...

Loading a dataset in streaming mode creates a new dataset type instance (instead of the classic :class:`datasets.Dataset` object), known as an :class:`datasets.IterableDataset`. This special type of dataset has its own set of processing methods shown below.

.. tip::

    An :class:`datasets.IterableDataset` is useful for iterative jobs like training a model. You shouldn't use a :class:`datasets.IterableDataset` for jobs that require random access to examples because you have to iterate all over it using a for loop. Getting the last example in an iterable dataset would require you to iterate over all the previous examples.

``Shuffle``
^^^^^^^^^^^

Like a regular :class:`datasets.Dataset` object, you can also shuffle a :class:`datasets.IterableDataset` with :func:`datasets.IterableDataset.shuffle`. 

The ``buffer_size`` argument controls the size of the buffer to randomly sample examples from. Let's say your dataset has one million examples, and you set the ``buffer_size`` to ten thousand. :func:`datasets.IterableDataset.shuffle` will randomly select examples from the first ten thousand examples in the buffer. Selected examples in the buffer are replaced with new examples.

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
   >>> shuffled_dataset = dataset.shuffle(buffer_size=10_000, seed=42)

.. tip::

   :func:`datasets.IterableDataset.shuffle` will also shuffle the order of the shards if the dataset is sharded into multiple sets.

Reshuffle
^^^^^^^^^

Sometimes you may want to reshuffle the dataset after each epoch. This will require you to set a different seed for each epoch. Use :func:`datasets.IterableDataset.set_epoch` in between epochs to tell the dataset what epoch you're on. 

Your seed effectively becomes: ``initial seed + current epoch``.

.. code-block::

   >>> for epoch in range(epochs):
   ...     shuffled_dataset.set_epoch(epoch)
   ...     for example in shuffled_dataset:
   ...         ...

Split dataset
^^^^^^^^^^^^^

You can split your dataset one of two ways:

* :func:`datasets.IterableDataset.take` returns the first ``n`` examples in a dataset:

.. code-block::

   >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
   >>> dataset_head = dataset.take(2)
   >>> list(dataset_head)
   [{'id': 0, 'text': 'Mtendere Village was...'}, '{id': 1, 'text': 'Lily James cannot fight the music...'}]

* :func:`datasets.IterableDataset.skip` omits the first ``n`` examples in a dataset and returns the remaining examples:

.. code::

   >>> train_dataset = shuffled_dataset.skip(1000)

.. important::

   ``take`` and ``skip`` prevent future calls to ``shuffle`` because they lock in the order of the shards. You should ``shuffle`` your dataset before splitting it.

.. _interleave_datasets:

``Interleave``
^^^^^^^^^^^^^^

:func:`datasets.interleave_datasets` can combine an :class:`datasets.IterableDataset` with other datasets. The combined dataset returns alternating examples from each of the original datasets. 

.. code-block::

   >>> from datasets import interleave_datasets
   >>> from itertools import islice
   >>> en_dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
   >>> fr_dataset = load_dataset('oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)
   
   >>> multilingual_dataset = interleave_datasets([en_dataset, fr_dataset])
   >>> print(list(islice(multilingual_dataset, 2)))
   [{'text': 'Mtendere Village was inspired by the vision...}, {'text': "Média de débat d'idées, de culture et de littérature....}]

Define sampling probabilities from each of the original datasets for more control over how each of them are sampled and combined. Set the ``probabilities`` argument with your desired sampling probabilities:

.. code-block::

   >>> multilingual_dataset_with_oversampling = interleave_datasets([en_dataset, fr_dataset], probabilities=[0.8, 0.2], seed=42)
   >>> print(list(islice(multilingual_dataset_with_oversampling, 2)))
   [{'text': 'Mtendere Village was inspired by the vision...}, {'text': 'Lily James cannot fight the music...}]

Around 80% of the final dataset is made of the ``en_dataset``, and 20% of the ``fr_dataset``.

Remove
^^^^^^

Remove columns on-the-fly with :func:`datasets.IterableDataset.remove_columns`. Specify the name of the column to remove:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('m4', 'en', streaming=True, split='train')
   >>> dataset = dataset.remove_columns('timestamp')

``Map``
^^^^^^^

Similar to the :func:`datasets.Dataset.map` function for a regular :class:`datasets.Dataset`, 🤗  Datasets features :func:`datasets.IterableDataset.map` for processing :class:`datasets.IterableDataset`\s.
:func:`datasets.IterableDataset.map` applies processing on-the-fly when examples are streamed.

It allows you to apply a processing function to each example in a dataset, independently or in batches. This function can even create new rows and columns.

The following example demonstrates how to tokenize a :class:`datasets.IterableDataset`. The function needs to accept and output a ``dict``:


.. code-block::

   >>> from datasets import load_dataset
   >>> from transformers import AutoTokenizer
   >>> dataset = load_dataset("mc4", "en", streaming=True, split="train")
   >>> tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
   >>> def encode(examples):
   ...     return tokenizer(examples['text'], truncation=True, padding='max_length')
   >>> dataset = dataset.map(encode, batched=True)
   >>> next(iter(dataset))
   {'input_ids': 101, 8466, 1018, 1010, 4029, 2475, 2062, 18558, 3100, 2061, ...,1106, 3739, 102],
   'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ..., 1, 1]}


Stream in a training loop
^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`datasets.IterableDataset` can be integrated into a training loop. First, shuffle the dataset:

.. code-block::

   >>> buffer_size, seed = 10_000, 42
   >>> dataset = dataset.shuffle(buffer_size, seed)

Lastly, create a simple training loop and start training:

.. tab:: PyTorch

   >>> import torch
   >>> from torch.utils.data import DataLoader
   >>> from transformers import AutoModelForMaskedLM, DataCollatorForLanguageModeling
   >>> from tqdm import tqdm
   >>> dataset = dataset.with_format("torch")
   >>> dataloader = DataLoader(dataset, collate_fn=DataCollatorForLanguageModeling(tokenizer))
   >>> device = 'cuda' if torch.cuda.is_available() else 'cpu' 
   >>> model = AutoModelForMaskedLM.from_pretrained("distilbert-base-uncased")
   >>> model.train().to(device)
   >>> optimizer = torch.optim.AdamW(params=model.parameters(), lr=1e-5)
   >>> for epoch in range(3):
   ...     dataset.set_epoch(epoch)
   ...     for i, batch in enumerate(tqdm(dataloader, total=5)):
   ...         if i == 5:
   ...             break
   ...         batch = {k: v.to(device) for k, v in batch.items()}
   ...         outputs = model(**batch)
   ...         loss = outputs[0]
   ...         loss.backward()
   ...         optimizer.step()
   ...         optimizer.zero_grad()
   ...         if i % 10 == 0:
   ...             print(f"loss: {loss}")

.. tab:: TensorFlow
  
   WIP
