Load
====

You have already seen how you can load a dataset from the Datasets Hub. But datasets are stored in a variety of places, and sometimes you won't find the one you want on the Hub. The datasets can be on your local machine, in a Github repository, and in data structures like Python dictionaries and Pandas DataFrames. Wherever your dataset may be stored, Datasets provides a way for you to load it and use it for training.

This guides shows you how to load a dataset from:

* local files
* in-memory data
* in streaming mode
* offline
* a specific slice of a split

Local files
-----------

Datasets can be loaded from local files stored on your computer. The datasets most likely exist as a ``csv``, ``json`` or ``txt`` file. Datasets provides the :func:`datasets.load_dataset` method for loading these file types.

CSV
^^^

Datasets can read a dataset made up of one or several CSV files.

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('csv', data_files='my_file.csv')

If you have more than one ``csv`` file:

    >>> dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv', 'my_file_3.csv'])

You can also map the training and test splits to specific ``csv`` files:

    >>> dataset = load_dataset('csv', data_files={'train': ['my_train_file_1.csv', 'my_train_file_2.csv'],
                                                  'test': 'my_test_file.csv'})

JSON
^^^^

``json`` files can be loaded directly as shown below:

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('json', data_files='my_file.json')

``json`` files can have diverse formats, but we think the most efficient ``json`` format is to have multiple ``json`` objects; each line represents an individual row of data. For example:

.. code-block::

    {"a": 1, "b": 2.0, "c": "foo", "d": false}
    {"a": 4, "b": -5.5, "c": null, "d": true}

Another common ``json`` format you may encounter is a nested field. In this situation, you will need to specify the ``field`` argument as shown in the following:

.. code-block::

    {"version": "0.1.0",
     "data": [{"a": 1, "b": 2.0, "c": "foo", "d": false},
              {"a": 4, "b": -5.5, "c": null, "d": true}]
    }

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('json', data_files='my_file.json', field='data')

While these are the most common formats, you may encounter other datasets that are stored differently. Datasets will recognize this, and fallback accordingly on the Python ``json`` loading methods to handle the various formats.

Text files
^^^^^^^^^^

Text files are one of the most common methods for storing a dataset. Datasets will read the text file line by line to build the dataset.

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('text', data_files={'train': ['my_text_1.txt', 'my_text_2.txt'], 'test': 'my_test_file.txt'})

In-memory data
--------------

Datasets will also allow you to create a Dataset directly from in-memory data structures. Currently, Datasets supports loading data directly from Python dictionaries and Pandas DataFrames.

Python dictionary
^^^^^^^^^^^^^^^^^

Python dictionaries can be loaded using the :func:`datasets.Dataset.from_dict()` method:

    >>> from datasets import Dataset
    >>> dataset = Dataset.from_dict(my_dict)

Pandas DataFrame
^^^^^^^^^^^^^^^^

Likewise, datasets in Pandas DataFrames can be instantiated by:

    >>> from datasets import Dataset
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2, 3]})
    >>> dataset = Dataset.from_pandas(df)

.. important::

    An object data type in pandas.Series doesn't always carry enough information for Arrow to automatically infer a type. Avoid this by constructing an explicit schema with :class:`datasets.Features` using the ``from_dict`` or ``from_pandas`` methods. See the Troubleshooting guide below for more details on how to specify a feature.

Streaming
--------------

Streaming a dataset is useful when you want to start using the dataset without having to wait to download the entire dataset. It also allows you to work with datasets that exceed the amount of disk space on your computer. The data is downloaded progressively as you iterate over the dataset. 

Stream a dataset by setting ``streaming=True`` in ``load_dataset()`` as shown below:

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> print(next(iter(dataset)))
    {'text': 'Mtendere Village was inspired by the vision of Chief Napoleon Dzombe, which he shared with John Blanchard during his first visit to Malawi. Chief Napoleon conveyed the desperate need for a program to intervene and care for the orphans and vulnerable children (OVC) in Malawi, and John committed to help...

Offline
-------

Even if you don't have an internet connection, it is still possible to load a dataset. As long as you've downloaded a dataset from the Hub or Datasets Github repository, it should be cached. This means you can reload the dataset from the cache and use it offline.

If you know you won't have internet access, you can run Datasets in full offline mode. This saves time because instead of waiting for the Dataset builder download to time out, Datasets will look directly at the cache. Set the environment variable ``HF_DATASETS_OFFLINE`` to ``1`` to enable full offline mode.

Slice splits
------------

You already know how to load a specific split of a dataset. But if you want even more control over how to load a split, you can load a specific slice of your split. There are two options for slicing a split: using strings or ``ReadInstruction``. Strings are more compact and readable for simple cases, while ``ReadInstruction`` is easier to use with variable slicing parameters.

Concatenate the ``train`` and ``test`` split by:

.. tab:: String API

    >>> train_test_ds = datasets.load_dataset('bookcorpus', split='train+test')

.. tab:: ReadInstruction

    >>> ri = datasets.ReadInstruction('train') + datasets.ReadInstruction('test')
    >>> train_test_ds = datasets.load_dataset('bookcorpus', split=ri)

Select specific rows of the ``train`` split:

.. tab:: String API

    >>> train_10_20_ds = datasets.load_dataset('bookcorpus', split='train[10:20]')

.. tab:: ReadInstruction

    >>> train_10_20_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction('train', from_=10, to=20, unit='abs'))

