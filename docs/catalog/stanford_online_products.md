<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="stanford_online_products" />
  <meta itemprop="description" content="Stanford Online Products Dataset&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;stanford_online_products&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/stanford_online_products" />
  <meta itemprop="sameAs" content="http://cvgl.stanford.edu/projects/lifted_struct/" />
  <meta itemprop="citation" content="@inproceedings{song2016deep,&#10; author    = {Song, Hyun Oh and Xiang, Yu and Jegelka, Stefanie and Savarese, Silvio},&#10; title     = {Deep Metric Learning via Lifted Structured Feature Embedding},&#10; booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},&#10; year      = {2016}&#10;}&#10;" />
</div>
# `stanford_online_products`

*   **Description**:

Stanford Online Products Dataset

*   **Homepage**:
    [http://cvgl.stanford.edu/projects/lifted_struct/](http://cvgl.stanford.edu/projects/lifted_struct/)
*   **Source code**:
    [`tfds.image.stanford_online_products.StanfordOnlineProducts`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/stanford_online_products.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `2.87 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 60,502
'train' | 59,551

*   **Features**:

```python
FeaturesDict({
    'class_id': ClassLabel(shape=(), dtype=tf.int64, num_classes=22634),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'super_class_id': ClassLabel(shape=(), dtype=tf.int64, num_classes=12),
    'super_class_id/num': ClassLabel(shape=(), dtype=tf.int64, num_classes=12),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@inproceedings{song2016deep,
 author    = {Song, Hyun Oh and Xiang, Yu and Jegelka, Stefanie and Savarese, Silvio},
 title     = {Deep Metric Learning via Lifted Structured Feature Embedding},
 booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
 year      = {2016}
}
```
