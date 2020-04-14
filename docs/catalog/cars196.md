<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="cars196" />
  <meta itemprop="description" content="The Cars dataset contains 16,185 images of 196 classes of cars. The data is split into 8,144 training images and 8,041 testing images, where each class has been split roughly in a 50-50 split. Classes are typically at the level of Make, Model, Year, e.g. 2012 Tesla Model S or 2012 BMW M3 coupe.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;cars196&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/cars196" />
  <meta itemprop="sameAs" content="https://ai.stanford.edu/~jkrause/cars/car_dataset.html" />
  <meta itemprop="citation" content="&#10;    @inproceedings{KrauseStarkDengFei-Fei_3DRR2013,&#10;  title = {3D Object Representations for Fine-Grained Categorization},&#10;  booktitle = {4th International IEEE Workshop on  3D Representation and Recognition (3dRR-13)},&#10;  year = {2013},&#10;  address = {Sydney, Australia},&#10;  author = {Jonathan Krause and Michael Stark and Jia Deng and Li Fei-Fei}&#10;  }&#10;&#10;" />
</div>
# `cars196`

*   **Description**:

The Cars dataset contains 16,185 images of 196 classes of cars. The data is
split into 8,144 training images and 8,041 testing images, where each class has
been split roughly in a 50-50 split. Classes are typically at the level of Make,
Model, Year, e.g. 2012 Tesla Model S or 2012 BMW M3 coupe.

*   **Homepage**:
    [https://ai.stanford.edu/~jkrause/cars/car_dataset.html](https://ai.stanford.edu/~jkrause/cars/car_dataset.html)
*   **Source code**:
    [`tfds.image.cars196.Cars196`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/cars196.py)
*   **Versions**:
    *   **`2.0.0`** (default): No release notes.
*   **Download size**: `1.82 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 8,041
'train' | 8,144

*   **Features**:

```python
FeaturesDict({
    'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=196),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@inproceedings{KrauseStarkDengFei-Fei_3DRR2013,
  title = {3D Object Representations for Fine-Grained Categorization},
  booktitle = {4th International IEEE Workshop on  3D Representation and Recognition (3dRR-13)},
  year = {2013},
  address = {Sydney, Australia},
  author = {Jonathan Krause and Michael Stark and Jia Deng and Li Fei-Fei}
  }
```
