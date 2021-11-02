Load
====

You have already seen how to load a dataset from the Hugging Face Hub. But datasets are stored in a variety of places, and sometimes you won't find the one you want on the Hub. A dataset can be on disk on your local machine, in a Github repository, and in in-memory data structures like Python dictionaries and Pandas DataFrames. Wherever your dataset may be stored, 🤗 Datasets provides a way for you to load and use it for training.

This guide will show you how to load a dataset from:

* The Hub without a dataset loading script
* Local files
* In-memory data
* Offline
* A specific slice of a split

You will also learn how to troubleshoot common errors, and how to load specific configurations of a metric.

.. _load-from-the-hub:

Hugging Face Hub
----------------

In the tutorial, you learned how to load a dataset from the Hub. This method relies on a dataset loading script that downloads and builds the dataset. However, you can also load a dataset from any dataset repository on the Hub **without** a loading script! 

First, create a dataset repository and upload your data files. Then you can use :func:`datasets.load_dataset` like you learned in the tutorial. For example, load the files from this `demo repository <https://huggingface.co/datasets/lhoestq/demo1>`_ by providing the repository namespace and dataset name:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('lhoestq/demo1')

This dataset repository contains CSV files, and this code loads all the data from the CSV files.

Some datasets may have more than one version, based on Git tags, branches or commits. Use the ``revision`` flag to specify which dataset version you want to load:

.. code-block::

   >>> dataset = load_dataset(
   >>>   "lhoestq/custom_squad",
   >>>   revision="main"  # tag name, or branch name, or commit hash
   >>> )

.. seealso::

   Refer to the :ref:`upload_dataset_repo` guide for more instructions on how to create a dataset repository on the Hub, and how to upload your data files.

If the dataset doesn't have a dataset loading script, then by default, all the data will be loaded in the ``train`` split. Use the ``data_files`` parameter to map data files to splits like ``train``, ``validation`` and ``test``:

.. code-block::

   >>> data_files = {"train": "train.csv", "test": "test.csv"}
   >>> dataset = load_dataset("namespace/your_dataset_name", data_files=data_files)

.. important::

   If you don't specify which data files to use, ``load_dataset`` will return all the data files. This can take a long time if you are loading a large dataset like C4, which is approximately 13TB of data.

You can also load a specific subset of the files with the ``data_files`` parameter. The example below loads files from the `C4 dataset <https://huggingface.co/datasets/allenai/c4>`_:

.. code-block::

   >>> from datasets import load_dataset
   >>> c4_subset = load_dataset('allenai/c4', data_files='en/c4-train.0000*-of-01024.json.gz')

Specify a custom split with the ``split`` parameter:

.. code-block::

   >>> data_files = {"validation": "en/c4-validation.*.json.gz"}
   >>> c4_validation = load_dataset("allenai/c4", data_files=data_files, split="validation")

Local and remote files
-----------------------

🤗 Datasets can be loaded from local files stored on your computer, and also from remote files. The datasets are most likely stored as a ``csv``, ``json``, ``txt`` or ``parquet`` file. The :func:`datasets.load_dataset` method is able to load each of these file types.

CSV
^^^

🤗 Datasets can read a dataset made up of one or several CSV files:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('csv', data_files='my_file.csv')

If you have more than one CSV file:

.. code::

   >>> dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv', 'my_file_3.csv'])

You can also map the training and test splits to specific CSV files:

.. code::

   >>> dataset = load_dataset('csv', data_files={'train': ['my_train_file_1.csv', 'my_train_file_2.csv'] 'test': 'my_test_file.csv'})

To load remote CSV files via HTTP, you can pass the URLs:

.. code::

   >>> base_url = "https://huggingface.co/datasets/lhoestq/demo1/resolve/main/data/"
   >>> dataset = load_dataset('csv', data_files={'train': base_url + 'train.csv', 'test': base_url + 'test.csv'})

JSON
^^^^

JSON files are loaded directly with :func:`datasets.load_dataset` as shown below:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('json', data_files='my_file.json')

JSON files can have diverse formats, but we think the most efficient format is to have multiple JSON objects; each line represents an individual row of data. For example:

.. code-block::

   {"a": 1, "b": 2.0, "c": "foo", "d": false}
   {"a": 4, "b": -5.5, "c": null, "d": true}

Another JSON format you may encounter is a nested field, in which case you will need to specify the ``field`` argument as shown in the following:

.. code-block::

   {"version": "0.1.0",
       "data": [{"a": 1, "b": 2.0, "c": "foo", "d": false},
               {"a": 4, "b": -5.5, "c": null, "d": true}]
   }
    
   >>> from datasets import load_dataset
   >>> dataset = load_dataset('json', data_files='my_file.json', field='data')

To load remote JSON files via HTTP, you can pass the URLs:

