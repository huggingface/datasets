<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="scene_parse150" />
  <meta itemprop="description" content="&#10;Scene parsing is to segment and parse an image into different image regions&#10;associated with semantic categories, such as sky, road, person, and bed.&#10;MIT Scene Parsing Benchmark (SceneParse150) provides a standard training and&#10;evaluation platform for the algorithms of scene parsing.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;scene_parse150&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/scene_parse150" />
  <meta itemprop="sameAs" content="http://sceneparsing.csail.mit.edu/" />
  <meta itemprop="citation" content="&#10;@inproceedings{zhou2017scene,&#10;title={Scene Parsing through ADE20K Dataset},&#10;author={Zhou, Bolei and Zhao, Hang and Puig, Xavier and Fidler, Sanja and Barriuso, Adela and Torralba, Antonio},&#10;booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},&#10;year={2017}&#10;}&#10;" />
</div>
# `scene_parse150`

*   **Description**:

Scene parsing is to segment and parse an image into different image regions
associated with semantic categories, such as sky, road, person, and bed. MIT
Scene Parsing Benchmark (SceneParse150) provides a standard training and
evaluation platform for the algorithms of scene parsing.

*   **Homepage**:
    [http://sceneparsing.csail.mit.edu/](http://sceneparsing.csail.mit.edu/)
*   **Source code**:
    [`tfds.image.scene_parse_150.SceneParse150`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/scene_parse_150.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `936.97 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 2,000
'train' | 20,210

*   **Features**:

```python
FeaturesDict({
    'annotation': Image(shape=(None, None, 3), dtype=tf.uint8),
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'annotation')`
*   **Citation**:

```
@inproceedings{zhou2017scene,
title={Scene Parsing through ADE20K Dataset},
author={Zhou, Bolei and Zhao, Hang and Puig, Xavier and Fidler, Sanja and Barriuso, Adela and Torralba, Antonio},
booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
year={2017}
}
```
