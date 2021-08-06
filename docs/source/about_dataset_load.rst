Build and Load
==============

Nearly every deep learning workflow begins with loading a dataset, which makes it one of the most important steps. With 🤗 Datasets, there are more than 900 datasets available. All you have to do is invoke a simple command: :func:`datasets.load_dataset`. This function is a true workhorse because it builds and loads every dataset you use.

ELI5: ``datasets.load_dataset``
-------------------------------

Let's begin with a basic Explain Like I'm Five.

At first, :func:`datasets.load_dataset` downloads and imports the dataset loading script associated with the requested dataset from the Hugging Face Hub. The Hub is a central repository where all the Hugging Face datasets and models are stored. Code in the loading script defines the dataset information (description, features, URL to the original files, etc.), and tells 🤗 Datasets how to generate and display examples from it.

.. seealso::

   Read the :doc:`Share <./share>` section for a step-by-step guide on how to write your own dataset loading script!

The loading script downloads the dataset files from the original URL, and caches the dataset in an Arrow table on your drive. If you've downloaded the dataset before, then 🤗 Datasets will reload it from the cache to save you the trouble of downloading it again. Finally, 🤗 Datasets will generate the dataset according to the code defined in the loading script.

Now that you have a high-level understanding about how datasets are built, let's get a little deeper into the nuts and bolts of how all this works.

Building a dataset
------------------

When you load a dataset for the first time, 🤗 Datasets takes the raw data file and builds it into a table of rows and typed columns. There are two main classes responsible for building a dataset: :class:`datasets.BuilderConfig` and :class:`datasets.DatasetBuilder`. 

.. image:: /imgs/builderconfig.png
   :align: center

:class:`datasets.BuilderConfig`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`datasets.BuilderConfig` is the base class of :class:`datasets.DatasetBuilder`. The :class:`datasets.BuilderConfig` contains the following basic attributes about a dataset:

.. list-table::
   :header-rows: 1

   * - Attribute
     - Description
   * - :obj:`name`
     - Short name of the dataset.
   * - :obj:`version`
     - Dataset version identifier.
   * - :obj:`data_dir`
     - Stores the path to a local folder containing the data files.
   * - :obj:`data_files`
     - Stores paths to local data files.
   * - :obj:`description`
     - Description of the dataset.

If you want to add additional attributes to your dataset such as the class labels, you can subclass the base :class:`datasets.BuilderConfig` class. There are two ways to populate the attributes of a :class:`datasets.BuilderConfig` class or subclass:

* Provide a list of predefined :class:`datasets.BuilderConfig` classes or subclasses in the datasets :attr:`datasets.DatasetBuilder.BUILDER_CONFIGS` attribute.

* When you call :func:`datasets.load_dataset`, any keyword arguments that are not specific to the method will be used to set the associated attributes of the :class:`datasets.BuilderConfig` class. This will override the predefined attributes if a specific configuration was selected.

:class:`datasets.DatasetBuilder`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`datasets.DatasetBuilder` accesses all the attributes inside :class:`datasets.BuilderConfig` to build the actual dataset. 

.. image:: /imgs/datasetbuilder.png
   :align: center

There are three main methods in :class:`datasets.DatasetBuilder`:

1. :func:`datasets.DatasetBuilder._info` is in charge of defining the dataset attributes. When you call ``dataset.info``, 🤗 Datasets returns the information stored here. Likewise, the :class:`datasets.Features` are also specified here. Remember, the :class:`datasets.Features` are like the skeleton of the dataset. It provides the names and types of each column.

2. :func:`datasets.DatasetBuilder._split_generator` downloads or retrieves the requested data files, organizes them into splits, and defines specific arguments for the generation process. This method has a :class:`datasets.DownloadManager` that downloads files or fetches them from your local filesystem. Within the :class:`datasets.DownloadManager`, there is a :func:`datasets.DownloadManager.download_and_extract` method that accepts a dictionary of URLs to the original data files, and downloads the requested files. Accepted inputs include: a single URL or path, or a list/dictionary of URLs or paths. Any compressed file types like tar, gzip and zip archives will be automatically extracted.

   Once the files are downloaded, :class:`datasets.SplitGenerator` organizes them into splits. The :class:`datasets.SplitGenerator` contains the name of the split, and any keyword arguments that are provided to the :func:`datasets.DatasetBuilder._generate_examples` method. The keyword arguments can be specific to each split, and typically comprise at least the local path to the data files for each split.

   .. tip::

       :func:`datasets.DownloadManager.download_and_extract` can download files from a wide range of sources. If the data files are hosted on a special access server, you should use :func:`datasets.DownloadManger.download_custom`. Refer to the package reference of :class:`datasets.DownloadManager` for more details.

3. :func:`datasets.DatasetBuilder._generate_examples` reads and parses the data files for a split. Then it yields dataset examples according to the format specified in the ``features`` from :func:`datasets.DatasetBuilder._info`. The input of :func:`datasets.DatasetBuilder._generate_examples` is actually the ``filepath`` provided in the keyword arguments of the last method. 

   The dataset is generated with a Python generator, which doesn't load all the data in memory. As a result, the generator can handle large datasets. However, before the generated samples are flushed to the dataset file on disk, they are stored in an ``ArrowWriter`` buffer. This means the generated samples are written by batch. If your dataset samples consumes a lot of memory (images or videos), then make sure to specify a low value for the ``DEFAULT_WRITER_BATCH_SIZE`` attribute in :class:`datasets.DatasetBuilder`. We recommend not exceeding a size of 200 MB.

Without loading scripts
-----------------------

As a user, you want to be able to quickly use a dataset. Implementing a dataset loading script can sometimes get in the way, or it may be a barrier for some people without a developer background. 🤗 Datasets removes this barrier by making it possible to load any dataset from the Hub without a dataset loading script. All a user has to do is upload the data files to a dataset repository on the Hub, and they will be able to load that dataset without having to create a loading script. This doesn't mean we are moving away from loading scripts because they still offer the most flexibility in controlling how a dataset is generated.

The no loading script method uses the `huggingface_hub <https://github.com/huggingface/huggingface_hub>`_ library to list the files in a dataset repository. You can also provide a path to a local directory instead of a repository name, in which case 🤗 Datasets will use `glob <https://docs.python.org/3/library/glob.html>`_ instead. Depending on the data files available, one of the data file builders will create your dataset for you. If you have a CSV file, the CSV builder will be used and if you have a Parquet file, the Parquet builder will be used. The drawback of this approach is it's not possible to simultaneously load a CSV and JSON file. In this case, you will need to load the two file types separately, and then concatenate them.

Maintaining integrity
---------------------

To ensure a dataset is complete, :func:`datasets.load_dataset` will perform a series of tests on the downloaded files to make sure everything is there. This way, you don't encounter any surprises when your requested dataset doesn't get generated as expected. :func:`datasets.load_dataset` verifies:

* The list of downloaded files.
* The number of bytes of the downloaded files.
* The SHA256 checksums of the downloaded files.
* The number of splits in the generated ``DatasetDict``.
* The number of samples in each split of the generated ``DatasetDict``.

TO DO: Explain why you would want to disable the verifications or override the information used to perform the verifications.
