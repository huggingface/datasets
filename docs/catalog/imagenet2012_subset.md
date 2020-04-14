<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>

  <meta itemprop="name" content="imagenet2012_subset" />
  <meta itemprop="description" content="Imagenet2012Subset is a subset of original ImageNet ILSVRC 2012 dataset.&#10;The dataset share the *same* validation set as the original ImageNet ILSVRC 2012&#10;dataset. However, the training set is subsampled in a label balanced fashion.&#10;In `1pct` configuration, 1%, or 12811, images are sampled, most classes have&#10;the same number of images (average 12.8), some classes randomly have 1 more&#10;example than others; and in `10pct` configuration, ~10%, or 128116, most classes&#10;have the same number of images (average 128), and some classes randomly have 1&#10;more example than others.&#10;&#10;This is supposed to be used as a benchmark for semi-supervised learning, and&#10;has been originally used in SimCLR paper (https://arxiv.org/abs/2002.05709).&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;imagenet2012_subset&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/imagenet2012_subset" />
  <meta itemprop="sameAs" content="http://image-net.org/" />
  <meta itemprop="citation" content="@article{chen2020simple,&#10;  title={A Simple Framework for Contrastive Learning of Visual Representations},&#10;  author={Chen, Ting and Kornblith, Simon and Norouzi, Mohammad and Hinton, Geoffrey},&#10;  journal={arXiv preprint arXiv:2002.05709},&#10;  year={2020}&#10;}&#10;@article{ILSVRC15,&#10;  Author = {Olga Russakovsky and Jia Deng and Hao Su and Jonathan Krause and Sanjeev Satheesh and Sean Ma and Zhiheng Huang and Andrej Karpathy and Aditya Khosla and Michael Bernstein and Alexander C. Berg and Li Fei-Fei},&#10;  Title = {{ImageNet Large Scale Visual Recognition Challenge}},&#10;  Year = {2015},&#10;  journal   = {International Journal of Computer Vision (IJCV)},&#10;  doi = {10.1007/s11263-015-0816-y},&#10;  volume={115},&#10;  number={3},&#10;  pages={211-252}&#10;}&#10;" />
</div>

# `imagenet2012_subset`

Warning: Manual download required. See instructions below.

*   **Description**:

Imagenet2012Subset is a subset of original ImageNet ILSVRC 2012 dataset. The
dataset share the *same* validation set as the original ImageNet ILSVRC 2012
dataset. However, the training set is subsampled in a label balanced fashion. In
`1pct` configuration, 1%, or 12811, images are sampled, most classes have the
same number of images (average 12.8), some classes randomly have 1 more example
than others; and in `10pct` configuration, ~10%, or 128116, most classes have
the same number of images (average 128), and some classes randomly have 1 more
example than others.

This is supposed to be used as a benchmark for semi-supervised learning, and has
been originally used in SimCLR paper (https://arxiv.org/abs/2002.05709).

*   **Homepage**: [http://image-net.org/](http://image-net.org/)
*   **Source code**:
    [`tfds.image.imagenet2012_subset.Imagenet2012Subset`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/imagenet2012_subset.py)
*   **Versions**:
    *   **`5.0.0`** (default): No release notes.
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/imagenet2012_subset/`):<br/>
    manual_dir should contain two files: ILSVRC2012_img_train.tar and
    ILSVRC2012_img_val.tar.
    You need to register on http://www.image-net.org/download-images in order
    to get the link to download the dataset.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Unknown
*   **Splits**:

Split | Examples
:---- | -------:

*   **Features**:

```python
FeaturesDict({
    'file_name': Text(shape=(), dtype=tf.string),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=1000),
})
```

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{chen2020simple,
  title={A Simple Framework for Contrastive Learning of Visual Representations},
  author={Chen, Ting and Kornblith, Simon and Norouzi, Mohammad and Hinton, Geoffrey},
  journal={arXiv preprint arXiv:2002.05709},
  year={2020}
}
@article{ILSVRC15,
  Author = {Olga Russakovsky and Jia Deng and Hao Su and Jonathan Krause and Sanjeev Satheesh and Sean Ma and Zhiheng Huang and Andrej Karpathy and Aditya Khosla and Michael Bernstein and Alexander C. Berg and Li Fei-Fei},
  Title = {{ImageNet Large Scale Visual Recognition Challenge}},
  Year = {2015},
  journal   = {International Journal of Computer Vision (IJCV)},
  doi = {10.1007/s11263-015-0816-y},
  volume={115},
  number={3},
  pages={211-252}
}
```

## imagenet2012_subset/1pct (default config)

*   **Config description**: 1pct of total ImageNet training set.

## imagenet2012_subset/10pct

*   **Config description**: 10pct of total ImageNet training set.
