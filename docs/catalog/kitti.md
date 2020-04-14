<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="kitti" />
  <meta itemprop="description" content="Kitti contains a suite of vision tasks built using an autonomous driving&#10;platform. The full benchmark contains many tasks such as stereo, optical flow,&#10;visual odometry, etc. This dataset contains the object detection dataset,&#10;including the monocular images and bounding boxes. The dataset contains 7481&#10;training images annotated with 3D bounding boxes. A full description of the&#10;annotations can be found in the readme of the object development kit readme on&#10;the Kitti homepage.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;kitti&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/kitti" />
  <meta itemprop="sameAs" content="http://www.cvlibs.net/datasets/kitti/" />
  <meta itemprop="citation" content="@inproceedings{Geiger2012CVPR,&#10;  author = {Andreas Geiger and Philip Lenz and Raquel Urtasun},&#10;  title = {Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite},&#10;  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},&#10;  year = {2012}&#10;}&#10;" />
</div>
# `kitti`

*   **Description**:

Kitti contains a suite of vision tasks built using an autonomous driving
platform. The full benchmark contains many tasks such as stereo, optical flow,
visual odometry, etc. This dataset contains the object detection dataset,
including the monocular images and bounding boxes. The dataset contains 7481
training images annotated with 3D bounding boxes. A full description of the
annotations can be found in the readme of the object development kit readme on
the Kitti homepage.

*   **Homepage**:
    [http://www.cvlibs.net/datasets/kitti/](http://www.cvlibs.net/datasets/kitti/)
*   **Source code**:
    [`tfds.object_detection.kitti.Kitti`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/object_detection/kitti.py)
*   **Versions**:
    *   **`3.2.0`** (default): Devkit updated.
    *   `3.1.0`: No release notes.
*   **Download size**: `11.71 GiB`
*   **Dataset size**: `5.27 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 711
'train'      | 6,347
'validation' | 423

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/file_name': Text(shape=(), dtype=tf.string),
    'objects': Sequence({
        'alpha': tf.float32,
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
        'dimensions': Tensor(shape=(3,), dtype=tf.float32),
        'location': Tensor(shape=(3,), dtype=tf.float32),
        'occluded': ClassLabel(shape=(), dtype=tf.int64, num_classes=4),
        'rotation_y': tf.float32,
        'truncated': tf.float32,
        'type': ClassLabel(shape=(), dtype=tf.int64, num_classes=8),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@inproceedings{Geiger2012CVPR,
  author = {Andreas Geiger and Philip Lenz and Raquel Urtasun},
  title = {Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite},
  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2012}
}
```
