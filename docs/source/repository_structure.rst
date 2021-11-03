How to structure your repository
================================

To host and share your dataset, you can upload create a dataset repository on the Hugging Face Dataset Hub and upload your data files.

This guide aims to explain what structure is expected when you upload a dataset.

Main use-case
-------------

Here is an easy structure that you can use for your repository. It contains two files: `train.csv` and `test.csv`.

It also contains the dataset card `README.md` that is the dataset card that is displayed on the dataset webpage.

```
my_dataset_repostiory/
├── README.md
├── train.csv
└── test.csv
```

Splits and file names
---------------------

The train/validation/test splits of your dataset are automatically infered from the file names.
All the files that contain "train" in their names are considered part of the train split.
This is the same for the test and validation split: all the files that contain "test" (resp. "valid") in their names are considered part of the test (resp. validation) split.
Here is an example where all the files are placed into a directory named `data`:

```
my_dataset_repostiory/
├── README.md
└── data/
    ├── train.csv
    └── test.csv
    └── valid.csv
```


Multiple files per split
------------------------

If your train is split into several files it also works. Just make sure that all the files of your train set have "train" inside their names (same for test and validation):

```
my_dataset_repostiory/
├── README.md
├── train_0.csv
├── train_1.csv
├── train_2.csv
├── train_3.csv
├── test_0.csv
└── test_1.csv
```

For convenience you can also place your data files into different directories. In this case the split name is infered from the directory name.

```
my_dataset_repostiory/
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
```


Multiple configuration (WIP)
----------------------------

WIP
