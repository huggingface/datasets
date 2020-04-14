<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="librispeech_lm" />
  <meta itemprop="description" content="Language modeling resources to be used in conjunction with the LibriSpeech ASR corpus.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;librispeech_lm&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/librispeech_lm" />
  <meta itemprop="sameAs" content="http://www.openslr.org/11" />
  <meta itemprop="citation" content="@inproceedings{panayotov2015librispeech,&#10;  title={Librispeech: an ASR corpus based on public domain audio books},&#10;  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},&#10;  booktitle={Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on},&#10;  pages={5206--5210},&#10;  year={2015},&#10;  organization={IEEE}&#10;}&#10;" />
</div>
# `librispeech_lm`

*   **Description**:

Language modeling resources to be used in conjunction with the LibriSpeech ASR
corpus.

*   **Homepage**: [http://www.openslr.org/11](http://www.openslr.org/11)
*   **Source code**:
    [`tfds.text.librispeech_lm.LibrispeechLm`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/librispeech_lm.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Download size**: `1.40 GiB`
*   **Dataset size**: `4.62 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | ---------:
'train' | 40,418,260

*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('text', 'text')`
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
