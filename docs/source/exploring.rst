What's in the Dataset object
==============================================================


The :class:`datasets.Dataset` object that you get when you execute for instance the following commands:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('glue', 'mrpc', split='train')

behaves like a normal python container. You can query its length, get rows, columns and also lot of metadata on the dataset (description, citation, split sizes, etc).

In this guide we will detail what's in this object and how to access all the information.

An :class:`datasets.Dataset` is a python container with a length coresponding to the number of examples in the dataset. You can access a single example by its index. Let's query the first sample in the dataset:

.. code-block::

    >>> len(dataset)
    3668
    >>> dataset[0]
    {'idx': 0,
     'label': 1,
     'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .'}

Features and columns
------------------------------------------------------

A :class:`datasets.Dataset` instance is more precisely a table with **rows** and **columns** in which the columns are typed. Querying an example (a single row) will thus return a python dictionary with keys corresponding to column names, and values corresponding to the example's value for each column.

You can get the number of rows and columns of the dataset with various standard attributes:

.. code-block::

    >>> dataset.shape
    (3668, 4)
    >>> dataset.num_columns
    4
    >>> dataset.num_rows
    3668
    >>> len(dataset)
    3668

You can list the column names with :func:`datasets.Dataset.column_names` and get their detailed types (called ``features``) with :attr:`datasets.Dataset.features`:

.. code-block::

    >>> dataset.column_names
    ['idx', 'label', 'sentence1', 'sentence2']
    >>> dataset.features
    {'idx': Value(dtype='int32', id=None),
     'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
     'sentence1': Value(dtype='string', id=None),
     'sentence2': Value(dtype='string', id=None),
    }

Here we can see that the column ``label`` is a :class:`datasets.ClassLabel` feature.

We can access this feature to get more information on the values in the ``label`` columns. In particular, a :class:`datasets.ClassLabel` feature provides a mapping from integers (as single integer, lists, numpy arrays or even pytorch/tensorflow tensors) to human-readable names and vice-versa:

.. code-block::

    >>> dataset.features['label'].num_classes
    2
    >>> dataset.features['label'].names
    ['not_equivalent', 'equivalent']
    >>> dataset.features['label'].str2int('equivalent')
    1
    >>> dataset.features['label'].str2int('not_equivalent')
    0

More details on the ``features`` can be found in the guide on :doc:`features` and in the package reference on :class:`datasets.Features`.

Metadata
------------------------------------------------------

The :class:`datasets.Dataset` object also host many important metadata on the dataset which are all stored in ``dataset.info``. Many of these metadata are also accessible on the lower level, i.e. directly as attributes of the Dataset for shorter access (e.g. ``dataset.info.features`` is also available as ``dataset.features``).

All these attributes are listed in the package reference on :class:`datasets.DatasetInfo`. The most important metadata are ``split``, ``description``, ``citation``, ``homepage`` (and ``licence`` when this one is available).

.. code-block::

    >>> dataset.split
    NamedSplit('train')
    >>> dataset.description
    'GLUE, the General Language Understanding Evaluation benchmark\n(https://gluebenchmark.com/) is a collection of resources for training,\nevaluating, and analyzing natural language understanding systems.\n\n'
    >>> dataset.citation
    '@inproceedings{dolan2005automatically,\n  title={Automatically constructing a corpus of sentential paraphrases},\n  author={Dolan, William B and Brockett, Chris},\n  booktitle={Proceedings of the Third International Workshop on Paraphrasing (IWP2005)},\n  year={2005}\n}\n@inproceedings{wang2019glue,\n  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},\n  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},\n  note={In the Proceedings of ICLR.},\n  year={2019}\n}\n\nNote that each GLUE dataset has its own citation. Please see the source to see\nthe correct citation for each contained dataset.'
    >>> dataset.homepage
    'https://www.microsoft.com/en-us/download/details.aspx?id=52398'
    >>> dataset.license
    ''

Accessing ``dataset.info`` will give you all the metadata in a single object.

Cache files and memory-usage
------------------------------------------------------

Datasets are backed by Apache Arrow cache files.

