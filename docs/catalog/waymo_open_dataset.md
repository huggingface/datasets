<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="waymo_open_dataset" />
  <meta itemprop="description" content="The Waymo Open Dataset is comprised of high resolution sensor data collected by Waymo self-driving cars in a wide variety of conditions. This data is licensed for non-commercial use.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;waymo_open_dataset&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/waymo_open_dataset" />
  <meta itemprop="sameAs" content="http://www.waymo.com/open/" />
  <meta itemprop="citation" content="&#10;@misc{waymo_open_dataset,&#10;  title = {Waymo Open Dataset: An autonomous driving dataset},&#10;  website = {url{https://www.waymo.com/open}},&#10;  year = {2020}&#10;}&#10;" />
</div>
# `waymo_open_dataset`

*   **Description**:

The Waymo Open Dataset is comprised of high resolution sensor data collected by
Waymo self-driving cars in a wide variety of conditions. This data is licensed
for non-commercial use.

*   **Homepage**: [http://www.waymo.com/open/](http://www.waymo.com/open/)
*   **Source code**:
    [`tfds.object_detection.waymo_open_dataset.WaymoOpenDataset`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/object_detection/waymo_open_dataset.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Unknown
*   **Splits**:

Split | Examples
:---- | -------:

*   **Features**:

```python
FeaturesDict({
    'camera_FRONT': FeaturesDict({
        'image': Image(shape=(1280, 1920, 3), dtype=tf.uint8),
        'labels': Sequence({
            'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
            'type': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
        }),
    }),
    'camera_FRONT_LEFT': FeaturesDict({
        'image': Image(shape=(1280, 1920, 3), dtype=tf.uint8),
        'labels': Sequence({
            'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
            'type': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
        }),
    }),
    'camera_FRONT_RIGHT': FeaturesDict({
        'image': Image(shape=(1280, 1920, 3), dtype=tf.uint8),
        'labels': Sequence({
            'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
            'type': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
        }),
    }),
    'camera_SIDE_LEFT': FeaturesDict({
        'image': Image(shape=(886, 1920, 3), dtype=tf.uint8),
        'labels': Sequence({
            'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
            'type': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
        }),
    }),
    'camera_SIDE_RIGHT': FeaturesDict({
        'image': Image(shape=(886, 1920, 3), dtype=tf.uint8),
        'labels': Sequence({
            'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
            'type': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
        }),
    }),
    'context': FeaturesDict({
        'name': Text(shape=(), dtype=tf.string),
    }),
    'timestamp_micros': tf.int64,
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@misc{waymo_open_dataset,
  title = {Waymo Open Dataset: An autonomous driving dataset},
  website = {url{https://www.waymo.com/open}},
  year = {2020}
}
```
