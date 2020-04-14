<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="imdb_reviews" />
  <meta itemprop="description" content="Large Movie Review Dataset.&#10;This is a dataset for binary sentiment classification containing substantially more data than previous benchmark datasets. We provide a set of 25,000 highly polar movie reviews for training, and 25,000 for testing. There is additional unlabeled data for use as well.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;imdb_reviews&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/imdb_reviews" />
  <meta itemprop="sameAs" content="http://ai.stanford.edu/~amaas/data/sentiment/" />
  <meta itemprop="citation" content="@InProceedings{maas-EtAl:2011:ACL-HLT2011,&#10;  author    = {Maas, Andrew L.  and  Daly, Raymond E.  and  Pham, Peter T.  and  Huang, Dan  and  Ng, Andrew Y.  and  Potts, Christopher},&#10;  title     = {Learning Word Vectors for Sentiment Analysis},&#10;  booktitle = {Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies},&#10;  month     = {June},&#10;  year      = {2011},&#10;  address   = {Portland, Oregon, USA},&#10;  publisher = {Association for Computational Linguistics},&#10;  pages     = {142--150},&#10;  url       = {http://www.aclweb.org/anthology/P11-1015}&#10;}&#10;" />
</div>
# `imdb_reviews`

*   **Description**:

Large Movie Review Dataset. This is a dataset for binary sentiment
classification containing substantially more data than previous benchmark
datasets. We provide a set of 25,000 highly polar movie reviews for training,
and 25,000 for testing. There is additional unlabeled data for use as well.

*   **Homepage**:
    [http://ai.stanford.edu/~amaas/data/sentiment/](http://ai.stanford.edu/~amaas/data/sentiment/)
*   **Source code**:
    [`tfds.text.imdb.IMDBReviews`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/imdb.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `80.23 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split          | Examples
:------------- | -------:
'test'         | 25,000
'train'        | 25,000
'unsupervised' | 50,000

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('text', 'label')`
*   **Citation**:

```
@InProceedings{maas-EtAl:2011:ACL-HLT2011,
  author    = {Maas, Andrew L.  and  Daly, Raymond E.  and  Pham, Peter T.  and  Huang, Dan  and  Ng, Andrew Y.  and  Potts, Christopher},
  title     = {Learning Word Vectors for Sentiment Analysis},
  booktitle = {Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies},
  month     = {June},
  year      = {2011},
  address   = {Portland, Oregon, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {142--150},
  url       = {http://www.aclweb.org/anthology/P11-1015}
}
```

## imdb_reviews/plain_text (default config)

*   **Config description**: Plain text
*   **Features**:

```python
FeaturesDict({
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'text': Text(shape=(), dtype=tf.string),
})
```

## imdb_reviews/bytes

*   **Config description**: Uses byte-level text encoding with
    `tfds.features.text.ByteTextEncoder`
*   **Features**:

```python
FeaturesDict({
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<ByteTextEncoder vocab_size=257>),
})
```

## imdb_reviews/subwords8k

*   **Config description**: Uses `tfds.features.text.SubwordTextEncoder` with 8k
    vocab size
*   **Features**:

```python
FeaturesDict({
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<SubwordTextEncoder vocab_size=8185>),
})
```

## imdb_reviews/subwords32k

*   **Config description**: Uses `tfds.features.text.SubwordTextEncoder` with
    32k vocab size
*   **Features**:

```python
FeaturesDict({
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<SubwordTextEncoder vocab_size=32650>),
})
```
