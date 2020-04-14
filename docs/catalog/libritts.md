<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="libritts" />
  <meta itemprop="description" content="LibriTTS is a multi-speaker English corpus of approximately 585 hours of read&#10;English speech at 24kHz sampling rate, prepared by Heiga Zen with the assistance&#10;of Google Speech and Google Brain team members. The LibriTTS corpus is designed&#10;for TTS research. It is derived from the original materials (mp3 audio files&#10;from LibriVox and text files from Project Gutenberg) of the LibriSpeech corpus.&#10;The main differences from the LibriSpeech corpus are listed below:&#10;&#10;1. The audio files are at 24kHz sampling rate.&#10;2. The speech is split at sentence breaks.&#10;3. Both original and normalized texts are included.&#10;4. Contextual information (e.g., neighbouring sentences) can be extracted.&#10;5. Utterances with significant background noise are excluded.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;libritts&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/libritts" />
  <meta itemprop="sameAs" content="http://www.openslr.org/60" />
  <meta itemprop="citation" content="@inproceedings{zen2019libritts,&#10;  title = {LibriTTS: A Corpus Derived from LibriSpeech for Text-to-Speech},&#10;  author = {H. Zen and V. Dang and R. Clark and Y. Zhang and R. J. Weiss and Y. Jia and Z. Chen and Y. Wu},&#10;  booktitle = {Proc. Interspeech},&#10;  month = sep,&#10;  year = {2019},&#10;  doi = {10.21437/Interspeech.2019-2441},&#10;}&#10;" />
</div>
# `libritts`

*   **Description**:

LibriTTS is a multi-speaker English corpus of approximately 585 hours of read
English speech at 24kHz sampling rate, prepared by Heiga Zen with the assistance
of Google Speech and Google Brain team members. The LibriTTS corpus is designed
for TTS research. It is derived from the original materials (mp3 audio files
from LibriVox and text files from Project Gutenberg) of the LibriSpeech corpus.
The main differences from the LibriSpeech corpus are listed below:

1.  The audio files are at 24kHz sampling rate.
2.  The speech is split at sentence breaks.
3.  Both original and normalized texts are included.
4.  Contextual information (e.g., neighbouring sentences) can be extracted.
5.  Utterances with significant background noise are excluded.

*   **Homepage**: [http://www.openslr.org/60](http://www.openslr.org/60)
*   **Source code**:
    [`tfds.audio.libritts.Libritts`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/audio/libritts.py)
*   **Versions**:
    *   **`1.0.1`** (default): No release notes.
*   **Download size**: `78.42 GiB`
*   **Dataset size**: `271.41 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split            | Examples
:--------------- | -------:
'dev_clean'      | 5,736
'dev_other'      | 4,613
'test_clean'     | 4,837
'test_other'     | 5,120
'train_clean100' | 33,236
'train_clean360' | 116,500
'train_other500' | 205,044

*   **Features**:

```python
FeaturesDict({
    'chapter_id': tf.int64,
    'id': tf.string,
    'speaker_id': tf.int64,
    'speech': Audio(shape=(None,), dtype=tf.int64),
    'text_normalized': Text(shape=(), dtype=tf.string),
    'text_original': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('text_normalized', 'speech')`
*   **Citation**:

```
@inproceedings{zen2019libritts,
  title = {LibriTTS: A Corpus Derived from LibriSpeech for Text-to-Speech},
  author = {H. Zen and V. Dang and R. Clark and Y. Zhang and R. J. Weiss and Y. Jia and Z. Chen and Y. Wu},
  booktitle = {Proc. Interspeech},
  month = sep,
  year = {2019},
  doi = {10.21437/Interspeech.2019-2441},
}
```