.. code-block::

   >>> base_url = "https://rajpurkar.github.io/SQuAD-explorer/dataset/"
   >>> dataset = load_dataset('json', data_files={'train': base_url + 'train-v1.1.json', 'validation': base_url + 'dev-v1.1.json'}, field="data")

While these are the most common JSON formats, you will see other datasets that are formatted differently. 🤗 Datasets recognizes these other formats, and will fallback accordingly on the Python JSON loading methods to handle them.

Text files
^^^^^^^^^^

Text files are one of the most common file types for storing a dataset. 🤗 Datasets will read the text file line by line to build the dataset.

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('text', data_files={'train': ['my_text_1.txt', 'my_text_2.txt'], 'test': 'my_test_file.txt'})

To load remote TXT files via HTTP, you can pass the URLs:

.. code-block::

   >>> dataset = load_dataset('text', data_files='https://huggingface.co/datasets/lhoestq/test/resolve/main/some_text.txt')

Parquet
^^^^^^^

Parquet files are stored in a columnar format unlike row-based files like CSV. Large datasets may be stored in a Parquet file because it is more efficient, and faster at returning your query. Load a Parquet file as shown in the following example:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset("parquet", data_files={'train': 'train.parquet', 'test': 'test.parquet'})

To load remote parquet files via HTTP, you can pass the URLs:

   >>> base_url = "https://storage.googleapis.com/huggingface-nlp/cache/datasets/wikipedia/20200501.en/1.0.0/"
   >>> data_files = {"train": base_url + "wikipedia-train.parquet"}
   >>> wiki = load_dataset("parquet", data_files=data_files, split="train")

In-memory data
--------------

🤗 Datasets will also allow you to create a :class:`datasets.Dataset` directly from in-memory data structures like Python dictionaries and Pandas DataFrames.

Python dictionary
^^^^^^^^^^^^^^^^^

Load Python dictionaries with :func:`datasets.Dataset.from_dict`:

.. code-block::

   >>> from datasets import Dataset
   >>> my_dict = {"a": [1, 2, 3]}
   >>> dataset = Dataset.from_dict(my_dict)

Pandas DataFrame
^^^^^^^^^^^^^^^^

Load Pandas DataFrames with :func:`datasets.Dataset.from_pandas`:

.. code-block::

   >>> from datasets import Dataset
   >>> import pandas as pd
   >>> df = pd.DataFrame({"a": [1, 2, 3]})
   >>> dataset = Dataset.from_pandas(df)

.. important::

   An object data type in `pandas.Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_ doesn't always carry enough information for Arrow to automatically infer a data type. For example, if a DataFrame is of length 0 or the Series only contains None/nan objects, the type is set to null. Avoid potential errors by constructing an explicit schema with :class:`datasets.Features` using the ``from_dict`` or ``from_pandas`` methods. See the :ref:`troubleshoot` for more details on how to explicitly specify your own features.

Offline
-------

Even if you don't have an internet connection, it is still possible to load a dataset. As long as you've downloaded a dataset from the Hub or 🤗 Datasets GitHub repository before, it should be cached. This means you can reload the dataset from the cache and use it offline.

If you know you won't have internet access, you can run 🤗 Datasets in full offline mode. This saves time because instead of waiting for the Dataset builder download to time out, 🤗 Datasets will look directly in the cache. Set the environment variable ``HF_DATASETS_OFFLINE`` to ``1`` to enable full offline mode.

Slice splits
------------

For even greater control over how to load a split, you can choose to only load specific slices of a split. There are two options for slicing a split: using strings or :class:`datasets.ReadInstruction`. Strings are more compact and readable for simple cases, while :class:`datasets.ReadInstruction` is easier to use with variable slicing parameters.

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

You can even select a combination of percentages from each split:

.. tab:: String API

   >>> train_10_80pct_ds = datasets.load_dataset('bookcorpus', split='train[:10%]+train[-80%:]')

.. tab:: ReadInstruction

   >>> ri = (datasets.ReadInstruction('train', to=10, unit='%') + datasets.ReadInstruction('train', from_=-80, unit='%'))
   >>> train_10_80pct_ds = datasets.load_dataset('bookcorpus', split=ri)

Finally, create cross-validated dataset splits by:

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

For datasets where the requested slice boundaries do not divide evenly by 100, the default behavior is to round the boundaries to the nearest integer. As a result, some slices may contain more examples than others as shown in the following example:

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

.. _troubleshoot:

Troubleshooting
---------------

Sometimes, you may get unexpected results when you load a dataset. In this section, you will learn how to solve two common issues you may encounter when you load a dataset: manually download a dataset, and specify features of a dataset.

Manual download
^^^^^^^^^^^^^^^

Certain datasets require you to manually download the dataset files due to licensing incompatibility, or if the files are hidden behind a login page. This will cause :func:`datasets.load_dataset` to throw an ``AssertionError``. But 🤗 Datasets provides detailed instructions for downloading the missing files. After you have downloaded the files, use the ``data_dir`` argument to specify the path to the files you just downloaded.

For example, if you try to download a configuration from the `MATINF <https://huggingface.co/datasets/matinf>`_ dataset:

