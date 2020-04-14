<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="image_label_folder" />
  <meta itemprop="description" content="Generic image classification dataset.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;image_label_folder&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/image_label_folder" />
  <meta itemprop="sameAs" content="https://www.tensorflow.org/datasets/catalog/image_label_folder" />
  <meta itemprop="citation" content="" />
</div>
# `image_label_folder`

Warning: Manual download required. See instructions below.

*   **Description**:

Generic image classification dataset.

*   **Homepage**:
    [https://www.tensorflow.org/datasets/catalog/image_label_folder](https://www.tensorflow.org/datasets/catalog/image_label_folder)
*   **Source code**:
    [`tfds.image.image_folder.ImageLabelFolder`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/image_folder.py)
*   **Versions**:
    *   **`2.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/image_label_folder/`):<br/>
    This is a 'template' dataset.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Unknown
*   **Splits**:

Split | Examples
:---- | -------:

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=None),
})
```

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
