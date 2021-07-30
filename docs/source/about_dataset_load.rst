Loading a Dataset
==================

Entire datasets are readily available with a single line of code: :func:`datasets.load_dataset`. But how does this simple function serve you whatever dataset you request? This guide will help you understand how :func:`datasets.load_dataset` works.

What happens when you call :func:`datasets.load_dataset`?
---------------------------------------------------------

In the beginning, :func:`datasets.load_dataset` downloads and imports the dataset loading script associated with the dataset you requested from the Hugging Face Hub. The Hub is a central repository where all the Hugging Face datasets and models are stored. Code in the loading script defines the dataset information (description, features, URL to the original files, etc.), and tells Datasets how to generate and display examples from it.

.. seealso::

    Read the Share section for a step-by-step guide on how to write your own Dataset loading script!

The loading script will download the dataset files from the original URL, and cache the dataset in an Arrow table on your drive. If you've downloaded the dataset before, then Datasets will reload it from the cache to save you the trouble of downloading it again. Finally, Datasets will return the dataset built from the splits specified by the user. In the next section, let's dive a little deeper into the nitty-gritty of how all this works.

Building a Dataset
------------------

When you load a dataset for the first time, Datasets takes the raw data file and builds it into a table of rows and typed columns. There are two main classes that are responsible for building a dataset: :class:`datasets.BuilderConfig` and :class:`datasets.DatasetBuilder`. 

.. image:: /imgs/builderconfig.png
   :align: center

:class:`datasets.BuilderConfig`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`datasets.BuilderConfig` is the base class for :class:`datasets.DatasetBuilder`. The :class:`datasets.BuilderConfig` contains the following basic attributes about the dataset:

.. list-table::
    :header-rows: 1

    * - Attribute
      - Description
    * - :obj:`name`
      - short name of the dataset
    * - :obj:`version`
      - dataset version identifier
    * - :obj:`data_dir`
      - stores the path to a local folder containing the data files
    * - :obj:`data_files`
      - stores paths to local data files
    * - :obj:`description`
      - description of the dataset

If you want to add additional attributes to your dataset such as the class labels, you can subclass the base :class:`datasets.BuilderConfig` class. There are two ways to populate the attributes of a :class:`datasets.BuilderConfig` class or subclass:

* Provide a list of predefined :class:`datasets.BuilderConfig` classes or subclasses that can be set in the :attr:`datasets.DatasetBuilder.BUILDER_CONFIGS` attribute of the dataset.

* When you call :func:`datasets.load_dataset`, any keyword arguments that are not specific to the method will be used to set the associated attributeds of the :class:`datasets.BuilderConfig` class. This overrides the predefined attributes.

:class:`datasets.DatasetBuilder`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`datasets.DatasetBuilder` accesses all the attributes inside :class:`datasets.BuilderConfig` to build the actual dataset. 

.. image:: /imgs/datasetbuilder.png
   :align: center

There are three main methods :class:`datasets.DatasetBuilder` uses:

1. :func:`datasets.DatasetBuilder._info` is in charge of defining the dataset attributes. When you call ``dataset.info``, Datasets returns the information stored here. Likewise, the :class:`datasets.Features` are also specified here. Remember the :class:`datasets.Features` is like the skeleton of the dataset, it provides the names and types of each column.

   .. seealso::

       Take a look at the package reference of :class:`datasets.DatasetInfo` for a full list of attributes.

2. :func:`datasets.DatasetBuilder._split_generator` downloads or retrieves the requested data files, organizes them into splits, and defines specific arguments for the generation process. This method has a :class:`datasets.DownloadManager` that downloads files or fetches them from your local filesystem. The DownloadManager contains a :func:`datasets.DownloadManager.download_and_extract` method that takes a dictionary of URLs to the original data files, and downloads or retrieves the requested files. It is flexible in the type of inputs it accepts: a single URL or path, or a list/dictionary of URLs or paths. On top of this, :func:`datasets.DownloadManager.download_and_extract` will also extract compressed tar, gzip and zip archives.

   It returns a list of :class:`datasets.SplitGenerator`. The :class:`datasets.SplitGenerator` contains the name of the split, and keyword arguments that are provided to the :func:`datasets.DatasetBuilder._generate_examples` method. The keyword arguments can be specific to each split, and typically comprise at least the local path to the data files to load for each split.

   .. tip::

       :func:`datasets.DownloadManager.download_and_extract` can download files from a wide range of sources. If the data files are hosted on a special access server, you should use :func:`datasets.DownloadManger.download_custom`. Refer to the package reference of :class:`datasets.DownloadManager` for more details.

3. :func:`datasets.DatasetBuilder._generate_examples` reads and parses the data files for a split, and yields examples with the format specified in the ``features`` from :func:`datasets.DatasetBuilder._info`. The input of :func:`datasets.DatasetBuilder._generate_examples` is the ``filepath`` provided in the last method. 

   The dataset is generated with a Python generator, which doesn't load all the data in memory. As a result, the generator can handle large datasets. However, before the generated samples are flushed to the dataset file on disk, they are stored in an ``ArrowWriter`` buffer. This means the generated samples are written by batch. If your dataset samples consumes a lot of memory (images or videos), then make sure to specify a low value for the ``DEFAULT_WRITER_BATCH_SIZE`` attribute in :class:`datasets.DatasetBuilder`. We recommend not exceeding a size of 200MB.


Maintaining integrity
---------------------

To ensure a dataset is complete, :func:`datasets.load_dataset` will perform some tests on the downloaded files to make sure everything is there. This way, you don't encounter any nasty surprises when your requested dataset doesn't get generated as expected. :func:`datasets.load_dataset` verifies:

* the list of downloaded files
* the number of bytes of the downloaded files
* the SHA256 checksums of the downloaded files
* the number of splits in the generated ``DatasetDict``
* the number of samples in each split of the generated ``DatasetDict``

TO DO: Explain why you would want to disable the verifications or override the information used to perform the verifications.