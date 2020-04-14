<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="celeb_a_hq" />
  <meta itemprop="description" content="High-quality version of the CELEBA&#10;dataset, consisting of 30000 images in 1024 x 1024 resolution.&#10;&#10;WARNING: This dataset currently requires you to prepare images on your own.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;celeb_a_hq&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/celeb_a_hq" />
  <meta itemprop="sameAs" content="https://github.com/tkarras/progressive_growing_of_gans" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/abs-1710-10196,&#10;  author    = {Tero Karras and&#10;               Timo Aila and&#10;               Samuli Laine and&#10;               Jaakko Lehtinen},&#10;  title     = {Progressive Growing of GANs for Improved Quality, Stability, and Variation},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1710.10196},&#10;  year      = {2017},&#10;  url       = {http://arxiv.org/abs/1710.10196},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1710.10196},&#10;  timestamp = {Mon, 13 Aug 2018 16:46:42 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1710-10196},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `celeb_a_hq`

Warning: Manual download required. See instructions below.

*   **Description**:

High-quality version of the CELEBA dataset, consisting of 30000 images in 1024 x
1024 resolution.

WARNING: This dataset currently requires you to prepare images on your own.

*   **Homepage**:
    [https://github.com/tkarras/progressive_growing_of_gans](https://github.com/tkarras/progressive_growing_of_gans)
*   **Source code**:
    [`tfds.image.celebahq.CelebAHq`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/celebahq.py)
*   **Versions**:
    *   **`2.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/celeb_a_hq/`):<br/>
    manual_dir should contain multiple tar files with images (data2x2.tar,
    data4x4.tar .. data1024x1024.tar).
    Detailed instructions are here:
    https://github.com/tkarras/progressive_growing_of_gans#preparing-datasets-for-training
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 30,000

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{DBLP:journals/corr/abs-1710-10196,
  author    = {Tero Karras and
               Timo Aila and
               Samuli Laine and
               Jaakko Lehtinen},
  title     = {Progressive Growing of GANs for Improved Quality, Stability, and Variation},
  journal   = {CoRR},
  volume    = {abs/1710.10196},
  year      = {2017},
  url       = {http://arxiv.org/abs/1710.10196},
  archivePrefix = {arXiv},
  eprint    = {1710.10196},
  timestamp = {Mon, 13 Aug 2018 16:46:42 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1710-10196},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## celeb_a_hq/1024 (default config)

*   **Config description**: CelebaHQ images in 1024 x 1024 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(1024, 1024, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/512

*   **Config description**: CelebaHQ images in 512 x 512 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(512, 512, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/256

*   **Config description**: CelebaHQ images in 256 x 256 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(256, 256, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/128

*   **Config description**: CelebaHQ images in 128 x 128 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(128, 128, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/64

*   **Config description**: CelebaHQ images in 64 x 64 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(64, 64, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/32

*   **Config description**: CelebaHQ images in 32 x 32 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(32, 32, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/16

*   **Config description**: CelebaHQ images in 16 x 16 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(16, 16, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/8

*   **Config description**: CelebaHQ images in 8 x 8 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(8, 8, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/4

*   **Config description**: CelebaHQ images in 4 x 4 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(4, 4, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/2

*   **Config description**: CelebaHQ images in 2 x 2 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(2, 2, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```

## celeb_a_hq/1

*   **Config description**: CelebaHQ images in 1 x 1 resolution
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(1, 1, 3), dtype=tf.uint8),
    'image/filename': Text(shape=(), dtype=tf.string),
})
```
