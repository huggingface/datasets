<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="cycle_gan" />
  <meta itemprop="description" content="A dataset consisting of images from two classes A and B (For example: horses/zebras, apple/orange,...)&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;cycle_gan&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/cycle_gan" />
  <meta itemprop="sameAs" content="https://people.eecs.berkeley.edu/~taesung_park/CycleGAN/datasets/" />
  <meta itemprop="citation" content="@article{DBLP:journals/corr/ZhuPIE17,&#10;  author    = {Jun{-}Yan Zhu and&#10;               Taesung Park and&#10;               Phillip Isola and&#10;               Alexei A. Efros},&#10;  title     = {Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial&#10;               Networks},&#10;  journal   = {CoRR},&#10;  volume    = {abs/1703.10593},&#10;  year      = {2017},&#10;  url       = {http://arxiv.org/abs/1703.10593},&#10;  archivePrefix = {arXiv},&#10;  eprint    = {1703.10593},&#10;  timestamp = {Mon, 13 Aug 2018 16:48:06 +0200},&#10;  biburl    = {https://dblp.org/rec/bib/journals/corr/ZhuPIE17},&#10;  bibsource = {dblp computer science bibliography, https://dblp.org}&#10;}&#10;" />
</div>
# `cycle_gan`

*   **Description**:

A dataset consisting of images from two classes A and B (For example:
horses/zebras, apple/orange,...)

*   **Config description**: A dataset consisting of images from two classes A
    and B (For example: horses/zebras, apple/orange,...)
*   **Homepage**:
    [https://people.eecs.berkeley.edu/~taesung_park/CycleGAN/datasets/](https://people.eecs.berkeley.edu/~taesung_park/CycleGAN/datasets/)
*   **Source code**:
    [`tfds.image.cycle_gan.CycleGAN`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/cycle_gan.py)
*   **Versions**:
    *   **`2.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{DBLP:journals/corr/ZhuPIE17,
  author    = {Jun{-}Yan Zhu and
               Taesung Park and
               Phillip Isola and
               Alexei A. Efros},
  title     = {Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial
               Networks},
  journal   = {CoRR},
  volume    = {abs/1703.10593},
  year      = {2017},
  url       = {http://arxiv.org/abs/1703.10593},
  archivePrefix = {arXiv},
  eprint    = {1703.10593},
  timestamp = {Mon, 13 Aug 2018 16:48:06 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/ZhuPIE17},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## cycle_gan/apple2orange (default config)

*   **Download size**: `74.82 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 266
'testB'  | 248
'trainA' | 995
'trainB' | 1,019

## cycle_gan/summer2winter_yosemite

*   **Download size**: `126.50 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 309
'testB'  | 238
'trainA' | 1,231
'trainB' | 962

## cycle_gan/horse2zebra

*   **Download size**: `111.45 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 120
'testB'  | 140
'trainA' | 1,067
'trainB' | 1,334

## cycle_gan/monet2photo

*   **Download size**: `291.09 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 121
'testB'  | 751
'trainA' | 1,072
'trainB' | 6,287

## cycle_gan/cezanne2photo

*   **Download size**: `266.92 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 58
'testB'  | 751
'trainA' | 525
'trainB' | 6,287

## cycle_gan/ukiyoe2photo

*   **Download size**: `279.38 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 263
'testB'  | 751
'trainA' | 562
'trainB' | 6,287

## cycle_gan/vangogh2photo

*   **Download size**: `292.39 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 400
'testB'  | 751
'trainA' | 400
'trainB' | 6,287

## cycle_gan/maps

*   **Download size**: `1.38 GiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 1,098
'testB'  | 1,098
'trainA' | 1,096
'trainB' | 1,096

## cycle_gan/cityscapes

*   **Download size**: `266.65 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 500
'testB'  | 500
'trainA' | 2,975
'trainB' | 2,975

## cycle_gan/facades

*   **Download size**: `33.51 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 106
'testB'  | 106
'trainA' | 400
'trainB' | 400

## cycle_gan/iphone2dslr_flower

*   **Download size**: `324.22 MiB`
*   **Splits**:

Split    | Examples
:------- | -------:
'testA'  | 569
'testB'  | 480
'trainA' | 1,812
'trainB' | 3,325
