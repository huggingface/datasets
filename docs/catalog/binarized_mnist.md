<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="binarized_mnist" />
  <meta itemprop="description" content="A specific binarization of the MNIST images originally used in&#10;(Salakhutdinov &amp; Murray, 2008). This dataset is frequently used to evaluate&#10;generative models of images, so labels are not provided.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;binarized_mnist&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/binarized_mnist" />
  <meta itemprop="sameAs" content="http://www.dmi.usherb.ca/~larocheh/mlpython/_modules/datasets/binarized_mnist.html" />
  <meta itemprop="citation" content="@inproceedings{salakhutdinov2008quantitative,&#10;title={On the quantitative analysis of deep belief networks},&#10;author={Salakhutdinov, Ruslan and Murray, Iain},&#10;booktitle={Proceedings of the 25th international conference on Machine learning},&#10;pages={872--879},&#10;year={2008},&#10;organization={ACM}&#10;}&#10;" />
</div>
# `binarized_mnist`

*   **Description**:

A specific binarization of the MNIST images originally used in (Salakhutdinov &
Murray, 2008). This dataset is frequently used to evaluate generative models of
images, so labels are not provided.

*   **Homepage**:
    [http://www.dmi.usherb.ca/~larocheh/mlpython/_modules/datasets/binarized_mnist.html](http://www.dmi.usherb.ca/~larocheh/mlpython/_modules/datasets/binarized_mnist.html)
*   **Source code**:
    [`tfds.image.binarized_mnist.BinarizedMNIST`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/binarized_mnist.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `104.68 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 10,000
'train'      | 50,000
'validation' | 10,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@inproceedings{salakhutdinov2008quantitative,
title={On the quantitative analysis of deep belief networks},
author={Salakhutdinov, Ruslan and Murray, Iain},
booktitle={Proceedings of the 25th international conference on Machine learning},
pages={872--879},
year={2008},
organization={ACM}
}
```
