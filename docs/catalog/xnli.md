<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="xnli" />
  <meta itemprop="description" content="XNLI is a subset of a few thousand examples from MNLI which has been translated&#10;into a 14 different languages (some low-ish resource). As with MNLI, the goal is&#10;to predict textual entailment (does sentence A imply/contradict/neither sentence&#10;B) and is a classification task (given two sentences, predict one of three&#10;labels).&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;xnli&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/xnli" />
  <meta itemprop="sameAs" content="https://www.nyu.edu/projects/bowman/xnli/" />
  <meta itemprop="citation" content="@InProceedings{conneau2018xnli,&#10;  author = &quot;Conneau, Alexis&#10;                 and Rinott, Ruty&#10;                 and Lample, Guillaume&#10;                 and Williams, Adina&#10;                 and Bowman, Samuel R.&#10;                 and Schwenk, Holger&#10;                 and Stoyanov, Veselin&quot;,&#10;  title = &quot;XNLI: Evaluating Cross-lingual Sentence Representations&quot;,&#10;  booktitle = &quot;Proceedings of the 2018 Conference on Empirical Methods&#10;               in Natural Language Processing&quot;,&#10;  year = &quot;2018&quot;,&#10;  publisher = &quot;Association for Computational Linguistics&quot;,&#10;  location = &quot;Brussels, Belgium&quot;,&#10;}" />
</div>
# `xnli`

*   **Description**:

XNLI is a subset of a few thousand examples from MNLI which has been translated
into a 14 different languages (some low-ish resource). As with MNLI, the goal is
to predict textual entailment (does sentence A imply/contradict/neither sentence
B) and is a classification task (given two sentences, predict one of three
labels).

*   **Config description**: Plain text import of XNLI
*   **Homepage**:
    [https://www.nyu.edu/projects/bowman/xnli/](https://www.nyu.edu/projects/bowman/xnli/)
*   **Source code**:
    [`tfds.text.xnli.Xnli`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/xnli.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `17.04 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 5,010
'validation' | 2,490

*   **Features**:

```python
FeaturesDict({
    'hypothesis': TranslationVariableLanguages({
        'language': Text(shape=(), dtype=tf.string),
        'translation': Text(shape=(), dtype=tf.string),
    }),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
    'premise': Translation({
        'ar': Text(shape=(), dtype=tf.string),
        'bg': Text(shape=(), dtype=tf.string),
        'de': Text(shape=(), dtype=tf.string),
        'el': Text(shape=(), dtype=tf.string),
        'en': Text(shape=(), dtype=tf.string),
        'es': Text(shape=(), dtype=tf.string),
        'fr': Text(shape=(), dtype=tf.string),
        'hi': Text(shape=(), dtype=tf.string),
        'ru': Text(shape=(), dtype=tf.string),
        'sw': Text(shape=(), dtype=tf.string),
        'th': Text(shape=(), dtype=tf.string),
        'tr': Text(shape=(), dtype=tf.string),
        'ur': Text(shape=(), dtype=tf.string),
        'vi': Text(shape=(), dtype=tf.string),
        'zh': Text(shape=(), dtype=tf.string),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@InProceedings{conneau2018xnli,
  author = "Conneau, Alexis
                 and Rinott, Ruty
                 and Lample, Guillaume
                 and Williams, Adina
                 and Bowman, Samuel R.
                 and Schwenk, Holger
                 and Stoyanov, Veselin",
  title = "XNLI: Evaluating Cross-lingual Sentence Representations",
  booktitle = "Proceedings of the 2018 Conference on Empirical Methods
               in Natural Language Processing",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  location = "Brussels, Belgium",
}
```

## xnli/plain_text (default config)
