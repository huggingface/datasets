<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="the300w_lp" />
  <meta itemprop="description" content="300W-LP Dataset is expanded from 300W, which standardises multiple alignment databases with 68 landmarks, including AFW, LFPW, HELEN, IBUG and XM2VTS. With 300W, 300W-LP adopt the proposed face profiling to generate 61,225 samples across large poses (1,786 from IBUG, 5,207 from AFW, 16,556 from LFPW and 37,676 from HELEN, XM2VTS is not used).&#10;&#10;The dataset can be employed as the training set for the following computer vision tasks: face attribute recognition and landmark (or facial part) locaization.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;the300w_lp&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/the300w_lp" />
  <meta itemprop="sameAs" content="http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/ZhuLLSL15,&#10;  author    = {Xiangyu Zhu and&#10;               Zhen Lei and&#10;               Xiaoming Liu and&#10;               Hailin Shi and&#10;               Stan Z. Li},&#10;  title     = {Face Alignment Across Large Poses: {A} 3D Solution},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1511.07212},&#10;  year      = {2015},&#10;  url       = {http://arxiv.org/abs/1511.07212},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1511.07212},&#10;  timestamp = {Mon, 13 Aug 2018 16:48:23 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/ZhuLLSL15},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `the300w_lp`

*   **Description**:

300W-LP Dataset is expanded from 300W, which standardises multiple alignment
databases with 68 landmarks, including AFW, LFPW, HELEN, IBUG and XM2VTS. With
300W, 300W-LP adopt the proposed face profiling to generate 61,225 samples
across large poses (1,786 from IBUG, 5,207 from AFW, 16,556 from LFPW and 37,676
from HELEN, XM2VTS is not used).

The dataset can be employed as the training set for the following computer
vision tasks: face attribute recognition and landmark (or facial part)
locaization.

*   **Homepage**:
    [http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm](http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm)
*   **Source code**:
    [`tfds.image.the300w_lp.The300wLp`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/the300w_lp.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `2.63 GiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 61,225

*   **Features**:

```python
FeaturesDict({
    'color_params': Tensor(shape=(7,), dtype=tf.float32),
    'exp_params': Tensor(shape=(29,), dtype=tf.float32),
    'illum_params': Tensor(shape=(10,), dtype=tf.float32),
    'image': Image(shape=(450, 450, 3), dtype=tf.uint8),
    'landmarks_2d': Tensor(shape=(68, 2), dtype=tf.float32),
    'landmarks_3d': Tensor(shape=(68, 2), dtype=tf.float32),
    'landmarks_origin': Tensor(shape=(68, 2), dtype=tf.float32),
    'pose_params': Tensor(shape=(7,), dtype=tf.float32),
    'roi': Tensor(shape=(4,), dtype=tf.float32),
    'shape_params': Tensor(shape=(199,), dtype=tf.float32),
    'tex_params': Tensor(shape=(199,), dtype=tf.float32),
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
