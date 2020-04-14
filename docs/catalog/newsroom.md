<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="newsroom" />
  <meta itemprop="description" content="&#10;NEWSROOM is a large dataset for training and evaluating summarization systems.&#10;It contains 1.3 million articles and summaries written by authors and&#10;editors in the newsrooms of 38 major publications.&#10;&#10;Dataset features includes:&#10;  - text: Input news text.&#10;  - summary: Summary for the news.&#10;And additional features:&#10;  - title: news title.&#10;  - url: url of the news.&#10;  - date: date of the article.&#10;  - density: extractive density.&#10;  - coverage: extractive coverage.&#10;  - compression: compression ratio.&#10;  - density_bin: low, medium, high.&#10;  - coverage_bin: extractive, abstractive.&#10;  - compression_bin: low, medium, high.&#10;&#10;This dataset can be downloaded upon requests. Unzip all the contents&#10;&quot;train.jsonl, dev.josnl, test.jsonl&quot; to the tfds folder.&#10;&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;newsroom&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/newsroom" />
  <meta itemprop="sameAs" content="https://summari.es" />
  <meta itemprop="citation" content="&#10;@article{Grusky_2018,&#10;   title={Newsroom: A Dataset of 1.3 Million Summaries with Diverse Extractive Strategies},&#10;   url={http://dx.doi.org/10.18653/v1/n18-1065},&#10;   DOI={10.18653/v1/n18-1065},&#10;   journal={Proceedings of the 2018 Conference of the North American Chapter of&#10;          the Association for Computational Linguistics: Human Language&#10;          Technologies, Volume 1 (Long Papers)},&#10;   publisher={Association for Computational Linguistics},&#10;   author={Grusky, Max and Naaman, Mor and Artzi, Yoav},&#10;   year={2018}&#10;}&#10;&#10;" />
</div>
# `newsroom`

Warning: Manual download required. See instructions below.

*   **Description**:

NEWSROOM is a large dataset for training and evaluating summarization systems.
It contains 1.3 million articles and summaries written by authors and editors in
the newsrooms of 38 major publications.

Dataset features includes: - text: Input news text. - summary: Summary for the
news. And additional features: - title: news title. - url: url of the news. -
date: date of the article. - density: extractive density. - coverage: extractive
coverage. - compression: compression ratio. - density_bin: low, medium, high. -
coverage_bin: extractive, abstractive. - compression_bin: low, medium, high.

This dataset can be downloaded upon requests. Unzip all the contents
"train.jsonl, dev.josnl, test.jsonl" to the tfds folder.

*   **Homepage**: [https://summari.es](https://summari.es)
*   **Source code**:
    [`tfds.summarization.newsroom.Newsroom`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/summarization/newsroom.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/newsroom/`):<br/>
    You should download the dataset from https://summari.es/download/
    The webpage requires registration.
    After downloading, please put dev.jsonl, test.jsonl and train.jsonl
    files in the manual_dir.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 108,862
'train'      | 995,041
'validation' | 108,837

*   **Features**:

```python
FeaturesDict({
    'compression': tf.float32,
    'compression_bin': Text(shape=(), dtype=tf.string),
    'coverage': tf.float32,
    'coverage_bin': Text(shape=(), dtype=tf.string),
    'date': Text(shape=(), dtype=tf.string),
    'density': tf.float32,
    'density_bin': Text(shape=(), dtype=tf.string),
    'summary': Text(shape=(), dtype=tf.string),
    'text': Text(shape=(), dtype=tf.string),
    'title': Text(shape=(), dtype=tf.string),
    'url': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('text', 'summary')`
*   **Citation**:

```
@article{Grusky_2018,
   title={Newsroom: A Dataset of 1.3 Million Summaries with Diverse Extractive Strategies},
   url={http://dx.doi.org/10.18653/v1/n18-1065},
   DOI={10.18653/v1/n18-1065},
   journal={Proceedings of the 2018 Conference of the North American Chapter of
          the Association for Computational Linguistics: Human Language
          Technologies, Volume 1 (Long Papers)},
   publisher={Association for Computational Linguistics},
   author={Grusky, Max and Naaman, Mor and Artzi, Yoav},
   year={2018}
}
```
