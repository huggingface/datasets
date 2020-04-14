<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="aflw2k3d" />
  <meta itemprop="description" content="AFLW2000-3D is a dataset of 2000 images that have been annotated with image-level&#10;68-point 3D facial landmarks.&#10;This dataset is typically used for evaluation of 3D facial landmark detection&#10;models. The head poses are very diverse and often hard to be detected by a &#10;cnn-based face detector.&#10;The 2D landmarks are skipped in this dataset, since some of the data are not&#10;consistent to 21 points, as the original paper mentioned.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;aflw2k3d&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/aflw2k3d" />
  <meta itemprop="sameAs" content="http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/ZhuLLSL15,&#10;  author    = {Xiangyu Zhu and&#10;               Zhen Lei and&#10;               Xiaoming Liu and&#10;               Hailin Shi and&#10;               Stan Z. Li},&#10;  title     = {Face Alignment Across Large Poses: {A} 3D Solution},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1511.07212},&#10;  year      = {2015},&#10;  url       = {http://arxiv.org/abs/1511.07212},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1511.07212},&#10;  timestamp = {Mon, 13 Aug 2018 16:48:23 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/ZhuLLSL15},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `aflw2k3d`

*   **Description**:

AFLW2000-3D is a dataset of 2000 images that have been annotated with
image-level 68-point 3D facial landmarks. This dataset is typically used for
evaluation of 3D facial landmark detection models. The head poses are very
diverse and often hard to be detected by a cnn-based face detector. The 2D
landmarks are skipped in this dataset, since some of the data are not consistent
to 21 points, as the original paper mentioned.

*   **Homepage**:
    [http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm](http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm)
*   **Source code**:
    [`tfds.image.aflw2k3d.Aflw2k3d`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/aflw2k3d.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `83.36 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(450, 450, 3), dtype=tf.uint8),
    'landmarks_68_3d_xy_normalized': Tensor(shape=(68, 2), dtype=tf.float32),
    'landmarks_68_3d_z': Tensor(shape=(68, 1), dtype=tf.float32),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{DBLP:journals/corr/ZhuLLSL15,
  author    = {Xiangyu Zhu and
               Zhen Lei and
               Xiaoming Liu and
               Hailin Shi and
               Stan Z. Li},
  title     = {Face Alignment Across Large Poses: {A} 3D Solution},
  journal   = {CoRR},
  volume    = {abs/1511.07212},
  year      = {2015},
  url       = {http://arxiv.org/abs/1511.07212},
  archivePrefix = {arXiv},
  eprint    = {1511.07212},
  timestamp = {Mon, 13 Aug 2018 16:48:23 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/ZhuLLSL15},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
