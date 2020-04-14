# Performance tips

This document provides TFDS-specific performance tips. Note that TFDS provides
datasets as `tf.data.Dataset`s, so the advice from the
[`tf.data` guide](https://www.tensorflow.org/guide/data_performance#optimize_performance)
still applies.

## Small datasets (< GB)

All TFDS datasets store the data on disk in the
[`TFRecord`](https://www.tensorflow.org/tutorials/load_data/tfrecord) format.
For small datasets (e.g. Mnist, Cifar,...), reading from `.tfrecord` can add
significant overhead.

As those datasets fit in memory, it is possible to significantly improve the
performance by caching or pre-loading the dataset. Note that TFDS automatically
caches small datasets (see next section for details).

### Caching the dataset

Here is an example of a data pipeline which explicitly caches the dataset after
normalizing the images.

```python
def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  return tf.cast(image, tf.float32) / 255., label


ds, ds_info = tfds.load(
    'mnist',
    split='train',
    as_supervised=True,  # returns `(img, label)` instead of dict(image=, ...)
    with_info=True,
)
# Applying normalization before `ds.cache()` to re-use it.
# Note: Random transformations (e.g. images augmentations) should be applied
# after both `ds.cache()` (to avoid caching randomness) and `ds.batch()` (for
# vectorization [1]).
ds = ds.map(normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
ds = ds.cache()
# For true randomness, we set the shuffle buffer to the full dataset size.
ds = ds.shuffle(ds_info.splits['train'].num_examples)
# Batch after shuffling to get unique batches at each epoch.
ds = ds.batch(128)
ds = ds.prefetch(tf.data.experimental.AUTOTUNE)
```

*   [[1] Vectorizing mapping](https://www.tensorflow.org/guide/data_performance#vectorizing_mapping)

When iterating over this dataset, the second iteration will be much faster than
the first one thanks to the caching.

### Auto-caching

By default, TFDS auto-caches datasets which satisfy the following constraints:

*   Total dataset size (all splits) is defined and < 250 MiB
*   `shuffle_files` is disabled, or only a single shard is read

It is possible to opt out of auto-caching by passing `try_autocaching=False` to
`tfds.ReadConfig` in `tfds.load`. Have a look at the dataset catalog
documentation to see if a specific dataset will use auto-cache.

### Loading the full data as a single Tensor

If your dataset fits into memory, you can also load the full dataset as a single
Tensor or NumPy array. It is possible to do so by setting `batch_size=-1` to
batch all examples in a single `tf.Tensor`. Then use `tfds.as_numpy` for the
conversion from `tf.Tensor` to `np.array`.

```
(img_train, label_train), (img_test, label_test) = tfds.as_numpy(tfds.load(
    'mnist',
    split=['train', 'test'],
    batch_size=-1,
    as_supervised=True,
))
```

## Large datasets

Large datasets are sharded (split in multiple files), and typically do not fit
in memory so they should not be cached.

### Shuffle and training

During training, it's important to shuffle the data well; poorly shuffled data
can result in lower training accuracy.

In addition to using `ds.shuffle` to shuffle records, you should also set
`shuffle_files=True` to get good shuffling behavior for larger datasets that are
sharded into multiple files. Otherwise, epochs will read the shards in the same
order, and so data won't be truly randomized.

```
ds = tfds.load('imagenet2012', split='train', shuffle_files=True)
```

Additionally, when `shuffle_files=True`, TFDS disables
[`options.experimental_deterministic`](https://www.tensorflow.org/api_docs/python/tf/data/Options?version=nightly#experimental_deterministic),
which may give a slight performance boost. To get deterministic shuffling, it is
possible to opt-out of this feature with `tfds.ReadConfig`: either by setting
`read_config.shuffle_seed` or overwriting
`read_config.options.experimental_deterministic`.

### Faster image decoding

By default TFDS automatically decodes images. However, there are cases where it
can be more performant to skip the image decoding with
`tfds.decode.SkipDecoding` and manually apply the `tf.io.decode_image` op:

*   When filtering examples (with `ds.filter`), to decode images after examples
    have been filtered.
*   When cropping images, to use the fused `tf.image.decode_and_crop_jpeg` op.

The code for both examples is available in the
[decode guide](https://www.tensorflow.org/datasets/decode#usage_examples).
