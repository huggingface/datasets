<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="mnist" />
  <meta itemprop="description" content="The MNIST database of handwritten digits.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;mnist&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/mnist" />
  <meta itemprop="sameAs" content="http://yann.lecun.com/exdb/mnist/" />
  <meta itemprop="citation" content="@article{lecun2010mnist,&#10;  title={MNIST handwritten digit database},&#10;  author={LeCun, Yann and Cortes, Corinna and Burges, CJ},&#10;  journal={ATT Labs [Online]. Available: http://yann. lecun. com/exdb/mnist},&#10;  volume={2},&#10;  year={2010}&#10;}&#10;" />
</div>
# `mnist`

*   **Description**:

The MNIST database of handwritten digits.

*   **Homepage**:
    [http://yann.lecun.com/exdb/mnist/](http://yann.lecun.com/exdb/mnist/)
*   **Source code**:
    [`tfds.image.mnist.MNIST`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/mnist.py)
*   **Versions**:
    *   **`3.0.1`** (default): No release notes.
*   **Download size**: `11.06 MiB`
*   **Dataset size**: `21.00 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
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
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{lecun2010mnist,
  title={MNIST handwritten digit database},
  author={LeCun, Yann and Cortes, Corinna and Burges, CJ},
  journal={ATT Labs [Online]. Available: http://yann. lecun. com/exdb/mnist},
  volume={2},
  year={2010}
}
```
