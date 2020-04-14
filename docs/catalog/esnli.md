<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="esnli" />
  <meta itemprop="description" content="&#10;The e-SNLI dataset extends the Stanford Natural Language Inference Dataset to&#10;include human-annotated natural language explanations of the entailment&#10;relations.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;esnli&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/esnli" />
  <meta itemprop="sameAs" content="https://github.com/OanaMariaCamburu/e-SNLI" />
  <meta itemprop="citation" content="&#10;@incollection{NIPS2018_8163,&#10;title = {e-SNLI: Natural Language Inference with Natural Language Explanations},&#10;author = {Camburu, Oana-Maria and Rockt&quot;{a}schel, Tim and Lukasiewicz, Thomas and Blunsom, Phil},&#10;booktitle = {Advances in Neural Information Processing Systems 31},&#10;editor = {S. Bengio and H. Wallach and H. Larochelle and K. Grauman and N. Cesa-Bianchi and R. Garnett},&#10;pages = {9539--9549},&#10;year = {2018},&#10;publisher = {Curran Associates, Inc.},&#10;url = {http://papers.nips.cc/paper/8163-e-snli-natural-language-inference-with-natural-language-explanations.pdf}&#10;}&#10;" />
</div>
# `esnli`

*   **Description**:

The e-SNLI dataset extends the Stanford Natural Language Inference Dataset to
include human-annotated natural language explanations of the entailment
relations.

*   **Config description**: Plain text import of e-SNLI
*   **Homepage**:
    [https://github.com/OanaMariaCamburu/e-SNLI](https://github.com/OanaMariaCamburu/e-SNLI)
*   **Source code**:
    [`tfds.text.esnli.Esnli`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/esnli.py)
*   **Versions**:
    *   **`0.0.2`** (default): No release notes.
*   **Download size**: `195.04 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 9,824
'train'      | 549,367
'validation' | 9,842

*   **Features**:

```python
FeaturesDict({
    'explanation_1': Text(shape=(), dtype=tf.string),
    'explanation_2': Text(shape=(), dtype=tf.string),
    'explanation_3': Text(shape=(), dtype=tf.string),
    'hypothesis': Text(shape=(), dtype=tf.string),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
    'premise': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@incollection{NIPS2018_8163,
title = {e-SNLI: Natural Language Inference with Natural Language Explanations},
author = {Camburu, Oana-Maria and Rockt"{a}schel, Tim and Lukasiewicz, Thomas and Blunsom, Phil},
booktitle = {Advances in Neural Information Processing Systems 31},
editor = {S. Bengio and H. Wallach and H. Larochelle and K. Grauman and N. Cesa-Bianchi and R. Garnett},
pages = {9539--9549},
year = {2018},
publisher = {Curran Associates, Inc.},
url = {http://papers.nips.cc/paper/8163-e-snli-natural-language-inference-with-natural-language-explanations.pdf}
}
```

## esnli/plain_text (default config)
