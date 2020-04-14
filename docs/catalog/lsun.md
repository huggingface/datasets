<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="lsun" />
  <meta itemprop="description" content="Large scale images showing different objects from given categories like bedroom, tower etc.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;lsun&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/lsun" />
  <meta itemprop="sameAs" content="https://www.yf.io/p/lsun" />
  <meta itemprop="citation" content="@article{journals/corr/YuZSSX15,&#10;  added-at = {2018-08-13T00:00:00.000+0200},&#10;  author = {Yu, Fisher and Zhang, Yinda and Song, Shuran and Seff, Ari and Xiao, Jianxiong},&#10;  biburl = {https://www.bibsonomy.org/bibtex/2446d4ffb99a5d7d2ab6e5417a12e195f/dblp},&#10;  ee = {http://arxiv.org/abs/1506.03365},&#10;  interhash = {3e9306c4ce2ead125f3b2ab0e25adc85},&#10;  intrahash = {446d4ffb99a5d7d2ab6e5417a12e195f},&#10;  journal = {CoRR},&#10;  keywords = {dblp},&#10;  timestamp = {2018-08-14T15:08:59.000+0200},&#10;  title = {LSUN: Construction of a Large-scale Image Dataset using Deep Learning with Humans in the Loop.},&#10;  url = {http://dblp.uni-trier.de/db/journals/corr/corr1506.html#YuZSSX15},&#10;  volume = {abs/1506.03365},&#10;  year = 2015&#10;}&#10;" />
</div>
# `lsun`

*   **Description**:

Large scale images showing different objects from given categories like bedroom,
tower etc.

*   **Homepage**: [https://www.yf.io/p/lsun](https://www.yf.io/p/lsun)
*   **Source code**:
    [`tfds.image.lsun.Lsun`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/lsun.py)
*   **Versions**:
    *   **`3.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
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
@article{journals/corr/YuZSSX15,
  added-at = {2018-08-13T00:00:00.000+0200},
  author = {Yu, Fisher and Zhang, Yinda and Song, Shuran and Seff, Ari and Xiao, Jianxiong},
  biburl = {https://www.bibsonomy.org/bibtex/2446d4ffb99a5d7d2ab6e5417a12e195f/dblp},
  ee = {http://arxiv.org/abs/1506.03365},
  interhash = {3e9306c4ce2ead125f3b2ab0e25adc85},
  intrahash = {446d4ffb99a5d7d2ab6e5417a12e195f},
  journal = {CoRR},
  keywords = {dblp},
  timestamp = {2018-08-14T15:08:59.000+0200},
  title = {LSUN: Construction of a Large-scale Image Dataset using Deep Learning with Humans in the Loop.},
  url = {http://dblp.uni-trier.de/db/journals/corr/corr1506.html#YuZSSX15},
  volume = {abs/1506.03365},
  year = 2015
}
```

## lsun/classroom (default config)

*   **Config description**: Images of category classroom
*   **Download size**: `3.06 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 168,103
'validation' | 300

## lsun/bedroom

*   **Config description**: Images of category bedroom
*   **Download size**: `42.77 GiB`
*   **Splits**:

Split        | Examples
:----------- | --------:
'train'      | 3,033,042
'validation' | 300

## lsun/bridge

*   **Config description**: Images of category bridge
*   **Download size**: `15.35 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 818,687
'validation' | 300

## lsun/church_outdoor

*   **Config description**: Images of category church_outdoor
*   **Download size**: `2.29 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 126,227
'validation' | 300

## lsun/conference_room

*   **Config description**: Images of category conference_room
*   **Download size**: `3.78 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 229,069
'validation' | 300

## lsun/dining_room

*   **Config description**: Images of category dining_room
*   **Download size**: `10.80 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 657,571
'validation' | 300

## lsun/kitchen

*   **Config description**: Images of category kitchen
*   **Download size**: `33.34 GiB`
*   **Splits**:

Split        | Examples
:----------- | --------:
'train'      | 2,212,277
'validation' | 300

## lsun/living_room

*   **Config description**: Images of category living_room
*   **Download size**: `21.23 GiB`
*   **Splits**:

Split        | Examples
:----------- | --------:
'train'      | 1,315,802
'validation' | 300

## lsun/restaurant

*   **Config description**: Images of category restaurant
*   **Download size**: `12.57 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 626,331
'validation' | 300

## lsun/tower

*   **Config description**: Images of category tower
*   **Download size**: `11.19 GiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 708,264
'validation' | 300
