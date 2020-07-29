Processing data in a Dataset
==============================================================

🤗nlp provides many methods to modify a Dataset, be it to reorder, split or shuffle the dataset or to apply data processing functions or evaluation functions to its elements.

We'll start by presenting the methods which change the order or number of elements before presenting methods which access and can change the content of the elements themselves.

As always, let's start by loading a small dataset for our demonstrations:

.. code-block::

    >>> from nlp import load_dataset
    >>> dataset = load_dataset('glue', 'mrpc', split='train')

.. note::

    **No in-place policy** All the methods in this chapter return a new :class:`nlp.Dataset`. No modification is done in-place and it's the thus responsibility of the user to decide to override the previous dataset with the newly returned one.

.. note::

    **Caching policy** All the methods in this chapter store the updated dataset in a cache file indexed by a hash of current state and all the argument used to call the method.

    A subsequent call to any of the methods detailed here (like :func:`nlp.Dataset.sort`, :func:`nlp.Dataset.map`, etc) will thus **reuse the cached file instead of recomputing the operation** (even in another python session).

    This usually makes it very efficient to process data with 🤗nlp.

    If the disk space is critical, these methods can be called with arguments to avoid this behavior (see the last section), or the cache files can be cleaned using the method :func:`nlp.Dataset.cleanup_cache_files`.


Selecting, sorting, shuffling, splitting rows
--------------------------------------------------

Several methods are provided to reorder rows and/or spit the dataset:

- sorting the dataset according to a column (:func:`nlp.Dataset.sort`)
- shuffling the dataset (:func:`nlp.Dataset.shuffle`)
- filtering rows either according to a list of indices (:func:`nlp.Dataset.select`) or with a filter function returning true for the rows to keep (:func:`nlp.Dataset.filter`),
- splitting the dataset in a (potentially shuffled) train and a test split (:func:`nlp.Dataset.train_test_split`),
- splitting the dataset in a deterministic list of shards (:func:`nlp.Dataset.shard`).

These methods have quite simple signature and should be for the most part self-explanatory.

Let's see them in action:

Sorting the dataset according to a column: ``sort``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The provided column has to be of a NumPy compatible column (typically a column containing numerical values).

.. code-block::

    >>> dataset['label'][:10]
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0]
    >>> sorted_dataset = dataset.sort('label')
    >>> sorted_dataset['label'][:10]
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> sorted_dataset['label'][-10:]
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

Shuffling the dataset: ``shuffle``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    >>> shuffled_dataset = sorted_dataset.shuffle(seed=42)
    >>> shuffled_dataset['label'][:10]
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0]

You can also provide a :obj:`numpy.random.Generator` to :func:`nlp.Dataset.shuffle` to control more finely the algorithm used to shuffle the dataset.

Filtering rows: ``select`` and ``filter``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can filter rows according to a list of indices (:func:`nlp.Dataset.select`) or with a filter function returning true for the rows to keep (:func:`nlp.Dataset.filter`):

.. code-block::

    >>> small_dataset = dataset.select([0, 10, 20, 30, 40, 50])
    >>> len(small_dataset)
    6

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

:func:`nlp.Dataset.filter` expect a function which can accept a single example of the dataset, i.e. the python dictionary returned by :obj:`dataset[i]` and return a boolean value. It's also possible to use the indice of each example in the function by setting :obj:`with_indices=True` in :func:`nlp.Dataset.filter`. In this case, the signature of the function given to :func:`nlp.Dataset.filter` should be :obj:`function(example: dict, indice: int) -> bool`:

.. code-block::

    >>> even_dataset = dataset.filter(lambda example, indice: indice % 2 == 0, with_indices=True)
    >>> len(even_dataset)
    1834
    >>> len(dataset) / 2
    1834.0

Splitting the dataset in train and test split: ``train_test_split``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method is adapted from scikit-learn celebrated :obj:`train_test_split` method with the omission of the stratified options.

