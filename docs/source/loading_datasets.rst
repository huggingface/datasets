Loading a Dataset
==============================================================

A :class:`datasets.Dataset` can be created from various sources of data:

- from the `Hugging Face Hub <https://huggingface.co/datasets>`__,
- from local or remote files, e.g. CSV/JSON/text/parquet/pandas files, or
- from in-memory data like python dict or a pandas dataframe.

In this section we study each option.

From the Hugging Face Hub
-------------------------------------------------

Over 1,000 datasets for many NLP tasks like text classification, question answering, language modeling, etc, are provided on the `Hugging Face Hub <https://huggingface.co/datasets>`__ and can be viewed and explored online with the `🤗 Datasets viewer <https://huggingface.co/datasets/viewer>`__.

.. note::

    You can also add a new dataset to the Hub to share with the community as detailed in the guide on :doc:`adding a new dataset </add_dataset>`.

All the datasets currently available on the `Hub <https://huggingface.co/datasets>`__ can be listed using :func:`datasets.list_datasets`:

.. code-block::

    >>> from datasets import list_datasets
    >>> datasets_list = list_datasets()
    >>> len(datasets_list)
    1103
    >>> print(', '.join(dataset for dataset in datasets_list))
    acronym_identification, ade_corpus_v2, adversarial_qa, aeslc, afrikaans_ner_corpus, ag_news, ai2_arc, air_dialogue, ajgt_twitter_ar,
    allegro_reviews, allocine, alt, amazon_polarity, amazon_reviews_multi, amazon_us_reviews, ambig_qa, amttl, anli, app_reviews, aqua_rat,
    aquamuse, ar_cov19, ar_res_reviews, ar_sarcasm, arabic_billion_words, arabic_pos_dialect, arabic_speech_corpus, arcd, arsentd_lev, art,
    arxiv_dataset, ascent_kb, aslg_pc12, asnq, asset, assin, assin2, atomic, autshumato, babi_qa, banking77, bbaw_egyptian, bbc_hindi_nli,
    bc2gm_corpus, best2009, bianet, bible_para, big_patent, billsum, bing_coronavirus_query_set, biomrc, blended_skill_talk, blimp,
    blog_authorship_corpus, bn_hate_speech [...]


To load a dataset from the Hub we use the :func:`datasets.load_dataset` command and give it the short name of the dataset you would like to load as listed above or on the `Hub <https://huggingface.co/datasets>`__.

Let's load the **SQuAD dataset for Question Answering**. You can explore this dataset and find more details about it `on the online viewer here <https://huggingface.co/datasets/viewer/?dataset=squad>`__ (which is actually just a wrapper on top of the :class:`datasets.Dataset` we will now create):

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('squad', split='train')

This call to :func:`datasets.load_dataset` does the following steps under the hood:

1. Download and import in the library the **SQuAD python processing script** from Hugging Face github repository or AWS bucket if it's not already stored in the library.

.. note::

    Processing scripts are small python scripts which define the info (citation, description) and format of the dataset and contain the URL to the original SQuAD JSON files and the code to load examples from the original SQuAD JSON files. You can find the SQuAD processing script `here <https://github.com/huggingface/datasets/tree/master/datasets/squad/squad.py>`__ for instance.

