<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="horses_or_humans" />
  <meta itemprop="description" content="A large set of images of horses and humans.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;horses_or_humans&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/horses_or_humans" />
  <meta itemprop="sameAs" content="http://laurencemoroney.com/horses-or-humans-dataset" />
  <meta itemprop="citation" content="@ONLINE {horses_or_humans,&#10;author = &quot;Laurence Moroney&quot;,&#10;title = &quot;Horses or Humans Dataset&quot;,&#10;month = &quot;feb&quot;,&#10;year = &quot;2019&quot;,&#10;url = &quot;http://laurencemoroney.com/horses-or-humans-dataset&quot;&#10;}&#10;" />
</div>
# `horses_or_humans`

*   **Description**:

A large set of images of horses and humans.

*   **Homepage**:
    [http://laurencemoroney.com/horses-or-humans-dataset](http://laurencemoroney.com/horses-or-humans-dataset)
*   **Source code**:
    [`tfds.image.horses_or_humans.HorsesOrHumans`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/horses_or_humans.py)
*   **Versions**:
    *   **`3.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `153.59 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 256
'train' | 1,027

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(300, 300, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@ONLINE {horses_or_humans,
author = "Laurence Moroney",
title = "Horses or Humans Dataset",
month = "feb",
year = "2019",
url = "http://laurencemoroney.com/horses-or-humans-dataset"
}
```
