<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="lm1b" />
  <meta itemprop="description" content="A benchmark corpus to be used for measuring progress in statistical language modeling. This has almost one billion words in the training data.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;lm1b&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/lm1b" />
  <meta itemprop="sameAs" content="http://www.statmt.org/lm-benchmark/" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/ChelbaMSGBK13,&#10;  author    = {Ciprian Chelba and&#10;               Tomas Mikolov and&#10;               Mike Schuster and&#10;               Qi Ge and&#10;               Thorsten Brants and&#10;               Phillipp Koehn},&#10;  title     = {One Billion Word Benchmark for Measuring Progress in Statistical Language&#10;               Modeling},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1312.3005},&#10;  year      = {2013},&#10;  url       = {http://arxiv.org/abs/1312.3005},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1312.3005},&#10;  timestamp = {Mon, 13 Aug 2018 16:46:16 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/ChelbaMSGBK13},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `lm1b`

*   **Description**:

A benchmark corpus to be used for measuring progress in statistical language
modeling. This has almost one billion words in the training data.

*   **Homepage**:
    [http://www.statmt.org/lm-benchmark/](http://www.statmt.org/lm-benchmark/)
*   **Source code**:
    [`tfds.text.lm1b.Lm1b`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/lm1b.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `1.67 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | ---------:
'test'  | 306,688
'train' | 30,301,028

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('text', 'text')`
*   **Citation**:

```
@article{DBLP:journals/corr/ChelbaMSGBK13,
  author    = {Ciprian Chelba and
               Tomas Mikolov and
               Mike Schuster and
               Qi Ge and
               Thorsten Brants and
               Phillipp Koehn},
  title     = {One Billion Word Benchmark for Measuring Progress in Statistical Language
               Modeling},
  journal   = {CoRR},
  volume    = {abs/1312.3005},
  year      = {2013},
  url       = {http://arxiv.org/abs/1312.3005},
  archivePrefix = {arXiv},
  eprint    = {1312.3005},
  timestamp = {Mon, 13 Aug 2018 16:46:16 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/ChelbaMSGBK13},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## lm1b/plain_text (default config)

*   **Config description**: Plain text
*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(), dtype=tf.string),
})
```

## lm1b/bytes

*   **Config description**: Uses byte-level text encoding with
    `tfds.features.text.ByteTextEncoder`
*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<ByteTextEncoder vocab_size=257>),
})
```

## lm1b/subwords8k

*   **Config description**: Uses `tfds.features.text.SubwordTextEncoder` with 8k
    vocab size
*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<SubwordTextEncoder vocab_size=8189>),
})
```

## lm1b/subwords32k

*   **Config description**: Uses `tfds.features.text.SubwordTextEncoder` with
    32k vocab size
*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<SubwordTextEncoder vocab_size=32711>),
})
```
