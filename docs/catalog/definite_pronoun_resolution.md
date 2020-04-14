<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="definite_pronoun_resolution" />
  <meta itemprop="description" content="Composed by 30 students from one of the author&#x27;s undergraduate classes. These&#10;sentence pairs cover topics ranging from real events (e.g., Iran&#x27;s plan to&#10;attack the Saudi ambassador to the U.S.) to events/characters in movies (e.g.,&#10;Batman) and purely imaginary situations, largely reflecting the pop culture as&#10;perceived by the American kids born in the early 90s. Each annotated example&#10;spans four lines: the first line contains the sentence, the second line contains&#10;the target pronoun, the third line contains the two candidate antecedents, and&#10;the fourth line contains the correct antecedent. If the target pronoun appears&#10;more than once in the sentence, its first occurrence is the one to be resolved.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;definite_pronoun_resolution&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/definite_pronoun_resolution" />
  <meta itemprop="sameAs" content="http://www.hlt.utdallas.edu/~vince/data/emnlp12/" />
  <meta itemprop="citation" content="@inproceedings{rahman2012resolving,&#10;  title={Resolving complex cases of definite pronouns: the winograd schema challenge},&#10;  author={Rahman, Altaf and Ng, Vincent},&#10;  booktitle={Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning},&#10;  pages={777--789},&#10;  year={2012},&#10;  organization={Association for Computational Linguistics}&#10;}" />
</div>
# `definite_pronoun_resolution`

*   **Description**:

Composed by 30 students from one of the author's undergraduate classes. These
sentence pairs cover topics ranging from real events (e.g., Iran's plan to
attack the Saudi ambassador to the U.S.) to events/characters in movies (e.g.,
Batman) and purely imaginary situations, largely reflecting the pop culture as
perceived by the American kids born in the early 90s. Each annotated example
spans four lines: the first line contains the sentence, the second line contains
the target pronoun, the third line contains the two candidate antecedents, and
the fourth line contains the correct antecedent. If the target pronoun appears
more than once in the sentence, its first occurrence is the one to be resolved.

*   **Config description**: Plain text import of the Definite Pronoun Resolution
    Dataset.
*   **Homepage**:
    [http://www.hlt.utdallas.edu/~vince/data/emnlp12/](http://www.hlt.utdallas.edu/~vince/data/emnlp12/)
*   **Source code**:
    [`tfds.text.definite_pronoun_resolution.DefinitePronounResolution`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/definite_pronoun_resolution.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `222.12 KiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 564
'train' | 1,322

*   **Features**:

```python
FeaturesDict({
    'candidates': Sequence(Text(shape=(), dtype=tf.string)),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    'pronoun': Text(shape=(), dtype=tf.string),
    'sentence': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('sentence', 'label')`
*   **Citation**:

```
@inproceedings{rahman2012resolving,
  title={Resolving complex cases of definite pronouns: the winograd schema challenge},
  author={Rahman, Altaf and Ng, Vincent},
  booktitle={Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning},
  pages={777--789},
  year={2012},
  organization={Association for Computational Linguistics}
}
```

## definite_pronoun_resolution/plain_text (default config)