2. Run the SQuAD python processing script which will download the SQuAD dataset from the original URL (if it's not already downloaded and cached) and process and cache all SQuAD in a cache Arrow table for each standard split stored on the drive.

.. note::

    An Apache Arrow Table is the internal storing format for 🤗 Datasets. It allows to store an arbitrarily long dataframe,
    typed with potentially complex nested types that can be mapped to numpy/pandas/python types. Apache Arrow allows you
    to map blobs of data on-drive without doing any deserialization. So caching the dataset directly on disk can use
    memory-mapping and pay effectively zero cost with O(1) random access. Alternatively, you can copy it in CPU memory
    (RAM) by setting the ``keep_in_memory`` argument of :func:`datasets.load_dataset` to ``True``.
    The default in 🤗 Datasets is to memory-map the dataset on disk unless you set ``datasets.config.IN_MEMORY_MAX_SIZE``
    different from ``0`` bytes (default). In that case, the dataset will be copied in-memory if its size is smaller than
    ``datasets.config.IN_MEMORY_MAX_SIZE`` bytes, and memory-mapped otherwise. This behavior can be enabled by setting
    either the configuration option ``datasets.config.IN_MEMORY_MAX_SIZE`` (higher precedence) or the environment
    variable ``HF_DATASETS_IN_MEMORY_MAX_SIZE`` (lower precedence) to nonzero.

3. Return a **dataset built from the splits** asked by the user (default: all); in the above example we create a dataset with the train split.


Selecting a split
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't provide a :obj:`split` argument to :func:`datasets.load_dataset`, this method will return a dictionary containing a datasets for each split in the dataset.

.. code-block::

    >>> from datasets import load_dataset
    >>> datasets = load_dataset('squad')
    >>> print(datasets)
    DatasetDict({
        train: Dataset({
            features: ['id', 'title', 'context', 'question', 'answers'],
            num_rows: 87599
        })
        validation: Dataset({
            features: ['id', 'title', 'context', 'question', 'answers'],
            num_rows: 10570
        })
    })

The :obj:`split` argument can actually be used to control extensively the generated dataset split. You can use this argument to build a split from only a portion of a split in absolute number of examples or in proportion (e.g. :obj:`split='train[:10%]'` will load only the first 10% of the train split) or to mix splits (e.g. :obj:`split='train[:100]+validation[:100]'` will create a split from the first 100 examples of the train split and the first 100 examples of the validation split).

You can find more details on the syntax for using :obj:`split` on the :doc:`dedicated tutorial on split <./splits>`.

Selecting a configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some datasets comprise several :obj:`configurations`. A Configuration defines a sub-part of a dataset which can be selected. Unlike split, you have to select a single configuration for the dataset, you cannot mix several configurations. Examples of dataset with several configurations are:

- the **GLUE** dataset which is an agregated benchmark comprised of 10 subsets: COLA, SST2, MRPC, QQP, STSB, MNLI, QNLI, RTE, WNLI and the diagnostic subset AX.
- the **wikipedia** dataset which is provided for several languages.

When a dataset is provided with more than one :obj:`configuration`, you will be requested to explicitely select a configuration among the possibilities.

Selecting a configuration is done by providing :func:`datasets.load_dataset` with a :obj:`name` argument. Here is an example for **GLUE**:

.. code-block::

    >>> from datasets import load_dataset

    >>> dataset = load_dataset('glue')
    ValueError: Config name is missing.
    Please pick one among the available configs: ['cola', 'sst2', 'mrpc', 'qqp', 'stsb', 'mnli', 'mnli_mismatched', 'mnli_matched', 'qnli', 'rte', 'wnli', 'ax']
    Example of usage:
            `load_dataset('glue', 'cola')`

    >>> dataset = load_dataset('glue', 'sst2')
    Downloading and preparing dataset glue/sst2 (download: 7.09 MiB, generated: 4.81 MiB, total: 11.90 MiB) to /Users/thomwolf/.cache/huggingface/datasets/glue/sst2/1.0.0...
    Downloading: 100%|██████████████████████████████████████████████████████████████| 7.44M/7.44M [00:01<00:00, 7.03MB/s]
    Dataset glue downloaded and prepared to /Users/huggignface/.cache/huggingface/datasets/glue/sst2/1.0.0. Subsequent calls will reuse this data.
    >>> print(dataset)
    DatasetDict({
        train: Dataset({
            features: ['sentence', 'label', 'idx'],
            num_rows: 67349
        })
        validation: Dataset({
            features: ['sentence', 'label', 'idx'],
            num_rows: 872
        })
        test: Dataset({
            features: ['sentence', 'label', 'idx'],
            num_rows: 1821
        })
    })

Manually downloading files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some dataset require you to download manually some files, usually because of licencing issues or when these files are behind a login page.

In this case specific instruction for dowloading the missing files will be provided when running the script with :func:`datasets.load_dataset` for the first time to explain where and how you can get the files.

After you've downloaded the files, you can point to the folder hosting them locally with the :obj:`data_dir` argument as follows:

.. code-block::

    >>> dataset = load_dataset("xtreme", "PAN-X.fr")
    Downloading and preparing dataset xtreme/PAN-X.fr (download: Unknown size, generated: 5.80 MiB, total: 5.80 MiB) to /Users/thomwolf/.cache/huggingface/datasets/xtreme/PAN-X.fr/1.0.0...
    AssertionError: The dataset xtreme with config PAN-X.fr requires manual data.
    Please follow the manual download instructions: You need to manually download the AmazonPhotos.zip file on Amazon Cloud Drive (https://www.amazon.com/clouddrive/share/d3KGCRCIYwhKJF0H3eWA26hjg2ZCRhjpEQtDL70FSBN). The folder containing the saved file can be used to load the dataset via 'datasets.load_dataset("xtreme", data_dir="<path/to/folder>")'


Apart from :obj:`name` and :obj:`split`, the :func:`datasets.load_dataset` method provide a few arguments which can be used to control where the data is cached (:obj:`cache_dir`), some options for the download process it-self like the proxies and whether the download cache should be used (:obj:`download_config`, :obj:`download_mode`).

The use of these arguments is discussed in the :ref:`load_dataset_cache_management` section below. You can also find the full details on these arguments on the package reference page for :func:`datasets.load_dataset`.

From a community dataset on the Hugging Face Hub
-----------------------------------------------------------

The community shares hundreds of datasets on the Hugging Face Hub using **dataset repositories**.
A dataset repository is a versioned repository of data files.
Everyone can create a dataset repository on the Hugging Face Hub and upload their data.

For example we have created a demo dataset at https://huggingface.co/datasets/lhoestq/demo1.
In this dataset repository we uploaded some CSV files, and you can load the dataset with:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('lhoestq/demo1')

You can even choose which files to load from a dataset repository.
For example you can load a subset of the **C4 dataset for language modeling**, hosted by AllenAI on the Hub.
You can browse the dataset repository at https://huggingface.co/datasets/allenai/c4

In the following example we specify which subset of the files to use with the ``data_files`` parameter:

.. code-block::

    >>> from datasets import load_dataset
    >>> c4_subset = load_dataset('allenai/c4', data_files='en/c4-train.0000*-of-01024.json.gz')


You can also specify custom splits:

.. code-block::

    >>> data_files = {"validation": "en/c4-validation.*.json.gz"}
    >>> c4_validation = load_dataset("allenai/c4", data_files=data_files, split="validation")

In these examples, ``load_dataset`` will return all the files that match the Unix style pattern passed in ``data_files``.
If you don't specify which data files to use, it will use all the data files (here all C4 is about 13TB of data).


.. _loading-from-local-files:

From local or remote files
-----------------------------------------------------------

It's also possible to create a dataset from your own local or remote files.

Generic loading scripts are provided for:

- CSV files (with the :obj:`csv` script),
- JSON files (with the :obj:`json` script),
- text files (read as a line-by-line dataset with the :obj:`text` script),
- parquet files (with the :obj:`parquet` script).
- pandas pickled dataframe (with the :obj:`pandas` script).

If you want more fine-grained control on how your files are loaded or if you have a file format that matches the format for one of the datasets provided on the `Hugging Face Hub <https://huggingface.co/datasets>`__, it can be more  simpler to create **your own loading script**, from scratch or by adapting one of the provided loading scripts. In this case, please go check the :doc:`add_dataset` section.

The :obj:`data_files` argument in :func:`datasets.load_dataset` is used to provide paths to one or several data source files. This argument currently accepts three types of inputs:

- :obj:`str`: A single string as the path to a single file (considered to constitute the `train` split by default).
- :obj:`Sequence[str]`: A list of strings as paths to a list of files (also considered to constitute the `train` split by default).
- :obj:`Mapping[str, Union[str, Sequence[str]]`: A dictionary mapping splits names to a single file path or a list of file paths.

Let's see an example of all the various ways you can provide files to :func:`datasets.load_dataset`:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('csv', data_files='my_file.csv')
    >>> dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv', 'my_file_3.csv'])
    >>> dataset = load_dataset('csv', data_files={'train': ['my_train_file_1.csv', 'my_train_file_2.csv'],
                                                  'test': 'my_test_file.csv'})
    >>> base_url = 'https://huggingface.co/datasets/lhoestq/demo1/resolve/main/data/'
    >>> dataset = load_dataset('csv', data_files={'train': base_url + 'train.csv', 'test': base_url + 'test.csv'})

.. note::

    The :obj:`split` argument will work similarly to what we detailed above for the datasets on the Hub and you can find more details on the syntax for using :obj:`split` on the :doc:`dedicated tutorial on split <./splits>`. The only specific behavior related to loading local files is that if you don't indicate which split each files is related to, the provided files are assumed to belong to the **train** split.


.. note::

    If you use a private dataset repository on the Hub, you just need to pass ``use_auth_token=True`` to ``load_dataset`` after logging in with the ``huggingface-cli login`` bash command. Alternatively you can pass your `API token <https://huggingface.co/settings/token>`__ in ``use_auth_token``.


CSV files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🤗 Datasets can read a dataset made of one or several CSV files.

All the CSV files in the dataset should have the same organization and in particular the same datatypes for the columns.

A few interesting features are provided out-of-the-box by the Apache Arrow backend:

- multi-threaded or single-threaded reading
- automatic decompression of input files (based on the filename extension, such as my_data.csv.gz)
- fetching column names from the first row in the CSV file
- column-wise type inference and conversion to one of null, int64, float64, timestamp[s], string or binary data
- detecting various spellings of null values such as NaN or #N/A

Here is an example loading two CSV file to create a ``train`` split (default split unless specify otherwise):

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv'])

You can also provide the URLs of remote csv files:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('csv', data_files="https://huggingface.co/datasets/lhoestq/demo1/resolve/main/data/train.csv")

The ``csv`` loading script provides a few simple access options to control parsing and reading the CSV files:

    - :obj:`skiprows` (int) - Number of first rows in the file to skip (default is 0)
    - :obj:`column_names` (list, optional) – The column names of the target table. If empty, fall back on autogenerate_column_names (default: empty).
    - :obj:`delimiter` (1-character string) – The character delimiting individual cells in the CSV data (default ``,``).
    - :obj:`quotechar` (1-character string) – The character used optionally for quoting CSV values (default ``"``).
    - :obj:`quoting` (int) – Control quoting behavior (default 0, setting this to 3 disables quoting, refer to `pandas.read_csv documentation <https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html>` for more details).


JSON files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🤗 Datasets supports building a dataset from JSON files in various formats.

The most efficient format is to have JSON files consisting of multiple JSON objects, one per line, representing individual data rows:

.. code-block::

    {"a": 1, "b": 2.0, "c": "foo", "d": false}
    {"a": 4, "b": -5.5, "c": null, "d": true}

In this case, interesting features are provided out-of-the-box by the Apache Arrow backend:

- multi-threaded reading
- automatic decompression of input files (based on the filename extension, such as my_data.json.gz)
- sophisticated type inference (see below)

You can load such a dataset direcly with:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('json', data_files='my_file.json')

You can also provide the URLs of remote JSON files:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('json', data_files='https://huggingface.co/datasets/allenai/c4/resolve/main/en/c4-train.00000-of-01024.json.gz')

In real-life though, JSON files can have diverse format and the ``json`` script will accordingly fallback on using python JSON loading methods to handle various JSON file format.

One common occurence is to have a JSON file with a single root dictionary where the dataset is contained in a specific field, as a list of dicts or a dict of lists.

.. code-block::

    {"version": "0.1.0",
     "data": [{"a": 1, "b": 2.0, "c": "foo", "d": false},
              {"a": 4, "b": -5.5, "c": null, "d": true}]
    }

In this case you will need to specify which field contains the dataset using the :obj:`field` argument as follows:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('json', data_files='my_file.json', field='data')


Text files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🤗 Datasets also supports building a dataset from text files read line by line (each line will be a row in the dataset).

This is simply done using the ``text`` loading script which will generate a dataset with a single column called ``text`` containing all the text lines of the input files as strings.

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('text', data_files={'train': ['my_text_1.txt', 'my_text_2.txt'], 'test': 'my_test_file.txt'})

You can also provide the URLs of remote text files:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('text', data_files={'train': 'https://huggingface.co/datasets/lhoestq/test/resolve/main/some_text.txt'})


Specifying the features of the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you create a dataset from local files, the :class:`datasets.Features` of the dataset are automatically guessed using an automatic type inference system based on `Apache Arrow Automatic Type Inference <https://arrow.apache.org/docs/python/json.html#automatic-type-inference>`__.

However sometime you may want to define yourself the features of the dataset, for instance to control the names and indices of labels using a :class:`datasets.ClassLabel`.

In this case you can use the :obj:`features` arguments to :func:`datasets.load_dataset` to supply a :class:`datasets.Features` instance definining the features of your dataset and overriding the default pre-computed features.

From in-memory data
-----------------------------------------------------------

Eventually, it's also possible to instantiate a :class:`datasets.Dataset` directly from in-memory data, currently:

- a python dict, or
- a pandas dataframe.

From a python dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say that you have already loaded some data in a in-memory object in your python session:

.. code-block::

    >>> my_dict = {'id': [0, 1, 2],
    >>>            'name': ['mary', 'bob', 'eve'],
    >>>            'age': [24, 53, 19]}

You can then directly create a :class:`datasets.Dataset` object using the :func:`datasets.Dataset.from_dict` or the :func:`datasets.Dataset.from_pandas` class methods of the :class:`datasets.Dataset` class:

.. code-block::

    >>> from datasets import Dataset
    >>> dataset = Dataset.from_dict(my_dict)

From a pandas dataframe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can similarly instantiate a Dataset object from a ``pandas`` DataFrame:

.. code-block::

    >>> from datasets import Dataset
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2, 3]})
    >>> dataset = Dataset.from_pandas(df)

