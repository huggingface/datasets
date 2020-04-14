<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="gap" />
  <meta itemprop="description" content="&#10;GAP is a gender-balanced dataset containing 8,908 coreference-labeled pairs of &#10;(ambiguous pronoun, antecedent name), sampled from Wikipedia and released by &#10;Google AI Language for the evaluation of coreference resolution in practical &#10;applications.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;gap&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/gap" />
  <meta itemprop="sameAs" content="https://github.com/google-research-datasets/gap-coreference" />
  <meta itemprop="citation" content="&#10;@article{DBLP:journals/corr/abs-1810-05201,&#10;  author    = {Kellie Webster and&#10;               Marta Recasens and&#10;               Vera Axelrod and&#10;               Jason Baldridge},&#10;  title     = {Mind the {GAP:} {A} Balanced Corpus of Gendered Ambiguous Pronouns},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1810.05201},&#10;  year      = {2018},&#10;  url       = {http://arxiv.org/abs/1810.05201},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1810.05201},&#10;  timestamp = {Tue, 30 Oct 2018 20:39:56 +0100},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1810-05201},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `gap`

*   **Description**:

GAP is a gender-balanced dataset containing 8,908 coreference-labeled pairs of
(ambiguous pronoun, antecedent name), sampled from Wikipedia and released by
Google AI Language for the evaluation of coreference resolution in practical
applications.

*   **Homepage**:
    [https://github.com/google-research-datasets/gap-coreference](https://github.com/google-research-datasets/gap-coreference)
*   **Source code**:
    [`tfds.text.gap.Gap`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/gap.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Download size**: `2.29 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 2,000
'train'      | 2,000
'validation' | 454

*   **Features**:

```python
FeaturesDict({
    'A': Text(shape=(), dtype=tf.string),
    'A-coref': tf.bool,
    'A-offset': tf.int32,
    'B': Text(shape=(), dtype=tf.string),
    'B-coref': tf.bool,
    'B-offset': tf.int32,
    'ID': Text(shape=(), dtype=tf.string),
    'Pronoun': Text(shape=(), dtype=tf.string),
    'Pronoun-offset': tf.int32,
    'Text': Text(shape=(), dtype=tf.string),
    'URL': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{DBLP:journals/corr/abs-1810-05201,
  author    = {Kellie Webster and
               Marta Recasens and
               Vera Axelrod and
               Jason Baldridge},
  title     = {Mind the {GAP:} {A} Balanced Corpus of Gendered Ambiguous Pronouns},
  journal   = {CoRR},
  volume    = {abs/1810.05201},
  year      = {2018},
  url       = {http://arxiv.org/abs/1810.05201},
  archivePrefix = {arXiv},
  eprint    = {1810.05201},
  timestamp = {Tue, 30 Oct 2018 20:39:56 +0100},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1810-05201},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
