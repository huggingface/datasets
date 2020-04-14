<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="flic" />
  <meta itemprop="description" content="&#10;From the paper: We collected a 5003 image dataset automatically from popular&#10;Hollywood movies. The images were obtained by running a state-of-the-art person&#10;detector on every tenth frame of 30 movies. People detected with high confidence&#10;(roughly 20K candidates) were then sent to the crowdsourcing marketplace Amazon&#10;Mechanical Turk to obtain groundtruthlabeling. Each image was annotated by five&#10;Turkers for $0.01 each to label 10 upperbody joints. The median-of-five labeling&#10;was taken in each image to be robust to outlier annotation. Finally, images were&#10;rejected manually by us if the person was occluded or severely non-frontal. We&#10;set aside 20% (1016 images) of the data for testing.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;flic&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/flic" />
  <meta itemprop="sameAs" content="https://bensapp.github.io/flic-dataset.html" />
  <meta itemprop="citation" content="@inproceedings{modec13,&#10;    title={MODEC: Multimodal Decomposable Models for Human Pose Estimation},&#10;    author={Sapp, Benjamin and Taskar, Ben},&#10;    booktitle={In Proc. CVPR},&#10;    year={2013},&#10;  }&#10;" />
</div>
# `flic`

*   **Description**:

From the paper: We collected a 5003 image dataset automatically from popular
Hollywood movies. The images were obtained by running a state-of-the-art person
detector on every tenth frame of 30 movies. People detected with high confidence
(roughly 20K candidates) were then sent to the crowdsourcing marketplace Amazon
Mechanical Turk to obtain groundtruthlabeling. Each image was annotated by five
Turkers for $0.01 each to label 10 upperbody joints. The median-of-five labeling
was taken in each image to be robust to outlier annotation. Finally, images were
rejected manually by us if the person was occluded or severely non-frontal. We
set aside 20% (1016 images) of the data for testing.

*   **Homepage**:
    [https://bensapp.github.io/flic-dataset.html](https://bensapp.github.io/flic-dataset.html)
*   **Source code**:
    [`tfds.image.flic.Flic`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/flic.py)
*   **Versions**:
    *   **`2.0.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,016
'train' | 3,987

*   **Features**:

```python
FeaturesDict({
    'currframe': tf.float64,
    'image': Image(shape=(480, 720, 3), dtype=tf.uint8),
    'moviename': Text(shape=(), dtype=tf.string),
    'poselet_hit_idx': Sequence(tf.uint16),
    'torsobox': BBoxFeature(shape=(4,), dtype=tf.float32),
    'xcoords': Sequence(tf.float64),
    'ycoords': Sequence(tf.float64),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@inproceedings{modec13,
    title={MODEC: Multimodal Decomposable Models for Human Pose Estimation},
    author={Sapp, Benjamin and Taskar, Ben},
    booktitle={In Proc. CVPR},
    year={2013},
  }
```

## flic/small (default config)

*   **Config description**: Uses 5003 examples used in CVPR13 MODEC paper.
*   **Download size**: `286.35 MiB`

## flic/full

*   **Config description**: Uses 20928 examples, a superset of FLIC consisting
    of more difficult examples.
*   **Download size**: `1.10 GiB`
