Process
=======

Datasets provides a wide range of tools for modifying the structure of a dataset, such as rearranging the order of rows or extracting nested fields into their own columns. For more powerful processing applications, you can even alter the contents of a dataset by applying a function to the entire dataset to generate new rows and columns. These processing methods provide a lot of control and flexibility to massage your dataset into the desired shape and size with the appropriate features.

This guide shows you how to:

* reorder rows and split the dataset
* rename and remove columns as well as other common column operations
* apply processing functions to each example in a dataset
* augment a dataset

Load the MRPC dataset to follow our examples 🤗 :

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('glue', 'mrpc', split='train')

.. attention::

    All the processing methods in this guide returns a new :class:`datasets.Dataset`. Modification is not done in-place. Be careful about overriding your previous dataset!

Sort, shuffle, select, and split
--------------------------------

There are several methods for rearranging the structure of a dataset. These are useful for only selecting the rows you want, creating train and test splits, and splitting very large datasets into smaller chunks.

``Sort``
^^^^^^^^

Use :func:`datasets.Dataset.sort` to sort a column's values according to their numerical values. The provided column must be NumPy compatible.

    >>> dataset['label'][:10]
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0]
    >>> sorted_dataset = dataset.sort('label')
    >>> sorted_dataset['label'][:10]
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> sorted_dataset['label'][-10:]
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

``Shuffle``
^^^^^^^^^^^

The :func:`datasets.Dataset.shuffle` method randomly rearranges the values of a column. You can specify the ``generator`` argument in this method to use a different ``numpy.random.Generator`` if you want more control over the algorithm used to shuffle the dataset.

    >>> shuffled_dataset = sorted_dataset.shuffle(seed=42)
    >>> shuffled_dataset['label'][:10]
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0]

``Select`` and ``Filter``
^^^^^^^^^^^^^^^^^^^^^^^^^

There are two options for filtering rows in a dataset: :func:`datasets.Dataset.select` and :func:`datasets.Dataset.filter`.

* The :func:`datasets.Dataset.select` method filters rows according to a list of indices:

    >>> small_dataset = dataset.select([0, 10, 20, 30, 40, 50])
    >>> len(small_dataset)
    6

* The :func:`datasets.Dataset.filter` method returns rows that match a specified condition:

    >>> start_with_ar = dataset.filter(lambda example: example['sentence1'].startswith('Ar'))
    >>> len(start_with_ar)
    6
    >>> start_with_ar['sentence1']
    ['Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .',
    'Arison said Mann may have been one of the pioneers of the world music movement and he had a deep love of Brazilian music .',
    'Arts helped coach the youth on an eighth-grade football team at Lombardi Middle School in Green Bay .',
    'Around 9 : 00 a.m. EDT ( 1300 GMT ) , the euro was at $ 1.1566 against the dollar , up 0.07 percent on the day .',
    "Arguing that the case was an isolated example , Canada has threatened a trade backlash if Tokyo 's ban is not justified on scientific grounds .",
    'Artists are worried the plan would harm those who need help most - performers who have a difficult time lining up shows .'
    ]

 This method can also filter by indices if you set ``with_indices=True``:

    >>> even_dataset = dataset.filter(lambda example, indice: indice % 2 == 0, with_indices=True)
    len(even_dataset)
    1834
    len(dataset) / 2
    1834.0

``Split``
^^^^^^^^^