You can select the test and train sizes as relative proportions or absolute number of samples.

The splits will be **shuffled by default** using the above described :func:`nlp.Dataset.shuffle` method. You can deactivate this behavior by setting :obj:`shuffle=False` in the arguments of :func:`nlp.Dataset.train_test_split`.

The two splits are returned as a dictionary of :class:`nlp.Dataset`.

.. code-block::

    >>> dataset.train_test_split(test_size=0.1)
    {'train': Dataset(schema: {'sentence1': 'string', 'sentence2': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 3301),
     'test': Dataset(schema: {'sentence1': 'string', 'sentence2': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 367)}
    >>> 0.1 * len(dataset)
    366.8

We can see that the test split is 10% of the original dataset.

The :func:`nlp.Dataset.train_test_split` has many ways to select the relative sizes of the train and test split so we refer the reader to the package reference of :func:`nlp.Dataset.train_test_split` for all the details.

Sharding the dataset: ``shard``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Eventually, it's possible to "shard" the dataset, i.e. divide it in a deterministic list of dataset of (almost) the same size.

The :func:`nlp.Dataset.shard` takes as arguments the total number of shards (:obj:`num_shards`) and the index of the currently requested shard (:obj:`index`)  and return a :class:`nlp.Dataset` instance constituted by the requested shard.

This method can be used to slice a very large dataset in a predefined number of chunks.

Processing data with ``map``
--------------------------------

All the methods we seen up to now operate on examples taken as a whole and don't inspect (excepted for the ``filter`` method) or modify the content of the samples.

We now turn to the :func:`nlp.Dataset.map` method which is a powerful method inspired by ``tf.data.Dataset`` map method and which you can use to apply a processing function to each examples in a dataset, independently or in batch and even generate new rows or columns.

:func:`nlp.Dataset.map` takes a callable accepting a dict as argument (same dict as returned by :obj:`dataset[i]`) and iterate over the dataset by calling the function with each example.

Let's print the length of the ``sentence1`` value for each sample in our dataset:

.. code-block::

    >>> small_dataset = dataset.select(range(10))
    >>> small_dataset
    Dataset(schema: {'sentence1': 'string', 'sentence2': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 10)
    >>> small_dataset.map(lambda example: print(len(example['sentence1'])), verbose=False)
    103
    89
    105
    119
    105
    97
    88
    54
    85
    108
    Dataset(schema: {'sentence1': 'string', 'sentence2': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 10)

This is basically the same as doing

.. code-block::

    for example in dataset:
        function(example)

The above example had no effect on the dataset because the method we supplied to :func:`nlp.Dataset.map` didn't return a :obj:`dict` or a :obj:`abc.Mapping` that could be used to update the examples in the dataset.

In such a case, :func:`nlp.Dataset.map` will return the original dataset (:obj:`self`) and the user is usually only interested in side effects of the provided method.

Now let's see how we can use a method that actually modify the dataset with :func:`nlp.Dataset.map`.

Processing data row by row
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main interest of :func:`nlp.Dataset.map` is to update and modify the content of the table and leverage smart caching and fast backend.

To use :func:`nlp.Dataset.map` to update elements in the table you need to provide a function with the following signature: :obj:`function(example: dict) -> dict`.

Let's add a prefix ``'My sentence: '`` to each ``sentence1`` values in our small dataset:

.. code-block::

    >>> def add_prefix(example):
    ...     example['sentence1'] = 'My sentence: ' + example['sentence1']
    ...     return example
    ... 
    >>> updated_dataset = small_dataset.map(add_prefix)
    >>> updated_dataset['sentence1'][:5]
    ['My sentence: Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     "My sentence: Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .",
     'My sentence: They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .',
     'My sentence: Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .',
    ]

This call to :func:`nlp.Dataset.map` computed and returned an updated table.

.. note::

    Calling :func:`nlp.Dataset.map` also stored the updated table in a cache file indexed by the current state and the mapped function.
    A subsequent call to :func:`nlp.Dataset.map` (even in another python session) will reuse the cached file instead of recomputing the operation.
    You can test this by running again the previous cell, you will see that the result are directly loaded from the cache and not re-computed again.

The function you provide to :func:`nlp.Dataset.map` should accept an input with the format of an item of the dataset: :obj:`function(dataset[0])` and return a python dict.

The columns and type of the outputs **can be different** from columns and type of the input dict. In this case the new keys will be **added** as additional columns in the dataset.

Each dataset example dict is updated with the dictionary returned by the function. Under the hood :obj:`map` operate like this:

.. code-block::

    new_dataset = []
    for example in dataset:
        processed_example = function(example)
        example.update(processed_example)
        new_dataset.append(example)
    return new_dataset

Since the input example dict is **updated** with output dict generated by our :obj:`add_prefix` function, we could have actually just returned the updated ``sentence1`` field, instead of the full example which is simpler to write:

.. code-block::

    >>> updated_dataset = small_dataset.map(lambda example: {'sentence1': 'My sentence: ' + example['sentence1']})
    >>> updated_dataset['sentence1'][:5]
    ['My sentence: Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     "My sentence: Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .", 'My sentence: They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .',
     'My sentence: Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .',
     'My sentence: The stock rose $ 2.11 , or about 11 percent , to close Friday at $ 21.51 on the New York Stock Exchange .']

Removing columns
^^^^^^^^^^^^^^^^^^^^^^^^

This process of **updating** the original example with the output of the mapped function is simpler to write when mostly adding new columns to a dataset but we need an additional mechanism to easily remove columns.


To this aim, the :obj:`remove_columns=List[str]` argument can be used and provided with a single name or a list of names of columns which should be removed during the :func:`nlp.Dataset.map` operation.

Column to remove are removed **after** the example has been provided to the mapped function so that the mapped function can use the content of these columns before they are removed.

Here is an example removing the ``sentence1`` column while adding a ``new_sentence`` column with the content of the ``new_sentence``. Said more simply, we are renaming the ``sentence1`` column as ``new_sentence``:

.. code-block::

    >>> updated_dataset = small_dataset.map(lambda example: {'new_sentence': example['sentence1']}, remove_columns=['sentence1'])
    >>> updated_dataset.column_names
    ['sentence2', 'label', 'idx', 'new_sentence']


Using row indices
^^^^^^^^^^^^^^^^^^^^^^

When the argument :obj:`with_indices` is set to :obj:`True`, the indices of the rows (from ``0`` to ``len(dataset)``) will be provided to the mapped function. This function must then have the following signature: :obj:`function(example: dict, indice: int) -> Union[None, dict]`.

In the following example, we add the index of the example as a prefix to the 'sentence2' field of each example:

.. code-block::

    >>> updated_dataset = small_dataset.map(lambda example, idx: {'sentence2': f'{idx}: ' + example['sentence2']}, with_indices=True)
    >>> updated_dataset['sentence2'][:5]
    ['0: Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
     "1: Yucaipa bought Dominick 's in 1995 for $ 693 million and sold it to Safeway for $ 1.8 billion in 1998 .",
     "2: On June 10 , the ship 's owners had published an advertisement on the Internet , offering the explosives for sale .",
     '3: Tab shares jumped 20 cents , or 4.6 % , to set a record closing high at A $ 4.57 .', 
     '4: PG & E Corp. shares jumped $ 1.63 or 8 percent to $ 21.03 on the New York Stock Exchange on Friday .']


Processing data in batches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`nlp.Dataset.map` can also work with batches of examples (slices of the dataset).

This is particularly interesting if you have a mapped function which can efficiently handle batches of inputs like the tokenizers of the fast `HuggingFace tokenizers library <https://github.com/huggingface/tokenizers>`__.

To operate on batch of example, just set :obj:`batched=True` when calling :func:`nlp.Dataset.map` and provide a function with the following signature: :obj:`function(examples: Dict[List]) -> Dict[List]` or, if you use indices (:obj:`with_indices=True`): :obj:`function(examples: Dict[List], indices: List[int]) -> Dict[List])`.

In other words, the mapped function should accept an input with the format of a slice of the dataset: :obj:`function(dataset[:10])`.

Let's take an example with a fast tokenizer of the 🤗transformers library.

Firsst install this library if you haven't already done it:

.. code-block::

    pip install transformers

Then we will import a fast tokenizer, for instance the tokenizer of the Bert model:

.. code-block::

    >>> from transformers import BertTokenizerFast
    >>> tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')

Now let's batch tokenize the 'sentence1' fields of our dataset. The tokenizers of the 🤗transformers library can accept lists of texts as inputs and tokenize them efficiently in batch (for the fast tokenizers in particular).

For more details on the tokenizers of the 🤗transformers library please refere to its `guide on processing data <https://huggingface.co/transformers/preprocessing.html>`__.

This tokenizer will output a dictionnary-like object with three fields: ``input_ids``, ``token_type_ids``, ``attention_mask`` corresponding to Bert model's required inputs. Each field contain a list (batch) of samples.

The output of the tokenizer is thus compatible with the :func:`nlp.Dataset.map` method which is also expected to return a dictionnary. We can thus directly return the dictionnary generated by the tokenizer as the output of our mapped function:

.. code-block::

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

We have indeed the added columns for ``input_ids``, ``token_type_ids``, ``attention_mask`` which contains the encoded version of the ``sentence1`` field.

The batch size provided to the mapped function can be controlled by the :obj:`batch_size` argument. The default value is ``1000``, i.e. batches of 1000 samples will be provided to the mapped function by default.

Augmenting the dataset
---------------------------

Using :func:`nlp.Dataset.map` in batched mode (i.e. with :obj:`batched=True`) actually let you control the size of the generate dataset freely.

More precisely, in batched mode :func:`nlp.Dataset.map` will provide batch of examples (as a dict of lists) to the mapped function and expect the mapped function to return back a batch of examples (as a dict of lists) but **the input and output batch are not required to be of the same size**.

In other words, a batch mapped function can take as input a batch of size ``N`` and return a batch of size ``M`` where ``M`` can be greater or less than ``N`` and can even be zero.

The resulting dataset can thus have a different size from the original dataset.

This can be taken advantage of for several use-cases:

- the :func:`nlp.Dataset.filter` method makes use of variable size batched mapping under the hood to change the size of the dataset and filter some columns,
- it's possible to cut examples which are too long in several snippets,
- it's also possible to do data augmentation on each example.

.. note::

    **One important condition on the output of the mapped function** Each field in the output dictionnary returned by the mapped function must contain the **same number of elements** as the other field in this output dictionnary otherwise it's not possible to define the number of examples in the output returned the mapped function. This number can vary between the successive batches processed by the mapped function but in a single batch, all fields of the output dictionnary should have the same number of elements.

Let's show how we can implemented the two simple examples we mentioned: "cutting examples which are too long in several snippets" and do some "data augmentation".

We'll start by chunking the ``sentence1`` field of our dataset in chunk of 50 characters and stack all these chunks to make our new dataset.

We will also remove all the columns of the dataset and only keep the chunks in order to avoid the issue of uneven field lengths mentioned in the above note (we could also duplicate the other fields to compensated but let's make it as simple as possible here):

.. code-block::

    >>> def chunk_examples(examples):
    ...     chunks = []
    ...     for sentence in examples['sentence1']:
    ...         chunks += [sentence[i:i + 50] for i in range(0, len(sentence), 50)]
    ...     return {'chunks': chunks}
    ... 
    >>> chunked_dataset = dataset.map(chunk_examples, batched=True, remove_columns=dataset.column_names)
    >>> chunked_dataset
    Dataset(schema: {'chunks': 'string'}, num_rows: 10470)
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

As we can see, our dataset is now much longer (10470 row) and contains a single column with chunks of 50 characters. Some chunks are smaller since they are the last part of the sentences which were smaller than 50 characters. We could then filter them with :func:`nlp.Dataset.filter` for instance.

Now let's finish with the other example and try to do some data augmentation. We will use a Roberta model to sample some masked tokens.

Here we can use the `FillMaskPipeline of transformers <https://huggingface.co/transformers/main_classes/pipelines.html?#transformers.pipeline>`__ to generate options for a masked token in a sentence.

We will randomly select a word to mask in the sentence and return the original sentence plus the two top replacements by Roberta.

Since the Roberta model is quite large to run on a small laptop CPU, we will restrict this example to a small dataset of 100 examples and we will lower the batch size to be able to follow the processing more precisely.

.. code-block::

    >>> from random import randint
    >>> from transformers import pipeline
    >>> 
    >>> fillmask = pipeline('fill-mask')
    >>> mask_token = fillmask.tokenizer.mask_token
    >>> smaller_dataset = dataset.filter(lambda e, i: i<100, with_indices=True)
    >>> 
    >>> def augment_data(examples):
    ...     outputs = []
    ...     for sentence in examples['sentence1']:
    ...         words = sentence.split(' ')
    ...         K = randint(1, len(words)-1)
    ...         masked_sentence = " ".join(words[:K]  + [mask_token] + words[K+1:])
    ...         predictions = fillmask(masked_sentence)
    ...         augmented_sequences = [predictions[i]['sequence']for i in range(3)]
    ...         outputs += [sentence] + augmented_sequences
    ...     
    ...     return {'data': outputs}
    ... 
    >>> augmented_dataset = smaller_dataset.map(augment_data, batched=True, remove_columns=dataset.column_names, batch_size=8)
    >>> len(augmented_dataset)
    400
    >>> augmented_dataset[:9]['data']
    ['Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     'Amrozi accused his brother, whom he called " the witness ", of deliberately withholding his evidence.',
     'Amrozi accused his brother, whom he called " the witness ", of deliberately suppressing his evidence.',
     'Amrozi accused his brother, whom he called " the witness ", of deliberately destroying his evidence.',
     "Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .",
     'Yucaipa owned Dominick Stores before selling the chain to Safeway in 1998 for $ 2.5 billion.',
     "Yucaipa owned Dominick's before selling the chain to Safeway in 1998 for $ 2.5 billion.", 
     'Yucaipa owned Dominick Pizza before selling the chain to Safeway in 1998 for $ 2.5 billion.']

Here we have now multiply the size of our dataset by ``4`` by adding three alternatives generated with Roberta to each example.  We can see that the word ``distorting`` in the first example was augmented with other possibilities by the Roberta model: ``withholding``, ``suppressing``, ``destroying``, while in the second sentence, it was the ``'s`` token which was randomly sampled and replaced by ``Stores`` and ``Pizza``.

Obviously this is a very simple example for data augmentation and it could be improved in several ways, the most interesting take-aways is probably how this can be written in roughtly ten lines of code without any loss in flexibility.

Processing several splits at once
-----------------------------------

When you load a dataset that has various splits, :func:`nlp.load_dataset` returns a :obj:`nlp.DatasetDict` that is a dictionary with split names as keys ('train', 'test' for example), and :obj:`nlp.Dataset` objects as values.
You can directly call map, filter, shuffle, and sort directly on a :obj:`nlp.DatasetDict` object:

.. code-block::

    >>> from nlp import load_dataset
    >>>
    >>> dataset = load_dataset('glue', 'mrpc')  # load all the splits
    >>> dataset.keys()
    dict_keys(['train', 'validation', 'test'])
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

This concludes our chapter on data processing with 🤗nlp (and 🤗transformers).

Controling the cache behavior
-----------------------------------

[UNDER CONSTRUCTION]
