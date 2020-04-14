<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="plantae_k" />
  <meta itemprop="description" content="&#10;This dataset contains 2153 images of healthy and unhealthy plant leaves divided&#10;16 categories by species and state of health. The images are in high resolution&#10;JPG format.&#10;&#10;Note: Each image is a separate download. Some might rarely fail, therefore make&#10;sure to restart if that happens. An exception will be raised in case one of the&#10;downloads repeatedly fails.&#10;&#10;Dataset URL: https://data.mendeley.com/datasets/t6j2h22jpx/1&#10;License: http://creativecommons.org/licenses/by/4.0&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;plantae_k&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/plantae_k" />
  <meta itemprop="sameAs" content="https://data.mendeley.com/datasets/t6j2h22jpx/1" />
  <meta itemprop="citation" content="&#10;@misc{,&#10;  author={Vippon Preet Kour, Sakshi Arora},&#10;  title={PlantaeK: A leaf database of native plants of Jammu and Kashmir},&#10;  howpublished={Mendeley Data},&#10;  year={2019}&#10;}&#10;" />
</div>
# `plantae_k`

*   **Description**:

This dataset contains 2153 images of healthy and unhealthy plant leaves divided
16 categories by species and state of health. The images are in high resolution
JPG format.

Note: Each image is a separate download. Some might rarely fail, therefore make
sure to restart if that happens. An exception will be raised in case one of the
downloads repeatedly fails.

Dataset URL: https://data.mendeley.com/datasets/t6j2h22jpx/1 License:
http://creativecommons.org/licenses/by/4.0

*   **Homepage**:
    [https://data.mendeley.com/datasets/t6j2h22jpx/1](https://data.mendeley.com/datasets/t6j2h22jpx/1)
*   **Source code**:
    [`tfds.image.plantae_k.PlantaeK`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/plantae_k.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Download size**: `4.30 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,153

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=16),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@misc{,
  author={Vippon Preet Kour, Sakshi Arora},
  title={PlantaeK: A leaf database of native plants of Jammu and Kashmir},
  howpublished={Mendeley Data},
  year={2019}
}
```
