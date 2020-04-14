<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="savee" />
  <meta itemprop="description" content="&#10;SAVEE (Surrey Audio-Visual Expressed Emotion) is an emotion recognition&#10;dataset. It consists of recordings from 4 male actors in 7 different emotions,&#10;480 British English utterances in total. The sentences were chosen from the&#10;standard TIMIT corpus and phonetically-balanced for each emotion.&#10;This release contains only the audio stream from the original audio-visual&#10;recording.&#10;The data is split so that the training set consists of 2 speakers, and both the&#10;validation and test set consists of samples from 1 speaker, respectively.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;savee&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/savee" />
  <meta itemprop="sameAs" content="http://kahlan.eps.surrey.ac.uk/savee/" />
  <meta itemprop="citation" content="&#10;@inproceedings{Vlasenko_combiningframe,&#10;author = {Vlasenko, Bogdan and Schuller, Bjorn and Wendemuth, Andreas and Rigoll, Gerhard},&#10;year = {2007},&#10;month = {01},&#10;pages = {2249-2252},&#10;title = {Combining frame and turn-level information for robust recognition of emotions within speech},&#10;journal = {Proceedings of Interspeech}&#10;}&#10;" />
</div>
# `savee`

Warning: Manual download required. See instructions below.

*   **Description**:

SAVEE (Surrey Audio-Visual Expressed Emotion) is an emotion recognition dataset.
It consists of recordings from 4 male actors in 7 different emotions, 480
British English utterances in total. The sentences were chosen from the standard
TIMIT corpus and phonetically-balanced for each emotion. This release contains
only the audio stream from the original audio-visual recording. The data is
split so that the training set consists of 2 speakers, and both the validation
and test set consists of samples from 1 speaker, respectively.

*   **Homepage**:
    [http://kahlan.eps.surrey.ac.uk/savee/](http://kahlan.eps.surrey.ac.uk/savee/)
*   **Source code**:
    [`tfds.audio.savee.Savee`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/audio/savee.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/savee/`):<br/>
    manual_dir should contain the file AudioData.zip. This file should be under
    Data/Zip/AudioData.zip in the dataset folder provided upon registration.
    You need to register at
    http://personal.ee.surrey.ac.uk/Personal/P.Jackson/SAVEE/Register.html in
    order to get the link to download the dataset.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Unknown
*   **Splits**:

Split | Examples
:---- | -------:

*   **Features**:

```python
FeaturesDict({
    'audio': Audio(shape=(None,), dtype=tf.int64),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=7),
    'speaker_id': tf.string,
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('audio', 'label')`
*   **Citation**:

```
@inproceedings{Vlasenko_combiningframe,
author = {Vlasenko, Bogdan and Schuller, Bjorn and Wendemuth, Andreas and Rigoll, Gerhard},
year = {2007},
month = {01},
pages = {2249-2252},
title = {Combining frame and turn-level information for robust recognition of emotions within speech},
journal = {Proceedings of Interspeech}
}
```