You can check the current cache files backing the dataset with the ``cache_file`` property

.. code-block::

    >>> dataset.cache_files
    [{'filename': '/Users/thomwolf/.cache/huggingface/datasets/glue/mrpc/1.0.0/glue-train.arrow'}]

Using cache files allows:

- to load arbitrary large datasets by using memory mapping (as long as the datasets can fit on the drive)
- to use a fast backend to process the dataset efficiently
- to do smart caching by storing and reusing the results of operations performed on the drive

Let's see how big is our dataset and how much RAM loading it requires:

.. code-block::

    >>> from datasets import total_allocated_bytes
    >>> print("The number of bytes allocated on the drive is", dataset.dataset_size)
    The number of bytes allocated on the drive is 1492156
    >>> print("For comparison, here is the number of bytes allocated in memory:", total_allocated_bytes())
    For comparison, here is the number of bytes allocated in memory: 0

This is not a typo. The dataset is memory-mapped on the drive and requires no space in RAM for storage. This memory-mapping is done using a zero-deserialization-cost format so the speed of reading/writing is usually really high as well.

You can clean up the cache files in the current dataset directory (only keeping the currently used one) with :func:`datasets.Dataset.cleanup_cache_files`:

.. code-block::

    >>> dataset.cleanup_cache_files()  # Returns the number of removed cache files
    2

.. note::

    Be careful to check that no other process might be using other cache files when running this command.


Getting rows, slices, batches and columns
------------------------------------------------------

While you can access a single row with the ``dataset[i]`` pattern, you can also access several rows using slice notation or with a list of indices (or a numpy/torch/tf array of indices):

.. code-block::

    >>> dataset[:3]
    {'idx': [0, 1, 2],
     'label': [1, 0, 1],
     'sentence1': ['Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .', "Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .", 'They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .'],
     'sentence2': ['Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .', "Yucaipa bought Dominick 's in 1995 for $ 693 million and sold it to Safeway for $ 1.8 billion in 1998 .", "On June 10 , the ship 's owners had published an advertisement on the Internet , offering the explosives for sale ."]
    }
    >>> dataset[[1, 3, 5]]
    {'idx': [1, 3, 5],
     'label': [0, 0, 1], 
     'sentence1': ["Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .", 'Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .', 'Revenue in the first quarter of the year dropped 15 percent from the same period a year earlier .'],
     'sentence2': ["Yucaipa bought Dominick 's in 1995 for $ 693 million and sold it to Safeway for $ 1.8 billion in 1998 .", 'Tab shares jumped 20 cents , or 4.6 % , to set a record closing high at A $ 4.57 .', "With the scandal hanging over Stewart 's company , revenue the first quarter of the year dropped 15 percent from the same period a year earlier ."]
    }


You can also get a full column by querying its name as a string. This will return a list of elements:

.. code-block::

    >>> dataset['sentence1'][:3]
    ['Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .', "Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .", 'They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .']

As you can see depending on the object queried (single row, batch of rows or column), the returned object is different:

- a single row like ``dataset[0]`` will be returned as a python dictionary of values,
- a batch like ``dataset[5:10]``) will be returned as a python dictionary of lists of values,
- a column like ``dataset['sentence1']`` will be returned as a python lists of values.

This may seems surprising at first but in our experiments it's actually easier to use these various format for data processing than returning the same format for each of these views on the dataset.

In particular, you can easily select a specific column in batches, and also naturally permute rows and column indexings with identical results:

.. code-block::

    >>> dataset[0]['sentence1'] == dataset['sentence1'][0]
    True
    >>> dataset[2:5]['sentence1'] == dataset['sentence1'][2:5]
    True


Working with NumPy, pandas, PyTorch, TensorFlow and on-the-fly formatting transforms
------------------------------------------------------------------------------------

Up to now, the rows/batches/columns returned when querying the elements of the dataset were python objects.

Sometimes we would like to have more sophisticated objects returned by our dataset, for instance NumPy arrays or PyTorch tensors instead of python lists.

🤗Datasets provides a way to do that through what is called a ``format``.

