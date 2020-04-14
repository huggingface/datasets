<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="stanford_dogs" />
  <meta itemprop="description" content="The Stanford Dogs dataset contains images of 120 breeds of dogs from around&#10;the world. This dataset has been built using images and annotation from&#10;ImageNet for the task of fine-grained image categorization. There are&#10;20,580 images, out of which 12,000 are used for training and 8580 for&#10;testing. Class labels and bounding box annotations are provided&#10;for all the 12,000 images.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;stanford_dogs&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/stanford_dogs" />
  <meta itemprop="sameAs" content="http://vision.stanford.edu/aditya86/ImageNetDogs/main.html" />
  <meta itemprop="citation" content="@inproceedings{KhoslaYaoJayadevaprakashFeiFei_FGVC2011,&#10;author = &quot;Aditya Khosla and Nityananda Jayadevaprakash and Bangpeng Yao and&#10;          Li Fei-Fei&quot;,&#10;title = &quot;Novel Dataset for Fine-Grained Image Categorization&quot;,&#10;booktitle = &quot;First Workshop on Fine-Grained Visual Categorization,&#10;             IEEE Conference on Computer Vision and Pattern Recognition&quot;,&#10;year = &quot;2011&quot;,&#10;month = &quot;June&quot;,&#10;address = &quot;Colorado Springs, CO&quot;,&#10;}&#10;@inproceedings{imagenet_cvpr09,&#10;        AUTHOR = {Deng, J. and Dong, W. and Socher, R. and Li, L.-J. and&#10;                  Li, K. and Fei-Fei, L.},&#10;        TITLE = {{ImageNet: A Large-Scale Hierarchical Image Database}},&#10;        BOOKTITLE = {CVPR09},&#10;        YEAR = {2009},&#10;        BIBSOURCE = &quot;http://www.image-net.org/papers/imagenet_cvpr09.bib&quot;}&#10;" />
</div>
# `stanford_dogs`

*   **Description**:

The Stanford Dogs dataset contains images of 120 breeds of dogs from around the
world. This dataset has been built using images and annotation from ImageNet for
the task of fine-grained image categorization. There are 20,580 images, out of
which 12,000 are used for training and 8580 for testing. Class labels and
bounding box annotations are provided for all the 12,000 images.

*   **Homepage**:
    [http://vision.stanford.edu/aditya86/ImageNetDogs/main.html](http://vision.stanford.edu/aditya86/ImageNetDogs/main.html)
*   **Source code**:
    [`tfds.image.stanford_dogs.StanfordDogs`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/stanford_dogs.py)
*   **Versions**:
    *   **`0.2.0`** (default): No release notes.
*   **Download size**: `778.12 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 8,580
'train' | 12,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=120),
    'objects': Sequence({
        'bbox': BBoxFeature(shape=(4,), dtype=tf.float32),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@inproceedings{KhoslaYaoJayadevaprakashFeiFei_FGVC2011,
author = "Aditya Khosla and Nityananda Jayadevaprakash and Bangpeng Yao and
          Li Fei-Fei",
title = "Novel Dataset for Fine-Grained Image Categorization",
booktitle = "First Workshop on Fine-Grained Visual Categorization,
             IEEE Conference on Computer Vision and Pattern Recognition",
year = "2011",
month = "June",
address = "Colorado Springs, CO",
}
@inproceedings{imagenet_cvpr09,
        AUTHOR = {Deng, J. and Dong, W. and Socher, R. and Li, L.-J. and
                  Li, K. and Fei-Fei, L.},
        TITLE = {{ImageNet: A Large-Scale Hierarchical Image Database}},
        BOOKTITLE = {CVPR09},
        YEAR = {2009},
        BIBSOURCE = "http://www.image-net.org/papers/imagenet_cvpr09.bib"}
```
