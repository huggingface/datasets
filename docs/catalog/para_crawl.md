<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="para_crawl" />
  <meta itemprop="description" content="Web-Scale Parallel Corpora for Official European Languages.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;para_crawl&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/para_crawl" />
  <meta itemprop="sameAs" content="https://paracrawl.eu/releases.html" />
  <meta itemprop="citation" content="@misc {paracrawl,&#10;    title  = &quot;ParaCrawl&quot;,&#10;    year   = &quot;2018&quot;,&#10;    url    = &quot;http://paracrawl.eu/download.html.&quot;&#10;}&#10;" />
</div>
# `para_crawl`

*   **Description**:

Web-Scale Parallel Corpora for Official European Languages.

*   **Homepage**:
    [https://paracrawl.eu/releases.html](https://paracrawl.eu/releases.html)
*   **Source code**:
    [`tfds.translate.para_crawl.ParaCrawl`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/translate/para_crawl.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Citation**:

```
@misc {paracrawl,
    title  = "ParaCrawl",
    year   = "2018",
    url    = "http://paracrawl.eu/download.html."
}
```

## para_crawl/enbg_plain_text (default config)

*   **Config description**: Translation dataset from English to bg, uses encoder
    plain_text.
*   **Download size**: `98.94 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,039,885

*   **Features**:

```python
Translation({
    'bg': Text(shape=(), dtype=tf.string),
    'en': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'bg')`

## para_crawl/encs_plain_text

*   **Config description**: Translation dataset from English to cs, uses encoder
    plain_text.
*   **Download size**: `187.31 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,981,949

*   **Features**:

```python
Translation({
    'cs': Text(shape=(), dtype=tf.string),
    'en': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'cs')`

## para_crawl/enda_plain_text

*   **Config description**: Translation dataset from English to da, uses encoder
    plain_text.
*   **Download size**: `174.34 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,414,895

*   **Features**:

```python
Translation({
    'da': Text(shape=(), dtype=tf.string),
    'en': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'da')`

## para_crawl/ende_plain_text

*   **Config description**: Translation dataset from English to de, uses encoder
    plain_text.
*   **Download size**: `1.22 GiB`
*   **Splits**:

Split   | Examples
:------ | ---------:
'train' | 16,264,448

*   **Features**:

```python
Translation({
    'de': Text(shape=(), dtype=tf.string),
    'en': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'de')`

## para_crawl/enel_plain_text

*   **Config description**: Translation dataset from English to el, uses encoder
    plain_text.
*   **Download size**: `184.59 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,985,233

*   **Features**:

```python
Translation({
    'el': Text(shape=(), dtype=tf.string),
    'en': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'el')`

## para_crawl/enes_plain_text

*   **Config description**: Translation dataset from English to es, uses encoder
    plain_text.
*   **Download size**: `1.82 GiB`
*   **Splits**:

Split   | Examples
:------ | ---------:
'train' | 21,987,267

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'es': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'es')`

## para_crawl/enet_plain_text

*   **Config description**: Translation dataset from English to et, uses encoder
    plain_text.
*   **Download size**: `66.91 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 853,422

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'et': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'et')`

## para_crawl/enfi_plain_text

*   **Config description**: Translation dataset from English to fi, uses encoder
    plain_text.
*   **Download size**: `151.83 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,156,069

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'fi': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'fi')`

## para_crawl/enfr_plain_text

*   **Config description**: Translation dataset from English to fr, uses encoder
    plain_text.
*   **Download size**: `2.63 GiB`
*   **Splits**:

Split   | Examples
:------ | ---------:
'train' | 31,374,161

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'fr': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'fr')`

## para_crawl/enga_plain_text

*   **Config description**: Translation dataset from English to ga, uses encoder
    plain_text.
*   **Download size**: `28.03 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 357,399

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'ga': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'ga')`

## para_crawl/enhr_plain_text

*   **Config description**: Translation dataset from English to hr, uses encoder
    plain_text.
*   **Download size**: `80.97 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,002,053

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'hr': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'hr')`

## para_crawl/enhu_plain_text

*   **Config description**: Translation dataset from English to hu, uses encoder
    plain_text.
*   **Download size**: `114.24 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,901,342

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'hu': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'hu')`

## para_crawl/enit_plain_text

*   **Config description**: Translation dataset from English to it, uses encoder
    plain_text.
*   **Download size**: `1017.30 MiB`
*   **Splits**:

Split   | Examples
:------ | ---------:
'train' | 12,162,239

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'it': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'it')`

## para_crawl/enlt_plain_text

*   **Config description**: Translation dataset from English to lt, uses encoder
    plain_text.
*   **Download size**: `63.28 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 844,643

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'lt': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'lt')`

## para_crawl/enlv_plain_text

*   **Config description**: Translation dataset from English to lv, uses encoder
    plain_text.
*   **Download size**: `45.17 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 553,060

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'lv': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'lv')`

## para_crawl/enmt_plain_text

*   **Config description**: Translation dataset from English to mt, uses encoder
    plain_text.
*   **Download size**: `18.15 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 195,502

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'mt': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'mt')`

## para_crawl/ennl_plain_text

*   **Config description**: Translation dataset from English to nl, uses encoder
    plain_text.
*   **Download size**: `400.63 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,659,268

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'nl': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'nl')`

## para_crawl/enpl_plain_text

*   **Config description**: Translation dataset from English to pl, uses encoder
    plain_text.
*   **Download size**: `257.90 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 3,503,276

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'pl': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'pl')`

## para_crawl/enpt_plain_text

*   **Config description**: Translation dataset from English to pt, uses encoder
    plain_text.
*   **Download size**: `608.62 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 8,141,940

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'pt': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'pt')`

## para_crawl/enro_plain_text

*   **Config description**: Translation dataset from English to ro, uses encoder
    plain_text.
*   **Download size**: `153.24 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,952,043

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'ro': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'ro')`

## para_crawl/ensk_plain_text

*   **Config description**: Translation dataset from English to sk, uses encoder
    plain_text.
*   **Download size**: `96.61 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,591,831

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'sk': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'sk')`

## para_crawl/ensl_plain_text

*   **Config description**: Translation dataset from English to sl, uses encoder
    plain_text.
*   **Download size**: `62.02 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 660,161

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'sl': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'sl')`

## para_crawl/ensv_plain_text

*   **Config description**: Translation dataset from English to sv, uses encoder
    plain_text.
*   **Download size**: `262.76 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 3,476,729

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'sv': Text(shape=(), dtype=tf.string),
})
```

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('en', 'sv')`