.. code-block::

   >>> dataset = load_dataset("matinf", "summarization")
   Downloading and preparing dataset matinf/summarization (download: Unknown size, generated: 246.89 MiB, post-processed: Unknown size, total: 246.89 MiB) to /root/.cache/huggingface/datasets/matinf/summarization/1.0.0/82eee5e71c3ceaf20d909bca36ff237452b4e4ab195d3be7ee1c78b53e6f540e...
   AssertionError: The dataset matinf with config summarization requires manual data. 
   Please follow the manual download instructions: To use MATINF you have to download it manually. Please fill this google form (https://forms.gle/nkH4LVE4iNQeDzsc9). You will receive a download link and a password once you complete the form. Please extract all files in one folder and load the dataset with: `datasets.load_dataset('matinf', data_dir='path/to/folder/folder_name')`. 
   Manual data can be loaded with `datasets.load_dataset(matinf, data_dir='<path/to/manual/data>')

Specify features
^^^^^^^^^^^^^^^^

When you create a dataset from local files, the :class:`datasets.Features` are automatically inferred by `Apache Arrow <https://arrow.apache.org/docs/>`_. However, the features of the dataset may not always align with your expectations or you may want to define the features yourself. 

The following example shows how you can add custom labels with :class:`datasets.ClassLabel`. First, define your own labels using the :class:`datasets.Features` class:

.. code-block::

   >>> class_names = ["sadness", "joy", "love", "anger", "fear", "surprise"]
   >>> emotion_features = Features({'text': Value('string'), 'label': ClassLabel(names=class_names)})

Next, specify the ``features`` argument in :func:`datasets.load_dataset` with the features you just created:

.. code::

   >>> dataset = load_dataset('csv', data_files=file_dict, delimiter=';', column_names=['text', 'label'], features=emotion_features)

Now when you look at your dataset features, you can see it uses the custom labels you defined:

.. code::

   >>> dataset['train'].features
   {'text': Value(dtype='string', id=None),
   'label': ClassLabel(num_classes=6, names=['sadness', 'joy', 'love', 'anger', 'fear', 'surprise'], names_file=None, id=None)}

Metrics
-------

When the metric you want to use is not supported by 🤗 Datasets, you can write and use your own metric script. Load your metric by providing the path to your local metric loading script:

.. code-block::

   >>> from datasets import load_metric
   >>> metric = load_metric('PATH/TO/MY/METRIC/SCRIPT')

   >>> # Example of typical usage
   >>> for batch in dataset:
   ...     inputs, references = batch
   ...     predictions = model(inputs)
   ...     metric.add_batch(predictions=predictions, references=references)
   >>> score = metric.compute()

.. seealso::

   See the :ref:`metric_script` guide for more details on how to write your own metric loading script.

Load configurations
^^^^^^^^^^^^^^^^^^^

It is possible for a metric to have different configurations. The configurations are stored in the :attr:`datasets.Metric.config_name` attribute. When you load a metric, provide the configuration name as shown in the following:

.. code-block::

   >>> from datasets import load_metric
   >>> metric = load_metric('bleurt', name='bleurt-base-128')
   >>> metric = load_metric('bleurt', name='bleurt-base-512')

Distributed setup
^^^^^^^^^^^^^^^^^

When you work in a distributed or parallel processing environment, loading and computing a metric can be tricky because these processes are executed in parallel on separate subsets of the data. 🤗 Datasets supports distributed usage with a few additional arguments when you load a metric.

For example, imagine you are training and evaluating on eight parallel processes. Here's how you would load a metric in this distributed setting:

1. Define the total number of processes with the ``num_process`` argument.

2. Set the process ``rank`` as an integer between zero and ``num_process - 1``. 

3. Load your metric with :func:`datasets.load_metric` with these arguments:

.. code-block::

   >>> from datasets import load_metric
   >>> metric = load_metric('glue', 'mrpc', num_process=num_process, process_id=rank)

.. tip::

   Once you've loaded a metric for distributed usage, you can compute the metric as usual. Behind the scenes, :func:`datasets.Metric.compute` gathers all the predictions and references from the nodes, and computes the final metric.

In some instances, you may be simultaneously running multiple independent distributed evaluations on the same server and files. To avoid any conflicts, it is important to provide an ``experiment_id`` to distinguish the separate evaluations:

.. code-block::

   >>> from datasets import load_metric
   >>> metric = load_metric('glue', 'mrpc', num_process=num_process, process_id=process_id, experiment_id="My_experiment_10")