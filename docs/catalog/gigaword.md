<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="gigaword" />
  <meta itemprop="description" content="&#10;Headline-generation on a corpus of article pairs from Gigaword consisting of&#10;around 4 million articles. Use the &#x27;org_data&#x27; provided by&#10;https://github.com/microsoft/unilm/ which is identical to&#10;https://github.com/harvardnlp/sent-summary but with better format.&#10;&#10;There are two features:&#10;  - document: article.&#10;  - summary: headline.&#10;&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;gigaword&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/gigaword" />
  <meta itemprop="sameAs" content="https://github.com/harvardnlp/sent-summary" />
  <meta itemprop="citation" content="&#10;@article{graff2003english,&#10;  title={English gigaword},&#10;  author={Graff, David and Kong, Junbo and Chen, Ke and Maeda, Kazuaki},&#10;  journal={Linguistic Data Consortium, Philadelphia},&#10;  volume={4},&#10;  number={1},&#10;  pages={34},&#10;  year={2003}&#10;}&#10;&#10;@article{Rush_2015,&#10;   title={A Neural Attention Model for Abstractive Sentence Summarization},&#10;   url={http://dx.doi.org/10.18653/v1/D15-1044},&#10;   DOI={10.18653/v1/d15-1044},&#10;   journal={Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing},&#10;   publisher={Association for Computational Linguistics},&#10;   author={Rush, Alexander M. and Chopra, Sumit and Weston, Jason},&#10;   year={2015}&#10;}&#10;" />
</div>
# `gigaword`

*   **Description**:

Headline-generation on a corpus of article pairs from Gigaword consisting of
around 4 million articles. Use the 'org_data' provided by
https://github.com/microsoft/unilm/ which is identical to
https://github.com/harvardnlp/sent-summary but with better format.

There are two features: - document: article. - summary: headline.

*   **Homepage**:
    [https://github.com/harvardnlp/sent-summary](https://github.com/harvardnlp/sent-summary)
*   **Source code**:
    [`tfds.summarization.gigaword.Gigaword`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/summarization/gigaword.py)
*   **Versions**:
    *   **`1.2.0`** (default): No release notes.
*   **Download size**: `551.61 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | --------:
'test'       | 1,951
'train'      | 3,803,957
'validation' | 189,651

*   **Features**:

```python
FeaturesDict({
    'document': Text(shape=(), dtype=tf.string),
    'summary': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('document', 'summary')`
*   **Citation**:

```
@article{graff2003english,
  title={English gigaword},
  author={Graff, David and Kong, Junbo and Chen, Ke and Maeda, Kazuaki},
  journal={Linguistic Data Consortium, Philadelphia},
  volume={4},
  number={1},
  pages={34},
  year={2003}
}

@article{Rush_2015,
   title={A Neural Attention Model for Abstractive Sentence Summarization},
   url={http://dx.doi.org/10.18653/v1/D15-1044},
   DOI={10.18653/v1/d15-1044},
   journal={Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing},
   publisher={Association for Computational Linguistics},
   author={Rush, Alexander M. and Chopra, Sumit and Weston, Jason},
   year={2015}
}
```
