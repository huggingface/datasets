Loading a Dataset
==============================================================

A :class:`datasets.Dataset` can be created from various source of data:

- from the `HuggingFace Hub <https://huggingface.co/datasets>`__,
- from local files, e.g. CSV/JSON/text/pandas files, or
- from in-memory data like python dict or a pandas dataframe.

In this section we study each option.

From the HuggingFace Hub
-------------------------------------------------

Over 135 datasets for many NLP tasks like text classification, question answering, language modeling, etc, are provided on the `HuggingFace Hub <https://huggingface.co/datasets>`__ and can be viewed and explored online with the `🤗datasets viewer <https://huggingface.co/nlp/viewer>`__.

.. note::

    You can also add new dataset to the Hub to share with the community as detailed in the guide on :doc:`adding a new dataset </add_dataset>`.

All the datasets currently available on the `Hub <https://huggingface.co/datasets>`__ can be listed using :func:`datasets.list_datasets`:

.. code-block::

    >>> from datasets import list_datasets
    >>> datasets_list = list_datasets()
    >>> len(datasets_list)
    136
    >>> print(', '.join(dataset.id for dataset in datasets_list))
    aeslc, ag_news, ai2_arc, allocine, anli, arcd, art, billsum, blended_skill_talk, blimp, blog_authorship_corpus, bookcorpus, boolq, break_data,
    c4, cfq, civil_comments, cmrc2018, cnn_dailymail, coarse_discourse, com_qa, commonsense_qa, compguesswhat, coqa, cornell_movie_dialog, cos_e, 
    cosmos_qa, crime_and_punish, csv, definite_pronoun_resolution, discofuse, docred, drop, eli5, empathetic_dialogues, eraser_multi_rc, esnli, 
    event2Mind, fever, flores, fquad, gap, germeval_14, ghomasHudson/cqc, gigaword, glue, hansards, hellaswag, hyperpartisan_news_detection, 
    imdb, jeopardy, json, k-halid/ar, kor_nli, lc_quad, lhoestq/c4, librispeech_lm, lm1b, math_dataset, math_qa, mlqa, movie_rationales, 
    multi_news, multi_nli, multi_nli_mismatch, mwsc, natural_questions, newsroom, openbookqa, opinosis, pandas, para_crawl, pg19, piaf, qa4mre, 
    qa_zre, qangaroo, qanta, qasc, quarel, quartz, quoref, race, reclor, reddit, reddit_tifu, rotten_tomatoes, scan, scicite, scientific_papers, 
    scifact, sciq, scitail, sentiment140, snli, social_i_qa, squad, squad_es, squad_it, squad_v1_pt, squad_v2, squadshifts, super_glue, ted_hrlr, 
    ted_multi, tiny_shakespeare, trivia_qa, tydiqa, ubuntu_dialogs_corpus, webis/tl_dr, wiki40b, wiki_dpr, wiki_qa, wiki_snippets, wiki_split, 
    wikihow, wikipedia, wikisql, wikitext, winogrande, wiqa, wmt14, wmt15, wmt16, wmt17, wmt18, wmt19, wmt_t2t, wnut_17, x_stance, xcopa, xnli, 
    xquad, xsum, xtreme, yelp_polarity


To load a dataset from the Hub we use the :func:`datasets.load_dataset` command and give it the short name of the dataset you would like to load as listed above or on the `Hub <https://huggingface.co/datasets>`__.

Let's load the **SQuAD dataset for Question Answering**. You can explore this dataset and find more details about it `on the online viewer here <https://huggingface.co/nlp/viewer/?dataset=squad>`__ (which is actually just a wrapper on top of the :class:`datasets.Dataset` we will now create):

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('squad', split='train')

This call to :func:`datasets.load_dataset` does the following steps under the hood:

1. Download and import in the library the **SQuAD python processing script** from HuggingFace github repository or AWS bucket if it's not already stored in the library.

.. note::

    Processing scripts are small python scripts which define the info (citation, description) and format of the dataset and contain the URL to the original SQuAD JSON files and the code to load examples from the original SQuAD JSON files. You can find the SQuAD processing script `here <https://github.com/huggingface/datasets/tree/master/datasets/squad/squad.py>`__ for instance.

