<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="shapes3d" />
  <meta itemprop="description" content="3dshapes is a dataset of 3D shapes procedurally generated from 6 ground truth&#10;independent latent factors. These factors are *floor colour*, *wall colour*, *object colour*,&#10;*scale*, *shape* and *orientation*.&#10;&#10;All possible combinations of these latents are present exactly once, generating N = 480000 total images.&#10;&#10;### Latent factor values&#10;&#10;*   floor hue: 10 values linearly spaced in [0, 1]&#10;*   wall hue: 10 values linearly spaced in [0, 1]&#10;*   object hue: 10 values linearly spaced in [0, 1]&#10;*   scale: 8 values linearly spaced in [0, 1]&#10;*   shape: 4 values in [0, 1, 2, 3]&#10;*   orientation: 15 values linearly spaced in [-30, 30]&#10;&#10;We varied one latent at a time (starting from orientation, then shape, etc), and sequentially stored the images in fixed order in the `images` array. The corresponding values of the factors are stored in the same order in the `labels` array.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;shapes3d&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/shapes3d" />
  <meta itemprop="sameAs" content="https://github.com/deepmind/3d-shapes" />
  <meta itemprop="citation" content="@misc{3dshapes18,&#10;  title={3D Shapes Dataset},&#10;  author={Burgess, Chris and Kim, Hyunjik},&#10;  howpublished={https://github.com/deepmind/3dshapes-dataset/},&#10;  year={2018}&#10;}&#10;" />
</div>
# `shapes3d`

*   **Description**:

3dshapes is a dataset of 3D shapes procedurally generated from 6 ground truth
independent latent factors. These factors are *floor colour*, *wall colour*,
*object colour*, *scale*, *shape* and *orientation*.

All possible combinations of these latents are present exactly once, generating
N = 480000 total images.

### Latent factor values

*   floor hue: 10 values linearly spaced in [0, 1]
*   wall hue: 10 values linearly spaced in [0, 1]
*   object hue: 10 values linearly spaced in [0, 1]
*   scale: 8 values linearly spaced in [0, 1]
*   shape: 4 values in [0, 1, 2, 3]
*   orientation: 15 values linearly spaced in [-30, 30]

We varied one latent at a time (starting from orientation, then shape, etc), and
sequentially stored the images in fixed order in the `images` array. The
corresponding values of the factors are stored in the same order in the `labels`
array.

*   **Homepage**:
    [https://github.com/deepmind/3d-shapes](https://github.com/deepmind/3d-shapes)
*   **Source code**:
    [`tfds.image.shapes3d.Shapes3d`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/shapes3d.py)
*   **Versions**:
    *   **`2.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `255.18 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 480,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(64, 64, 3), dtype=tf.uint8),
    'label_floor_hue': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
    'label_object_hue': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
    'label_orientation': ClassLabel(shape=(), dtype=tf.int64, num_classes=15),
    'label_scale': ClassLabel(shape=(), dtype=tf.int64, num_classes=8),
    'label_shape': ClassLabel(shape=(), dtype=tf.int64, num_classes=4),
    'label_wall_hue': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
    'value_floor_hue': tf.float32,
    'value_object_hue': tf.float32,
    'value_orientation': tf.float32,
    'value_scale': tf.float32,
    'value_shape': tf.float32,
    'value_wall_hue': tf.float32,
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@misc{3dshapes18,
  title={3D Shapes Dataset},
  author={Burgess, Chris and Kim, Hyunjik},
  howpublished={https://github.com/deepmind/3dshapes-dataset/},
  year={2018}
}
```
