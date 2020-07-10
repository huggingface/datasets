Loading a Dataset
==============================================================

A :class:`nlp.Dataset` can be created from various source of data:

- from the `HuggingFace Hub <https://huggingface.co/datasets>`__,
- from local files, e.g. CSV/JSON/text/pandas files, or
- from in-memory data like python dict or a pandas dataframe.

In this section we study each option.

Loading a dataset from the HuggingFace Hub
-----------------------------------------------------------

Over 135 datasets for many NLP tasks like text classification, question answering, language modeling, etc, are provided on the `HuggingFace Hub <https://huggingface.co/datasets>`__ and can be viewed and explored online with the `🤗nlp viewer <https://huggingface.co/nlp/viewer>`__.

.. note::

    You can also add new dataset to the Hub to share with the community as detailed in the guide on :doc:`adding a new dataset </add_dataset>`.

All the datasets currently available on the `Hub <https://huggingface.co/datasets>`__ can be listed using :func:`nlp.list_datasets`:

.. code-block::

    >>> from nlp import list_datasets
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


To load a dataset from the Hub we use the :func:`nlp.load_dataset` command and give it the short name of the dataset you would like to load as listed above or on the `Hub <https://huggingface.co/datasets>`__.

Let's load the **SQuAD dataset for Question Answering**. You can explore this dataset and find more details about it `on the online viewer here <https://huggingface.co/nlp/viewer/?dataset=squad>`__ (which is actually just a wrapper on top of the :class:`nlp.Dataset` we will now create):

.. code-block::

    >>> from nlp import load_dataset
    >>> dataset = load_dataset('squad', split='train')

This call to :func:`nlp.load_dataset` does the following steps under the hood:

1. Download and import in the library the **SQuAD python processing script** from HuggingFace AWS bucket if it's not already stored in the library.

.. note::

    Processing scripts are small python scripts which define the info (citation, description) and format of the dataset and contain the URL to the original SQuAD JSON files and the code to load examples from the original SQuAD JSON files. You can find the SQuAD processing script `here <https://github.com/huggingface/nlp/tree/master/datasets/squad/squad.py>`__ for instance.

