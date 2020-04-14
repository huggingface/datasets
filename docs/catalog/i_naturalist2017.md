<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="i_naturalist2017" />
  <meta itemprop="description" content="This dataset contains a total of 5,089 categories, across 579,184 training&#10;images and 95,986 validation images. For the training set, the distribution of&#10;images per category follows the observation frequency of that category by the&#10;iNaturalist community.&#10;&#10;Although the original dataset contains some images with bounding boxes,&#10;currently, only image-level annotations are provided (single label/image).&#10;In addition, the organizers have not published the test labels, so we only&#10;provide the test images (label = -1).&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;i_naturalist2017&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/i_naturalist2017" />
  <meta itemprop="sameAs" content="https://github.com/visipedia/inat_comp/tree/master/2017" />
  <meta itemprop="citation" content="@InProceedings{Horn_2018_CVPR,&#10;author = {&#10;Van Horn, Grant and Mac Aodha, Oisin and Song, Yang and Cui, Yin and Sun, Chen&#10;and Shepard, Alex and Adam, Hartwig and Perona, Pietro and Belongie, Serge},&#10;title = {The INaturalist Species Classification and Detection Dataset},&#10;booktitle = {&#10;The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},&#10;month = {June},&#10;year = {2018}&#10;}&#10;" />
</div>
# `i_naturalist2017`

*   **Description**:

This dataset contains a total of 5,089 categories, across 579,184 training
images and 95,986 validation images. For the training set, the distribution of
images per category follows the observation frequency of that category by the
iNaturalist community.

Although the original dataset contains some images with bounding boxes,
currently, only image-level annotations are provided (single label/image). In
addition, the organizers have not published the test labels, so we only provide
the test images (label = -1).

*   **Homepage**:
    [https://github.com/visipedia/inat_comp/tree/master/2017](https://github.com/visipedia/inat_comp/tree/master/2017)
*   **Source code**:
    [`tfds.image.inaturalist.INaturalist2017`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/inaturalist.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Download size**: `237.35 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 182,707
'train'      | 579,184
'validation' | 95,986

*   **Features**:

```python
FeaturesDict({
    'id': Text(shape=(), dtype=tf.string),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=5089),
    'supercategory': ClassLabel(shape=(), dtype=tf.int64, num_classes=13),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@InProceedings{Horn_2018_CVPR,
author = {
Van Horn, Grant and Mac Aodha, Oisin and Song, Yang and Cui, Yin and Sun, Chen
and Shepard, Alex and Adam, Hartwig and Perona, Pietro and Belongie, Serge},
title = {The INaturalist Species Classification and Detection Dataset},
booktitle = {
The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2018}
}
```
