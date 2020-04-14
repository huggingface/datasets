<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>

  <meta itemprop="name" content="wiki40b" />
  <meta itemprop="description" content="&#10;Clean-up text for 40+ Wikipedia languages editions of pages&#10;correspond to entities. The datasets have train/dev/test splits per language.&#10;The dataset is cleaned up by page filtering to remove disambiguation pages,&#10;redirect pages, deleted pages, and non-entity pages. Each example contains the&#10;wikidata id of the entity, and the full Wikipedia article after page processing&#10;that removes non-content sections and structured objects.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;wiki40b&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/wiki40b" />
  <meta itemprop="sameAs" content="https://www.tensorflow.org/datasets/catalog/wiki40b" />
  <meta itemprop="citation" content="&#10;" />
</div>

# `wiki40b`

*   **Description**:

Clean-up text for 40+ Wikipedia languages editions of pages correspond to
entities. The datasets have train/dev/test splits per language. The dataset is
cleaned up by page filtering to remove disambiguation pages, redirect pages,
deleted pages, and non-entity pages. Each example contains the wikidata id of
the entity, and the full Wikipedia article after page processing that removes
non-content sections and structured objects.

*   **Homepage**:
    [https://www.tensorflow.org/datasets/catalog/wiki40b](https://www.tensorflow.org/datasets/catalog/wiki40b)
*   **Source code**:
    [`tfds.text.wiki40b.Wiki40b`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/wiki40b.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Unknown
*   **Splits**:

Split | Examples
:---- | -------:

*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(), dtype=tf.string),
    'wikidata_id': Text(shape=(), dtype=tf.string),
})
```

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```

```

## wiki40b/Wiki40B.en (default config)

*   **Config description**: Wiki40B dataset for en.

## wiki40b/Wiki40B.ar

*   **Config description**: Wiki40B dataset for ar.

## wiki40b/Wiki40B.zh-cn

*   **Config description**: Wiki40B dataset for zh-cn.

## wiki40b/Wiki40B.zh-tw

*   **Config description**: Wiki40B dataset for zh-tw.

## wiki40b/Wiki40B.nl

*   **Config description**: Wiki40B dataset for nl.

## wiki40b/Wiki40B.fr

*   **Config description**: Wiki40B dataset for fr.

## wiki40b/Wiki40B.de

*   **Config description**: Wiki40B dataset for de.

## wiki40b/Wiki40B.it

*   **Config description**: Wiki40B dataset for it.

## wiki40b/Wiki40B.ja

*   **Config description**: Wiki40B dataset for ja.

## wiki40b/Wiki40B.ko

*   **Config description**: Wiki40B dataset for ko.

## wiki40b/Wiki40B.pl

*   **Config description**: Wiki40B dataset for pl.

## wiki40b/Wiki40B.pt

*   **Config description**: Wiki40B dataset for pt.

## wiki40b/Wiki40B.ru

*   **Config description**: Wiki40B dataset for ru.

## wiki40b/Wiki40B.es

*   **Config description**: Wiki40B dataset for es.

## wiki40b/Wiki40B.th

*   **Config description**: Wiki40B dataset for th.

## wiki40b/Wiki40B.tr

*   **Config description**: Wiki40B dataset for tr.

## wiki40b/Wiki40B.bg

*   **Config description**: Wiki40B dataset for bg.

## wiki40b/Wiki40B.ca

*   **Config description**: Wiki40B dataset for ca.

## wiki40b/Wiki40B.cs

*   **Config description**: Wiki40B dataset for cs.

## wiki40b/Wiki40B.da

*   **Config description**: Wiki40B dataset for da.

## wiki40b/Wiki40B.el

*   **Config description**: Wiki40B dataset for el.

## wiki40b/Wiki40B.et

*   **Config description**: Wiki40B dataset for et.

## wiki40b/Wiki40B.fa

*   **Config description**: Wiki40B dataset for fa.

## wiki40b/Wiki40B.fi

*   **Config description**: Wiki40B dataset for fi.

## wiki40b/Wiki40B.he

*   **Config description**: Wiki40B dataset for he.

## wiki40b/Wiki40B.hi

*   **Config description**: Wiki40B dataset for hi.

## wiki40b/Wiki40B.hr

*   **Config description**: Wiki40B dataset for hr.

## wiki40b/Wiki40B.hu

*   **Config description**: Wiki40B dataset for hu.

## wiki40b/Wiki40B.id

*   **Config description**: Wiki40B dataset for id.

## wiki40b/Wiki40B.lt

*   **Config description**: Wiki40B dataset for lt.

## wiki40b/Wiki40B.lv

*   **Config description**: Wiki40B dataset for lv.

## wiki40b/Wiki40B.ms

*   **Config description**: Wiki40B dataset for ms.

## wiki40b/Wiki40B.no

*   **Config description**: Wiki40B dataset for no.

## wiki40b/Wiki40B.ro

*   **Config description**: Wiki40B dataset for ro.

## wiki40b/Wiki40B.sk

*   **Config description**: Wiki40B dataset for sk.

## wiki40b/Wiki40B.sl

*   **Config description**: Wiki40B dataset for sl.

## wiki40b/Wiki40B.sr

*   **Config description**: Wiki40B dataset for sr.

## wiki40b/Wiki40B.sv

*   **Config description**: Wiki40B dataset for sv.

## wiki40b/Wiki40B.tl

*   **Config description**: Wiki40B dataset for tl.

## wiki40b/Wiki40B.uk

*   **Config description**: Wiki40B dataset for uk.

## wiki40b/Wiki40B.vi

*   **Config description**: Wiki40B dataset for vi.
