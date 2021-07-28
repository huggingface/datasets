Loading a Dataset
==================

Entire datasets are readily available to you with a single line of code: :func:`datasets.load_dataset`. But how does this simple function serve you whatever dataset you request? This guide will help you understand how :func:`datasets.load_dataset` works.

What happens when you call :func:`datasets.load_dataset`?
--------------------------------------------------------

In the beginning, :func:`datasets.load_dataset` downloads and imports the dataset loading script associated with the dataset you requested from the Hugging Face Hub. The Hub is the central repository where all the Hugging Face datasets and models are stored. Code in the loading script defines the dataset information (description, features, URL to the original files, etc.) and tells Datasets how to generate and display examples from it.

.. seealso::

    Read the Share section for a step-by-step guide on how to write your own Dataset loading script!

The loading script will download the dataset files from the original URL and cache the dataset in an Arrow table on the drive. If you've downloaded the dataset before, then Datasets will reload it from the cache to save you the trouble of downloading it again. Finally, Datasets will return the dataset built from the splits specified by the user.

Maintaining integrity
---------------------

To ensure a dataset is complete, :func:`datasets.load_dataset` will perform some tests on the downloaded files to make sure everything is there. This way, you don't encounter any nasty surprises when your requested dataset doesn't get generated as expected. :func:`datasets.load_dataset` verifies:

* the list of downloaded files
* the number of bytes of the downloaded files
* the SHA256 checksums of the downloaded files
* the number of splits in the generated ``DatasetDict``
* the number of samples in each split of the generated ``DatasetDict``

TO DO: Explain why you would want to disable the verifications or override the information used to perform the verifications.