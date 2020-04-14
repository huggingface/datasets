<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="wmt19_translate" />
  <meta itemprop="description" content="Translate dataset based on the data from statmt.org.&#10;&#10;Versions exists for the different years using a combination of multiple data&#10;sources. The base `wmt_translate` allows you to create your own config to choose&#10;your own data/language pair by creating a custom `tfds.translate.wmt.WmtConfig`.&#10;&#10;```&#10;config = tfds.translate.wmt.WmtConfig(&#10;    version=&quot;0.0.1&quot;,&#10;    language_pair=(&quot;fr&quot;, &quot;de&quot;),&#10;    subsets={&#10;        tfds.Split.TRAIN: [&quot;commoncrawl_frde&quot;],&#10;        tfds.Split.VALIDATION: [&quot;euelections_dev2019&quot;],&#10;    },&#10;)&#10;builder = tfds.builder(&quot;wmt_translate&quot;, config=config)&#10;```&#10;&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;wmt19_translate&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/wmt19_translate" />
  <meta itemprop="sameAs" content="http://www.statmt.org/wmt19/translation-task.html" />
  <meta itemprop="citation" content="&#10;@ONLINE {wmt19translate,&#10;    author = &quot;Wikimedia Foundation&quot;,&#10;    title  = &quot;ACL 2019 Fourth Conference on Machine Translation (WMT19), Shared Task: Machine Translation of News&quot;,&#10;    url    = &quot;http://www.statmt.org/wmt19/translation-task.html&quot;&#10;}&#10;" />
</div>
# `wmt19_translate`

Warning: Manual download required. See instructions below.

*   **Description**:

Translate dataset based on the data from statmt.org.

Versions exists for the different years using a combination of multiple data
sources. The base `wmt_translate` allows you to create your own config to choose
your own data/language pair by creating a custom `tfds.translate.wmt.WmtConfig`.

```
config = tfds.translate.wmt.WmtConfig(
    version="0.0.1",
    language_pair=("fr", "de"),
    subsets={
        tfds.Split.TRAIN: ["commoncrawl_frde"],
        tfds.Split.VALIDATION: ["euelections_dev2019"],
    },
)
builder = tfds.builder("wmt_translate", config=config)
```

*   **Homepage**:
    [http://www.statmt.org/wmt19/translation-task.html](http://www.statmt.org/wmt19/translation-task.html)
*   **Source code**:
    [`tfds.translate.wmt19.Wmt19Translate`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/translate/wmt19.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/wmt19_translate/`):<br/>
    Some of the wmt configs here, require a manual download.
    Please look into wmt.py to see the exact path (and file name) that has to
    be downloaded.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Citation**:

```
@ONLINE {wmt19translate,
    author = "Wikimedia Foundation",
    title  = "ACL 2019 Fourth Conference on Machine Translation (WMT19), Shared Task: Machine Translation of News",
    url    = "http://www.statmt.org/wmt19/translation-task.html"
}
```

## wmt19_translate/cs-en (default config)

*   **Config description**: WMT 2019 cs-en translation task dataset.
*   **Download size**: `1.88 GiB`
*   **Splits**:

Split        | Examples
:----------- | ---------:
'train'      | 20,246,548
'validation' | 2,983

*   **Features**:

```python
Translation({
    'cs': Text(shape=(), dtype=tf.string),
    'en': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('cs', 'en')`

## wmt19_translate/de-en

*   **Config description**: WMT 2019 de-en translation task dataset.
*   **Download size**: `9.71 GiB`
*   **Splits**:

Split        | Examples
:----------- | ---------:
'train'      | 38,690,334
'validation' | 2,998

*   **Features**:

```python
Translation({
    'de': Text(shape=(), dtype=tf.string),
    'en': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('de', 'en')`

## wmt19_translate/fi-en

*   **Config description**: WMT 2019 fi-en translation task dataset.
*   **Download size**: `959.46 MiB`
*   **Splits**:

Split        | Examples
:----------- | --------:
'train'      | 6,587,448
'validation' | 3,000

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'fi': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('fi', 'en')`

## wmt19_translate/gu-en

*   **Config description**: WMT 2019 gu-en translation task dataset.
*   **Download size**: `37.03 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 11,670
'validation' | 1,998

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'gu': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('gu', 'en')`

## wmt19_translate/kk-en

*   **Config description**: WMT 2019 kk-en translation task dataset.
*   **Download size**: `39.58 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'train'      | 126,583
'validation' | 2,066

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'kk': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('kk', 'en')`

## wmt19_translate/lt-en

*   **Config description**: WMT 2019 lt-en translation task dataset.
*   **Download size**: `392.20 MiB`
*   **Splits**:

Split        | Examples
:----------- | --------:
'train'      | 2,344,893
'validation' | 2,000

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'lt': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('lt', 'en')`

## wmt19_translate/ru-en

*   **Config description**: WMT 2019 ru-en translation task dataset.
*   **Download size**: `3.86 GiB`
*   **Splits**:

Split        | Examples
:----------- | ---------:
'train'      | 38,492,126
'validation' | 3,000

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'ru': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('ru', 'en')`

## wmt19_translate/zh-en

*   **Config description**: WMT 2019 zh-en translation task dataset.
*   **Download size**: `2.04 GiB`
*   **Splits**:

Split        | Examples
:----------- | ---------:
'train'      | 25,986,436
'validation' | 3,981

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'zh': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('zh', 'en')`

## wmt19_translate/fr-de

*   **Config description**: WMT 2019 fr-de translation task dataset.
*   **Download size**: `722.20 MiB`
*   **Splits**:

Split        | Examples
:----------- | --------:
'train'      | 9,824,476
'validation' | 1,512

*   **Features**:

```python
Translation({
    'de': Text(shape=(), dtype=tf.string),
    'fr': Text(shape=(), dtype=tf.string),
})
```

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('fr', 'de')`
