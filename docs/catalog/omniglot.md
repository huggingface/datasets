<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="omniglot" />
  <meta itemprop="description" content="Omniglot data set for one-shot learning. This dataset contains 1623 different&#10;handwritten characters from 50 different alphabets.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;omniglot&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/omniglot" />
  <meta itemprop="sameAs" content="https://github.com/brendenlake/omniglot/" />
  <meta itemprop="citation" content="@article{lake2015human,&#10;  title={Human-level concept learning through probabilistic program induction},&#10;  author={Lake, Brenden M and Salakhutdinov, Ruslan and Tenenbaum, Joshua B},&#10;  journal={Science},&#10;  volume={350},&#10;  number={6266},&#10;  pages={1332--1338},&#10;  year={2015},&#10;  publisher={American Association for the Advancement of Science}&#10;}&#10;" />
</div>
# `omniglot`

*   **Description**:

Omniglot data set for one-shot learning. This dataset contains 1623 different
handwritten characters from 50 different alphabets.

*   **Homepage**:
    [https://github.com/brendenlake/omniglot/](https://github.com/brendenlake/omniglot/)
*   **Source code**:
    [`tfds.image.omniglot.Omniglot`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/omniglot.py)
*   **Versions**:
    *   **`3.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `17.95 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split    | Examples
:------- | -------:
'small1' | 2,720
'small2' | 3,120
'test'   | 13,180
'train'  | 19,280

*   **Features**:

```python
FeaturesDict({
    'alphabet': ClassLabel(shape=(), dtype=tf.int64, num_classes=50),
    'alphabet_char_id': tf.int64,
    'image': Image(shape=(105, 105, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=1623),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{lake2015human,
  title={Human-level concept learning through probabilistic program induction},
  author={Lake, Brenden M and Salakhutdinov, Ruslan and Tenenbaum, Joshua B},
  journal={Science},
  volume={350},
  number={6266},
  pages={1332--1338},
  year={2015},
  publisher={American Association for the Advancement of Science}
}
```
