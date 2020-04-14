<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="multi_news" />
  <meta itemprop="description" content="&#10;Multi-News, consists of news articles and human-written summaries&#10;of these articles from the site newser.com.&#10;Each summary is professionally written by editors and&#10;includes links to the original articles cited.&#10;&#10;There are two features:&#10;  - document: text of news articles seperated by special token &quot;|||||&quot;.&#10;  - summary: news summary.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;multi_news&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/multi_news" />
  <meta itemprop="sameAs" content="https://github.com/Alex-Fabbri/Multi-News" />
  <meta itemprop="citation" content="&#10;@misc{alex2019multinews,&#10;    title={Multi-News: a Large-Scale Multi-Document Summarization Dataset and Abstractive Hierarchical Model},&#10;    author={Alexander R. Fabbri and Irene Li and Tianwei She and Suyi Li and Dragomir R. Radev},&#10;    year={2019},&#10;    eprint={1906.01749},&#10;    archivePrefix={arXiv},&#10;    primaryClass={cs.CL}&#10;}&#10;" />
</div>
# `multi_news`

*   **Description**:

Multi-News, consists of news articles and human-written summaries of these
articles from the site newser.com. Each summary is professionally written by
editors and includes links to the original articles cited.

There are two features: - document: text of news articles seperated by special
token "|||||". - summary: news summary.

*   **Homepage**:
    [https://github.com/Alex-Fabbri/Multi-News](https://github.com/Alex-Fabbri/Multi-News)
*   **Source code**:
    [`tfds.summarization.multi_news.MultiNews`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/summarization/multi_news.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `245.06 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 5,622
'train'      | 44,972
'validation' | 5,622

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
@misc{alex2019multinews,
    title={Multi-News: a Large-Scale Multi-Document Summarization Dataset and Abstractive Hierarchical Model},
    author={Alexander R. Fabbri and Irene Li and Tianwei She and Suyi Li and Dragomir R. Radev},
    year={2019},
    eprint={1906.01749},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```