2. Run the SQuAD python processing script which will download the SQuAD dataset from the original URL (if it's not already downloaded and cached) and process and cache all SQuAD in a cache Arrow table for each standard splits stored on the drive.

.. note::

    An Apache Arrow Table is the internal storing format for 🤗nlp. It allows to store arbitrarly long dataframe, typed with potentially complex nested types that can be mapped to numpy/pandas/python types. Apache Arrow allows you to map blobs of data on-drive without doing any deserialization. So caching the dataset directly on disk can use memory-mapping and pay effectively zero cost with O(1) random access. The default in 🤗nlp is thus to always memory-map dataset on drive.

3. Return a **dataset build from the splits** asked by the user (default: all), in the above example we create a dataset with the first 10% of the validation split.


Selecting a split
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't provide a :obj:`split` argument to :func:`nlp.load_dataset`, this method will return a dictionnary containing a datasets for each split in the dataset.

.. code-block::

    >>> from nlp import load_dataset
    >>> datasets = load_dataset('squad')
    >>> print(datasets)
    {'train': Dataset(schema: {'id': 'string', 'title': 'string', 'context': 'string', 'question': 'string', 'answers': 'struct<text: list<item: string>, answer_start: list<item: int32>>'}, num_rows: 87599),
     'validation': Dataset(schema: {'id': 'string', 'title': 'string', 'context': 'string', 'question': 'string', 'answers': 'struct<text: list<item: string>, answer_start: list<item: int32>>'}, num_rows: 10570)
    }

The :obj:`split` argument can actually be used to control extensively the generated dataset split. You can use this argument to build a split from only a portion of a split in absolute number of examples or in proportion (e.g. :obj:`split='train[:10%]'` will load only the first 10% of the train split) or to mix splits (e.g. :obj:`split='train[:100]+validation[:100]'` will create a split from the first 100 examples of the train split and the first 100 examples of the validation split).

You can find more details on the syntax for using :obj:`split` on the :doc:`dedicated tutorial on split <./split>`.

Selecting a configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some datasets comprise several :obj:`configurations`. A Configuration define a sub-part of a dataset which can be selected. Unlike split, you have to select a single configuration for the dataset, you cannot mix severla configurations. Examples of dataset with several configurations are:

- the **GLUE** dataset which is an agregated benchmark comprised of 10 subsets: COLA, SST2, MRPC, QQP, STSB, MNLI, QNLI, RTE, WNLI and the diagnostic subset AX.
- the **wikipedia** dataset which is provided for several languages.

When a dataset is provided with more than one :obj:`configurations`, you will be requested to explicitely select a configuration among the possibilities.

Selecting a configuration is done by providing :func: `nlp.load_dataset` with a :obj:`name` argument. Here is an example for **GLUE**:

.. code-block::

    >>> from nlp import load_dataset

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

Manually downloading some files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some dataset require you to download manually some files, usually because of licencing issues or when these files are behind a login page.

In this case specific instruction for dowloading the missing files will be provided when running the script with :func:`nlp.load_dataset` for the first time to explain where and how you can get the files.

After you've downloaded the files, you can point to the folder hosting them locally with the :obj:`data_dir` argument as follow

.. code-block::

    >>> dataset = load_dataset("xtreme", "PAN-X.fr")
    Downloading and preparing dataset xtreme/PAN-X.fr (download: Unknown size, generated: 5.80 MiB, total: 5.80 MiB) to /Users/thomwolf/.cache/huggingface/datasets/xtreme/PAN-X.fr/1.0.0...
    AssertionError: The dataset xtreme with config PAN-X.fr requires manual data. 
    Please follow the manual download instructions: You need to manually download the AmazonPhotos.zip file on Amazon Cloud Drive (https://www.amazon.com/clouddrive/share/d3KGCRCIYwhKJF0H3eWA26hjg2ZCRhjpEQtDL70FSBN). The folder containing the saved file can be used to load the dataset via 'nlp.load_dataset("xtreme", data_dir="<path/to/folder>")'


Apart from :obj:`name` and :obj:`split`, the :func:`nlp.load_dataset` method provide a few arguments which can be used to control where the data is cached (:obj:`cache_dir`), some options for the download process it-self like the proxies and whether the download cache should be used (:obj:`download_config`, :obj:`download_mode`).

You can find the full details on these arguments on the package reference page for :func:`nlp.load_dataset`.

Loading a dataset from local files
-----------------------------------------------------------

It's also possible to load a dataset from local files using relevant script and providing path to the files.

Currently loading scripts are provided for:
- CSV files (:obj:`csv`)
- JSON files (:obj:`json`)
- text files (read as a line-by-line dataset) (:obj:`text`)
- pandas pickled dataframe. (:obj:`pandas`)

The :obj:`data_files` arguments is used to provide paths to on or several files and accept three possible format:
- a single string as the path to a single files (considered to constitute the `train` split by default)
- a list of strings as paths to a list of files (also considered to constitute the `train` split by default)
- a dictionnary mapping splits to single files or list of files.

Let's see an example of all the various ways you can provide files to :func:`nlp.load_dataset`:

.. code-block::

    >>> from nlp import load_dataset
    >>> dataset = load_dataset('csv', data_files='my_file.csv')
    >>> dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv', 'my_file_3.csv'])
    >>> dataset = load_dataset('csv', data_files={'train': ['my_train_file_1.csv', 'my_train_file_2.csv'], 
                                                  'test': 'my_test_file.csv'})

The :obj:`split` argument will work similarly to what we detailed above for the datasets on the Hub and you can find more details on the syntax for using :obj:`split` on the :doc:`dedicated tutorial on split <./split>`. The only specific behavior related to loading local files is that if you don't indicate which split each files is realted to, the provided files are assumed to belong to the **train** split.

Defining the features of the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you create a dataset from local files, the :class:`nlp.Feature` of the dataset are automatically guessed using an automatic type inference system based on `Apache Arrow Automatic Type Inference <https://arrow.apache.org/docs/python/json.html#automatic-type-inference>`__.

However sometime you may want to define yourself the features of the dataset, for instance to control the names and indices of labels using a :class:`nlp.ClassLabel`.


Loading a dataset from in-memory data
-----------------------------------------------------------

It's also possible to load a dataset from in-memory data like a python dict or a pandas dataframe.

In this case, we assume that you have already loaded some data in a in-memory object in your python session.

You can then directly create a :class:`nlp.Dataset` object using one of the class methode of the :class:`nlp.Dataset` class.

Here is an examples with a python dictionnary:

.. code-block::

    >>> from nlp import Dataset

