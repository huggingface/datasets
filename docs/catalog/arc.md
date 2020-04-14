<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="arc" />
  <meta itemprop="description" content="&#10;ARC can be seen as a general artificial intelligence benchmark, as a program&#10;synthesis benchmark, or as a psychometric intelligence test. It is targeted at&#10;both humans and artificially intelligent systems that aim at emulating a&#10;human-like form of general fluid intelligence.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;arc&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/arc" />
  <meta itemprop="sameAs" content="https://github.com/fchollet/ARC/" />
  <meta itemprop="citation" content="&#10;@misc{chollet_francois_2019,&#10;  title     = {The Measure of Intelligence},&#10;  url       = {https://arxiv.org/abs/1911.01547},&#10;  journal   = {arXiv.org},&#10;  author    = {Francois Chollet},&#10;  year      = {2019},&#10;  month     = {Nov}&#10;}&#10;" />
</div>
# `arc`

*   **Description**:

ARC can be seen as a general artificial intelligence benchmark, as a program
synthesis benchmark, or as a psychometric intelligence test. It is targeted at
both humans and artificially intelligent systems that aim at emulating a
human-like form of general fluid intelligence.

*   **Config description**: ARC commit bd9e2c9 from 2019-12-06
*   **Homepage**:
    [https://github.com/fchollet/ARC/](https://github.com/fchollet/ARC/)
*   **Source code**:
    [`tfds.image.arc.ARC`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/arc.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `465.07 KiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 400
'train' | 400

*   **Features**:

```python
FeaturesDict({
    'task_id': Text(shape=(), dtype=tf.string),
    'test': Sequence({
        'input': Sequence(Sequence(tf.int32)),
        'output': Sequence(Sequence(tf.int32)),
    }),
    'train': Sequence({
        'input': Sequence(Sequence(tf.int32)),
        'output': Sequence(Sequence(tf.int32)),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@misc{chollet_francois_2019,
  title     = {The Measure of Intelligence},
  url       = {https://arxiv.org/abs/1911.01547},
  journal   = {arXiv.org},
  author    = {Francois Chollet},
  year      = {2019},
  month     = {Nov}
}
```

## arc/2019-12-06 (default config)
