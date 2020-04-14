<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="ljspeech" />
  <meta itemprop="description" content="This is a public domain speech dataset consisting of 13,100 short audio clips of&#10;a single speaker reading passages from 7 non-fiction books. A transcription is&#10;provided for each clip. Clips vary in length from 1 to 10 seconds and have a&#10;total length of approximately 24 hours.&#10;&#10;The texts were published between 1884 and 1964, and are in the public domain.&#10;The audio was recorded in 2016-17 by the LibriVox project and is also in the&#10;public domain.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;ljspeech&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/ljspeech" />
  <meta itemprop="sameAs" content="https://keithito.com/LJ-Speech-Dataset/" />
  <meta itemprop="citation" content="@misc{ljspeech17,&#10;  author       = {Keith Ito},&#10;  title        = {The LJ Speech Dataset},&#10;  howpublished = {\url{https://keithito.com/LJ-Speech-Dataset/}},&#10;  year         = 2017&#10;}&#10;" />
</div>
# `ljspeech`

*   **Description**:

This is a public domain speech dataset consisting of 13,100 short audio clips of
a single speaker reading passages from 7 non-fiction books. A transcription is
provided for each clip. Clips vary in length from 1 to 10 seconds and have a
total length of approximately 24 hours.

The texts were published between 1884 and 1964, and are in the public domain.
The audio was recorded in 2016-17 by the LibriVox project and is also in the
public domain.

*   **Homepage**:
    [https://keithito.com/LJ-Speech-Dataset/](https://keithito.com/LJ-Speech-Dataset/)
*   **Source code**:
    [`tfds.audio.ljspeech.Ljspeech`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/audio/ljspeech.py)
*   **Versions**:
    *   **`1.1.0`** (default): No release notes.
*   **Download size**: `2.56 GiB`
*   **Dataset size**: `10.73 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 13,100

*   **Features**:

```python
FeaturesDict({
    'id': tf.string,
    'speech': Audio(shape=(None,), dtype=tf.int64),
    'text': Text(shape=(), dtype=tf.string),
    'text_normalized': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('text_normalized', 'speech')`
*   **Citation**:

```
@misc{ljspeech17,
  author       = {Keith Ito},
  title        = {The LJ Speech Dataset},
  howpublished = {\url{https://keithito.com/LJ-Speech-Dataset/}},
  year         = 2017
}
```
