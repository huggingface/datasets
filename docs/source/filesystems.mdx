# Cloud storage

🤗 Datasets supports access to cloud storage providers through a `fsspec` FileSystem implementations.
You can save and load datasets from any cloud storage in a Pythonic way.
Take a look at the following table for some example of supported cloud storage providers:

| Storage provider     | Filesystem implementation                                     |
|----------------------|---------------------------------------------------------------|
| Amazon S3            | [s3fs](https://s3fs.readthedocs.io/en/latest/)                |
| Google Cloud Storage | [gcsfs](https://gcsfs.readthedocs.io/en/latest/)              |
| Azure Blob/DataLake  | [adlfs](https://github.com/fsspec/adlfs)                      |
| Dropbox              | [dropboxdrivefs](https://github.com/MarineChap/dropboxdrivefs)|
| Google Drive         | [gdrivefs](https://github.com/intake/gdrivefs)                |
| Oracle Cloud Storage | [ocifs](https://ocifs.readthedocs.io/en/latest/)              |

This guide will show you how to save and load datasets with any cloud storage.
Here are examples for S3, Google Cloud Storage, Azure Blob Storage, and Oracle Cloud Object Storage.

## Set up your cloud storage FileSystem

### Amazon S3

1. Install the S3 FileSystem implementation:

```
>>> pip install s3fs
```

2. Define your credentials

To use an anonymous connection, use `anon=True`.
Otherwise, include your `aws_access_key_id` and `aws_secret_access_key` whenever you are interacting with a private S3 bucket.

```py
>>> storage_options = {"anon": True}  # for anonymous connection
# or use your credentials
>>> storage_options = {"key": aws_access_key_id, "secret": aws_secret_access_key}  # for private buckets
# or use a botocore session
>>> import aiobotocore.session
>>> s3_session = aiobotocore.session.AioSession(profile="my_profile_name")
>>> storage_options = {"session": s3_session}
```

3. Create your FileSystem instance

```py
>>> import s3fs
>>> fs = s3fs.S3FileSystem(**storage_options)
```

### Google Cloud Storage

1. Install the Google Cloud Storage implementation:

```
>>> conda install -c conda-forge gcsfs
# or install with pip
>>> pip install gcsfs
```

2. Define your credentials

```py
>>> storage_options={"token": "anon"}  # for anonymous connection
# or use your credentials of your default gcloud credentials or from the google metadata service
>>> storage_options={"project": "my-google-project"}
# or use your credentials from elsewhere, see the documentation at https://gcsfs.readthedocs.io/
>>> storage_options={"project": "my-google-project", "token": TOKEN}
```

3. Create your FileSystem instance

```py
>>> import gcsfs
>>> fs = gcsfs.GCSFileSystem(**storage_options)
```

### Azure Blob Storage

1. Install the Azure Blob Storage implementation:

```
>>> conda install -c conda-forge adlfs
# or install with pip
>>> pip install adlfs
```

2. Define your credentials

```py
>>> storage_options = {"anon": True}  # for anonymous connection
# or use your credentials
>>> storage_options = {"account_name": ACCOUNT_NAME, "account_key": ACCOUNT_KEY}  # gen 2 filesystem
# or use your credentials with the gen 1 filesystem
>>> storage_options={"tenant_id": TENANT_ID, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
```

3. Create your FileSystem instance

```py
>>> import adlfs
>>> fs = adlfs.AzureBlobFileSystem(**storage_options)
```

### Oracle Cloud Object Storage

1. Install the OCI FileSystem implementation:

```
>>> pip install ocifs
```

2. Define your credentials

```py
>>> storage_options = {"config": "~/.oci/config", "region": "us-ashburn-1"} 
```

3. Create your FileSystem instance

```py
>>> import ocifs
>>> fs = ocifs.OCIFileSystem(**storage_options)
```

## Load and Save your datasets using your cloud storage FileSystem

### Download and prepare a dataset into a cloud storage

You can download and prepare a dataset into your cloud storage by specifying a remote `output_dir` in `download_and_prepare`.
Don't forget to use the previously defined `storage_options` containing your credentials to write into a private cloud storage.

The `download_and_prepare` method works in two steps:
1. it first downloads the raw data files (if any) in your local cache. You can set your cache directory by passing `cache_dir` to [`load_dataset_builder`]
2. then it generates the dataset in Arrow or Parquet format in your cloud storage by iterating over the raw data files.

Load a dataset builder from the Hugging Face Hub (see [how to load from the Hugging Face Hub](./loading#hugging-face-hub)):

```py
>>> output_dir = "s3://my-bucket/imdb"
>>> builder = load_dataset_builder("imdb")
>>> builder.download_and_prepare(output_dir, storage_options=storage_options, file_format="parquet")
```

Load a dataset builder using a loading script (see [how to load a local loading script](./loading#local-loading-script)):

```py
>>> output_dir = "s3://my-bucket/imdb"
>>> builder = load_dataset_builder("path/to/local/loading_script/loading_script.py")
>>> builder.download_and_prepare(output_dir, storage_options=storage_options, file_format="parquet")
```

Use your own data files (see [how to load local and remote files](./loading#local-and-remote-files)):

```py
>>> data_files = {"train": ["path/to/train.csv"]}
>>> output_dir = "s3://my-bucket/imdb"
>>> builder = load_dataset_builder("csv", data_files=data_files)
>>> builder.download_and_prepare(output_dir, storage_options=storage_options, file_format="parquet")
```

It is highly recommended to save the files as compressed Parquet files to optimize I/O by specifying `file_format="parquet"`.
Otherwise the dataset is saved as an uncompressed Arrow file.

You can also specify the size of the shards using `max_shard_size` (default is 500MB):

```py
>>> builder.download_and_prepare(output_dir, storage_options=storage_options, file_format="parquet", max_shard_size="1GB")
```

#### Dask

Dask is a parallel computing library and it has a pandas-like API for working with larger than memory Parquet datasets in parallel.
Dask can use multiple threads or processes on a single machine, or a cluster of machines to process data in parallel.
Dask supports local data but also data from a cloud storage.

Therefore you can load a dataset saved as sharded Parquet files in Dask with

```py
import dask.dataframe as dd

df = dd.read_parquet(output_dir, storage_options=storage_options)

# or if your dataset is split into train/valid/test
df_train = dd.read_parquet(output_dir + f"/{builder.name}-train-*.parquet", storage_options=storage_options)
df_valid = dd.read_parquet(output_dir + f"/{builder.name}-validation-*.parquet", storage_options=storage_options)
df_test = dd.read_parquet(output_dir + f"/{builder.name}-test-*.parquet", storage_options=storage_options)
```

You can find more about dask dataframes in their [documentation](https://docs.dask.org/en/stable/dataframe.html).

## Saving serialized datasets

After you have processed your dataset, you can save it to your cloud storage with [`Dataset.save_to_disk`]:

```py
# saves encoded_dataset to amazon s3
>>> encoded_dataset.save_to_disk("s3://my-private-datasets/imdb/train", storage_options=storage_options)
# saves encoded_dataset to google cloud storage
>>> encoded_dataset.save_to_disk("gcs://my-private-datasets/imdb/train", storage_options=storage_options)
# saves encoded_dataset to microsoft azure blob/datalake
>>> encoded_dataset.save_to_disk("adl://my-private-datasets/imdb/train", storage_options=storage_options)
```

<Tip>

Remember to define your credentials in your [FileSystem instance](#set-up-your-cloud-storage-filesystem) `fs` whenever you are interacting with a private cloud storage.

</Tip>

## Listing serialized datasets

List files from a cloud storage with your FileSystem instance `fs`, using `fs.ls`:

```py
>>> fs.ls("my-private-datasets/imdb/train", detail=False)
["dataset_info.json.json","dataset.arrow","state.json"]
```

### Load serialized datasets

When you are ready to use your dataset again, reload it with [`Dataset.load_from_disk`]:

```py
>>> from datasets import load_from_disk
# load encoded_dataset from cloud storage
>>> dataset = load_from_disk("s3://a-public-datasets/imdb/train", storage_options=storage_options)  
>>> print(len(dataset))
25000
```