If your dataset doesn't have a train or test split, you can create your own with :func:`datasets.Dataset.train_test_split`. This allows you to control the relative proportions or absolute number of samples in each split. In the example below, you use the ``test_size`` argument to create a test split that is 10% of the original dataset:

    >>> dataset.train_test_split(test_size=0.1)
    {'train': Dataset(schema: {'sentence1': 'string', 'sentence2': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 3301),
    'test': Dataset(schema: {'sentence1': 'string', 'sentence2': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 367)}
    >>> 0.1 * len(dataset)
    366.8

The splits are shuffled by default, but you can set ``shuffle=False`` to prevent shuffling. For even more options selecting relative sizes of the train and test split, see the reference for :func:`datasets.Dataset.train_test_split`.

``Shard``
^^^^^^^^^

Datasets supports sharding to divide a very large dataset into a predefined number of chunks. Specify the ``num_shards`` argument in :func:`datasets.Dataset.shard` to specify the number of shards to split the dataset into. You will also need to provide the shard you want to return with the ``index`` argument.

For example, the `imdb <https://huggingface.co/datasets/imdb>`_ dataset has 25000 examples:

    >>> from datasets import load_dataset
    >>> datasets = load_dataset('imdb', split='train')
    >>> print(dataset)
    Dataset({
        features: ['text', 'label'],
        num_rows: 25000
    })

After you shard it into 4 chunks, the first chunk only has 6250 examples:

    >>> dataset.shard(num_shards=4, index=0)
    Dataset({
        features: ['text', 'label'],
        num_rows: 6250
    })
    >>> print(25000/4)
    6250.0


Rename, remove, cast, and flatten
---------------------------------

The following methods lets you edit the columns of a dataset. These are useful for renaming or removing columns, changing columns to a new set of features, and flattening nested column structures.

``Rename``
^^^^^^^^^^

Use :func:`datasets.Dataset.rename` when you need to rename a column in your dataset. Features associated with the original column are actually moved under the new column name, instead of just replacing the original column in-place. 

Provide this method with the name of the original column, and the new column name:

    >>> dataset = dataset.rename_column("sentence1", "sentenceA")
    >>> dataset = dataset.rename_column("sentence2", "sentenceB")
    >>> dataset
    Dataset({
        features: ['sentenceA', 'sentenceB', 'label', 'idx'],
        num_rows: 3668
    })

``Remove``
^^^^^^^^^^

When you need to remove one or more columns, give :func:`datasets.Dataset.remove_columns` the name of the column to remove. To remove more than one column, provide a list of column names.

    >>> dataset = dataset.remove_columns("label")
    >>> dataset
    Dataset({
        features: ['sentence1', 'sentence2', 'idx'],
        num_rows: 3668
    })
    >>> dataset = dataset.remove_columns(['sentence1', 'sentence2'])
    >>> dataset
    Dataset({
        features: ['idx'],
        num_rows: 3668
    })

``Cast``
^^^^^^^^

:func:`datasets.Dataset.cast` is another very useful method in Datasets that lets you change the feature type of one or more columns. This method takes your new :obj:`datasets.Features` as arguments. The following sample code shows how to change the :obj:`datasets.ClassLabel` and :obj:`datasets.Value`:

    >>> dataset.features
    {'sentence1': Value(dtype='string', id=None),
    'sentence2': Value(dtype='string', id=None),
    'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
    'idx': Value(dtype='int32', id=None)}
    >>> from datasets import ClassLabel, Value
    >>> new_features = dataset.features.copy()
    >>> new_features["label"] = ClassLabel(names=['negative', 'positive'])
    >>> new_features["idx"] = Value('int64')
    >>> dataset = dataset.cast(new_features)
    >>> dataset.features
    {'sentence1': Value(dtype='string', id=None),
    'sentence2': Value(dtype='string', id=None),
    'label': ClassLabel(num_classes=2, names=['negative', 'positive'], names_file=None, id=None),
    'idx': Value(dtype='int64', id=None)}

.. tip::

    Casting only works if the original feature type and new feature type are compatible. For example, you can cast a column with the feature type ``Value('int32')`` to ``Value('bool')`` if the original column only contains ones and zeros. 

``Flatten``
^^^^^^^^^^^

Sometimes a column can be a nested structure of several types. In these scenarios, use :func:`datasets.Dataset.flatten` to extract the subfields into their own separate columns. Take a look at the nested structure below from the SQuAD dataset:

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('squad', split='train')
    >>> dataset.features
    {'answers': Sequence(feature={'text': Value(dtype='string', id=None), 'answer_start': Value(dtype='int32', id=None)}, length=-1, id=None),
    'context': Value(dtype='string', id=None),
    'id': Value(dtype='string', id=None),
    'question': Value(dtype='string', id=None),
    'title': Value(dtype='string', id=None)}

The **answers** field contains two subfields: **text** and **answer_start**. After you use :func:`datasets.Dataset.flatten`, these subfields are now their own independent columns:

    >>> flat_dataset = dataset.flatten()
    >>> flat_dataset
    Dataset({
        features: ['id', 'title', 'context', 'question', 'answers.text', 'answers.answer_start'],
        num_rows: 87599
    })

Concatenate
------------

Separate datasets can be concatenated if they share the same column types. Concatenate datasets with :func:`datasets.concatenate_datasets`:

   >>> from datasets import concatenate_datasets, load_dataset
   >>>
   >>> bookcorpus = load_dataset("bookcorpus", split="train")
   >>> wiki = load_dataset("wikipedia", "20200501.en", split="train")
   >>> wiki = wiki.remove_columns("title")  # only keep the text
   >>>
   >>> assert bookcorpus.features.type == wiki.features.type
   >>> bert_dataset = concatenate_datasets([bookcorpus, wiki])

.. seealso::

    You can also mix several datasets together by taking alternating examples from each one to create a new dataset. This is known as interleaving datasets, and you can use it with :func:`datasets.interleave_datasets`.  See the ``IterableDataset`` section for an example of how it's used.

``map``
-------

Some of the more powerful applications provided by Datasets come from using :func:`datasets.Dataset.map`. It allows you to apply a processing function to each example in a dataset, independently or in batches. This function can even create new rows and columns. 

The primary utility of :func:`datasets.Dataset.map` is to update and modify the contents of a dataset. In the following example, you will prefix each ``sentence1`` value in the dataset with ``'My sentence: '``. First, create a function that will add ``'My sentence: '`` to the beginning of each sentence. The function needs to accept and outputs a :obj:`dict`:

    >>> def add_prefix(example):
    ...     example['sentence1'] = 'My sentence: ' + example['sentence1']
    ...     return example
        
Next, apply this function to your dataset with :func:`datasets.Dataset.map`:

    >>> updated_dataset = small_dataset.map(add_prefix)
    >>> updated_dataset['sentence1'][:5]
    ['My sentence: Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
    "My sentence: Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .",
    'My sentence: They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .',
    'My sentence: Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .',
    ]

Let's take a look at another example, except this time, you will remove a column with :func:`datasets.Dataset.map`. When you remove a column, it is only removed after the example has been provided to the mapped function. This allows the mapped function to use the content of the columns before they are removed. 

Specify the column to remove with the ``remove_columns=List[str]`` argument in :func:`datasets.Dataset.map`:

    >>> updated_dataset = dataset.map(lambda example: {'new_sentence': example['sentence1']}, remove_columns=['sentence1'])
    >>> updated_dataset.column_names
    ['sentence2', 'label', 'idx', 'new_sentence']

.. tip::

    Datasets also has a :func:`datasets.Dataset.remove_columns` method that is functionally identical, but faster, because it doesn't copy the data to a new dataset object.

You can also use :func:`datasets.Dataset.map` with indices if you set ``with_indices=True``. The sample code below adds the index to the beginning of each sentence:

    >>> updated_dataset = dataset.map(lambda example, idx: {'sentence2': f'{idx}: ' + example['sentence2']}, with_indices=True)
    >>> updated_dataset['sentence2'][:5]
    ['0: Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
     "1: Yucaipa bought Dominick 's in 1995 for $ 693 million and sold it to Safeway for $ 1.8 billion in 1998 .",
     "2: On June 10 , the ship 's owners had published an advertisement on the Internet , offering the explosives for sale .",
     '3: Tab shares jumped 20 cents , or 4.6 % , to set a record closing high at A $ 4.57 .', 
     '4: PG & E Corp. shares jumped $ 1.63 or 8 percent to $ 21.03 on the New York Stock Exchange on Friday .']

Batch processing
^^^^^^^^^^^^^^^^

:func:`datasets.Dataset.map` also supports working with batches of examples. You can operate on batches by setting ``batched=True``. The default batch size is 1000, but you can change it with the ``batch_size`` argument. This opens the door to many interesting applications such as tokenization, splitting long sentences into shorter chunks, and data augmentation. 

Tokenization
""""""""""""

One of the most obvious use-cases for batch processing is tokenization which accepts batches of inputs. First, load the tokenizer from the BERT model:

    >>> from transformers import BertTokenizerFast
    >>> tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')

Next, apply the tokenizer to batches of the ``sentence1`` field:

    >>> encoded_dataset = dataset.map(lambda examples: tokenizer(examples['sentence1']), batched=True)
    >>> encoded_dataset.column_names
    ['sentence1', 'sentence2', 'label', 'idx', 'input_ids', 'token_type_ids', 'attention_mask']
    >>> encoded_dataset[0]
    {'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
    'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
    'label': 1,
    'idx': 0,
    'input_ids': [  101,  7277,  2180,  5303,  4806,  1117,  1711,   117,  2292, 1119,  1270,   107,  1103,  7737,   107,   117,  1104,  9938, 4267, 12223, 21811,  1117,  2554,   119,   102],
    'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

Now you have three new columns, ``input_ids``, ``token_type_ids``, ``attention_mask``, that contain the encoded version of the ``sentence1`` field.

Split long examples
"""""""""""""""""""

When your examples are too long, you may want to split it into several smaller snippets. The first thing to do is create a function that splits the ``sentence1`` field into snippets of 50 characters, and stack all the snippets together to create the new dataset:

    >>> def chunk_examples(examples):
    ...     chunks = []
    ...     for sentence in examples['sentence1']:
    ...         chunks += [sentence[i:i + 50] for i in range(0, len(sentence), 50)]
    ...     return {'chunks': chunks}

Then apply the function with :func:`datasets.Dataset.map`:

    >>> chunked_dataset = dataset.map(chunk_examples, batched=True, remove_columns=dataset.column_names)
    >>> chunked_dataset[:10]
    {'chunks': ['Amrozi accused his brother , whom he called " the ',
                'witness " , of deliberately distorting his evidenc',
                'e .',
                "Yucaipa owned Dominick 's before selling the chain",
                ' to Safeway in 1998 for $ 2.5 billion .',
                'They had published an advertisement on the Interne',
                't on June 10 , offering the cargo for sale , he ad',
                'ded .',
                'Around 0335 GMT , Tab shares were up 19 cents , or',
                ' 4.4 % , at A $ 4.56 , having earlier set a record']}

The sentences are split into shorter chunks now, and there are more rows in the dataset.

    >>> dataset
    Dataset({
    features: ['sentence1', 'sentence2', 'label', 'idx'],
    num_rows: 3668
    })
    >>> chunked_dataset
    Dataset(schema: {'chunks': 'string'}, num_rows: 10470)

Data augmentation
"""""""""""""""""

With batch processing, you can even augment your dataset with additional examples. In the following sample scenario, you will generate additional words for a masked token in a sentence. 

Load the `RoBERTA <https://huggingface.co/roberta-base>`_ model to use in the Transformer `FillMaskPipeline <https://huggingface.co/transformers/main_classes/pipelines.html?#transformers.FillMaskPipeline>`_:

    >>> from random import randint
    >>> from transformers import pipeline
    >>>
    >>> fillmask = pipeline('fill-mask', model='roberta-base')
    >>> mask_token = fillmask.tokenizer.mask_token
    >>> smaller_dataset = dataset.filter(lambda e, i: i<100, with_indices=True)

Next, create a function to randomly select a work to mask in the sentence. The function should also return the original sentence and the top two replacements generated by RoBERTA.

    >>> def augment_data(examples):
    ...     outputs = []
    ...     for sentence in examples['sentence1']:
    ...         words = sentence.split(' ')
    ...         K = randint(1, len(words)-1)
    ...         masked_sentence = " ".join(words[:K]  + [mask_token] + words[K+1:])
    ...         predictions = fillmask(masked_sentence)
    ...         augmented_sequences = [predictions[i]['sequence'] for i in range(3)]
    ...         outputs += [sentence] + augmented_sequences
    ...
    ...     return {'data': outputs}

Use :func:`datasets.Dataset.map` to apply the function across the whole dataset:

    >>> augmented_dataset = smaller_dataset.map(augment_data, batched=True, remove_columns=dataset.column_names, batch_size=8)
    >>> augmented_dataset[:9]['data']
    ['Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
    'Amrozi accused his brother, whom he called " the witness ", of deliberately withholding his evidence.',
    'Amrozi accused his brother, whom he called " the witness ", of deliberately suppressing his evidence.',
    'Amrozi accused his brother, whom he called " the witness ", of deliberately destroying his evidence.',
    "Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .",
    'Yucaipa owned Dominick Stores before selling the chain to Safeway in 1998 for $ 2.5 billion.',
    "Yucaipa owned Dominick's before selling the chain to Safeway in 1998 for $ 2.5 billion.",
    'Yucaipa owned Dominick Pizza before selling the chain to Safeway in 1998 for $ 2.5 billion.']

For each original sentence, RoBERTA augmented a random word with three alternatives. In the first sentence, the word ``distorting`` is augmented with ``withholding``, ``suppressing``, and ``destroying``.

Process multiple splits
^^^^^^^^^^^^^^^^^^^^^^^

Many datasets have splits that we can process simultaneously with :func:`datasets.Dataset.map`. You can tokenize the ``sentence1`` field in the train and test split by:

    >>> from datasets import load_dataset
    >>>
    # load all the splits
    >>> dataset = load_dataset('glue', 'mrpc')
    >>> encoded_dataset = dataset.map(lambda examples: tokenizer(examples['sentence1']), batched=True)
    >>> encoded_dataset["train"][0]
    {'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
    'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
    'label': 1,
    'idx': 0,
    'input_ids': [  101,  7277,  2180,  5303,  4806,  1117,  1711,   117,  2292, 1119,  1270,   107,  1103,  7737,   107,   117,  1104,  9938, 4267, 12223, 21811,  1117,  2554,   119,   102],
    'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

Distributed usage
^^^^^^^^^^^^^^^^^

When you use :func:`datasets.Dataset.map` in a distributed setting, you should also use `torch.distributed.barrier <https://pytorch.org/docs/stable/distributed.html?highlight=barrier#torch.distributed.barrier>`_. This ensures the main process perform the mapping, while the other processes load the results, thereby avoiding duplicate work. The following example shows how you can use ``torch.distributed.barrier`` to synchronize the processes:

   >>> from datasets import Dataset
   >>> import torch.distributed
   >>>
   >>> dataset1 = Dataset.from_dict({"a": [0, 1, 2]})
   >>>
   >>> if training_args.local_rank > 0:
   ...     print("Waiting for main process to perform the mapping")
   ...     torch.distributed.barrier()
   >>>
   >>> dataset2 = dataset1.map(lambda x: {"a": x["a"] + 1})
   >>>
   >>> if training_args.local_rank == 0:
   ...     print("Loading results from main process")
   ...     torch.distributed.barrier()

:class:`IterableDataset`
------------------------

An :class:`IterableDataset` is a unique instance of the classic :class:`datasets.Dataset`. The iterable Dataset results from when a dataset is loaded in streaming mode. This type of dataset has it's own set of processing methods shown below:

.. note::

    This type of Dataset is useful for iterative jobs such as training a model. You shouldn't use an iterable Dataset for jobs that require random access to examples.

Shuffle
^^^^^^^

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

.. _mix_label:
Mix
^^^

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

Format
------

Another way to set the format is with :func:`datasets.Dataset.with_format`. This will return a new Dataset object with your specified format.

    >>> dataset.with_format(type='tensorflow', columns=['input_ids', 'token_type_ids', 'attention_mask', 'label'])

If you need to reset the dataset to the original format, use :func:`datasets.Dataset.reset_format`:

    >>> dataset.format
    {'type': 'torch', 'format_kwargs': {}, 'columns': ['label'], 'output_all_columns': False}
    >>> dataset.reset_format()
    >>> dataset.format
    {'type': 'python', 'format_kwargs': {}, 'columns': ['idx', 'label', 'sentence1', 'sentence2'], 'output_all_columns': False}

Format transform
^^^^^^^^^^^^^^^^

You can also use :func:`datasets.Dataset.set_transform` to apply a custom formatting transform on-the-fly. This will replace any previously specified format. For example, you can use this method to tokenize and pad tokens on-the-fly:

    >>> from transformers import BertTokenizer
    >>> tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    >>> def encode(batch):
    >>>     return tokenizer(batch["sentence1"], padding="longest", truncation=True, max_length=512, return_tensors="pt")
    >>> dataset.set_transform(encode)
    >>> dataset.format
    {'type': 'custom', 'format_kwargs': {'transform': <function __main__.encode(batch)>}, 'columns': ['idx', 'label', 'sentence1', 'sentence2'], 'output_all_columns': False}
    >>> dataset[:2]
    {'input_ids': tensor([[  101,  2572,  3217, ... 102]]), 'token_type_ids': tensor([[0, 0, 0, ... 0]]), 'attention_mask': tensor([[1, 1, 1, ... 1]])}


Save and export
---------------

Once you are done processing your dataset, you can save and reuse it later. The following table shows which save method you should use depending on your Dataset object:

.. list-table::
    :header-rows: 1

    * - Object type
      - Save method
    * - :obj:`datasets.Dataset`
      - :func:`datasets.Dataset.save_to_disk`
    * - :obj:`datasets.DatasetDict`
      - :func:`datasets.DatasetDict.save_to_disk`

Save your dataset by providing the path to the directory you wish to save it to:

    >>> encoded_dataset.save_to_disk("path/of/my/dataset/directory")

When you want to use it again, use :func:`load_from_disk` to reload the dataset:

    >>> from datasets import load_from_disk
    >>> reloaded_encoded_dataset = load_from_disk("path/of/my/dataset/directory")

.. note::

    Want to save your dataset to a cloud storage provider? Read our :doc:`Cloud Storage <./fss>` guide on how to save your dataset to AWS or Google Cloud Storage!

Export
^^^^^^

Datasets supports exporting so you can work with your dataset in other applications. The following table shows currently supported file formats you can export as:

.. list-table::
    :header-rows: 1

    * - File type
      - Export method
    * - CSV
      - :func:`datasets.Dataset.to_csv`
    * - JSON
      - :func:`datasets.Dataset.to_json`
    * - Parquet
      - :func:`datasets.Dataset.to_parquet`
    * - Python object
      - :func:`datasets.Dataset.to_pandas` or :func:`datasets.Dataset.to_dict`

For example, you can export your dataset to a CSV like this:

    >>> encoded_dataset.to_csv("path/of/my/dataset/directory")