.. note::

    The column types in the resulting Arrow Table are inferred from the dtypes of the pandas.Series in the DataFrame. In the case of non-object Series, the NumPy dtype is translated to its Arrow equivalent. In the case of `object`, we need to guess the datatype by looking at the Python objects in this Series.

    Be aware that Series of the `object` dtype don't carry enough information to always lead to a meaningful Arrow type. In the case that we cannot infer a type, e.g. because the DataFrame is of length 0 or the Series only contains None/nan objects, the type is set to null. This behavior can be avoided by constructing an explicit schema and passing it to this function.

To be sure that the schema and type of the instantiated :class:`datasets.Dataset` are as intended, you can explicitely provide the features of the dataset as a :class:`datasets.Features` object to the ``from_dict`` and ``from_pandas`` methods.

Using a custom dataset loading script
-----------------------------------------------------------

If the provided loading scripts for Hub dataset or for local files are not adapted for your use case, you can also easily write and use your own dataset loading script.

You can use a local loading script by providing its path instead of the usual shortcut name:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('PATH/TO/MY/LOADING/SCRIPT', data_files='PATH/TO/MY/FILE')

We provide more details on how to create your own dataset generation script on the :doc:`add_dataset` page and you can also find some inspiration in all the already provided loading scripts on the `GitHub repository <https://github.com/huggingface/datasets/tree/master/datasets>`__.

