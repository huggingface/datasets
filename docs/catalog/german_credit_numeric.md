<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="german_credit_numeric" />
  <meta itemprop="description" content="&#10;This dataset classifies people described by a set of attributes as good or bad&#10;credit risks. The version here is the &quot;numeric&quot; variant where categorical and&#10;ordered categorical attributes have been encoded as indicator and integer&#10;quantities respectively.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;german_credit_numeric&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/german_credit_numeric" />
  <meta itemprop="sameAs" content="https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)" />
  <meta itemprop="citation" content="@misc{Dua:2019 ,&#10;author = &quot;Dua, Dheeru and Graff, Casey&quot;,&#10;year = &quot;2017&quot;,&#10;title = &quot;{UCI} Machine Learning Repository&quot;,&#10;url = &quot;http://archive.ics.uci.edu/ml&quot;,&#10;institution = &quot;University of California, Irvine, School of Information and Computer Sciences&quot;&#10;}&#10;" />
</div>
# `german_credit_numeric`

*   **Description**:

This dataset classifies people described by a set of attributes as good or bad
credit risks. The version here is the "numeric" variant where categorical and
ordered categorical attributes have been encoded as indicator and integer
quantities respectively.

*   **Homepage**:
    [https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)](https://archive.ics.uci.edu/ml/datasets/Statlog+\(German+Credit+Data\))
*   **Source code**:
    [`tfds.structured.german_credit_numeric.GermanCreditNumeric`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/structured/german_credit_numeric.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `99.61 KiB`
*   **Dataset size**: `58.61 KiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,000

*   **Features**:

```python
FeaturesDict({
    'features': Tensor(shape=(24,), dtype=tf.int32),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('features', 'label')`
*   **Citation**:

```
@misc{Dua:2019 ,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences"
}
```
