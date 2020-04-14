<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="food101" />
  <meta itemprop="description" content="This dataset consists of 101 food categories, with 101&#x27;000 images. For each class, 250 manually reviewed test images are provided as well as 750 training images. On purpose, the training images were not cleaned, and thus still contain some amount of noise. This comes mostly in the form of intense colors and sometimes wrong labels. All images were rescaled to have a maximum side length of 512 pixels.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;food101&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/food101" />
  <meta itemprop="sameAs" content="https://www.vision.ee.ethz.ch/datasets_extra/food-101/" />
  <meta itemprop="citation" content="@inproceedings{bossard14,&#10;  title = {Food-101 -- Mining Discriminative Components with Random Forests},&#10;  author = {Bossard, Lukas and Guillaumin, Matthieu and Van Gool, Luc},&#10;  booktitle = {European Conference on Computer Vision},&#10;  year = {2014}&#10;}&#10;" />
</div>
# `food101`

*   **Description**:

This dataset consists of 101 food categories, with 101'000 images. For each
class, 250 manually reviewed test images are provided as well as 750 training
images. On purpose, the training images were not cleaned, and thus still contain
some amount of noise. This comes mostly in the form of intense colors and
sometimes wrong labels. All images were rescaled to have a maximum side length
of 512 pixels.

*   **Homepage**:
    [https://www.vision.ee.ethz.ch/datasets_extra/food-101/](https://www.vision.ee.ethz.ch/datasets_extra/food-101/)
*   **Source code**:
    [`tfds.image.food101.Food101`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/food101.py)
*   **Versions**:
    *   **`2.0.0`** (default): No release notes.
    *   `1.0.0`: No release notes.
*   **Download size**: `4.65 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 75,750
'validation' | 25,250

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=101),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@inproceedings{bossard14,
  title = {Food-101 -- Mining Discriminative Components with Random Forests},
  author = {Bossard, Lukas and Guillaumin, Matthieu and Van Gool, Luc},
  booktitle = {European Conference on Computer Vision},
  year = {2014}
}
```
