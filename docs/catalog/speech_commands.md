<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="speech_commands" />
  <meta itemprop="description" content="&#10;An audio dataset of spoken words designed to help train and evaluate keyword&#10;spotting systems. Its primary goal is to provide a way to build and test small&#10;models that detect when a single word is spoken, from a set of ten target words,&#10;with as few false positives as possible from background noise or unrelated&#10;speech. Note that in the train and validation set, the label &quot;unknown&quot; is much&#10;more prevalent than the labels of the target words or background noise.&#10;One difference from the release version is the handling of silent segments.&#10;While in the test set the silence segments are regular 1 second files, in the&#10;training they are provided as long segments under &quot;background_noise&quot; folder.&#10;Here we split these background noise into 1 second clips, and also keep one of&#10;the files for the validation set.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;speech_commands&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/speech_commands" />
  <meta itemprop="sameAs" content="https://arxiv.org/abs/1804.03209" />
  <meta itemprop="citation" content="&#10;@article{speechcommandsv2,&#10;   author = {{Warden}, P.},&#10;    title = &quot;{Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition}&quot;,&#10;  journal = {ArXiv e-prints},&#10;  archivePrefix = &quot;arXiv&quot;,&#10;  eprint = {1804.03209},&#10;  primaryClass = &quot;cs.CL&quot;,&#10;  keywords = {Computer Science - Computation and Language, Computer Science - Human-Computer Interaction},&#10;    year = 2018,&#10;    month = apr,&#10;    url = {https://arxiv.org/abs/1804.03209},&#10;}&#10;" />
</div>
# `speech_commands`

*   **Description**:

An audio dataset of spoken words designed to help train and evaluate keyword
spotting systems. Its primary goal is to provide a way to build and test small
models that detect when a single word is spoken, from a set of ten target words,
with as few false positives as possible from background noise or unrelated
speech. Note that in the train and validation set, the label "unknown" is much
more prevalent than the labels of the target words or background noise. One
difference from the release version is the handling of silent segments. While in
the test set the silence segments are regular 1 second files, in the training
they are provided as long segments under "background_noise" folder. Here we
split these background noise into 1 second clips, and also keep one of the files
for the validation set.

*   **Homepage**:
    [https://arxiv.org/abs/1804.03209](https://arxiv.org/abs/1804.03209)
*   **Source code**:
    [`tfds.audio.speech_commands.SpeechCommands`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/audio/speech_commands.py)
*   **Versions**:
    *   **`0.0.2`** (default): No release notes.
*   **Download size**: `2.37 GiB`
*   **Dataset size**: `8.17 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 4,890
'train'      | 85,511
'validation' | 10,102

*   **Features**:

```python
FeaturesDict({
    'audio': Audio(shape=(None,), dtype=tf.int64),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=12),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('audio', 'label')`
*   **Citation**:

```
@article{speechcommandsv2,
   author = {{Warden}, P.},
    title = "{Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition}",
  journal = {ArXiv e-prints},
  archivePrefix = "arXiv",
  eprint = {1804.03209},
  primaryClass = "cs.CL",
  keywords = {Computer Science - Computation and Language, Computer Science - Human-Computer Interaction},
    year = 2018,
    month = apr,
    url = {https://arxiv.org/abs/1804.03209},
}
```
