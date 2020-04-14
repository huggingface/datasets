<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="librispeech" />
  <meta itemprop="description" content="LibriSpeech is a corpus of approximately 1000 hours of read English speech with sampling rate of 16 kHz,&#10;prepared by Vassil Panayotov with the assistance of Daniel Povey. The data is derived from read&#10;audiobooks from the LibriVox project, and has been carefully segmented and aligned.87&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;librispeech&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/librispeech" />
  <meta itemprop="sameAs" content="http://www.openslr.org/12" />
  <meta itemprop="citation" content="@inproceedings{panayotov2015librispeech,&#10;  title={Librispeech: an ASR corpus based on public domain audio books},&#10;  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},&#10;  booktitle={Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on},&#10;  pages={5206--5210},&#10;  year={2015},&#10;  organization={IEEE}&#10;}&#10;" />
</div>
# `librispeech`

*   **Description**:

LibriSpeech is a corpus of approximately 1000 hours of read English speech with
sampling rate of 16 kHz, prepared by Vassil Panayotov with the assistance of
Daniel Povey. The data is derived from read audiobooks from the LibriVox
project, and has been carefully segmented and aligned.87

*   **Homepage**: [http://www.openslr.org/12](http://www.openslr.org/12)
*   **Source code**:
    [`tfds.audio.librispeech.Librispeech`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/audio/librispeech.py)
*   **Versions**:
    *   **`1.1.0`** (default): No release notes.
*   **Download size**: `57.14 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split            | Examples
:--------------- | -------:
'dev_clean'      | 2,703
'dev_other'      | 2,864
'test_clean'     | 2,620
'test_other'     | 2,939
'train_clean100' | 28,539
'train_clean360' | 104,014
'train_other500' | 148,688

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('speech', 'text')`
*   **Citation**:

```
@inproceedings{panayotov2015librispeech,
  title={Librispeech: an ASR corpus based on public domain audio books},
  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},
  booktitle={Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on},
  pages={5206--5210},
  year={2015},
  organization={IEEE}
}
```

## librispeech/plain_text (default config)

*   **Config description**: Transcriptions are in plain text.
*   **Dataset size**: `304.47 GiB`
*   **Features**:

```python
FeaturesDict({
    'chapter_id': tf.int64,
    'id': tf.string,
    'speaker_id': tf.int64,
    'speech': Audio(shape=(None,), dtype=tf.int64),
    'text': Text(shape=(), dtype=tf.string),
})
```

## librispeech/subwords8k

*   **Config description**: Transcriptions use the SubwordTextEncoder
*   **Dataset size**: `304.44 GiB`
*   **Features**:

```python
FeaturesDict({
    'chapter_id': tf.int64,
    'id': tf.string,
    'speaker_id': tf.int64,
    'speech': Audio(shape=(None,), dtype=tf.int64),
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<SubwordTextEncoder vocab_size=8215>),
})
```

## librispeech/subwords32k

*   **Config description**: Transcriptions use the SubwordTextEncoder
*   **Dataset size**: `304.44 GiB`
*   **Features**:

```python
FeaturesDict({
    'chapter_id': tf.int64,
    'id': tf.string,
    'speaker_id': tf.int64,
    'speech': Audio(shape=(None,), dtype=tf.int64),
    'text': Text(shape=(None,), dtype=tf.int64, encoder=<SubwordTextEncoder vocab_size=32550>),
})
```