2. Run the SQuAD python processing script which will download the SQuAD dataset from the original URL (if it's not already downloaded and cached) and process and cache all SQuAD in a cache Arrow table for each standard splits stored on the drive.

.. note::

    An Apache Arrow Table is the internal storing format for 🤗datasets. It allows to store arbitrarily long dataframe, typed with potentially complex nested types that can be mapped to numpy/pandas/python types. Apache Arrow allows you to map blobs of data on-drive without doing any deserialization. So caching the dataset directly on disk can use memory-mapping and pay effectively zero cost with O(1) random access. The default in 🤗datasets is thus to always memory-map dataset on drive.

3. Return a **dataset build from the splits** asked by the user (default: all), in the above example we create a dataset with the first 10% of the validation split.


Selecting a split
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't provide a :obj:`split` argument to :func:`datasets.load_dataset`, this method will return a dictionary containing a datasets for each split in the dataset.

.. code-block::

    >>> from datasets import load_dataset
    >>> datasets = load_dataset('squad')
    >>> print(datasets)
    {'train': Dataset(schema: {'id': 'string', 'title': 'string', 'context': 'string', 'question': 'string', 'answers': 'struct<text: list<item: string>, answer_start: list<item: int32>>'}, num_rows: 87599),
     'validation': Dataset(schema: {'id': 'string', 'title': 'string', 'context': 'string', 'question': 'string', 'answers': 'struct<text: list<item: string>, answer_start: list<item: int32>>'}, num_rows: 10570)
    }

The :obj:`split` argument can actually be used to control extensively the generated dataset split. You can use this argument to build a split from only a portion of a split in absolute number of examples or in proportion (e.g. :obj:`split='train[:10%]'` will load only the first 10% of the train split) or to mix splits (e.g. :obj:`split='train[:100]+validation[:100]'` will create a split from the first 100 examples of the train split and the first 100 examples of the validation split).

You can find more details on the syntax for using :obj:`split` on the :doc:`dedicated tutorial on split <./splits>`.

Selecting a configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some datasets comprise several :obj:`configurations`. A Configuration define a sub-part of a dataset which can be selected. Unlike split, you have to select a single configuration for the dataset, you cannot mix several configurations. Examples of dataset with several configurations are:

- the **GLUE** dataset which is an agregated benchmark comprised of 10 subsets: COLA, SST2, MRPC, QQP, STSB, MNLI, QNLI, RTE, WNLI and the diagnostic subset AX.
- the **wikipedia** dataset which is provided for several languages.

When a dataset is provided with more than one :obj:`configurations`, you will be requested to explicitely select a configuration among the possibilities.

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
    {'train': Dataset(schema: {'sentence': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 67349),
     'validation': Dataset(schema: {'sentence': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 872),
     'test': Dataset(schema: {'sentence': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 1821)
    }

Manually downloading files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some dataset require you to download manually some files, usually because of licencing issues or when these files are behind a login page.

In this case specific instruction for dowloading the missing files will be provided when running the script with :func:`datasets.load_dataset` for the first time to explain where and how you can get the files.

After you've downloaded the files, you can point to the folder hosting them locally with the :obj:`data_dir` argument as follow

.. code-block::

    >>> dataset = load_dataset("xtreme", "PAN-X.fr")
    Downloading and preparing dataset xtreme/PAN-X.fr (download: Unknown size, generated: 5.80 MiB, total: 5.80 MiB) to /Users/thomwolf/.cache/huggingface/datasets/xtreme/PAN-X.fr/1.0.0...
    AssertionError: The dataset xtreme with config PAN-X.fr requires manual data. 
    Please follow the manual download instructions: You need to manually download the AmazonPhotos.zip file on Amazon Cloud Drive (https://www.amazon.com/clouddrive/share/d3KGCRCIYwhKJF0H3eWA26hjg2ZCRhjpEQtDL70FSBN). The folder containing the saved file can be used to load the dataset via 'datasets.load_dataset("xtreme", data_dir="<path/to/folder>")'


Apart from :obj:`name` and :obj:`split`, the :func:`datasets.load_dataset` method provide a few arguments which can be used to control where the data is cached (:obj:`cache_dir`), some options for the download process it-self like the proxies and whether the download cache should be used (:obj:`download_config`, :obj:`download_mode`).

You can find the full details on these arguments on the package reference page for :func:`datasets.load_dataset`.


.. _loading-from-local-files:

From local files
-----------------------------------------------------------

It's also possible to create a dataset from local files.

Generic loading scripts are provided for:

- CSV files (with the :obj:`csv` script),
- JSON files (with the :obj:`json` script),
- text files (read as a line-by-line dataset with the :obj:`text` script),
- pandas pickled dataframe (with the :obj:`pandas` script).

If you want to control better how you files are loaded, or if you have a file format exactly reproducing the file format for one of the datasets provided on the `HuggingFace Hub <https://huggingface.co/datasets>`__, it can be more flexible and simpler to create **your own loading script**, from scratch or by adapting one of the provided loading scripts. In this case, please go check the :doc:`add_dataset` chapter.

The :obj:`data_files` argument in :func:`datasets.load_dataset` is used to provide paths to one or several files. This arguments currently accept three types of inputs:

- :obj:`str`: a single string as the path to a single file (considered to constitute the `train` split by default)
- :obj:`List[str]`: a list of strings as paths to a list of files (also considered to constitute the `train` split by default)
- :obj:`Dict[Union[str, List[str]]]`: a dictionary mapping splits names to a single file or a list of files.

Let's see an example of all the various ways you can provide files to :func:`datasets.load_dataset`:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('csv', data_files='my_file.csv')
    >>> dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv', 'my_file_3.csv'])
    >>> dataset = load_dataset('csv', data_files={'train': ['my_train_file_1.csv', 'my_train_file_2.csv'], 
                                                  'test': 'my_test_file.csv'})

.. note::

    The :obj:`split` argument will work similarly to what we detailed above for the datasets on the Hub and you can find more details on the syntax for using :obj:`split` on the :doc:`dedicated tutorial on split <./splits>`. The only specific behavior related to loading local files is that if you don't indicate which split each files is realted to, the provided files are assumed to belong to the **train** split.


CSV files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🤗datasets can read a dataset made of on or several CSV files.

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

The ``csv`` loading script provides a few simple access options to control parsing and reading the CSV files:

    - :obj:`skip_rows` (int) - Number of first rows in the file to skip (default is 0)
    - :obj:`column_names` (list, optional) – The column names of the target table. If empty, fall back on autogenerate_column_names (default: empty).
    - :obj:`autogenerate_column_names` (bool) – Whether to autogenerate column names if column_names is empty. If true, column names will be of the form “f0”, “f1”… If false, column names will be read from the first CSV row after skip_rows (default False).
    - :obj:`delimiter` (1-character string) – The character delimiting individual cells in the CSV data (default ``','``).
    - :obj:`quote_char` (1-character string or False) – The character used optionally for quoting CSV values (False if quoting is not allowed, default '"').

If you want more control, the ``csv`` script provide full control on reading, parsong and convertion through the Apache Arrow `pyarrow.csv.ReadOptions <https://arrow.apache.org/docs/python/generated/pyarrow.csv.ReadOptions.html>`__, `pyarrow.csv.ParseOptions <https://arrow.apache.org/docs/python/generated/pyarrow.csv.ParseOptions.html>`__ and `pyarrow.csv.ConvertOptions <https://arrow.apache.org/docs/python/generated/pyarrow.csv.ConvertOptions.html>`__

    - :obj:`read_options` — Can be provided with a `pyarrow.csv.ReadOptions <https://arrow.apache.org/docs/python/generated/pyarrow.csv.ReadOptions.html>`__ to control all the reading options. If :obj:`skip_rows`, :obj:`column_names` or :obj:`autogenerate_column_names` are also provided (see above), they will take priority over the attributes in :obj:`read_options`.
    - :obj:`parse_options` — Can be provided with a `pyarrow.csv.ParseOptions <https://arrow.apache.org/docs/python/generated/pyarrow.csv.ParseOptions.html>`__ to control all the parsing options. If :obj:`delimiter` or :obj:`quote_char` are also provided (see above), they will take priority over the attributes in :obj:`parse_options`.
    - :obj:`convert_options` — Can be provided with a `pyarrow.csv.ConvertOptions <https://arrow.apache.org/docs/python/generated/pyarrow.csv.ConvertOptions.html>`__ to control all the conversion options.


JSON files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🤗datasets supports building a dataset from JSON files in various format.

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

In real-life though, JSON files can have diverse format and the ``json`` script will accordingly fallback on using python JSON loading methods to handle various JSON file format.

One common occurence is to have a JSON file with a single root dictionary where the dataset is contained in a specific field, as a list of dicts or a dict of lists.

.. code-block::

    {"version: "0.1.0",
     "data": [{"a": 1, "b": 2.0, "c": "foo", "d": false},
              {"a": 4, "b": -5.5, "c": null, "d": true}]
    }

In this case you will need to specify which field contains the dataset using the :obj:`field` argument as follow:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('json', data_files='my_file.json', field='data')


Text files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🤗datasets also supports building a dataset from text files read line by line (each line will be a row in the dataset).

This is simply done using the ``text`` loading script which will generate a dataset with a single column called ``text`` containing all the text lines of the input files as strings.

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('text', data_files={'train': ['my_text_1.txt', 'my_text_2.txt'], 'test': 'my_test_file.txt'})


Specifying the features of the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you create a dataset from local files, the :class:`datasets.Feature` of the dataset are automatically guessed using an automatic type inference system based on `Apache Arrow Automatic Type Inference <https://arrow.apache.org/docs/python/json.html#automatic-type-inference>`__.

However sometime you may want to define yourself the features of the dataset, for instance to control the names and indices of labels using a :class:`datasets.ClassLabel`.

In this case you can use the :obj:`feature` arguments to :func:`datasets.load_dataset` to supply a :class:`datasets.Features` instance definining the features of your dataset and overriding the default pre-computed features.

From in-memory data
-----------------------------------------------------------

Eventually, it's also possible to instantiate a :class:`datasets.Dataset` directly from in-memory data, currently one or:

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

To be sure that the schema and type of the instantiated :class:`datasets.Dataset` are as intended, you can explicitely provide the features of the dataset as a :class:`datasets.Feature` object to the ``from_dict`` and ``from_pandas`` methods.

Using a custom dataset loading script
-----------------------------------------------------------

If the provided loading scripts for Hub dataset or for local files are not adapted for your use case, you can also easily write and use your own dataset loading script.

You can use a local loading script just by providing its path instead of the usual shortcut name:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('PATH/TO/MY/LOADING/SCRIPT', data_files='PATH/TO/MY/FILE')

We provide more details on how to create your own dataset generation script on the :doc:`add_dataset` page and you can also find some inspiration in all the already provided loading scripts on the `GitHub repository <https://github.com/huggingface/datasets/tree/master/datasets>`__.


