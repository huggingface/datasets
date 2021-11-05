Structure your repository
=========================

To host and share your dataset, you can create a dataset repository on the Hugging Face Dataset Hub and upload your data files.

This guide aims to explain what structure is expected when you upload a dataset.

In the following examples, CSV files are used. However you can use any supported format (text, JSON, JSON Lines, CSV, Parquet).

Main use-case
-------------

Here is an easy structure that you can use for your repository. It contains two files: `train.csv` and `test.csv`.

It also contains the dataset card `README.md` that is the `dataset card <dataset_card.html>`__ that is displayed on the dataset webpage.

::

    my_dataset_repository/
    ├── README.md
    ├── train.csv
    └── test.csv


Splits and file names
---------------------

The train/validation/test splits of your dataset are automatically infered from the file names.
All the files that contain "train" in their names are considered part of the train split.
This is the same for the test and validation split: all the files that contain "test" (resp. "valid") in their names are considered part of the test (resp. validation) split.
Here is an example where all the files are placed into a directory named `data`:

::

    my_dataset_repository/
    ├── README.md
    └── data/
        ├── train.csv
        ├── test.csv
        └── valid.csv


Multiple files per split
------------------------

If your train is split into several files it also works.

::

    my_dataset_repository/
    ├── README.md
    ├── train_0.csv
    ├── train_1.csv
    ├── train_2.csv
    ├── train_3.csv
    ├── test_0.csv
    └── test_1.csv

Just make sure that all the files of your train set have "train" inside their names (same for test and validation).
It doesn't matter if you add a prefix before "train" or a suffix after "train" in the file name (like "my_train_file_00001.csv" for example).

For convenience you can also place your data files into different directories. In this case the split name is infered from the directory name.

::

    my_dataset_repository/
    ├── README.md
    └── data/
        ├── train/
        │   ├── shard_0.csv
        │   ├── shard_1.csv
        │   ├── shard_2.csv
        │   └── shard_3.csv
        └── test/
            ├── shard_0.csv
            └── shard_1.csv


Custom split names
------------------

If you have other splits in addition to the traditionnal train/validation/test, you must use the following structure.
Note that in this case you must follow the file name format exactly: "data/<split_name>-xxxxx-of-xxxxx.csv".
Here is an example with three splits "train", "test" and "random":

::

    my_dataset_repository/
    ├── README.md
    └── data/
        ├── train-00000-of-00003.csv
        ├── train-00001-of-00003.csv
        ├── train-00002-of-00003.csv
        ├── test-00000-of-00001.csv
        ├── random-00000-of-00003.csv
        ├── random-00001-of-00003.csv
        └── random-00002-of-00003.csv


Multiple configuration (WIP)
----------------------------

You can separate different configurations of your dataset (for example if it is splti in different languages) by using one directory per configuration.

These structures is not yet supported, but are a work in progress:


::

    my_dataset_repository/
    ├── README.md
    ├── en/
    │   ├── train.csv
    │   └── test.csv
    └── fr/
        ├── train.csv
        └── test.csv

Or with one directory per split:

::

    my_dataset_repository/
    ├── README.md
    ├── en/
    │   ├── train/
    │   │   ├── shard_0.csv
    │   │   └── shard_1.csv
    │   └── test/
    │       ├── shard_0.csv
    │       └── shard_1.csv
    └── fr/
        ├── train/
        │   ├── shard_0.csv
        │   └── shard_1.csv
        └── test/
            ├── shard_0.csv
            └── shard_1.csv
