<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="open_images_challenge2019_detection" />
  <meta itemprop="description" content="Open Images is a collaborative release of ~9 million images annotated with&#10;image-level labels, object bounding boxes, object segmentation masks, and&#10;visual relationships. This uniquely large and diverse dataset is designed to&#10;spur state of the art advances in analyzing and understanding images.&#10;&#10;&#10;This contains the data from thee Object Detection track of the competition.&#10;The goal in this track is to predict a tight bounding box around all object&#10;instances of 500 classes.&#10;&#10;The images are annotated with positive image-level labels, indicating certain&#10;object classes are present, and with negative image-level labels, indicating&#10;certain classes are absent. In the competition, all other unannotated classes&#10;are excluded from evaluation in that image. For each positive image-level label&#10;in an image, every instance of that object class in the image was annotated.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;open_images_challenge2019_detection&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/open_images_challenge2019_detection" />
  <meta itemprop="sameAs" content="https://storage.googleapis.com/openimages/web/challenge2019.html" />
  <meta itemprop="citation" content="" />
</div>
# `open_images_challenge2019_detection`

*   **Description**:

Open Images is a collaborative release of ~9 million images annotated with
image-level labels, object bounding boxes, object segmentation masks, and visual
relationships. This uniquely large and diverse dataset is designed to spur state
of the art advances in analyzing and understanding images.

This contains the data from thee Object Detection track of the competition. The
goal in this track is to predict a tight bounding box around all object
instances of 500 classes.

The images are annotated with positive image-level labels, indicating certain
object classes are present, and with negative image-level labels, indicating
certain classes are absent. In the competition, all other unannotated classes
are excluded from evaluation in that image. For each positive image-level label
in an image, every instance of that object class in the image was annotated.

*   **Homepage**:
    [https://storage.googleapis.com/openimages/web/challenge2019.html](https://storage.googleapis.com/openimages/web/challenge2019.html)
*   **Source code**:
    [`tfds.object_detection.open_images_challenge2019.OpenImagesChallenge2019Detection`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/object_detection/open_images_challenge2019.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `534.63 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | --------:
'test'       | 99,999
'train'      | 1,743,042
'validation' | 41,620

*   **Features**:

```python
FeaturesDict({
    'bobjects': Sequence({
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
        'is_group_of': tf.bool,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=500),
    }),
    'id': Text(shape=(), dtype=tf.string),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'objects': Sequence({
        'confidence': tf.float32,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=500),
        'source': Text(shape=(), dtype=tf.string),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`

## open_images_challenge2019_detection/200k (default config)

*   **Config description**: Images have at most 200,000 pixels, at 72 JPEG
    quality.
*   **Dataset size**: `59.40 GiB`

## open_images_challenge2019_detection/300k

*   **Config description**: Images have at most 300,000 pixels, at 72 JPEG
    quality.
*   **Dataset size**: `80.44 GiB`
