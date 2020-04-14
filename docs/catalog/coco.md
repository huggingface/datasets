<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="coco" />
  <meta itemprop="description" content="COCO is a large-scale object detection, segmentation, and&#10;captioning dataset. This version contains images, bounding boxes &quot;&#10;and labels for the 2014 version.&#10;Note:&#10; * Some images from the train and validation sets don&#x27;t have annotations.&#10; * Coco 2014 and 2017 uses the same images, but different train/val/test splits&#10; * The test split don&#x27;t have any annotations (only images).&#10; * Coco defines 91 classes but the data only uses 80 classes.&#10; * Panotptic annotations defines defines 200 classes but only uses 133.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;coco&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/coco" />
  <meta itemprop="sameAs" content="http://cocodataset.org/#home" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/LinMBHPRDZ14,&#10;  author    = {Tsung{-}Yi Lin and&#10;               Michael Maire and&#10;               Serge J. Belongie and&#10;               Lubomir D. Bourdev and&#10;               Ross B. Girshick and&#10;               James Hays and&#10;               Pietro Perona and&#10;               Deva Ramanan and&#10;               Piotr Doll{&#x27;{a}}r and&#10;               C. Lawrence Zitnick},&#10;  title     = {Microsoft {COCO:} Common Objects in Context},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1405.0312},&#10;  year      = {2014},&#10;  url       = {http://arxiv.org/abs/1405.0312},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1405.0312},&#10;  timestamp = {Mon, 13 Aug 2018 16:48:13 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/LinMBHPRDZ14},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `coco`

*   **Homepage**: [http://cocodataset.org/#home](http://cocodataset.org/#home)
*   **Source code**:
    [`tfds.object_detection.coco.Coco`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/object_detection/coco.py)
*   **Versions**:
    *   **`1.1.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{DBLP:journals/corr/LinMBHPRDZ14,
  author    = {Tsung{-}Yi Lin and
               Michael Maire and
               Serge J. Belongie and
               Lubomir D. Bourdev and
               Ross B. Girshick and
               James Hays and
               Pietro Perona and
               Deva Ramanan and
               Piotr Doll{'{a}}r and
               C. Lawrence Zitnick},
  title     = {Microsoft {COCO:} Common Objects in Context},
  journal   = {CoRR},
  volume    = {abs/1405.0312},
  year      = {2014},
  url       = {http://arxiv.org/abs/1405.0312},
  archivePrefix = {arXiv},
  eprint    = {1405.0312},
  timestamp = {Mon, 13 Aug 2018 16:48:13 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/LinMBHPRDZ14},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## coco/2014 (default config)

*   **Description**:

COCO is a large-scale object detection, segmentation, and captioning dataset.
This version contains images, bounding boxes " and labels for the 2014 version.
Note: * Some images from the train and validation sets don't have annotations. *
Coco 2014 and 2017 uses the same images, but different train/val/test splits *
The test split don't have any annotations (only images). * Coco defines 91
classes but the data only uses 80 classes. * Panotptic annotations defines
defines 200 classes but only uses 133.

*   **Config description**: COCO is a large-scale object detection,
    segmentation, and captioning dataset. This version contains images, bounding
    boxes " and labels for the 2014 version. Note:
    *   Some images from the train and validation sets don't have annotations.
    *   Coco 2014 and 2017 uses the same images, but different train/val/test
        splits
    *   The test split don't have any annotations (only images).
    *   Coco defines 91 classes but the data only uses 80 classes.
    *   Panotptic annotations defines defines 200 classes but only uses 133.
*   **Download size**: `37.57 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 40,775
'test2015'   | 81,434
'train'      | 82,783
'validation' | 40,504

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'image/id': tf.int64,
    'objects': Sequence({
        'area': tf.int64,
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
        'id': tf.int64,
        'is_crowd': tf.bool,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=80),
    }),
})
```

## coco/2017

*   **Description**:

COCO is a large-scale object detection, segmentation, and captioning dataset.
This version contains images, bounding boxes " and labels for the 2017 version.
Note: * Some images from the train and validation sets don't have annotations. *
Coco 2014 and 2017 uses the same images, but different train/val/test splits *
The test split don't have any annotations (only images). * Coco defines 91
classes but the data only uses 80 classes. * Panotptic annotations defines
defines 200 classes but only uses 133.

*   **Config description**: COCO is a large-scale object detection,
    segmentation, and captioning dataset. This version contains images, bounding
    boxes " and labels for the 2017 version. Note:
    *   Some images from the train and validation sets don't have annotations.
    *   Coco 2014 and 2017 uses the same images, but different train/val/test
        splits
    *   The test split don't have any annotations (only images).
    *   Coco defines 91 classes but the data only uses 80 classes.
    *   Panotptic annotations defines defines 200 classes but only uses 133.
*   **Download size**: `25.20 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 40,670
'train'      | 118,287
'validation' | 5,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'image/id': tf.int64,
    'objects': Sequence({
        'area': tf.int64,
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
        'id': tf.int64,
        'is_crowd': tf.bool,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=80),
    }),
})
```

## coco/2017_panoptic

*   **Description**:

COCO is a large-scale object detection, segmentation, and captioning dataset.
This version contains images, bounding boxes " and labels for the 2017 version.
Note: * Some images from the train and validation sets don't have annotations. *
Coco 2014 and 2017 uses the same images, but different train/val/test splits *
The test split don't have any annotations (only images). * Coco defines 91
classes but the data only uses 80 classes. * Panotptic annotations defines
defines 200 classes but only uses 133.

*   **Config description**: COCO is a large-scale object detection,
    segmentation, and captioning dataset. This version contains images, bounding
    boxes " and labels for the 2017 version. Note:
    *   Some images from the train and validation sets don't have annotations.
    *   Coco 2014 and 2017 uses the same images, but different train/val/test
        splits
    *   The test split don't have any annotations (only images).
    *   Coco defines 91 classes but the data only uses 80 classes.
    *   Panotptic annotations defines defines 200 classes but only uses 133.
*   **Download size**: `19.57 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 118,287
'validation' | 5,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'image/id': tf.int64,
    'panoptic_image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'panoptic_image/filename': Text(shape=(), dtype=tf.string),
    'panoptic_objects': Sequence({
        'area': tf.int64,
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
        'id': tf.int64,
        'is_crowd': tf.bool,
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=133),
    }),
})
```
