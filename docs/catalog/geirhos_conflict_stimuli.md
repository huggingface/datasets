<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="geirhos_conflict_stimuli" />
  <meta itemprop="description" content="Shape/texture conflict stimuli from &quot;ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness.&quot;&#10;&#10;Note that, although the dataset source contains images with matching shape and&#10;texture and we include them here, they are ignored for most evaluations in the&#10;original paper.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;geirhos_conflict_stimuli&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/geirhos_conflict_stimuli" />
  <meta itemprop="sameAs" content="https://github.com/rgeirhos/texture-vs-shape" />
  <meta itemprop="citation" content="@inproceedings{&#10;  geirhos2018imagenettrained,&#10;  title={ImageNet-trained {CNN}s are biased towards texture; increasing shape&#10;         bias improves accuracy and robustness.},&#10;  author={Robert Geirhos and Patricia Rubisch and Claudio Michaelis and&#10;          Matthias Bethge and Felix A. Wichmann and Wieland Brendel},&#10;  booktitle={International Conference on Learning Representations},&#10;  year={2019},&#10;  url={https://openreview.net/forum?id=Bygh9j09KX},&#10;}&#10;" />
</div>
# `geirhos_conflict_stimuli`

*   **Description**:

Shape/texture conflict stimuli from "ImageNet-trained CNNs are biased towards
texture; increasing shape bias improves accuracy and robustness."

Note that, although the dataset source contains images with matching shape and
texture and we include them here, they are ignored for most evaluations in the
original paper.

*   **Homepage**:
    [https://github.com/rgeirhos/texture-vs-shape](https://github.com/rgeirhos/texture-vs-shape)
*   **Source code**:
    [`tfds.image.geirhos_conflict_stimuli.GeirhosConflictStimuli`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/geirhos_conflict_stimuli.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `153.96 MiB`
*   **Dataset size**: `130.44 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Only when `shuffle_files=False` (test)
*   **Splits**:

Split  | Examples
:----- | -------:
'test' | 1,280

*   **Features**:

```python
FeaturesDict({
    'file_name': Text(shape=(), dtype=tf.string),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'shape_imagenet_labels': Sequence(ClassLabel(shape=(), dtype=tf.int64, num_classes=1000)),
    'shape_label': ClassLabel(shape=(), dtype=tf.int64, num_classes=16),
    'texture_imagenet_labels': Sequence(ClassLabel(shape=(), dtype=tf.int64, num_classes=1000)),
    'texture_label': ClassLabel(shape=(), dtype=tf.int64, num_classes=16),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'shape_label')`
*   **Citation**:

```
@inproceedings{
  geirhos2018imagenettrained,
  title={ImageNet-trained {CNN}s are biased towards texture; increasing shape
         bias improves accuracy and robustness.},
  author={Robert Geirhos and Patricia Rubisch and Claudio Michaelis and
          Matthias Bethge and Felix A. Wichmann and Wieland Brendel},
  booktitle={International Conference on Learning Representations},
  year={2019},
  url={https://openreview.net/forum?id=Bygh9j09KX},
}
```
