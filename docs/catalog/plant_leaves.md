<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="plant_leaves" />
  <meta itemprop="description" content="&#10;This dataset consists of 4502 images of healthy and unhealthy plant leaves&#10;divided into 22 categories by species and state of health. The images are in&#10;high resolution JPG format.&#10;&#10;There are no files with label prefix 0000, therefore label encoding is shifted&#10;by one (e.g. file with label prefix 0001 gets encoded label 0).&#10;&#10;Note: Each image is a separate download. Some might rarely fail, therefore make&#10;sure to restart if that happens. An exception will be raised in case one of the&#10;downloads repeatedly fails.&#10;&#10;Dataset URL: https://data.mendeley.com/datasets/hb74ynkjcn/1&#10;License: http://creativecommons.org/licenses/by/4.0&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;plant_leaves&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/plant_leaves" />
  <meta itemprop="sameAs" content="https://data.mendeley.com/datasets/hb74ynkjcn/1" />
  <meta itemprop="citation" content="&#10;@misc{,&#10;  author={Siddharth Singh Chouhan, Ajay Kaul, Uday Pratap Singh, Sanjeev&#10;Jain},&#10;  title={A Database of Leaf Images: Practice towards Plant Conservation with&#10;Plant Pathology},&#10;  howpublished={Mendeley Data},&#10;  year={2019}&#10;}&#10;" />
</div>
# `plant_leaves`

*   **Description**:

This dataset consists of 4502 images of healthy and unhealthy plant leaves
divided into 22 categories by species and state of health. The images are in
high resolution JPG format.

There are no files with label prefix 0000, therefore label encoding is shifted
by one (e.g. file with label prefix 0001 gets encoded label 0).

Note: Each image is a separate download. Some might rarely fail, therefore make
sure to restart if that happens. An exception will be raised in case one of the
downloads repeatedly fails.

Dataset URL: https://data.mendeley.com/datasets/hb74ynkjcn/1 License:
http://creativecommons.org/licenses/by/4.0

*   **Homepage**:
    [https://data.mendeley.com/datasets/hb74ynkjcn/1](https://data.mendeley.com/datasets/hb74ynkjcn/1)
*   **Source code**:
    [`tfds.image.plant_leaves.PlantLeaves`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/plant_leaves.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Download size**: `6.81 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,502

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=22),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@misc{,
  author={Siddharth Singh Chouhan, Ajay Kaul, Uday Pratap Singh, Sanjeev
Jain},
  title={A Database of Leaf Images: Practice towards Plant Conservation with
Plant Pathology},
  howpublished={Mendeley Data},
  year={2019}
}
```
