# Using Google Cloud Storage to store preprocessed data

Normally when you use TensorFlow Datasets, the downloaded and prepared data
will be cached in a local directory (by default `~/tensorflow_datasets`).

In some environments where local disk may be ephemeral (a temporary cloud server
or a [Colab notebook](https://colab.research.google.com)) or you need the data
to be accessible by multiple machines, it's useful to
set `data_dir` to a cloud storage system, like a Google Cloud Storage (GCS)
bucket.

## How?

1.  First,
    [create a GCS bucket](https://cloud.google.com/storage/docs/creating-buckets)
    and ensure you have read/write permissions on it.
2.  If you'll be running from GCP machines where your personal credentials may
    not be available, you may want to
    [create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts)
    and give it permissions on your bucket.
3.  On a non-GCP machine, you'll have to use export a service account's key as
    JSON (
    [instructions to create a new key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys))
    and set the environment variable:

```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credential/json/file
```

When you use `tfds`, you can set `data_dir` to `"gs://YOUR_BUCKET_NAME"`

```python
ds_train, ds_test = tfds.load(name="mnist", split=["train", "test"], data_dir="gs://YOUR_BUCKET_NAME")
```


## Caveats:

* This approach works for datasets that only use `tf.io.gfile` for data access.
  This is true for most datasets, but not all.
* Remember that accessing GCS is accessing a remote server and streaming data
  from it, so you may incur network costs.