While the internal storage of the dataset is always the Apache Arrow format, by setting a specific format on a dataset, you can filter some columns and cast the output of :func:`datasets.Dataset.__getitem__` in NumPy/pandas/PyTorch/TensorFlow, on-the-fly.

A specific format can be activated with :func:`datasets.Dataset.set_format`.

:func:`datasets.Dataset.set_format` accepts those inputs to control the format of the dataset:

- :obj:`type` (``Union[None, str]``, default to ``None``) defines the return type for the dataset :obj:`__getitem__` method and is one of ``[None, 'numpy', 'pandas', 'torch', 'tensorflow']`` (``None`` means return python objects),
- :obj:`columns` (``Union[None, str, List[str]]``, default to ``None``) defines the columns returned by :obj:`__getitem__` and takes the name of a column in the dataset or a list of columns to return (``None`` means return all columns),
- :obj:`output_all_columns` (``bool``, default to ``False``) controls whether the columns which cannot be formatted (e.g. a column with ``string`` cannot be cast in a PyTorch Tensor) are still outputted as python objects.
- :obj:`format_kwargs` can be used to provide additional keywords arguments that will be forwarded to the convertiong function like ``np.array``, ``torch.tensor`` or ``tensorflow.ragged.constant``. For instance, to create ``torch.Tensor`` directly on the GPU you can specify ``device='cuda'``.

.. note::

    The format is only applied to a single row or batches of rows (i.e. when querying :obj:`dataset[0]` or :obj:`dataset[10:20]`). Querying a column (e.g. :obj:`dataset['sentence1']`) will return the column even if it's filtered by the format. In this case the un-formatted column is returned.
    This design choice was made because it's quite rare to use column-only access when working with deep-learning frameworks and it's quite usefull to be able to access column even when they are masked by the format.

Here is an example:

.. code-block::

    >>> dataset.set_format(type='torch', columns=['label'])
    >>> dataset[0]
    {'label': tensor(1)}

It's also possible to use :func:`datasets.Dataset.with_format` instead, to get a new dataset object with the specified format.

The current format of the dataset can be queried with ``datasets.Dataset.format`` and can be reset to the original format (python and no column filtered) with :func:`datasets.Dataset.reset_format`:

.. code-block::

    >>> dataset.format
    {'type': 'torch', 'format_kwargs': {}, 'columns': ['label'], 'output_all_columns': False}
    >>> dataset.reset_format()
    >>> dataset.format
    {'type': 'python', 'format_kwargs': {}, 'columns': ['idx', 'label', 'sentence1', 'sentence2'], 'output_all_columns': False}

You can also define your own formatting transform that is applied on-the-fly. To do so you can use :func:`datasets.Dataset.set_transform`. It replaces any format that may have been defined beforehand.
A formatting transform is a callable that takes a batch (as a dict) as input and returns a batch.

Here is an example to tokenize and pad tokens on-the-fly when accessing the samples:

.. code-block::

    >>> from transformers import BertTokenizer
    >>> tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    >>> def encode(batch):
    >>>     return tokenizer(batch["sentence1"], padding="longest", truncation=True, max_length=512, return_tensors="pt")
    >>> dataset.set_transform(encode)
    >>> dataset.format
    {'type': 'custom', 'format_kwargs': {'transform': <function __main__.encode(batch)>}, 'columns': ['idx', 'label', 'sentence1', 'sentence2'], 'output_all_columns': False}
    >>> dataset[:2]
    {'input_ids': tensor([[  101,  2572,  3217, ... 102]]), 'token_type_ids': tensor([[0, 0, 0, ... 0]]), 'attention_mask': tensor([[1, 1, 1, ... 1]])}

It’s also possible to use :func:`datasets.Dataset.with_transform` instead, to get a new dataset object with the specified transform.

Since the formatting function is applied on-the-fly, your original data are intact:

.. code-block::

    >>> dataset.reset_format()
    >>> dataset[0]
    {'idx': 0, 'label': 1, 'sentence1': 'Amrozi accused his [...] evidence .', 'sentence2': 'Referring to him [...] evidence .'}