.. _load_dataset_cache_management:


Loading datasets in streaming mode
-----------------------------------------------------------

When a dataset is in streaming mode, you can iterate over it directly without having to download the entire dataset.
The data are downloaded progressively as you iterate over the dataset.
You can enable dataset streaming by passing ``streaming=True`` in the :func:`load_dataset` function to get an iterable dataset.

For example, you can start iterating over big datasets like OSCAR without having to download terabytes of data using this code:


.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    >>> print(next(iter(dataset)))
    {'text': 'Mtendere Village was inspired by the vision of Chief Napoleon Dzombe, which he shared with John Blanchard during his first visit to Malawi. Chief Napoleon conveyed the desperate need for a program to intervene and care for the orphans and vulnerable children (OVC) in Malawi, and John committed to help...

.. note::

    A dataset in streaming mode is not a :class:`datasets.Dataset` object, but an :class:`datasets.IterableDataset` object. You can find more information about iterable datasets in the `dataset streaming documentation <dataset_streaming.html>`__

Cache management and integrity verifications
-----------------------------------------------------------

Cache directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To avoid re-downloading the whole dataset every time you use it, the `datasets` library caches the data on your computer.

By default, the `datasets` library caches the datasets and the downloaded data files under the following directory: `~/.cache/huggingface/datasets`.

If you want to change the location where the datasets cache is stored, simply set the `HF_DATASETS_CACHE` environment variable. For example, if you're using linux:

.. code-block::

    $ export HF_DATASETS_CACHE="/path/to/another/directory"

In addition, you can control where the data is cached when invoking the loading script, by setting the :obj:`cache_dir` parameter:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('LOADING_SCRIPT', cache_dir="PATH/TO/MY/CACHE/DIR")

Download mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can control the way the the :func:`datasets.load_dataset` function handles already downloaded data by setting its :obj:`download_mode` parameter.

By default, :obj:`download_mode` is set to ``"reuse_dataset_if_exists"``. The :func:`datasets.load_dataset` function will reuse both raw downloads and the prepared dataset, if they exist in the cache directory.

The following table describes the three available modes for download:

.. list-table:: Behavior of :func:`datasets.load_dataset` depending on :obj:`download_mode`
   :header-rows: 1

   * - :obj:`download_mode` parameter value
     - Downloaded files (raw data)
     - Dataset object
   * - ``"reuse_dataset_if_exists"`` (default)
     - Reuse
     - Reuse
   * - ``"reuse_cache_if_exists"``
     - Reuse
     - Fresh
   * - ``"force_redownload"``
     - Fresh
     - Fresh

For example, you can run the following if you want to force the re-download of the SQuAD raw data files:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('squad', download_mode="force_redownload")


Integrity verifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When downloading a dataset from the 🤗 Datasets Hub, the :func:`datasets.load_dataset` function performs by default a number of verifications on the downloaded files. These verifications include:

- Verifying the list of downloaded files
- Verifying the number of bytes of the downloaded files
- Verifying the SHA256 checksums of the downloaded files
- Verifying the number of splits in the generated `DatasetDict`
- Verifying the number of samples in each split of the generated `DatasetDict`

You can disable these verifications by setting the :obj:`ignore_verifications` parameter to ``True``.

You also have the possibility to locally override the informations used to perform the integrity verifications by setting the :obj:`save_infos` parameter to ``True``.

For example, run the following to skip integrity verifications when loading the IMDB dataset:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('imdb', ignore_verifications=True)


Loading datasets offline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each dataset builder (e.g. "squad") is a Python script that is downloaded and cached either from the 🤗 Datasets GitHub repository or from the `Hugging Face Hub <https://huggingface.co/datasets>`__.
Only the ``text``, ``csv``, ``json``, ``parquet`` and ``pandas`` builders are included in ``datasets`` without requiring external downloads.

Therefore if you don't have an internet connection you can't load a dataset that is not packaged with ``datasets``, unless the dataset is already cached.
Indeed, if you've already loaded the dataset once before (when you had an internet connection), then the dataset is reloaded from the cache and you can use it offline.

You can even set the environment variable `HF_DATASETS_OFFLINE` to ``1`` to tell ``datasets`` to run in full offline mode.
This mode disables all the network calls of the library.
This way, instead of waiting for a dataset builder download to time out, the library looks directly at the cache.

.. _load_dataset_load_builder:

Loading a dataset builder
-----------------------------------------------------------

You can use :func:`datasets.load_dataset_builder` to inspect metadata (cache directory, configs, dataset info, etc.) that is required to build a dataset without downloading the dataset itself.

For example, run the following to get the path to the cache directory of the IMDB dataset:

.. code-block::

    >>> from datasets import load_dataset_builder
    >>> dataset_builder = load_dataset_builder('imdb')
    >>> print(dataset_builder.cache_dir)
    /Users/thomwolf/.cache/huggingface/datasets/imdb/plain_text/1.0.0/fdc76b18d5506f14b0646729b8d371880ef1bc48a26d00835a7f3da44004b676
    >>> print(dataset_builder.info.features)
    {'text': Value(dtype='string', id=None), 'label': ClassLabel(num_classes=2, names=['neg', 'pos'], names_file=None, id=None)}
    >>> print(dataset_builder.info.splits)
    {'train': SplitInfo(name='train', num_bytes=33432835, num_examples=25000, dataset_name='imdb'), 'test': SplitInfo(name='test', num_bytes=32650697, num_examples=25000, dataset_name='imdb'), 'unsupervised': SplitInfo(name='unsupervised', num_bytes=67106814, num_examples=50000, dataset_name='imdb')}

You can see all the attributes of ``dataset_builder.info`` in the documentation of :class:`datasets.DatasetInfo`


.. _load_dataset_enhancing_performance:

Enhancing performance
-----------------------------------------------------------

If you would like to speed up dataset operations, you can disable caching and copy the dataset in-memory by setting
``datasets.config.IN_MEMORY_MAX_SIZE`` to a nonzero size (in bytes) that fits in your RAM memory. In that case, the
dataset will be copied in-memory if its size is smaller than ``datasets.config.IN_MEMORY_MAX_SIZE`` bytes, and
memory-mapped otherwise. This behavior can be enabled by setting either the configuration option
``datasets.config.IN_MEMORY_MAX_SIZE`` (higher precedence) or the environment variable
``HF_DATASETS_IN_MEMORY_MAX_SIZE`` (lower precedence) to nonzero.
