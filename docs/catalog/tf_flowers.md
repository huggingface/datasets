<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="tf_flowers" />
  <meta itemprop="description" content="A large set of images of flowers&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;tf_flowers&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/tf_flowers" />
  <meta itemprop="sameAs" content="https://www.tensorflow.org/tutorials/load_data/images" />
  <meta itemprop="citation" content="@ONLINE {tfflowers,&#10;author = &quot;The TensorFlow Team&quot;,&#10;title = &quot;Flowers&quot;,&#10;month = &quot;jan&quot;,&#10;year = &quot;2019&quot;,&#10;url = &quot;http://download.tensorflow.org/example_images/flower_photos.tgz&quot; }&#10;" />
</div>
# `tf_flowers`

*   **Description**:

A large set of images of flowers

*   **Homepage**:
    [https://www.tensorflow.org/tutorials/load_data/images](https://www.tensorflow.org/tutorials/load_data/images)
*   **Source code**:
    [`tfds.image.flowers.TFFlowers`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/flowers.py)
*   **Versions**:
    *   **`3.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `218.21 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,670

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@ONLINE {tfflowers,
author = "The TensorFlow Team",
title = "Flowers",
month = "jan",
year = "2019",
url = "http://download.tensorflow.org/example_images/flower_photos.tgz" }
```
