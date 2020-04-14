<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="multi_nli_mismatch" />
  <meta itemprop="description" content="The Multi-Genre Natural Language Inference (MultiNLI) corpus is a&#10;crowd-sourced collection of 433k sentence pairs annotated with textual&#10;entailment information. The corpus is modeled on the SNLI corpus, but differs in&#10;that covers a range of genres of spoken and written text, and supports a&#10;distinctive cross-genre generalization evaluation. The corpus served as the&#10;basis for the shared task of the RepEval 2017 Workshop at EMNLP in Copenhagen.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;multi_nli_mismatch&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/multi_nli_mismatch" />
  <meta itemprop="sameAs" content="https://www.nyu.edu/projects/bowman/multinli/" />
  <meta itemprop="citation" content="@InProceedings{N18-1101,&#10;  author = &quot;Williams, Adina&#10;            and Nangia, Nikita&#10;            and Bowman, Samuel&quot;,&#10;  title = &quot;A Broad-Coverage Challenge Corpus for&#10;           Sentence Understanding through Inference&quot;,&#10;  booktitle = &quot;Proceedings of the 2018 Conference of&#10;               the North American Chapter of the&#10;               Association for Computational Linguistics:&#10;               Human Language Technologies, Volume 1 (Long&#10;               Papers)&quot;,&#10;  year = &quot;2018&quot;,&#10;  publisher = &quot;Association for Computational Linguistics&quot;,&#10;  pages = &quot;1112--1122&quot;,&#10;  location = &quot;New Orleans, Louisiana&quot;,&#10;  url = &quot;http://aclweb.org/anthology/N18-1101&quot;&#10;}&#10;" />
</div>
# `multi_nli_mismatch`

*   **Description**:

The Multi-Genre Natural Language Inference (MultiNLI) corpus is a crowd-sourced
collection of 433k sentence pairs annotated with textual entailment information.
The corpus is modeled on the SNLI corpus, but differs in that covers a range of
genres of spoken and written text, and supports a distinctive cross-genre
generalization evaluation. The corpus served as the basis for the shared task of
the RepEval 2017 Workshop at EMNLP in Copenhagen.

*   **Config description**: Plain text
*   **Homepage**:
    [https://www.nyu.edu/projects/bowman/multinli/](https://www.nyu.edu/projects/bowman/multinli/)
*   **Source code**:
    [`tfds.text.multi_nli_mismatch.MultiNLIMismatch`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/multi_nli_mismatch.py)
*   **Versions**:
    *   **`0.0.1`** (default): No release notes.
*   **Download size**: `216.34 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 392,702
'validation' | 10,000

*   **Features**:

```python
FeaturesDict({
    'hypothesis': Text(shape=(), dtype=tf.string),
    'label': Text(shape=(), dtype=tf.string),
    'premise': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@InProceedings{N18-1101,
  author = "Williams, Adina
            and Nangia, Nikita
            and Bowman, Samuel",
  title = "A Broad-Coverage Challenge Corpus for
           Sentence Understanding through Inference",
  booktitle = "Proceedings of the 2018 Conference of
               the North American Chapter of the
               Association for Computational Linguistics:
               Human Language Technologies, Volume 1 (Long
               Papers)",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  pages = "1112--1122",
  location = "New Orleans, Louisiana",
  url = "http://aclweb.org/anthology/N18-1101"
}
```

## multi_nli_mismatch/plain_text (default config)
