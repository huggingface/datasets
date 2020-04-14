<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="citrus_leaves" />
  <meta itemprop="description" content="&#10;The original citrus dataset contains 759 images of healthy and unhealthy citrus&#10;fruits and leaves. However, for now we only export 594 images of citrus leaves&#10;with the following labels: Black Spot, Canker, Greening, and Healthy. The&#10;exported images are in PNG format and have 256x256 pixels.&#10;&#10;NOTE: Leaf images with Melanose label were dropped due to very small count and&#10;other non-leaf images being present in the same directory.&#10;&#10;Dataset URL: https://data.mendeley.com/datasets/3f83gxmv57/2&#10;License: http://creativecommons.org/licenses/by/4.0&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;citrus_leaves&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/citrus_leaves" />
  <meta itemprop="sameAs" content="https://data.mendeley.com/datasets/3f83gxmv57/2" />
  <meta itemprop="citation" content="&#10;@article{rauf2019citrus,&#10;  title={A citrus fruits and leaves dataset for detection and classification of&#10;citrus diseases through machine learning},&#10;  author={Rauf, Hafiz Tayyab and Saleem, Basharat Ali and Lali, M Ikram Ullah&#10;and Khan, Muhammad Attique and Sharif, Muhammad and Bukhari, Syed Ahmad Chan},&#10;  journal={Data in brief},&#10;  volume={26},&#10;  pages={104340},&#10;  year={2019},&#10;  publisher={Elsevier}&#10;}&#10;" />
</div>
# `citrus_leaves`

*   **Description**:

The original citrus dataset contains 759 images of healthy and unhealthy citrus
fruits and leaves. However, for now we only export 594 images of citrus leaves
with the following labels: Black Spot, Canker, Greening, and Healthy. The
exported images are in PNG format and have 256x256 pixels.

NOTE: Leaf images with Melanose label were dropped due to very small count and
other non-leaf images being present in the same directory.

Dataset URL: https://data.mendeley.com/datasets/3f83gxmv57/2 License:
http://creativecommons.org/licenses/by/4.0

*   **Homepage**:
    [https://data.mendeley.com/datasets/3f83gxmv57/2](https://data.mendeley.com/datasets/3f83gxmv57/2)
*   **Source code**:
    [`tfds.image.citrus.CitrusLeaves`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/citrus.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Download size**: `63.87 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 594

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=4),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{rauf2019citrus,
  title={A citrus fruits and leaves dataset for detection and classification of
citrus diseases through machine learning},
  author={Rauf, Hafiz Tayyab and Saleem, Basharat Ali and Lali, M Ikram Ullah
and Khan, Muhammad Attique and Sharif, Muhammad and Bukhari, Syed Ahmad Chan},
  journal={Data in brief},
  volume={26},
  pages={104340},
  year={2019},
  publisher={Elsevier}
}
```
