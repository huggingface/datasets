<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="open_images_v4" />
  <meta itemprop="description" content="Open Images is a dataset of ~9M images that have been annotated with image-level&#10; labels and object bounding boxes.&#10;&#10;The training set of V4 contains 14.6M bounding boxes for 600 object classes on&#10;1.74M images, making it the largest existing dataset with object location&#10;annotations. The boxes have been largely manually drawn by professional&#10;annotators to ensure accuracy and consistency. The images are very diverse and&#10;often contain complex scenes with several objects (8.4 per image on average).&#10;Moreover, the dataset is annotated with image-level labels spanning thousands of&#10;classes.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;open_images_v4&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/open_images_v4" />
  <meta itemprop="sameAs" content="https://storage.googleapis.com/openimages/web/index.html" />
  <meta itemprop="citation" content="@article{OpenImages,&#10;  author = {Alina Kuznetsova and&#10;            Hassan Rom and&#10;            Neil Alldrin and&#10;            Jasper Uijlings and&#10;            Ivan Krasin and&#10;            Jordi Pont-Tuset and&#10;            Shahab Kamali and&#10;            Stefan Popov and&#10;            Matteo Malloci and&#10;            Tom Duerig and&#10;            Vittorio Ferrari},&#10;  title = {The Open Images Dataset V4: Unified image classification,&#10;           object detection, and visual relationship detection at scale},&#10;  year = {2018},&#10;  journal = {arXiv:1811.00982}&#10;}&#10;@article{OpenImages2,&#10;  author = {Krasin, Ivan and&#10;            Duerig, Tom and&#10;            Alldrin, Neil and&#10;            Ferrari, Vittorio&#10;            and Abu-El-Haija, Sami and&#10;            Kuznetsova, Alina and&#10;            Rom, Hassan and&#10;            Uijlings, Jasper and&#10;            Popov, Stefan and&#10;            Kamali, Shahab and&#10;            Malloci, Matteo and&#10;            Pont-Tuset, Jordi and&#10;            Veit, Andreas and&#10;            Belongie, Serge and&#10;            Gomes, Victor and&#10;            Gupta, Abhinav and&#10;            Sun, Chen and&#10;            Chechik, Gal and&#10;            Cai, David and&#10;            Feng, Zheyun and&#10;            Narayanan, Dhyanesh and&#10;            Murphy, Kevin},&#10;  title = {OpenImages: A public dataset for large-scale multi-label and&#10;           multi-class image classification.},&#10;  journal = {Dataset available from&#10;             https://storage.googleapis.com/openimages/web/index.html},&#10;  year={2017}&#10;}&#10;" />
</div>
# `open_images_v4`

*   **Description**:

Open Images is a dataset of ~9M images that have been annotated with image-level
labels and object bounding boxes.

The training set of V4 contains 14.6M bounding boxes for 600 object classes on
1.74M images, making it the largest existing dataset with object location
annotations. The boxes have been largely manually drawn by professional
annotators to ensure accuracy and consistency. The images are very diverse and
often contain complex scenes with several objects (8.4 per image on average).
Moreover, the dataset is annotated with image-level labels spanning thousands of
classes.

*   **Homepage**:
    [https://storage.googleapis.com/openimages/web/index.html](https://storage.googleapis.com/openimages/web/index.html)
*   **Source code**:
    [`tfds.object_detection.open_images.OpenImagesV4`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/object_detection/open_images.py)
*   **Versions**:
    *   **`2.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `565.11 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | --------:
'test'       | 125,436
'train'      | 1,743,042
'validation' | 41,620

*   **Features**:

```python
FeaturesDict({
    'bobjects': Sequence({
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
        'is_depiction': tf.int8,
        'is_group_of': tf.int8,
        'is_inside': tf.int8,
        'is_occluded': tf.int8,
        'is_truncated': tf.int8,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=601),
        'source': ClassLabel(shape=(), dtype=tf.int64, num_classes=6),
    }),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'objects': Sequence({
        'confidence': tf.int32,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=19995),
        'source': ClassLabel(shape=(), dtype=tf.int64, num_classes=6),
    }),
    'objects_trainable': Sequence({
        'confidence': tf.int32,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=7186),
        'source': ClassLabel(shape=(), dtype=tf.int64, num_classes=6),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{OpenImages,
  author = {Alina Kuznetsova and
            Hassan Rom and
            Neil Alldrin and
            Jasper Uijlings and
            Ivan Krasin and
            Jordi Pont-Tuset and
            Shahab Kamali and
            Stefan Popov and
            Matteo Malloci and
            Tom Duerig and
            Vittorio Ferrari},
  title = {The Open Images Dataset V4: Unified image classification,
           object detection, and visual relationship detection at scale},
  year = {2018},
  journal = {arXiv:1811.00982}
}
@article{OpenImages2,
  author = {Krasin, Ivan and
            Duerig, Tom and
            Alldrin, Neil and
            Ferrari, Vittorio
            and Abu-El-Haija, Sami and
            Kuznetsova, Alina and
            Rom, Hassan and
            Uijlings, Jasper and
            Popov, Stefan and
            Kamali, Shahab and
            Malloci, Matteo and
            Pont-Tuset, Jordi and
            Veit, Andreas and
            Belongie, Serge and
            Gomes, Victor and
            Gupta, Abhinav and
            Sun, Chen and
            Chechik, Gal and
            Cai, David and
            Feng, Zheyun and
            Narayanan, Dhyanesh and
            Murphy, Kevin},
  title = {OpenImages: A public dataset for large-scale multi-label and
           multi-class image classification.},
  journal = {Dataset available from
             https://storage.googleapis.com/openimages/web/index.html},
  year={2017}
}
```

## open_images_v4/original (default config)

*   **Config description**: Images at their original resolution and quality.

## open_images_v4/300k

*   **Config description**: Images have roughly 300,000 pixels, at 72 JPEG
    quality.

## open_images_v4/200k

*   **Config description**: Images have roughly 200,000 pixels, at 72 JPEG
    quality.