Or select a percentage of the split with:

.. tab:: String API

    >>> train_10pct_ds = datasets.load_dataset('bookcorpus', split='train[:10%]')

.. tab:: ReadInstruction

    >>> train_10_20_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction('train', to=10, unit='%'))

You can even select a combination of percentages of a split as shown in the following:

.. tab:: String API

    >>> train_10_80pct_ds = datasets.load_dataset('bookcorpus', split='train[:10%]+train[-80%:]')

.. tab:: ReadInstruction

    >>> ri = (datasets.ReadInstruction('train', to=10, unit='%') + datasets.ReadInstruction('train', from_=-80, unit='%'))
    >>> train_10_80pct_ds = datasets.load_dataset('bookcorpus', split=ri)

Datasets also supports creating cross-validated dataset splits:

.. tab:: String API

    >>> # 10-fold cross-validation (see also next section on rounding behavior):
    >>> # The validation datasets are each going to be 10%:
    >>> # [0%:10%], [10%:20%], ..., [90%:100%].
    >>> # And the training datasets are each going to be the complementary 90%:
    >>> # [10%:100%] (for a corresponding validation set of [0%:10%]),
    >>> # [0%:10%] + [20%:100%] (for a validation set of [10%:20%]), ...,
    >>> # [0%:90%] (for a validation set of [90%:100%]).
    >>> vals_ds = datasets.load_dataset('bookcorpus', split=[f'train[{k}%:{k+10}%]' for k in range(0, 100, 10)])
    >>> trains_ds = datasets.load_dataset('bookcorpus', split=[f'train[:{k}%]+train[{k+10}%:]' for k in range(0, 100, 10)])

.. tab:: ReadInstruction

    >>> # 10-fold cross-validation (see also next section on rounding behavior):
    >>> # The validation datasets are each going to be 10%:
    >>> # [0%:10%], [10%:20%], ..., [90%:100%].
    >>> # And the training datasets are each going to be the complementary 90%:
    >>> # [10%:100%] (for a corresponding validation set of [0%:10%]),
    >>> # [0%:10%] + [20%:100%] (for a validation set of [10%:20%]), ...,
    >>> # [0%:90%] (for a validation set of [90%:100%]).
    >>> vals_ds = datasets.load_dataset('bookcorpus', [datasets.ReadInstruction('train', from_=k, to=k+10, unit='%') for k in range(0, 100, 10)])
    >>> trains_ds = datasets.load_dataset('bookcorpus', [(datasets.ReadInstruction('train', to=k, unit='%') + datasets.ReadInstruction('train', from_=k+10, unit='%')) for k in range(0, 100, 10)])


Percent slicing and rounding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For Datasets where the requested slice boundaries do not divide evenly by 100, the default behavior is to round the boundaries to the nearest integer. As a result, some slices may contain more examples than others as shown in the following example:

.. code-block::

    # Assuming `train` split contains 999 records.
    # 19 records, from 500 (included) to 519 (excluded).
    >>> train_50_52_ds = datasets.load_dataset('bookcorpus', split='train[50%:52%]')
    # 20 records, from 519 (included) to 539 (excluded).
    >>> train_52_54_ds = datasets.load_dataset('bookcorpus', split='train[52%:54%]')

If you want equal sized splits, use ``pct1_dropremainder`` rounding instead. This will treat the specified percentage boundaries as multiples of 1%. 

.. code-block::

    # 18 records, from 450 (included) to 468 (excluded).
    >>> train_50_52pct1_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction( 'train', from_=50, to=52, unit='%', rounding='pct1_dropremainder'))
    # 18 records, from 468 (included) to 486 (excluded).
    >>> train_52_54pct1_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction('train',from_=52, to=54, unit='%', rounding='pct1_dropremainder'))
    # Or equivalently:
    >>> train_50_52pct1_ds = datasets.load_dataset('bookcorpus', split='train[50%:52%](pct1_dropremainder)')
    >>> train_52_54pct1_ds = datasets.load_dataset('bookcorpus', split='train[52%:54%](pct1_dropremainder)')

.. important::

    Using ``pct1_dropremainder`` rounding may truncate the last examples in a dataset if the number of examples in your dataset don't divide evenly by 100.

Troubleshooting
---------------

