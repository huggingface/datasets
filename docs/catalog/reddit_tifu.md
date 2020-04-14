<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="reddit_tifu" />
  <meta itemprop="description" content="&#10;Reddit dataset, where TIFU denotes the name of subbreddit /r/tifu.&#10;As defined in the publication, styel &quot;short&quot; uses title as summary and&#10;&quot;long&quot; uses tldr as summary.&#10;&#10;Features includes:&#10;  - document: post text without tldr.&#10;  - tldr: tldr line.&#10;  - title: trimmed title without tldr.&#10;  - ups: upvotes.&#10;  - score: score.&#10;  - num_comments: number of comments.&#10;  - upvote_ratio: upvote ratio.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;reddit_tifu&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/reddit_tifu" />
  <meta itemprop="sameAs" content="https://github.com/ctr4si/MMN" />
  <meta itemprop="citation" content="&#10;@misc{kim2018abstractive,&#10;    title={Abstractive Summarization of Reddit Posts with Multi-level Memory Networks},&#10;    author={Byeongchang Kim and Hyunwoo Kim and Gunhee Kim},&#10;    year={2018},&#10;    eprint={1811.00783},&#10;    archivePrefix={arXiv},&#10;    primaryClass={cs.CL}&#10;}&#10;" />
</div>
# `reddit_tifu`

*   **Description**:

Reddit dataset, where TIFU denotes the name of subbreddit /r/tifu. As defined in
the publication, styel "short" uses title as summary and "long" uses tldr as
summary.

Features includes: - document: post text without tldr. - tldr: tldr line. -
title: trimmed title without tldr. - ups: upvotes. - score: score. -
num_comments: number of comments. - upvote_ratio: upvote ratio.

*   **Homepage**: [https://github.com/ctr4si/MMN](https://github.com/ctr4si/MMN)
*   **Source code**:
    [`tfds.summarization.reddit_tifu.RedditTifu`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/summarization/reddit_tifu.py)
*   **Versions**:
    *   **`1.1.0`** (default): No release notes.
*   **Download size**: `639.54 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Features**:

```python
FeaturesDict({
    'documents': Text(shape=(), dtype=tf.string),
    'num_comments': tf.float32,
    'score': tf.float32,
    'title': Text(shape=(), dtype=tf.string),
    'tldr': Text(shape=(), dtype=tf.string),
    'ups': tf.float32,
    'upvote_ratio': tf.float32,
})
```
*   **Citation**:

```
@misc{kim2018abstractive,
    title={Abstractive Summarization of Reddit Posts with Multi-level Memory Networks},
    author={Byeongchang Kim and Hyunwoo Kim and Gunhee Kim},
    year={2018},
    eprint={1811.00783},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

## reddit_tifu/short (default config)

*   **Config description**: Using title as summary.
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 79,740

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('documents', 'title')`

## reddit_tifu/long

*   **Config description**: Using TLDR as summary.
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 42,139

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('documents', 'tldr')`
