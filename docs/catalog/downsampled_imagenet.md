<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="downsampled_imagenet" />
  <meta itemprop="description" content="Dataset with images of 2 resolutions (see config name for information on the resolution).&#10;It is used for density estimation and generative modeling experiments.&#10;&#10;For resized ImageNet for supervised learning ([link](https://patrykchrabaszcz.github.io/Imagenet32/)) see `imagenet_resized`.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;downsampled_imagenet&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/downsampled_imagenet" />
  <meta itemprop="sameAs" content="http://image-net.org/small/download.php" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/OordKK16,&#10;  author    = {A{&quot;{a}}ron van den Oord and&#10;               Nal Kalchbrenner and&#10;               Koray Kavukcuoglu},&#10;  title     = {Pixel Recurrent Neural Networks},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1601.06759},&#10;  year      = {2016},&#10;  url       = {http://arxiv.org/abs/1601.06759},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1601.06759},&#10;  timestamp = {Mon, 13 Aug 2018 16:46:29 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/OordKK16},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `downsampled_imagenet`

*   **Description**:

Dataset with images of 2 resolutions (see config name for information on the
resolution). It is used for density estimation and generative modeling
experiments.

For resized ImageNet for supervised learning
([link](https://patrykchrabaszcz.github.io/Imagenet32/)) see `imagenet_resized`.

*   **Homepage**:
    [http://image-net.org/small/download.php](http://image-net.org/small/download.php)
*   **Source code**:
    [`tfds.image.downsampled_imagenet.DownsampledImagenet`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/downsampled_imagenet.py)
*   **Versions**:
    *   **`2.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | --------:
'train'      | 1,281,149
'validation' | 49,999

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{DBLP:journals/corr/OordKK16,
  author    = {A{"{a}}ron van den Oord and
               Nal Kalchbrenner and
               Koray Kavukcuoglu},
  title     = {Pixel Recurrent Neural Networks},
  journal   = {CoRR},
  volume    = {abs/1601.06759},
  year      = {2016},
  url       = {http://arxiv.org/abs/1601.06759},
  archivePrefix = {arXiv},
  eprint    = {1601.06759},
  timestamp = {Mon, 13 Aug 2018 16:46:29 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/OordKK16},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## downsampled_imagenet/32x32 (default config)

*   **Config description**: A dataset consisting of Train and Validation images
    of 32x32 resolution.
*   **Download size**: `3.98 GiB`

## downsampled_imagenet/64x64

*   **Config description**: A dataset consisting of Train and Validation images
    of 64x64 resolution.
*   **Download size**: `11.73 GiB`