Sometimes, loading a dataset is not as simple as calling :func:`dataset.load_dataset`. In this section, you will learn how to solve two of the most common issues you may encounter when you load a dataset: manually download a dataset, and specify features of a dataset.

Manual download
^^^^^^^^^^^^^^^

Certain datasets will require you to manually download the dataset files due to licensing incompatibility or if the files are hidden behind a login page. This will cause :func:`dataset.load_dataset` to throw an ``AssertionError``. But Datasets provides detailed instructions for downloading the missing files. After you have downloaded the files, use the ``data_dir`` argument to specify the path to the files you just downloaded. For example, if you try to download the PAN-X.fr configuration from the `xtreme dataset <https://sites.research.google/xtreme>`_:

    >>> dataset = load_dataset("xtreme", "PAN-X.fr")
    Downloading and preparing dataset xtreme/PAN-X.fr (download: Unknown size, generated: 5.80 MiB, total: 5.80 MiB) to /Users/thomwolf/.cache/huggingface/datasets/xtreme/PAN-X.fr/1.0.0...
    AssertionError: The dataset xtreme with config PAN-X.fr requires manual data.
    Please follow the manual download instructions: You need to manually download the AmazonPhotos.zip file on Amazon Cloud Drive (https://www.amazon.com/clouddrive/share/d3KGCRCIYwhKJF0H3eWA26hjg2ZCRhjpEQtDL70FSBN). The folder containing the saved file can be used to load the dataset via 'datasets.load_dataset("xtreme", data_dir="<path/to/folder>")'

Specify features
^^^^^^^^^^^^^^^^

When you create a dataset from local files, the :class:`dataset.Features` are automatically generated by `Apache Arrow's Automatic Type Inference <https://arrow.apache.org/docs/python/json.html#automatic-type-inference>`_. However, the features of the dataset may not always align with your expectations or you may want to define the features yourself. 

The following example shows how you can add custom labels with :class:`datasets.ClassLabel`. First, define your own labels using the :class:`datasets.Features` class:

    >>> class_names = ["sadness", "joy", "love", "anger", "fear", "surprise"]
    >>> emotion_features = Features({'text': Value('string'), 'label': ClassLabel(names=class_names)})

Next, specify the ``features`` argument in :func:`dataset.load_dataset` with the features you just created:

    >>> dataset = load_dataset('csv', data_files=file_dict, delimiter=';', column_names=['text', 'label'], features=emotion_features)

Now when you look at the features of your dataset, you can see that it uses the custom labels you supplied:

    >>> dataset['train'].features
    {'text': Value(dtype='string', id=None),
    'label': ClassLabel(num_classes=6, names=['sadness', 'joy', 'love', 'anger', 'fear', 'surprise'], names_file=None, id=None)}

Metrics
-------

When the metric you want to use is not supported by Datasets, you can write and use your own metric script. Load it by providing the path to your local metric script:

    >>> from datasets import load_metric
    >>> metric = load_metric('PATH/TO/MY/METRIC/SCRIPT')
    >>>
    >>> # Example of typical usage
    >>> for batch in dataset:
    >>>     inputs, references = batch
    >>>     predictions = model(inputs)
    >>>     metric.add_batch(predictions=predictions, references=references)
    >>> score = metric.compute()

Load configurations
^^^^^^^^^^^^^^^^^^^

It is possible to specify different configurations for a metric. The different configurations are stored in the :attr:`datasets.Metric.config_name` attribute. When you load a metric, provide the configuration name as shown in the following:

    >>> from datasets import load_metric
    >>> metric = load_metric('bleurt', name='bleurt-base-128')
    >>> metric = load_metric('bleurt', name='bleurt-base-512')

Distributed setup
^^^^^^^^^^^^^^^^^

When you work in a distributed or parallel processing environment, loading and computing a metric can be tricky because these processes are executed on separate subsets of the data. Datasets supports distributed usage with a few additional arguments when you load a metric.

For example, imagine you are training and evaluating eight parallel processes. Here's how you would load a metric in this distributed setting:

1. Define the total numner of processes with the ``num_process`` argument.

2. Set the process ``rank`` as an integer between 0 and ``num_process - 1``. 

3. Load your metric with :func:`datasets.load_metric` with these arguments:

   >>> from datasets import load_metric
   >>> metric = load_metric('glue', 'mrpc', num_process=num_process, process_id=rank)

.. tip::

    Once you've loaded a metric for distributed usage, you can compute the metric as usual. Behind the scenes, :func:`datasets.Metric.compute` gathers all the predictions and references from the nodes, and computes the final metric.

In some instances, you may have be simulatenously running multiple independent distributed evaluations on the same server and files. To avoid any conflicts, it is important to provide an ``experiment_id`` to distinguish the separate evaluations:

   >>> from datasets import load_metric
   >>> metric = load_metric('glue', 'mrpc', num_process=num_process, process_id=process_id,experiment_id="My_experiment_10")