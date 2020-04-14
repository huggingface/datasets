<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>

  <meta itemprop="name" content="coil100" />
  <meta itemprop="description" content="The dataset contains 7200 color images of 100 objects&#10;(72 images per object). The objects have a wide variety of complex geometric and reflectance characteristics.&#10;The objects were placed on a motorized turntable against a black background.&#10;The turntable was rotated through 360 degrees to vary object pose with respect to a fxed color camera.&#10;Images of the objects were taken at pose intervals of   5 degrees.This corresponds to&#10;72 poses per object&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;coil100&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/coil100" />
  <meta itemprop="sameAs" content="http://www.cs.columbia.edu/CAVE/software/softlib/coil-100.php" />
  <meta itemprop="citation" content="@article{nene1996columbia,&#10;  title={Columbia object image library (coil-20)},&#10;  author={Nene, Sameer A and Nayar, Shree K and Murase, Hiroshi and others},&#10;  year={1996},&#10;  publisher={Technical report CUCS-005-96}&#10;}&#10;" />
</div>

# `coil100`

*   **Description**:

The dataset contains 7200 color images of 100 objects (72 images per object).
The objects have a wide variety of complex geometric and reflectance
characteristics. The objects were placed on a motorized turntable against a
black background. The turntable was rotated through 360 degrees to vary object
pose with respect to a fxed color camera. Images of the objects were taken at
pose intervals of 5 degrees.This corresponds to 72 poses per object

*   **Homepage**:
    [http://www.cs.columbia.edu/CAVE/software/softlib/coil-100.php](http://www.cs.columbia.edu/CAVE/software/softlib/coil-100.php)
*   **Source code**:
    [`tfds.image.coil100.Coil100`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/coil100.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `124.63 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 7,200

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(128, 128, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=72),
    'object_id': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{nene1996columbia,
  title={Columbia object image library (coil-20)},
  author={Nene, Sameer A and Nayar, Shree K and Murase, Hiroshi and others},
  year={1996},
  publisher={Technical report CUCS-005-96}
}
```
