<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="crema_d" />
  <meta itemprop="description" content="&#10;CREMA-D is an audio-visual data set for emotion recognition. The data set&#10;consists of facial and vocal emotional expressions in sentences spoken in a&#10;range of basic emotional states (happy, sad, anger, fear, disgust, and neutral).&#10;7,442 clips of 91 actors with diverse ethnic backgrounds were collected.&#10;This release contains only the audio stream from the original audio-visual&#10;recording.&#10;The samples are splitted between train, validation and testing so that samples &#10;from each speaker belongs to exactly one split.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;crema_d&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/crema_d" />
  <meta itemprop="sameAs" content="https://github.com/CheyneyComputerScience/CREMA-D" />
  <meta itemprop="citation" content="&#10;@article{cao2014crema,&#10;  title={{CREMA-D}: Crowd-sourced emotional multimodal actors dataset},&#10;  author={Cao, Houwei and Cooper, David G and Keutmann, Michael K and Gur, Ruben C and Nenkova, Ani and Verma, Ragini},&#10;  journal={IEEE transactions on affective computing},&#10;  volume={5},&#10;  number={4},&#10;  pages={377--390},&#10;  year={2014},&#10;  publisher={IEEE}&#10;}&#10;" />
</div>
# `crema_d`

*   **Description**:

CREMA-D is an audio-visual data set for emotion recognition. The data set
consists of facial and vocal emotional expressions in sentences spoken in a
range of basic emotional states (happy, sad, anger, fear, disgust, and neutral).
7,442 clips of 91 actors with diverse ethnic backgrounds were collected. This
release contains only the audio stream from the original audio-visual recording.
The samples are splitted between train, validation and testing so that samples
from each speaker belongs to exactly one split.

*   **Homepage**:
    [https://github.com/CheyneyComputerScience/CREMA-D](https://github.com/CheyneyComputerScience/CREMA-D)
*   **Source code**:
    [`tfds.audio.crema_d.CremaD`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/audio/crema_d.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `579.25 MiB`
*   **Dataset size**: `1.65 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1,556
'train'      | 5,144
'validation' | 738

*   **Features**:

```python
FeaturesDict({
    'audio': Audio(shape=(None,), dtype=tf.int64),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=6),
    'speaker_id': tf.string,
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('audio', 'label')`
*   **Citation**:

```
@article{cao2014crema,
  title={{CREMA-D}: Crowd-sourced emotional multimodal actors dataset},
  author={Cao, Houwei and Cooper, David G and Keutmann, Michael K and Gur, Ruben C and Nenkova, Ani and Verma, Ragini},
  journal={IEEE transactions on affective computing},
  volume={5},
  number={4},
  pages={377--390},
  year={2014},
  publisher={IEEE}
}
```
