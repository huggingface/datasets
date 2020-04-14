<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="starcraft_video" />
  <meta itemprop="description" content="This data set contains videos generated from Starcraft.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;starcraft_video&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/starcraft_video" />
  <meta itemprop="sameAs" content="https://storage.googleapis.com/scv_dataset/README.html" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/abs-1812-01717,&#10;  author    = {Thomas Unterthiner and&#10;               Sjoerd van Steenkiste and&#10;               Karol Kurach and&#10;               Rapha{&quot;{e}}l Marinier and&#10;               Marcin Michalski and&#10;               Sylvain Gelly},&#10;  title     = {Towards Accurate Generative Models of Video: {A} New Metric and&#10;               Challenges},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1812.01717},&#10;  year      = {2018},&#10;  url       = {http://arxiv.org/abs/1812.01717},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1812.01717},&#10;  timestamp = {Tue, 01 Jan 2019 15:01:25 +0100},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1812-01717},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `starcraft_video`

*   **Description**:

This data set contains videos generated from Starcraft.

*   **Homepage**:
    [https://storage.googleapis.com/scv_dataset/README.html](https://storage.googleapis.com/scv_dataset/README.html)
*   **Source code**:
    [`tfds.video.starcraft.StarcraftVideo`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/video/starcraft.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 2,000
'train'      | 10,000
'validation' | 2,000

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{DBLP:journals/corr/abs-1812-01717,
  author    = {Thomas Unterthiner and
               Sjoerd van Steenkiste and
               Karol Kurach and
               Rapha{"{e}}l Marinier and
               Marcin Michalski and
               Sylvain Gelly},
  title     = {Towards Accurate Generative Models of Video: {A} New Metric and
               Challenges},
  journal   = {CoRR},
  volume    = {abs/1812.01717},
  year      = {2018},
  url       = {http://arxiv.org/abs/1812.01717},
  archivePrefix = {arXiv},
  eprint    = {1812.01717},
  timestamp = {Tue, 01 Jan 2019 15:01:25 +0100},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1812-01717},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## starcraft_video/brawl_64 (default config)

*   **Config description**: Brawl map with 64x64 resolution.
*   **Download size**: `6.40 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(64, 64, 3), dtype=tf.uint8)),
})
```

## starcraft_video/brawl_128

*   **Config description**: Brawl map with 128x128 resolution.
*   **Download size**: `20.76 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(128, 128, 3), dtype=tf.uint8)),
})
```

## starcraft_video/collect_mineral_shards_64

*   **Config description**: CollectMineralShards map with 64x64 resolution.
*   **Download size**: `7.83 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(64, 64, 3), dtype=tf.uint8)),
})
```

## starcraft_video/collect_mineral_shards_128

*   **Config description**: CollectMineralShards map with 128x128 resolution.
*   **Download size**: `24.83 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(128, 128, 3), dtype=tf.uint8)),
})
```

## starcraft_video/move_unit_to_border_64

*   **Config description**: MoveUnitToBorder map with 64x64 resolution.
*   **Download size**: `1.77 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(64, 64, 3), dtype=tf.uint8)),
})
```

## starcraft_video/move_unit_to_border_128

*   **Config description**: MoveUnitToBorder map with 128x128 resolution.
*   **Download size**: `5.75 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(128, 128, 3), dtype=tf.uint8)),
})
```

## starcraft_video/road_trip_with_medivac_64

*   **Config description**: RoadTripWithMedivac map with 64x64 resolution.
*   **Download size**: `2.48 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(64, 64, 3), dtype=tf.uint8)),
})
```

## starcraft_video/road_trip_with_medivac_128

*   **Config description**: RoadTripWithMedivac map with 128x128 resolution.
*   **Download size**: `7.80 GiB`
*   **Features**:

```python
FeaturesDict({
    'rgb_screen': Video(Image(shape=(128, 128, 3), dtype=tf.uint8)),
})
```
