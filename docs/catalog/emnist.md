<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="emnist" />
  <meta itemprop="description" content="The EMNIST dataset is a set of handwritten character digits derived from the NIST Special Database 19 and converted to a 28x28 pixel image format and dataset structure that directly matches the MNIST dataset.&#10;&#10;Note: Like the original EMNIST data, images provided here are inverted horizontally and rotated 90 anti-clockwise. You can use `tf.transpose` within `ds.map` to convert the images to a human-friendlier format.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;emnist&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/emnist" />
  <meta itemprop="sameAs" content="https://www.nist.gov/itl/products-and-services/emnist-dataset" />
  <meta itemprop="citation" content="@article{cohen_afshar_tapson_schaik_2017,&#10;    title={EMNIST: Extending MNIST to handwritten letters},&#10;    DOI={10.1109/ijcnn.2017.7966217},&#10;    journal={2017 International Joint Conference on Neural Networks (IJCNN)},&#10;    author={Cohen, Gregory and Afshar, Saeed and Tapson, Jonathan and Schaik, Andre Van},&#10;    year={2017}&#10;}&#10;" />
</div>
# `emnist`

*   **Description**:

The EMNIST dataset is a set of handwritten character digits derived from the
NIST Special Database 19 and converted to a 28x28 pixel image format and dataset
structure that directly matches the MNIST dataset.

Note: Like the original EMNIST data, images provided here are inverted
horizontally and rotated 90 anti-clockwise. You can use `tf.transpose` within
`ds.map` to convert the images to a human-friendlier format.

*   **Homepage**:
    [https://www.nist.gov/itl/products-and-services/emnist-dataset](https://www.nist.gov/itl/products-and-services/emnist-dataset)
*   **Source code**:
    [`tfds.image.mnist.EMNIST`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/mnist.py)
*   **Versions**:
    *   **`3.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `535.73 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{cohen_afshar_tapson_schaik_2017,
    title={EMNIST: Extending MNIST to handwritten letters},
    DOI={10.1109/ijcnn.2017.7966217},
    journal={2017 International Joint Conference on Neural Networks (IJCNN)},
    author={Cohen, Gregory and Afshar, Saeed and Tapson, Jonathan and Schaik, Andre Van},
    year={2017}
}
```

## emnist/byclass (default config)

*   **Config description**: EMNIST ByClass
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 116,323
'train' | 697,932

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=62),
})
```

## emnist/bymerge

*   **Config description**: EMNIST ByMerge
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 116,323
'train' | 697,932

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=47),
})
```

## emnist/balanced

*   **Config description**: EMNIST Balanced
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 18,800
'train' | 112,800

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=47),
})
```

## emnist/letters

*   **Config description**: EMNIST Letters
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 14,800
'train' | 88,800

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=37),
})
```

## emnist/digits

*   **Config description**: EMNIST Digits
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 40,000
'train' | 240,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
})
```

## emnist/mnist

*   **Config description**: EMNIST MNIST
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 10,000
'train' | 60,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
})
```
