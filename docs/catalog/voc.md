<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>

  <meta itemprop="name" content="voc" />
  <meta itemprop="description" content="This dataset contains the data from the PASCAL Visual Object Classes Challenge&#10;2007, a.k.a. VOC2007, corresponding to the Classification and Detection&#10;competitions.&#10;A total of 9963 images are included in this dataset, where each image&#10;contains a set of objects, out of 20 different classes, making a total of&#10;24640 annotated objects.&#10;In the Classification competition, the goal is to predict the set of labels&#10;contained in the image, while in the Detection competition the goal is to&#10;predict the bounding box and label of each individual object.&#10;WARNING: As per the official dataset, the test set of VOC2012 does not contain&#10;annotations.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;voc&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/voc" />
  <meta itemprop="sameAs" content="http://host.robots.ox.ac.uk/pascal/VOC/voc2007/" />
  <meta itemprop="citation" content="@misc{pascal-voc-2007,&#10;    author = &quot;Everingham, M. and Van~Gool, L. and Williams, C. K. I. and Winn, J. and Zisserman, A.&quot;,&#10;    title = &quot;The {PASCAL} {V}isual {O}bject {C}lasses {C}hallenge 2007 {(VOC2007)} {R}esults&quot;,&#10;   howpublished = &quot;http://www.pascal-network.org/challenges/VOC/voc2007/workshop/index.html&quot;}&#10;" />
</div>

# `voc`

*   **Source code**:
    [`tfds.object_detection.voc.Voc`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/object_detection/voc.py)
*   **Versions**:
    *   **`4.0.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'labels': Sequence(ClassLabel(shape=(), dtype=tf.int64, num_classes=20)),
    'labels_no_difficult': Sequence(ClassLabel(shape=(), dtype=tf.int64, num_classes=20)),
    'objects': Sequence({
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
        'is_difficult': tf.bool,
        'is_truncated': tf.bool,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=20),
        'pose': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`

## voc/2007 (default config)

*   **Description**:

This dataset contains the data from the PASCAL Visual Object Classes Challenge
2007, a.k.a. VOC2007, corresponding to the Classification and Detection
competitions. A total of 9963 images are included in this dataset, where each
image contains a set of objects, out of 20 different classes, making a total of
24640 annotated objects. In the Classification competition, the goal is to
predict the set of labels contained in the image, while in the Detection
competition the goal is to predict the bounding box and label of each individual
object. WARNING: As per the official dataset, the test set of VOC2012 does not
contain annotations.

*   **Config description**: This dataset contains the data from the PASCAL
    Visual Object Classes Challenge 2007, a.k.a. VOC2007, corresponding to the
    Classification and Detection competitions. A total of 9963 images are
    included in this dataset, where each image contains a set of objects, out of
    20 different classes, making a total of 24640 annotated objects. In the
    Classification competition, the goal is to predict the set of labels
    contained in the image, while in the Detection competition the goal is to
    predict the bounding box and label of each individual object. WARNING: As
    per the official dataset, the test set of VOC2012 does not contain
    annotations.
*   **Homepage**:
    [http://host.robots.ox.ac.uk/pascal/VOC/voc2007/](http://host.robots.ox.ac.uk/pascal/VOC/voc2007/)
*   **Download size**: `868.85 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 4,952
'train'      | 2,501
'validation' | 2,510

*   **Citation**:

```
@misc{pascal-voc-2007,
    author = "Everingham, M. and Van~Gool, L. and Williams, C. K. I. and Winn, J. and Zisserman, A.",
    title = "The {PASCAL} {V}isual {O}bject {C}lasses {C}hallenge 2007 {(VOC2007)} {R}esults",
    howpublished = "http://www.pascal-network.org/challenges/VOC/voc2007/workshop/index.html"}
```

## voc/2012

*   **Description**:

This dataset contains the data from the PASCAL Visual Object Classes Challenge
2012, a.k.a. VOC2012, corresponding to the Classification and Detection
competitions. A total of 11540 images are included in this dataset, where each
image contains a set of objects, out of 20 different classes, making a total of
27450 annotated objects. In the Classification competition, the goal is to
predict the set of labels contained in the image, while in the Detection
competition the goal is to predict the bounding box and label of each individual
object. WARNING: As per the official dataset, the test set of VOC2012 does not
contain annotations.

*   **Config description**: This dataset contains the data from the PASCAL
    Visual Object Classes Challenge 2012, a.k.a. VOC2012, corresponding to the
    Classification and Detection competitions. A total of 11540 images are
    included in this dataset, where each image contains a set of objects, out of
    20 different classes, making a total of 27450 annotated objects. In the
    Classification competition, the goal is to predict the set of labels
    contained in the image, while in the Detection competition the goal is to
    predict the bounding box and label of each individual object. WARNING: As
    per the official dataset, the test set of VOC2012 does not contain
    annotations.
*   **Homepage**:
    [http://host.robots.ox.ac.uk/pascal/VOC/voc2012/](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/)
*   **Download size**: `3.59 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 10,991
'train'      | 5,717
'validation' | 5,823

*   **Citation**:

```
@misc{pascal-voc-2012,
    author = "Everingham, M. and Van~Gool, L. and Williams, C. K. I. and Winn, J. and Zisserman, A.",
    title = "The {PASCAL} {V}isual {O}bject {C}lasses {C}hallenge 2012 {(VOC2012)} {R}esults",
    howpublished = "http://www.pascal-network.org/challenges/VOC/voc2012/workshop/index.html"}
```
