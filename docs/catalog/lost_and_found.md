<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="lost_and_found" />
  <meta itemprop="description" content="&#10;The LostAndFound Dataset addresses the problem of detecting unexpected small obstacles on&#10;the road often caused by lost cargo. The dataset comprises 112 stereo video sequences&#10;with 2104 annotated frames (picking roughly every tenth frame from the recorded data).&#10;&#10;The dataset is designed analogous to the &#x27;Cityscapes&#x27; dataset. The datset provides:&#10;- stereo image pairs in either 8 or 16 bit color resolution&#10;- precomputed disparity maps&#10;- coarse semantic labels for objects and street&#10;&#10;Descriptions of the labels are given here: http://www.6d-vision.com/laf_table.pdf&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;lost_and_found&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/lost_and_found" />
  <meta itemprop="sameAs" content="http://www.6d-vision.com/lostandfounddataset" />
  <meta itemprop="citation" content="&#10;@inproceedings{pinggera2016lost,&#10;  title={Lost and found: detecting small road hazards for self-driving vehicles},&#10;  author={Pinggera, Peter and Ramos, Sebastian and Gehrig, Stefan and Franke, Uwe and Rother, Carsten and Mester, Rudolf},&#10;  booktitle={2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},&#10;  year={2016}&#10;}&#10;" />
</div>
# `lost_and_found`

*   **Description**:

The LostAndFound Dataset addresses the problem of detecting unexpected small
obstacles on the road often caused by lost cargo. The dataset comprises 112
stereo video sequences with 2104 annotated frames (picking roughly every tenth
frame from the recorded data).

The dataset is designed analogous to the 'Cityscapes' dataset. The datset
provides: - stereo image pairs in either 8 or 16 bit color resolution -
precomputed disparity maps - coarse semantic labels for objects and street

Descriptions of the labels are given here:
http://www.6d-vision.com/laf_table.pdf

*   **Homepage**:
    [http://www.6d-vision.com/lostandfounddataset](http://www.6d-vision.com/lostandfounddataset)
*   **Source code**:
    [`tfds.image.lost_and_found.LostAndFound`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/lost_and_found.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,203
'train' | 1,036

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@inproceedings{pinggera2016lost,
  title={Lost and found: detecting small road hazards for self-driving vehicles},
  author={Pinggera, Peter and Ramos, Sebastian and Gehrig, Stefan and Franke, Uwe and Rother, Carsten and Mester, Rudolf},
  booktitle={2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year={2016}
}
```

## lost_and_found/semantic_segmentation (default config)

*   **Config description**: Lost and Found semantic segmentation dataset.
*   **Download size**: `5.44 GiB`
*   **Features**:

```python
FeaturesDict({
    'image_id': Text(shape=(), dtype=tf.string),
    'image_left': Image(shape=(1024, 2048, 3), dtype=tf.uint8),
    'segmentation_label': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
})
```

## lost_and_found/stereo_disparity

*   **Config description**: Lost and Found stereo images and disparity maps.
*   **Download size**: `12.16 GiB`
*   **Features**:

```python
FeaturesDict({
    'disparity_map': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
    'image_id': Text(shape=(), dtype=tf.string),
    'image_left': Image(shape=(1024, 2048, 3), dtype=tf.uint8),
    'image_right': Image(shape=(1024, 2048, 3), dtype=tf.uint8),
})
```

## lost_and_found/full

*   **Config description**: Full Lost and Found dataset.
*   **Download size**: `12.19 GiB`
*   **Features**:

```python
FeaturesDict({
    'disparity_map': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
    'image_id': Text(shape=(), dtype=tf.string),
    'image_left': Image(shape=(1024, 2048, 3), dtype=tf.uint8),
    'image_right': Image(shape=(1024, 2048, 3), dtype=tf.uint8),
    'instance_id': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
    'segmentation_label': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
})
```

## lost_and_found/full_16bit

*   **Config description**: Full Lost and Found dataset.
*   **Download size**: `34.90 GiB`
*   **Features**:

```python
FeaturesDict({
    'disparity_map': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
    'image_id': Text(shape=(), dtype=tf.string),
    'image_left': Image(shape=(1024, 2048, 3), dtype=tf.uint8),
    'image_right': Image(shape=(1024, 2048, 3), dtype=tf.uint8),
    'instance_id': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
    'segmentation_label': Image(shape=(1024, 2048, 1), dtype=tf.uint8),
})
```
