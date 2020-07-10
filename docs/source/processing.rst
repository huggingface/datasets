Processing data in a Dataset
==============================================================

🤗nlp provides many methods to modify a Dataset, be it to reorder, split or shuffle the dataset or to apply data processing functions or evaluation functions to its elements.

We'll start by presenting the methods which change the order or number of elements before presenting methods which access and can change the content of the elements themselves.

As always, let's start by loading a small dataset for our demonstrations:

.. code-block::

    >>> from nlp import load_dataset
    >>> dataset = load_dataset('glue', 'mrpc', split='train')

.. note::

    **No in-place policy**: all the methods in this page will return a :class:`nlp.Dataset` instance. No modification is done in-place and it's the thus responsibility of the user to decide to override the previous dataset with the newly returned one.

.. note::

    **Caching policy**: all the methods in this page will store the updated dataset in a cache file indexed by a hash of current state and all the argument used to call the method.

    A subsequent call to any of the methods detailed here like :func:`nlp.Dataset.sort`, :func:`nlp.Dataset.map`, etc will thus **reuse the cached file instead of recomputing the operation** (even in another python session).

    This usually makes it very efficient to process data with 🤗nlp.

    If the disk space is critical, these methods can be called with some options to avoid this behavior, or the cache files can be cleaned using the method :func:`nlp.Dataset.clean_cache_files`.


Selecting, sorting, shuffling, splitting rows
--------------------------------------------------

Several methods are provided to create one or several new dataset(s) from the current dataset by:

- sorting the dataset according to a column which should be a NumPy compatible type (:func:`nlp.Dataset.sort`)
- shuffling the dataset (:func:`nlp.Dataset.shuffle`)
- filtering rows either according to a list of indices (:func:`nlp.Dataset.select`) or with a filter function returning true for the rows to keep (:func:`nlp.Dataset.filter`),
- spliting the dataset in a (potentially shuffled) train and a test split (:func:`nlp.Dataset.train_test_split`),
- spliting the dataset in a deterministic list of shards (:func:`nlp.Dataset.shard`).

These methods have quite simple signature and should be for the most part self-explanatory.

Let's see them in action:

1. Sorting the dataset according to a NumPy compatible column (:func:`nlp.Dataset.sort`):

..code-block::

    >>> dataset['label'][:10]
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0]
    >>> sorted_dataset = dataset.sort('label')
    >>> sorted_dataset['label'][:10]
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> sorted_dataset['label'][-10:]
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

2. Shuffling the dataset (:func:`nlp.Dataset.shuffle`):

..code-block::

    >>> shuffled_dataset = sorted_dataset.shuffle(seed=42)
    >>> shuffled_dataset['label'][:10]
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0]

You can also provide a :obj:`numpy.random.Generator` to :func:`nlp.Dataset.shuffle` to control more finely the algorithm used to shuffle the dataset.

3. Filtering rows according to a list of indices (:func:`nlp.Dataset.select`) or with a filter function returning true for the rows to keep (:func:`nlp.Dataset.filter`):

..code-block::

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

4. Spliting the dataset in a train and a test split (:func:`nlp.Dataset.train_test_split`).

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

As you can see the test split is 10% of the original dataset.

The :func:`nlp.Dataset.train_test_split` has many ways to select the relative sizes of the train and test split so we refer the reader to the package reference of :func:`nlp.Dataset.train_test_split` for all the details.

5. Spliting the dataset in a deterministic list of shards (:func:`nlp.Dataset.shard`).

Eventually, it's possible to "shard" the dataset, i.e. divide it in a deterministic list of dataset of (almost) the same size.

The :func:`nlp.Dataset.shard` takes as arguments the total number of shards (:obj:`num_shards`) and the index of the currently requested shard (:obj:`index`)  and return a :class:`nlp.Dataset` instance constituted by the requested shard.

This method can be used to slice a very large dataset in a predefined number of chunks.

The map method
-------------------------

All the methods we seen up to now (excepted maybe the ``filter`` method) only operate on examples taken as a whole and don't inspect of modify the content of the samples.



Augmenting the dataset
---------------------------


