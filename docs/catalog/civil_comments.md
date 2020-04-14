<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="civil_comments" />
  <meta itemprop="description" content="&#10;The comments in this dataset come from an archive of the Civil Comments&#10;platform, a commenting plugin for independent news sites. These public comments&#10;were created from 2015 - 2017 and appeared on approximately 50 English-language&#10;news sites across the world. When Civil Comments shut down in 2017, they chose&#10;to make the public comments available in a lasting open archive to enable future&#10;research. The original data, published on figshare, includes the public comment&#10;text, some associated metadata such as article IDs, timestamps and&#10;commenter-generated &quot;civility&quot; labels, but does not include user ids. Jigsaw&#10;extended this dataset by adding additional labels for toxicity and identity&#10;mentions. This data set is an exact replica of the data released for the&#10;Jigsaw Unintended Bias in Toxicity Classification Kaggle challenge.  This&#10;dataset is released under CC0, as is the underlying comment text.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;civil_comments&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/civil_comments" />
  <meta itemprop="sameAs" content="https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data" />
  <meta itemprop="citation" content="&#10;@article{DBLP:journals/corr/abs-1903-04561,&#10;  author    = {Daniel Borkan and&#10;               Lucas Dixon and&#10;               Jeffrey Sorensen and&#10;               Nithum Thain and&#10;               Lucy Vasserman},&#10;  title     = {Nuanced Metrics for Measuring Unintended Bias with Real Data for Text&#10;               Classification},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1903.04561},&#10;  year      = {2019},&#10;  url       = {http://arxiv.org/abs/1903.04561},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1903.04561},&#10;  timestamp = {Sun, 31 Mar 2019 19:01:24 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1903-04561},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `civil_comments`

*   **Description**:

The comments in this dataset come from an archive of the Civil Comments
platform, a commenting plugin for independent news sites. These public comments
were created from 2015 - 2017 and appeared on approximately 50 English-language
news sites across the world. When Civil Comments shut down in 2017, they chose
to make the public comments available in a lasting open archive to enable future
research. The original data, published on figshare, includes the public comment
text, some associated metadata such as article IDs, timestamps and
commenter-generated "civility" labels, but does not include user ids. Jigsaw
extended this dataset by adding additional labels for toxicity and identity
mentions. This data set is an exact replica of the data released for the Jigsaw
Unintended Bias in Toxicity Classification Kaggle challenge. This dataset is
released under CC0, as is the underlying comment text.

*   **Homepage**:
    [https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data)
*   **Source code**:
    [`tfds.text.civil_comments.CivilComments`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/civil_comments.py)
*   **Versions**:
    *   **`0.9.0`** (default): No release notes.
*   **Download size**: `395.73 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | --------:
'test'       | 97,320
'train'      | 1,804,874
'validation' | 97,320

*   **Features**:

```python
FeaturesDict({
    'identity_attack': tf.float32,
    'insult': tf.float32,
    'obscene': tf.float32,
    'severe_toxicity': tf.float32,
    'sexual_explicit': tf.float32,
    'text': Text(shape=(), dtype=tf.string),
    'threat': tf.float32,
    'toxicity': tf.float32,
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('text', 'toxicity')`
*   **Citation**:

```
@article{DBLP:journals/corr/abs-1903-04561,
  author    = {Daniel Borkan and
               Lucas Dixon and
               Jeffrey Sorensen and
               Nithum Thain and
               Lucy Vasserman},
  title     = {Nuanced Metrics for Measuring Unintended Bias with Real Data for Text
               Classification},
  journal   = {CoRR},
  volume    = {abs/1903.04561},
  year      = {2019},
  url       = {http://arxiv.org/abs/1903.04561},
  archivePrefix = {arXiv},
  eprint    = {1903.04561},
  timestamp = {Sun, 31 Mar 2019 19:01:24 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1903-04561},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
