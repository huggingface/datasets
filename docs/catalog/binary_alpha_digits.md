<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="binary_alpha_digits" />
  <meta itemprop="description" content="Binary 20x16 digits of &#x27;0&#x27; through &#x27;9&#x27; and capital &#x27;A&#x27; through &#x27;Z&#x27;. 39 examples of each class.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;binary_alpha_digits&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/binary_alpha_digits" />
  <meta itemprop="sameAs" content="https://cs.nyu.edu/~roweis/data/" />
  <meta itemprop="citation" content="&#10;" />
</div>
# `binary_alpha_digits`

*   **Description**:

Binary 20x16 digits of '0' through '9' and capital 'A' through 'Z'. 39 examples
of each class.

*   **Homepage**:
    [https://cs.nyu.edu/~roweis/data/](https://cs.nyu.edu/~roweis/data/)
*   **Source code**:
    [`tfds.image.binary_alpha_digits.BinaryAlphaDigits`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/binary_alpha_digits.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `519.83 KiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,404

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(20, 16, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=36),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```

```
