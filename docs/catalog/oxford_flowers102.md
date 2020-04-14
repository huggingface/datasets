<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="oxford_flowers102" />
  <meta itemprop="description" content="&#10;The Oxford Flowers 102 dataset is a consistent of 102 flower categories commonly occurring&#10;in the United Kingdom. Each class consists of between 40 and 258 images. The images have&#10;large scale, pose and light variations. In addition, there are categories that have large&#10;variations within the category and several very similar categories.&#10;&#10;The dataset is divided into a training set, a validation set and a test set.&#10;The training set and validation set each consist of 10 images per class (totalling 1020 images each).&#10;The test set consists of the remaining 6149 images (minimum 20 per class).&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;oxford_flowers102&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/oxford_flowers102" />
  <meta itemprop="sameAs" content="https://www.robots.ox.ac.uk/~vgg/data/flowers/102/" />
  <meta itemprop="citation" content="@InProceedings{Nilsback08,&#10;   author = &quot;Nilsback, M-E. and Zisserman, A.&quot;,&#10;   title = &quot;Automated Flower Classification over a Large Number of Classes&quot;,&#10;   booktitle = &quot;Proceedings of the Indian Conference on Computer Vision, Graphics and Image Processing&quot;,&#10;   year = &quot;2008&quot;,&#10;   month = &quot;Dec&quot;&#10;}&#10;" />
</div>
# `oxford_flowers102`

*   **Description**:

The Oxford Flowers 102 dataset is a consistent of 102 flower categories commonly
occurring in the United Kingdom. Each class consists of between 40 and 258
images. The images have large scale, pose and light variations. In addition,
there are categories that have large variations within the category and several
very similar categories.

The dataset is divided into a training set, a validation set and a test set. The
training set and validation set each consist of 10 images per class (totalling
1020 images each). The test set consists of the remaining 6149 images (minimum
20 per class).

*   **Homepage**:
    [https://www.robots.ox.ac.uk/~vgg/data/flowers/102/](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/)
*   **Source code**:
    [`tfds.image.oxford_flowers102.OxfordFlowers102`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/oxford_flowers102.py)
*   **Versions**:
    *   **`2.1.0`** (default): Added label names
*   **Download size**: `336.76 MiB`
*   **Dataset size**: `331.34 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 6,149
'train'      | 1,020
'validation' | 1,020

*   **Features**:

```python
FeaturesDict({
    'file_name': Text(shape=(), dtype=tf.string),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=102),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@InProceedings{Nilsback08,
   author = "Nilsback, M-E. and Zisserman, A.",
   title = "Automated Flower Classification over a Large Number of Classes",
   booktitle = "Proceedings of the Indian Conference on Computer Vision, Graphics and Image Processing",
   year = "2008",
   month = "Dec"
}
```
