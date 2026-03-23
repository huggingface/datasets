# Cloud storage

## Hugging Face Datasets

The Hugging Face Dataset Hub is home to a growing collection of datasets that span a variety of domains and tasks.

It's more than a cloud storage: the Dataset Hub is a platform that provides data versioning thanks to git, as well as a Dataset Viewer to explore the data, making it a great place to store AI-ready datasets.

This guide shows how to import data from other cloud storage using the filesystems implementations from `fsspec`.

## Hugging Face Storage Buckets

Storage Buckets are a repo type on the Hugging Face Hub providing S3-like object storage, powered by the Xet storage backend. Unlike Git-based dataset repositories, buckets are non-versioned and mutable, designed for use cases where you need simple, fast storage such as logs, intermediate artifacts, or any large collection of files that doesn’t need version control.

## Import data from a cloud storage

Most cloud storage providers have a `fsspec` FileSystem implementation, which is useful to import data from any cloud provider with the same code.
This is especially useful to publish datasets on Hugging Face.

Take a look at the following table for some example of supported cloud storage providers:

| Storage provider     | Filesystem implementation                                     |
|----------------------|---------------------------------------------------------------|
| Amazon S3            | [s3fs](https://s3fs.readthedocs.io/en/latest/)                |
| Google Cloud Storage | [gcsfs](https://gcsfs.readthedocs.io/en/latest/)              |
| Azure Blob/DataLake  | [adlfs](https://github.com/fsspec/adlfs)                      |
| Oracle Cloud Storage | [ocifs](https://ocifs.readthedocs.io/en/latest/)              |

This guide will show you how to import data files from any cloud storage and save a dataset on Hugging Face.

Let's say we want to publish a dataset on Hugging Face from Parquet files from a cloud storage.

First, instantiate your cloud storage filesystem and list the files you'd like to import:

```python
>>> import fsspec
>>> fs = fsspec.filesystem("...")  # s3 / gcs / abfs / adl / oci / ...
>>> data_dir = "path/to/my/data/"
>>> pattern = "*.parquet"
>>> data_files = fs.glob(data_dir + pattern)
["path/to/my/data/0001.parquet", "path/to/my/data/0001.parquet", ...]
```

### Publish a Dataset

Then you can create a dataset on Hugging Face and import the data files, using for example:

```python
>>> from huggingface_hub import create_repo, upload_folder
>>> from tqdm.auto import tqdm
>>> destination_dataset = "username/my-dataset"
>>> create_repo(destination_dataset, repo_type="dataset")
>>> batch_size = 100
>>> for data_files in batched(tqdm(fs.glob(data_dir + pattern)), batch_size):
...     with TemporaryDirectory() as tmp_dir:
...         tmp_files = [os.path.join(tmp_dir, x[len(data_dir):]) for x in data_files]
...         fs.download(data_files, tmp_files)
...         upload_folder(
...             repo_id=destination_dataset,
...             folder_path=tmp_dir,
...             repo_type="dataset",
...         )
```

Check out the [huggingface_hub](https://huggingface.co/docs/huggingface_hub) documentation on files uploads [here](https://huggingface.co/docs/huggingface_hub/en/guides/upload) if you're looking for more upload options.

Finally you can now load the dataset using 🤗 Datasets:

```python
>>> from datasets import load_dataset
>>> ds = load_dataset("username/my-dataset")
```

### Import raw data to Storage Buckets

Alternatively if you wish not to publish a dataset but simply import raw data files in a Hugging Face [Storage Bucket](https://huggingface.co/docs/hub/storage-buckets), you can use:

```python
>>> from huggingface_hub import create_bucket, sync_bucket
>>> from tqdm.auto import tqdm
>>> from itertools import batched
>>> from tempfile import TemporaryDirectory
>>> import os
>>> create_bucket("username/my-bucket")
>>> bucket_files_location = "hf://buckets/username/my-bucket/path/to/raw/files"
>>> batch_size = 100
>>> for data_files in batched(tqdm(fs.glob(data_dir + pattern)), batch_size):
...     with TemporaryDirectory() as tmp_dir:
...         tmp_files = [os.path.join(tmp_dir, x[len(data_dir):]) for x in data_files]
...         fs.download(data_files, tmp_files)
...         sync_bucket(tmp_dir, bucket_files_location)
```

Check out the [huggingface_hub](https://huggingface.co/docs/huggingface_hub) documentation on Storage Buckets [here](https://huggingface.co/docs/hub/storage-buckets) if you're looking for more upload options.

Then later you can load the raw files using 🤗 Datasets, transform them and upload the final AI-ready datasets, e.g. in a streaming manner:

If the files are in a format supported by 🤗 Datasets:

```python
>>> from datasets import load_dataset
>>> ds = load_dataset(bucket_files_location, streaming=True)
>>> ds = ds.map(...).filter(...)
>>> ds.push_to_hub("username/my-dataset", num_proc=4)
>>> # and later
>>> ds = load_dataset("username/my-dataset")
```

Otherwise you can use your own file parsing function:

```python
>>> from datasets import IterableDataset
>>> from huggingface_hub import hffs
>>> data_files = hffs.find(bucket_files_location)
>>> num_shards = 1024  # For parallelism. PS: every shard should fit in RAM
>>> ds = IterableDataset.from_dict({"data_file": data_files}, num_shards=num_shards)
>>> def parse_data_files(data_files):
...     ...
...     return {"col_1": [...], "col_2": [...]}
>>> ds = ds.map(parse_data_files, batched=True, input_column=["data_file"])
>>> ds.push_to_hub("username/my-dataset", num_proc=4)
>>> # and later
>>> ds = load_dataset("username/my-dataset")
```
