<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="wikipedia" />
  <meta itemprop="description" content="Wikipedia dataset containing cleaned articles of all languages.&#10;The datasets are built from the Wikipedia dump&#10;(https://dumps.wikimedia.org/) with one split per language. Each example&#10;contains the content of one full Wikipedia article with cleaning to strip&#10;markdown and unwanted sections (references, etc.).&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;wikipedia&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/wikipedia" />
  <meta itemprop="sameAs" content="https://dumps.wikimedia.org" />
  <meta itemprop="citation" content="@ONLINE {wikidump,&#10;    author = &quot;Wikimedia Foundation&quot;,&#10;    title  = &quot;Wikimedia Downloads&quot;,&#10;    url    = &quot;https://dumps.wikimedia.org&quot;&#10;}&#10;" />
</div>
# `wikipedia`

*   **Description**:

Wikipedia dataset containing cleaned articles of all languages. The datasets are
built from the Wikipedia dump (https://dumps.wikimedia.org/) with one split per
language. Each example contains the content of one full Wikipedia article with
cleaning to strip markdown and unwanted sections (references, etc.).

*   **Homepage**: [https://dumps.wikimedia.org](https://dumps.wikimedia.org)
*   **Source code**:
    [`tfds.text.wikipedia.Wikipedia`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/wikipedia.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(), dtype=tf.string),
    'title': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@ONLINE {wikidump,
    author = "Wikimedia Foundation",
    title  = "Wikimedia Downloads",
    url    = "https://dumps.wikimedia.org"
}
```

## wikipedia/20190301.aa (default config)

*   **Config description**: Wikipedia dataset for aa, parsed from 20190301 dump.
*   **Download size**: `44.09 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1

## wikipedia/20190301.ab

*   **Config description**: Wikipedia dataset for ab, parsed from 20190301 dump.
*   **Download size**: `1.31 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,053

## wikipedia/20190301.ace

*   **Config description**: Wikipedia dataset for ace, parsed from 20190301
    dump.
*   **Download size**: `2.66 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 9,264

## wikipedia/20190301.ady

*   **Config description**: Wikipedia dataset for ady, parsed from 20190301
    dump.
*   **Download size**: `349.43 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 547

## wikipedia/20190301.af

*   **Config description**: Wikipedia dataset for af, parsed from 20190301 dump.
*   **Download size**: `84.13 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 92,366

## wikipedia/20190301.ak

*   **Config description**: Wikipedia dataset for ak, parsed from 20190301 dump.
*   **Download size**: `377.84 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 628

## wikipedia/20190301.als

*   **Config description**: Wikipedia dataset for als, parsed from 20190301
    dump.
*   **Download size**: `46.90 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 27,705

## wikipedia/20190301.am

*   **Config description**: Wikipedia dataset for am, parsed from 20190301 dump.
*   **Download size**: `6.54 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 13,231

## wikipedia/20190301.an

*   **Config description**: Wikipedia dataset for an, parsed from 20190301 dump.
*   **Download size**: `31.39 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 47,536

## wikipedia/20190301.ang

*   **Config description**: Wikipedia dataset for ang, parsed from 20190301
    dump.
*   **Download size**: `3.77 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,135

## wikipedia/20190301.ar

*   **Config description**: Wikipedia dataset for ar, parsed from 20190301 dump.
*   **Download size**: `805.82 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,272,226

## wikipedia/20190301.arc

*   **Config description**: Wikipedia dataset for arc, parsed from 20190301
    dump.
*   **Download size**: `952.49 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,272

## wikipedia/20190301.arz

*   **Config description**: Wikipedia dataset for arz, parsed from 20190301
    dump.
*   **Download size**: `20.32 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 28,136

## wikipedia/20190301.as

*   **Config description**: Wikipedia dataset for as, parsed from 20190301 dump.
*   **Download size**: `19.06 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,435

## wikipedia/20190301.ast

*   **Config description**: Wikipedia dataset for ast, parsed from 20190301
    dump.
*   **Download size**: `216.68 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 106,275

## wikipedia/20190301.atj

*   **Config description**: Wikipedia dataset for atj, parsed from 20190301
    dump.
*   **Download size**: `467.05 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,005

## wikipedia/20190301.av

*   **Config description**: Wikipedia dataset for av, parsed from 20190301 dump.
*   **Download size**: `3.61 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,918

## wikipedia/20190301.ay

*   **Config description**: Wikipedia dataset for ay, parsed from 20190301 dump.
*   **Download size**: `2.06 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,773

## wikipedia/20190301.az

*   **Config description**: Wikipedia dataset for az, parsed from 20190301 dump.
*   **Download size**: `163.04 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 161,901

## wikipedia/20190301.azb

*   **Config description**: Wikipedia dataset for azb, parsed from 20190301
    dump.
*   **Download size**: `50.59 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 159,459

## wikipedia/20190301.ba

*   **Config description**: Wikipedia dataset for ba, parsed from 20190301 dump.
*   **Download size**: `55.04 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 51,934

## wikipedia/20190301.bar

*   **Config description**: Wikipedia dataset for bar, parsed from 20190301
    dump.
*   **Download size**: `30.14 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 42,237

## wikipedia/20190301.bat-smg

*   **Config description**: Wikipedia dataset for bat-smg, parsed from 20190301
    dump.
*   **Download size**: `4.61 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 19,344

## wikipedia/20190301.bcl

*   **Config description**: Wikipedia dataset for bcl, parsed from 20190301
    dump.
*   **Download size**: `6.18 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 9,025

## wikipedia/20190301.be

*   **Config description**: Wikipedia dataset for be, parsed from 20190301 dump.
*   **Download size**: `192.23 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 164,589

## wikipedia/20190301.be-x-old

*   **Config description**: Wikipedia dataset for be-x-old, parsed from 20190301
    dump.
*   **Download size**: `74.77 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 93,527

## wikipedia/20190301.bg

*   **Config description**: Wikipedia dataset for bg, parsed from 20190301 dump.
*   **Download size**: `326.20 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 362,723

## wikipedia/20190301.bh

*   **Config description**: Wikipedia dataset for bh, parsed from 20190301 dump.
*   **Download size**: `13.28 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,725

## wikipedia/20190301.bi

*   **Config description**: Wikipedia dataset for bi, parsed from 20190301 dump.
*   **Download size**: `424.88 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,352

## wikipedia/20190301.bjn

*   **Config description**: Wikipedia dataset for bjn, parsed from 20190301
    dump.
*   **Download size**: `2.09 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,476

## wikipedia/20190301.bm

*   **Config description**: Wikipedia dataset for bm, parsed from 20190301 dump.
*   **Download size**: `447.98 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 729

## wikipedia/20190301.bn

*   **Config description**: Wikipedia dataset for bn, parsed from 20190301 dump.
*   **Download size**: `145.04 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 87,566

## wikipedia/20190301.bo

*   **Config description**: Wikipedia dataset for bo, parsed from 20190301 dump.
*   **Download size**: `12.41 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 11,301

## wikipedia/20190301.bpy

*   **Config description**: Wikipedia dataset for bpy, parsed from 20190301
    dump.
*   **Download size**: `5.05 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 25,360

## wikipedia/20190301.br

*   **Config description**: Wikipedia dataset for br, parsed from 20190301 dump.
*   **Download size**: `49.14 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 76,055

## wikipedia/20190301.bs

*   **Config description**: Wikipedia dataset for bs, parsed from 20190301 dump.
*   **Download size**: `103.26 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 181,802

## wikipedia/20190301.bug

*   **Config description**: Wikipedia dataset for bug, parsed from 20190301
    dump.
*   **Download size**: `1.76 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14,378

## wikipedia/20190301.bxr

*   **Config description**: Wikipedia dataset for bxr, parsed from 20190301
    dump.
*   **Download size**: `3.21 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,594

## wikipedia/20190301.ca

*   **Config description**: Wikipedia dataset for ca, parsed from 20190301 dump.
*   **Download size**: `849.65 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 650,189

## wikipedia/20190301.cbk-zam

*   **Config description**: Wikipedia dataset for cbk-zam, parsed from 20190301
    dump.
*   **Download size**: `1.84 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,289

## wikipedia/20190301.cdo

*   **Config description**: Wikipedia dataset for cdo, parsed from 20190301
    dump.
*   **Download size**: `3.22 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 15,422

## wikipedia/20190301.ce

*   **Config description**: Wikipedia dataset for ce, parsed from 20190301 dump.
*   **Download size**: `43.89 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 213,978

## wikipedia/20190301.ceb

*   **Config description**: Wikipedia dataset for ceb, parsed from 20190301
    dump.
*   **Download size**: `1.79 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,379,484

## wikipedia/20190301.ch

*   **Config description**: Wikipedia dataset for ch, parsed from 20190301 dump.
*   **Download size**: `684.97 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 496

## wikipedia/20190301.cho

*   **Config description**: Wikipedia dataset for cho, parsed from 20190301
    dump.
*   **Download size**: `25.99 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14

## wikipedia/20190301.chr

*   **Config description**: Wikipedia dataset for chr, parsed from 20190301
    dump.
*   **Download size**: `651.25 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 947

## wikipedia/20190301.chy

*   **Config description**: Wikipedia dataset for chy, parsed from 20190301
    dump.
*   **Download size**: `325.90 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 773

## wikipedia/20190301.ckb

*   **Config description**: Wikipedia dataset for ckb, parsed from 20190301
    dump.
*   **Download size**: `22.16 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 23,099

## wikipedia/20190301.co

*   **Config description**: Wikipedia dataset for co, parsed from 20190301 dump.
*   **Download size**: `3.38 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,232

## wikipedia/20190301.cr

*   **Config description**: Wikipedia dataset for cr, parsed from 20190301 dump.
*   **Download size**: `259.71 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 118

## wikipedia/20190301.crh

*   **Config description**: Wikipedia dataset for crh, parsed from 20190301
    dump.
*   **Download size**: `4.01 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,341

## wikipedia/20190301.cs

*   **Config description**: Wikipedia dataset for cs, parsed from 20190301 dump.
*   **Download size**: `759.21 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 539,754

## wikipedia/20190301.csb

*   **Config description**: Wikipedia dataset for csb, parsed from 20190301
    dump.
*   **Download size**: `2.03 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,620

## wikipedia/20190301.cu

*   **Config description**: Wikipedia dataset for cu, parsed from 20190301 dump.
*   **Download size**: `631.49 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,463

## wikipedia/20190301.cv

*   **Config description**: Wikipedia dataset for cv, parsed from 20190301 dump.
*   **Download size**: `22.23 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 44,865

## wikipedia/20190301.cy

*   **Config description**: Wikipedia dataset for cy, parsed from 20190301 dump.
*   **Download size**: `64.37 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 142,397

## wikipedia/20190301.da

*   **Config description**: Wikipedia dataset for da, parsed from 20190301 dump.
*   **Download size**: `323.53 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 244,767

## wikipedia/20190301.de

*   **Config description**: Wikipedia dataset for de, parsed from 20190301 dump.
*   **Download size**: `4.97 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,925,588

## wikipedia/20190301.din

*   **Config description**: Wikipedia dataset for din, parsed from 20190301
    dump.
*   **Download size**: `457.06 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 228

## wikipedia/20190301.diq

*   **Config description**: Wikipedia dataset for diq, parsed from 20190301
    dump.
*   **Download size**: `7.24 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 11,948

## wikipedia/20190301.dsb

*   **Config description**: Wikipedia dataset for dsb, parsed from 20190301
    dump.
*   **Download size**: `3.54 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,438

## wikipedia/20190301.dty

*   **Config description**: Wikipedia dataset for dty, parsed from 20190301
    dump.
*   **Download size**: `4.95 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,323

## wikipedia/20190301.dv

*   **Config description**: Wikipedia dataset for dv, parsed from 20190301 dump.
*   **Download size**: `4.24 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,156

## wikipedia/20190301.dz

*   **Config description**: Wikipedia dataset for dz, parsed from 20190301 dump.
*   **Download size**: `360.01 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 286

## wikipedia/20190301.ee

*   **Config description**: Wikipedia dataset for ee, parsed from 20190301 dump.
*   **Download size**: `434.14 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 368

## wikipedia/20190301.el

*   **Config description**: Wikipedia dataset for el, parsed from 20190301 dump.
*   **Download size**: `324.40 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 224,159

## wikipedia/20190301.eml

*   **Config description**: Wikipedia dataset for eml, parsed from 20190301
    dump.
*   **Download size**: `7.72 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 13,957

## wikipedia/20190301.en

*   **Config description**: Wikipedia dataset for en, parsed from 20190301 dump.
*   **Download size**: `15.72 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,824,596

## wikipedia/20190301.eo

*   **Config description**: Wikipedia dataset for eo, parsed from 20190301 dump.
*   **Download size**: `245.73 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 353,663

## wikipedia/20190301.es

*   **Config description**: Wikipedia dataset for es, parsed from 20190301 dump.
*   **Download size**: `2.93 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,728,167

## wikipedia/20190301.et

*   **Config description**: Wikipedia dataset for et, parsed from 20190301 dump.
*   **Download size**: `196.03 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 288,641

## wikipedia/20190301.eu

*   **Config description**: Wikipedia dataset for eu, parsed from 20190301 dump.
*   **Download size**: `180.35 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 400,162

## wikipedia/20190301.ext

*   **Config description**: Wikipedia dataset for ext, parsed from 20190301
    dump.
*   **Download size**: `2.40 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,278

## wikipedia/20190301.fa

*   **Config description**: Wikipedia dataset for fa, parsed from 20190301 dump.
*   **Download size**: `693.84 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,201,990

## wikipedia/20190301.ff

*   **Config description**: Wikipedia dataset for ff, parsed from 20190301 dump.
*   **Download size**: `387.75 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 298

## wikipedia/20190301.fi

*   **Config description**: Wikipedia dataset for fi, parsed from 20190301 dump.
*   **Download size**: `656.44 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 619,207

## wikipedia/20190301.fiu-vro

*   **Config description**: Wikipedia dataset for fiu-vro, parsed from 20190301
    dump.
*   **Download size**: `2.00 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,050

## wikipedia/20190301.fj

*   **Config description**: Wikipedia dataset for fj, parsed from 20190301 dump.
*   **Download size**: `262.98 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 507

## wikipedia/20190301.fo

*   **Config description**: Wikipedia dataset for fo, parsed from 20190301 dump.
*   **Download size**: `13.67 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 12,935

## wikipedia/20190301.fr

*   **Config description**: Wikipedia dataset for fr, parsed from 20190301 dump.
*   **Download size**: `4.14 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,087,215

## wikipedia/20190301.frp

*   **Config description**: Wikipedia dataset for frp, parsed from 20190301
    dump.
*   **Download size**: `2.03 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,262

## wikipedia/20190301.frr

*   **Config description**: Wikipedia dataset for frr, parsed from 20190301
    dump.
*   **Download size**: `7.88 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 9,706

## wikipedia/20190301.fur

*   **Config description**: Wikipedia dataset for fur, parsed from 20190301
    dump.
*   **Download size**: `2.29 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,508

## wikipedia/20190301.fy

*   **Config description**: Wikipedia dataset for fy, parsed from 20190301 dump.
*   **Download size**: `45.52 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 41,573

## wikipedia/20190301.ga

*   **Config description**: Wikipedia dataset for ga, parsed from 20190301 dump.
*   **Download size**: `24.78 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 56,252

## wikipedia/20190301.gag

*   **Config description**: Wikipedia dataset for gag, parsed from 20190301
    dump.
*   **Download size**: `2.04 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,034

## wikipedia/20190301.gan

*   **Config description**: Wikipedia dataset for gan, parsed from 20190301
    dump.
*   **Download size**: `3.82 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,503

## wikipedia/20190301.gd

*   **Config description**: Wikipedia dataset for gd, parsed from 20190301 dump.
*   **Download size**: `8.51 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14,891

## wikipedia/20190301.gl

*   **Config description**: Wikipedia dataset for gl, parsed from 20190301 dump.
*   **Download size**: `235.07 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 203,961

## wikipedia/20190301.glk

*   **Config description**: Wikipedia dataset for glk, parsed from 20190301
    dump.
*   **Download size**: `1.91 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,432

## wikipedia/20190301.gn

*   **Config description**: Wikipedia dataset for gn, parsed from 20190301 dump.
*   **Download size**: `3.37 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,337

## wikipedia/20190301.gom

*   **Config description**: Wikipedia dataset for gom, parsed from 20190301
    dump.
*   **Download size**: `6.07 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,259

## wikipedia/20190301.gor

*   **Config description**: Wikipedia dataset for gor, parsed from 20190301
    dump.
*   **Download size**: `1.28 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,467

## wikipedia/20190301.got

*   **Config description**: Wikipedia dataset for got, parsed from 20190301
    dump.
*   **Download size**: `604.10 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 715

## wikipedia/20190301.gu

*   **Config description**: Wikipedia dataset for gu, parsed from 20190301 dump.
*   **Download size**: `27.23 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 28,607

## wikipedia/20190301.gv

*   **Config description**: Wikipedia dataset for gv, parsed from 20190301 dump.
*   **Download size**: `5.32 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,996

## wikipedia/20190301.ha

*   **Config description**: Wikipedia dataset for ha, parsed from 20190301 dump.
*   **Download size**: `1.62 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,795

## wikipedia/20190301.hak

*   **Config description**: Wikipedia dataset for hak, parsed from 20190301
    dump.
*   **Download size**: `3.28 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 11,445

## wikipedia/20190301.haw

*   **Config description**: Wikipedia dataset for haw, parsed from 20190301
    dump.
*   **Download size**: `1017.76 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,935

## wikipedia/20190301.he

*   **Config description**: Wikipedia dataset for he, parsed from 20190301 dump.
*   **Download size**: `572.30 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 393,436

## wikipedia/20190301.hi

*   **Config description**: Wikipedia dataset for hi, parsed from 20190301 dump.
*   **Download size**: `137.86 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 156,142

## wikipedia/20190301.hif

*   **Config description**: Wikipedia dataset for hif, parsed from 20190301
    dump.
*   **Download size**: `4.57 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 10,036

## wikipedia/20190301.ho

*   **Config description**: Wikipedia dataset for ho, parsed from 20190301 dump.
*   **Download size**: `18.37 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3

## wikipedia/20190301.hr

*   **Config description**: Wikipedia dataset for hr, parsed from 20190301 dump.
*   **Download size**: `246.05 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 228,044

## wikipedia/20190301.hsb

*   **Config description**: Wikipedia dataset for hsb, parsed from 20190301
    dump.
*   **Download size**: `10.38 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14,693

## wikipedia/20190301.ht

*   **Config description**: Wikipedia dataset for ht, parsed from 20190301 dump.
*   **Download size**: `10.23 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 56,093

## wikipedia/20190301.hu

*   **Config description**: Wikipedia dataset for hu, parsed from 20190301 dump.
*   **Download size**: `810.17 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 625,614

## wikipedia/20190301.hy

*   **Config description**: Wikipedia dataset for hy, parsed from 20190301 dump.
*   **Download size**: `277.53 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 575,357

## wikipedia/20190301.ia

*   **Config description**: Wikipedia dataset for ia, parsed from 20190301 dump.
*   **Download size**: `7.85 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 18,780

## wikipedia/20190301.id

*   **Config description**: Wikipedia dataset for id, parsed from 20190301 dump.
*   **Download size**: `523.94 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 947,627

## wikipedia/20190301.ie

*   **Config description**: Wikipedia dataset for ie, parsed from 20190301 dump.
*   **Download size**: `1.70 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,403

## wikipedia/20190301.ig

*   **Config description**: Wikipedia dataset for ig, parsed from 20190301 dump.
*   **Download size**: `1.00 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,710

## wikipedia/20190301.ii

*   **Config description**: Wikipedia dataset for ii, parsed from 20190301 dump.
*   **Download size**: `30.88 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14

## wikipedia/20190301.ik

*   **Config description**: Wikipedia dataset for ik, parsed from 20190301 dump.
*   **Download size**: `238.12 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 647

## wikipedia/20190301.ilo

*   **Config description**: Wikipedia dataset for ilo, parsed from 20190301
    dump.
*   **Download size**: `15.22 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 11,808

## wikipedia/20190301.inh

*   **Config description**: Wikipedia dataset for inh, parsed from 20190301
    dump.
*   **Download size**: `1.26 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 932

## wikipedia/20190301.io

*   **Config description**: Wikipedia dataset for io, parsed from 20190301 dump.
*   **Download size**: `12.56 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 29,629

## wikipedia/20190301.is

*   **Config description**: Wikipedia dataset for is, parsed from 20190301 dump.
*   **Download size**: `41.86 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 66,219

## wikipedia/20190301.it

*   **Config description**: Wikipedia dataset for it, parsed from 20190301 dump.
*   **Download size**: `2.66 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,800,218

## wikipedia/20190301.iu

*   **Config description**: Wikipedia dataset for iu, parsed from 20190301 dump.
*   **Download size**: `284.06 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 510

## wikipedia/20190301.ja

*   **Config description**: Wikipedia dataset for ja, parsed from 20190301 dump.
*   **Download size**: `2.74 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,382,683

## wikipedia/20190301.jam

*   **Config description**: Wikipedia dataset for jam, parsed from 20190301
    dump.
*   **Download size**: `895.29 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,692

## wikipedia/20190301.jbo

*   **Config description**: Wikipedia dataset for jbo, parsed from 20190301
    dump.
*   **Download size**: `1.06 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,301

## wikipedia/20190301.jv

*   **Config description**: Wikipedia dataset for jv, parsed from 20190301 dump.
*   **Download size**: `39.32 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 72,893

## wikipedia/20190301.ka

*   **Config description**: Wikipedia dataset for ka, parsed from 20190301 dump.
*   **Download size**: `131.78 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 161,290

## wikipedia/20190301.kaa

*   **Config description**: Wikipedia dataset for kaa, parsed from 20190301
    dump.
*   **Download size**: `1.35 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,192

## wikipedia/20190301.kab

*   **Config description**: Wikipedia dataset for kab, parsed from 20190301
    dump.
*   **Download size**: `3.62 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,415

## wikipedia/20190301.kbd

*   **Config description**: Wikipedia dataset for kbd, parsed from 20190301
    dump.
*   **Download size**: `1.65 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,608

## wikipedia/20190301.kbp

*   **Config description**: Wikipedia dataset for kbp, parsed from 20190301
    dump.
*   **Download size**: `1.24 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,706

## wikipedia/20190301.kg

*   **Config description**: Wikipedia dataset for kg, parsed from 20190301 dump.
*   **Download size**: `439.26 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,240

## wikipedia/20190301.ki

*   **Config description**: Wikipedia dataset for ki, parsed from 20190301 dump.
*   **Download size**: `370.78 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,482

## wikipedia/20190301.kj

*   **Config description**: Wikipedia dataset for kj, parsed from 20190301 dump.
*   **Download size**: `16.58 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5

## wikipedia/20190301.kk

*   **Config description**: Wikipedia dataset for kk, parsed from 20190301 dump.
*   **Download size**: `113.46 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 266,609

## wikipedia/20190301.kl

*   **Config description**: Wikipedia dataset for kl, parsed from 20190301 dump.
*   **Download size**: `862.51 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,713

## wikipedia/20190301.km

*   **Config description**: Wikipedia dataset for km, parsed from 20190301 dump.
*   **Download size**: `21.92 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 10,889

## wikipedia/20190301.kn

*   **Config description**: Wikipedia dataset for kn, parsed from 20190301 dump.
*   **Download size**: `69.62 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 24,679

## wikipedia/20190301.ko

*   **Config description**: Wikipedia dataset for ko, parsed from 20190301 dump.
*   **Download size**: `625.16 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 980,493

## wikipedia/20190301.koi

*   **Config description**: Wikipedia dataset for koi, parsed from 20190301
    dump.
*   **Download size**: `2.12 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,964

## wikipedia/20190301.krc

*   **Config description**: Wikipedia dataset for krc, parsed from 20190301
    dump.
*   **Download size**: `3.16 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,317

## wikipedia/20190301.ks

*   **Config description**: Wikipedia dataset for ks, parsed from 20190301 dump.
*   **Download size**: `309.15 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 399

## wikipedia/20190301.ksh

*   **Config description**: Wikipedia dataset for ksh, parsed from 20190301
    dump.
*   **Download size**: `3.07 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,356

## wikipedia/20190301.ku

*   **Config description**: Wikipedia dataset for ku, parsed from 20190301 dump.
*   **Download size**: `17.09 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 30,811

## wikipedia/20190301.kv

*   **Config description**: Wikipedia dataset for kv, parsed from 20190301 dump.
*   **Download size**: `3.36 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,733

## wikipedia/20190301.kw

*   **Config description**: Wikipedia dataset for kw, parsed from 20190301 dump.
*   **Download size**: `1.71 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,913

## wikipedia/20190301.ky

*   **Config description**: Wikipedia dataset for ky, parsed from 20190301 dump.
*   **Download size**: `33.13 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 79,311

## wikipedia/20190301.la

*   **Config description**: Wikipedia dataset for la, parsed from 20190301 dump.
*   **Download size**: `82.72 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 130,161

## wikipedia/20190301.lad

*   **Config description**: Wikipedia dataset for lad, parsed from 20190301
    dump.
*   **Download size**: `3.39 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,261

## wikipedia/20190301.lb

*   **Config description**: Wikipedia dataset for lb, parsed from 20190301 dump.
*   **Download size**: `45.70 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 61,607

## wikipedia/20190301.lbe

*   **Config description**: Wikipedia dataset for lbe, parsed from 20190301
    dump.
*   **Download size**: `1.22 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,545

## wikipedia/20190301.lez

*   **Config description**: Wikipedia dataset for lez, parsed from 20190301
    dump.
*   **Download size**: `4.16 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,348

## wikipedia/20190301.lfn

*   **Config description**: Wikipedia dataset for lfn, parsed from 20190301
    dump.
*   **Download size**: `2.81 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,741

## wikipedia/20190301.lg

*   **Config description**: Wikipedia dataset for lg, parsed from 20190301 dump.
*   **Download size**: `1.58 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,359

## wikipedia/20190301.li

*   **Config description**: Wikipedia dataset for li, parsed from 20190301 dump.
*   **Download size**: `13.86 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14,155

## wikipedia/20190301.lij

*   **Config description**: Wikipedia dataset for lij, parsed from 20190301
    dump.
*   **Download size**: `2.73 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,281

## wikipedia/20190301.lmo

*   **Config description**: Wikipedia dataset for lmo, parsed from 20190301
    dump.
*   **Download size**: `21.34 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 43,911

## wikipedia/20190301.ln

*   **Config description**: Wikipedia dataset for ln, parsed from 20190301 dump.
*   **Download size**: `1.83 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,192

## wikipedia/20190301.lo

*   **Config description**: Wikipedia dataset for lo, parsed from 20190301 dump.
*   **Download size**: `3.44 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,074

## wikipedia/20190301.lrc

*   **Config description**: Wikipedia dataset for lrc, parsed from 20190301
    dump.
*   **Download size**: `4.71 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,774

## wikipedia/20190301.lt

*   **Config description**: Wikipedia dataset for lt, parsed from 20190301 dump.
*   **Download size**: `174.73 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 217,121

## wikipedia/20190301.ltg

*   **Config description**: Wikipedia dataset for ltg, parsed from 20190301
    dump.
*   **Download size**: `798.18 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 920

## wikipedia/20190301.lv

*   **Config description**: Wikipedia dataset for lv, parsed from 20190301 dump.
*   **Download size**: `127.47 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 91,567

## wikipedia/20190301.mai

*   **Config description**: Wikipedia dataset for mai, parsed from 20190301
    dump.
*   **Download size**: `10.80 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14,523

## wikipedia/20190301.map-bms

*   **Config description**: Wikipedia dataset for map-bms, parsed from 20190301
    dump.
*   **Download size**: `4.49 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 13,710

## wikipedia/20190301.mdf

*   **Config description**: Wikipedia dataset for mdf, parsed from 20190301
    dump.
*   **Download size**: `1.04 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,344

## wikipedia/20190301.mg

*   **Config description**: Wikipedia dataset for mg, parsed from 20190301 dump.
*   **Download size**: `25.64 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 126,066

## wikipedia/20190301.mh

*   **Config description**: Wikipedia dataset for mh, parsed from 20190301 dump.
*   **Download size**: `27.71 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 8

## wikipedia/20190301.mhr

*   **Config description**: Wikipedia dataset for mhr, parsed from 20190301
    dump.
*   **Download size**: `5.69 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 12,204

## wikipedia/20190301.mi

*   **Config description**: Wikipedia dataset for mi, parsed from 20190301 dump.
*   **Download size**: `1.96 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 7,174

## wikipedia/20190301.min

*   **Config description**: Wikipedia dataset for min, parsed from 20190301
    dump.
*   **Download size**: `25.05 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 226,002

## wikipedia/20190301.mk

*   **Config description**: Wikipedia dataset for mk, parsed from 20190301 dump.
*   **Download size**: `140.69 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 138,779

## wikipedia/20190301.ml

*   **Config description**: Wikipedia dataset for ml, parsed from 20190301 dump.
*   **Download size**: `117.24 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 112,979

## wikipedia/20190301.mn

*   **Config description**: Wikipedia dataset for mn, parsed from 20190301 dump.
*   **Download size**: `28.23 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 23,195

## wikipedia/20190301.mr

*   **Config description**: Wikipedia dataset for mr, parsed from 20190301 dump.
*   **Download size**: `49.58 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 95,825

## wikipedia/20190301.mrj

*   **Config description**: Wikipedia dataset for mrj, parsed from 20190301
    dump.
*   **Download size**: `3.01 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 10,826

## wikipedia/20190301.ms

*   **Config description**: Wikipedia dataset for ms, parsed from 20190301 dump.
*   **Download size**: `205.79 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 357,957

## wikipedia/20190301.mt

*   **Config description**: Wikipedia dataset for mt, parsed from 20190301 dump.
*   **Download size**: `8.21 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,610

## wikipedia/20190301.mus

*   **Config description**: Wikipedia dataset for mus, parsed from 20190301
    dump.
*   **Download size**: `14.20 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2

## wikipedia/20190301.mwl

*   **Config description**: Wikipedia dataset for mwl, parsed from 20190301
    dump.
*   **Download size**: `8.95 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,279

## wikipedia/20190301.my

*   **Config description**: Wikipedia dataset for my, parsed from 20190301 dump.
*   **Download size**: `34.60 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 46,348

## wikipedia/20190301.myv

*   **Config description**: Wikipedia dataset for myv, parsed from 20190301
    dump.
*   **Download size**: `7.79 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,077

## wikipedia/20190301.mzn

*   **Config description**: Wikipedia dataset for mzn, parsed from 20190301
    dump.
*   **Download size**: `6.47 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 18,184

## wikipedia/20190301.na

*   **Config description**: Wikipedia dataset for na, parsed from 20190301 dump.
*   **Download size**: `480.57 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,316

## wikipedia/20190301.nah

*   **Config description**: Wikipedia dataset for nah, parsed from 20190301
    dump.
*   **Download size**: `4.30 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 10,613

## wikipedia/20190301.nap

*   **Config description**: Wikipedia dataset for nap, parsed from 20190301
    dump.
*   **Download size**: `5.55 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 15,167

## wikipedia/20190301.nds

*   **Config description**: Wikipedia dataset for nds, parsed from 20190301
    dump.
*   **Download size**: `33.28 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 45,754

## wikipedia/20190301.nds-nl

*   **Config description**: Wikipedia dataset for nds-nl, parsed from 20190301
    dump.
*   **Download size**: `6.67 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 8,644

## wikipedia/20190301.ne

*   **Config description**: Wikipedia dataset for ne, parsed from 20190301 dump.
*   **Download size**: `29.26 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 33,465

## wikipedia/20190301.new

*   **Config description**: Wikipedia dataset for new, parsed from 20190301
    dump.
*   **Download size**: `16.91 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 72,872

## wikipedia/20190301.ng

*   **Config description**: Wikipedia dataset for ng, parsed from 20190301 dump.
*   **Download size**: `91.11 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 21

## wikipedia/20190301.nl

*   **Config description**: Wikipedia dataset for nl, parsed from 20190301 dump.
*   **Download size**: `1.38 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,409,491

## wikipedia/20190301.nn

*   **Config description**: Wikipedia dataset for nn, parsed from 20190301 dump.
*   **Download size**: `126.01 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 213,859

## wikipedia/20190301.no

*   **Config description**: Wikipedia dataset for no, parsed from 20190301 dump.
*   **Download size**: `610.74 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 783,420

## wikipedia/20190301.nov

*   **Config description**: Wikipedia dataset for nov, parsed from 20190301
    dump.
*   **Download size**: `1.12 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,780

## wikipedia/20190301.nrm

*   **Config description**: Wikipedia dataset for nrm, parsed from 20190301
    dump.
*   **Download size**: `1.56 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,048

## wikipedia/20190301.nso

*   **Config description**: Wikipedia dataset for nso, parsed from 20190301
    dump.
*   **Download size**: `2.20 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 8,075

## wikipedia/20190301.nv

*   **Config description**: Wikipedia dataset for nv, parsed from 20190301 dump.
*   **Download size**: `2.52 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 7,105

## wikipedia/20190301.ny

*   **Config description**: Wikipedia dataset for ny, parsed from 20190301 dump.
*   **Download size**: `1.18 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 566

## wikipedia/20190301.oc

*   **Config description**: Wikipedia dataset for oc, parsed from 20190301 dump.
*   **Download size**: `70.97 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 91,840

## wikipedia/20190301.olo

*   **Config description**: Wikipedia dataset for olo, parsed from 20190301
    dump.
*   **Download size**: `1.55 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,348

## wikipedia/20190301.om

*   **Config description**: Wikipedia dataset for om, parsed from 20190301 dump.
*   **Download size**: `1.06 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,054

## wikipedia/20190301.or

*   **Config description**: Wikipedia dataset for or, parsed from 20190301 dump.
*   **Download size**: `24.90 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 28,368

## wikipedia/20190301.os

*   **Config description**: Wikipedia dataset for os, parsed from 20190301 dump.
*   **Download size**: `7.31 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 13,490

## wikipedia/20190301.pa

*   **Config description**: Wikipedia dataset for pa, parsed from 20190301 dump.
*   **Download size**: `40.39 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 40,578

## wikipedia/20190301.pag

*   **Config description**: Wikipedia dataset for pag, parsed from 20190301
    dump.
*   **Download size**: `1.29 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,042

## wikipedia/20190301.pam

*   **Config description**: Wikipedia dataset for pam, parsed from 20190301
    dump.
*   **Download size**: `8.17 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 8,721

## wikipedia/20190301.pap

*   **Config description**: Wikipedia dataset for pap, parsed from 20190301
    dump.
*   **Download size**: `1.33 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,126

## wikipedia/20190301.pcd

*   **Config description**: Wikipedia dataset for pcd, parsed from 20190301
    dump.
*   **Download size**: `4.14 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,485

## wikipedia/20190301.pdc

*   **Config description**: Wikipedia dataset for pdc, parsed from 20190301
    dump.
*   **Download size**: `1.10 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,331

## wikipedia/20190301.pfl

*   **Config description**: Wikipedia dataset for pfl, parsed from 20190301
    dump.
*   **Download size**: `3.22 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,744

## wikipedia/20190301.pi

*   **Config description**: Wikipedia dataset for pi, parsed from 20190301 dump.
*   **Download size**: `586.77 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,057

## wikipedia/20190301.pih

*   **Config description**: Wikipedia dataset for pih, parsed from 20190301
    dump.
*   **Download size**: `654.11 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 748

## wikipedia/20190301.pl

*   **Config description**: Wikipedia dataset for pl, parsed from 20190301 dump.
*   **Download size**: `1.76 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,610,189

## wikipedia/20190301.pms

*   **Config description**: Wikipedia dataset for pms, parsed from 20190301
    dump.
*   **Download size**: `13.42 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 65,551

## wikipedia/20190301.pnb

*   **Config description**: Wikipedia dataset for pnb, parsed from 20190301
    dump.
*   **Download size**: `24.31 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 50,764

## wikipedia/20190301.pnt

*   **Config description**: Wikipedia dataset for pnt, parsed from 20190301
    dump.
*   **Download size**: `533.84 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 521

## wikipedia/20190301.ps

*   **Config description**: Wikipedia dataset for ps, parsed from 20190301 dump.
*   **Download size**: `14.09 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 10,554

## wikipedia/20190301.pt

*   **Config description**: Wikipedia dataset for pt, parsed from 20190301 dump.
*   **Download size**: `1.58 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,393,069

## wikipedia/20190301.qu

*   **Config description**: Wikipedia dataset for qu, parsed from 20190301 dump.
*   **Download size**: `11.42 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 29,495

## wikipedia/20190301.rm

*   **Config description**: Wikipedia dataset for rm, parsed from 20190301 dump.
*   **Download size**: `5.85 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 3,710

## wikipedia/20190301.rmy

*   **Config description**: Wikipedia dataset for rmy, parsed from 20190301
    dump.
*   **Download size**: `509.61 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 693

## wikipedia/20190301.rn

*   **Config description**: Wikipedia dataset for rn, parsed from 20190301 dump.
*   **Download size**: `779.25 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 696

## wikipedia/20190301.ro

*   **Config description**: Wikipedia dataset for ro, parsed from 20190301 dump.
*   **Download size**: `449.49 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 393,012

## wikipedia/20190301.roa-rup

*   **Config description**: Wikipedia dataset for roa-rup, parsed from 20190301
    dump.
*   **Download size**: `931.23 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,245

## wikipedia/20190301.roa-tara

*   **Config description**: Wikipedia dataset for roa-tara, parsed from 20190301
    dump.
*   **Download size**: `5.98 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 9,288

## wikipedia/20190301.ru

*   **Config description**: Wikipedia dataset for ru, parsed from 20190301 dump.
*   **Download size**: `3.51 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,449,364

## wikipedia/20190301.rue

*   **Config description**: Wikipedia dataset for rue, parsed from 20190301
    dump.
*   **Download size**: `4.11 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 7,526

## wikipedia/20190301.rw

*   **Config description**: Wikipedia dataset for rw, parsed from 20190301 dump.
*   **Download size**: `904.81 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,950

## wikipedia/20190301.sa

*   **Config description**: Wikipedia dataset for sa, parsed from 20190301 dump.
*   **Download size**: `14.29 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 21,846

## wikipedia/20190301.sah

*   **Config description**: Wikipedia dataset for sah, parsed from 20190301
    dump.
*   **Download size**: `11.88 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 15,504

## wikipedia/20190301.sat

*   **Config description**: Wikipedia dataset for sat, parsed from 20190301
    dump.
*   **Download size**: `2.36 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,036

## wikipedia/20190301.sc

*   **Config description**: Wikipedia dataset for sc, parsed from 20190301 dump.
*   **Download size**: `4.39 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,214

## wikipedia/20190301.scn

*   **Config description**: Wikipedia dataset for scn, parsed from 20190301
    dump.
*   **Download size**: `11.83 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 31,330

## wikipedia/20190301.sco

*   **Config description**: Wikipedia dataset for sco, parsed from 20190301
    dump.
*   **Download size**: `57.80 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 53,525

## wikipedia/20190301.sd

*   **Config description**: Wikipedia dataset for sd, parsed from 20190301 dump.
*   **Download size**: `12.62 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 16,930

## wikipedia/20190301.se

*   **Config description**: Wikipedia dataset for se, parsed from 20190301 dump.
*   **Download size**: `3.30 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 8,127

## wikipedia/20190301.sg

*   **Config description**: Wikipedia dataset for sg, parsed from 20190301 dump.
*   **Download size**: `286.02 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 281

## wikipedia/20190301.sh

*   **Config description**: Wikipedia dataset for sh, parsed from 20190301 dump.
*   **Download size**: `406.72 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 3,923,606

## wikipedia/20190301.si

*   **Config description**: Wikipedia dataset for si, parsed from 20190301 dump.
*   **Download size**: `36.84 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 25,922

## wikipedia/20190301.simple

*   **Config description**: Wikipedia dataset for simple, parsed from 20190301
    dump.
*   **Download size**: `156.11 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 143,427

## wikipedia/20190301.sk

*   **Config description**: Wikipedia dataset for sk, parsed from 20190301 dump.
*   **Download size**: `254.37 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 244,877

## wikipedia/20190301.sl

*   **Config description**: Wikipedia dataset for sl, parsed from 20190301 dump.
*   **Download size**: `201.41 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 191,938

## wikipedia/20190301.sm

*   **Config description**: Wikipedia dataset for sm, parsed from 20190301 dump.
*   **Download size**: `678.46 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 957

## wikipedia/20190301.sn

*   **Config description**: Wikipedia dataset for sn, parsed from 20190301 dump.
*   **Download size**: `2.02 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,656

## wikipedia/20190301.so

*   **Config description**: Wikipedia dataset for so, parsed from 20190301 dump.
*   **Download size**: `8.17 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,587

## wikipedia/20190301.sq

*   **Config description**: Wikipedia dataset for sq, parsed from 20190301 dump.
*   **Download size**: `77.55 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 102,156

## wikipedia/20190301.sr

*   **Config description**: Wikipedia dataset for sr, parsed from 20190301 dump.
*   **Download size**: `725.30 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 3,043,191

## wikipedia/20190301.srn

*   **Config description**: Wikipedia dataset for srn, parsed from 20190301
    dump.
*   **Download size**: `634.21 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,234

## wikipedia/20190301.ss

*   **Config description**: Wikipedia dataset for ss, parsed from 20190301 dump.
*   **Download size**: `737.58 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 495

## wikipedia/20190301.st

*   **Config description**: Wikipedia dataset for st, parsed from 20190301 dump.
*   **Download size**: `482.27 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 605

## wikipedia/20190301.stq

*   **Config description**: Wikipedia dataset for stq, parsed from 20190301
    dump.
*   **Download size**: `3.26 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 4,477

## wikipedia/20190301.su

*   **Config description**: Wikipedia dataset for su, parsed from 20190301 dump.
*   **Download size**: `20.52 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 43,393

## wikipedia/20190301.sv

*   **Config description**: Wikipedia dataset for sv, parsed from 20190301 dump.
*   **Download size**: `1.64 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,950,503

## wikipedia/20190301.sw

*   **Config description**: Wikipedia dataset for sw, parsed from 20190301 dump.
*   **Download size**: `27.60 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 48,434

## wikipedia/20190301.szl

*   **Config description**: Wikipedia dataset for szl, parsed from 20190301
    dump.
*   **Download size**: `4.06 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 8,603

## wikipedia/20190301.ta

*   **Config description**: Wikipedia dataset for ta, parsed from 20190301 dump.
*   **Download size**: `141.07 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 154,505

## wikipedia/20190301.tcy

*   **Config description**: Wikipedia dataset for tcy, parsed from 20190301
    dump.
*   **Download size**: `2.33 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,267

## wikipedia/20190301.te

*   **Config description**: Wikipedia dataset for te, parsed from 20190301 dump.
*   **Download size**: `113.16 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 91,857

## wikipedia/20190301.tet

*   **Config description**: Wikipedia dataset for tet, parsed from 20190301
    dump.
*   **Download size**: `1.06 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,556

## wikipedia/20190301.tg

*   **Config description**: Wikipedia dataset for tg, parsed from 20190301 dump.
*   **Download size**: `36.95 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 96,808

## wikipedia/20190301.th

*   **Config description**: Wikipedia dataset for th, parsed from 20190301 dump.
*   **Download size**: `254.00 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 224,144

## wikipedia/20190301.ti

*   **Config description**: Wikipedia dataset for ti, parsed from 20190301 dump.
*   **Download size**: `309.72 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 304

## wikipedia/20190301.tk

*   **Config description**: Wikipedia dataset for tk, parsed from 20190301 dump.
*   **Download size**: `4.50 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 6,743

## wikipedia/20190301.tl

*   **Config description**: Wikipedia dataset for tl, parsed from 20190301 dump.
*   **Download size**: `50.85 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 76,905

## wikipedia/20190301.tn

*   **Config description**: Wikipedia dataset for tn, parsed from 20190301 dump.
*   **Download size**: `1.21 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 751

## wikipedia/20190301.to

*   **Config description**: Wikipedia dataset for to, parsed from 20190301 dump.
*   **Download size**: `775.10 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,577

## wikipedia/20190301.tpi

*   **Config description**: Wikipedia dataset for tpi, parsed from 20190301
    dump.
*   **Download size**: `1.39 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,523

## wikipedia/20190301.tr

*   **Config description**: Wikipedia dataset for tr, parsed from 20190301 dump.
*   **Download size**: `497.19 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 548,768

## wikipedia/20190301.ts

*   **Config description**: Wikipedia dataset for ts, parsed from 20190301 dump.
*   **Download size**: `1.39 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 665

## wikipedia/20190301.tt

*   **Config description**: Wikipedia dataset for tt, parsed from 20190301 dump.
*   **Download size**: `53.23 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 120,720

## wikipedia/20190301.tum

*   **Config description**: Wikipedia dataset for tum, parsed from 20190301
    dump.
*   **Download size**: `309.58 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 638

## wikipedia/20190301.tw

*   **Config description**: Wikipedia dataset for tw, parsed from 20190301 dump.
*   **Download size**: `345.96 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 697

## wikipedia/20190301.ty

*   **Config description**: Wikipedia dataset for ty, parsed from 20190301 dump.
*   **Download size**: `485.56 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,279

## wikipedia/20190301.tyv

*   **Config description**: Wikipedia dataset for tyv, parsed from 20190301
    dump.
*   **Download size**: `2.60 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,563

## wikipedia/20190301.udm

*   **Config description**: Wikipedia dataset for udm, parsed from 20190301
    dump.
*   **Download size**: `2.94 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,768

## wikipedia/20190301.ug

*   **Config description**: Wikipedia dataset for ug, parsed from 20190301 dump.
*   **Download size**: `5.64 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,908

## wikipedia/20190301.uk

*   **Config description**: Wikipedia dataset for uk, parsed from 20190301 dump.
*   **Download size**: `1.28 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,131,279

## wikipedia/20190301.ur

*   **Config description**: Wikipedia dataset for ur, parsed from 20190301 dump.
*   **Download size**: `129.57 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 330,776

## wikipedia/20190301.uz

*   **Config description**: Wikipedia dataset for uz, parsed from 20190301 dump.
*   **Download size**: `60.85 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 149,537

## wikipedia/20190301.ve

*   **Config description**: Wikipedia dataset for ve, parsed from 20190301 dump.
*   **Download size**: `257.59 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 337

## wikipedia/20190301.vec

*   **Config description**: Wikipedia dataset for vec, parsed from 20190301
    dump.
*   **Download size**: `10.65 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 13,433

## wikipedia/20190301.vep

*   **Config description**: Wikipedia dataset for vep, parsed from 20190301
    dump.
*   **Download size**: `4.59 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 7,230

## wikipedia/20190301.vi

*   **Config description**: Wikipedia dataset for vi, parsed from 20190301 dump.
*   **Download size**: `623.74 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,377,623

## wikipedia/20190301.vls

*   **Config description**: Wikipedia dataset for vls, parsed from 20190301
    dump.
*   **Download size**: `6.58 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 7,233

## wikipedia/20190301.vo

*   **Config description**: Wikipedia dataset for vo, parsed from 20190301 dump.
*   **Download size**: `23.80 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 122,640

## wikipedia/20190301.wa

*   **Config description**: Wikipedia dataset for wa, parsed from 20190301 dump.
*   **Download size**: `8.75 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 15,283

## wikipedia/20190301.war

*   **Config description**: Wikipedia dataset for war, parsed from 20190301
    dump.
*   **Download size**: `256.72 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,263,705

## wikipedia/20190301.wo

*   **Config description**: Wikipedia dataset for wo, parsed from 20190301 dump.
*   **Download size**: `1.54 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,336

## wikipedia/20190301.wuu

*   **Config description**: Wikipedia dataset for wuu, parsed from 20190301
    dump.
*   **Download size**: `9.08 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 19,269

## wikipedia/20190301.xal

*   **Config description**: Wikipedia dataset for xal, parsed from 20190301
    dump.
*   **Download size**: `1.64 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,794

## wikipedia/20190301.xh

*   **Config description**: Wikipedia dataset for xh, parsed from 20190301 dump.
*   **Download size**: `1.26 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,004

## wikipedia/20190301.xmf

*   **Config description**: Wikipedia dataset for xmf, parsed from 20190301
    dump.
*   **Download size**: `9.40 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 14,297

## wikipedia/20190301.yi

*   **Config description**: Wikipedia dataset for yi, parsed from 20190301 dump.
*   **Download size**: `11.56 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 23,430

## wikipedia/20190301.yo

*   **Config description**: Wikipedia dataset for yo, parsed from 20190301 dump.
*   **Download size**: `11.55 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 31,968

## wikipedia/20190301.za

*   **Config description**: Wikipedia dataset for za, parsed from 20190301 dump.
*   **Download size**: `735.93 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 2,404

## wikipedia/20190301.zea

*   **Config description**: Wikipedia dataset for zea, parsed from 20190301
    dump.
*   **Download size**: `2.47 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 5,408

## wikipedia/20190301.zh

*   **Config description**: Wikipedia dataset for zh, parsed from 20190301 dump.
*   **Download size**: `1.71 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,482,100

## wikipedia/20190301.zh-classical

*   **Config description**: Wikipedia dataset for zh-classical, parsed from
    20190301 dump.
*   **Download size**: `13.37 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 10,173

## wikipedia/20190301.zh-min-nan

*   **Config description**: Wikipedia dataset for zh-min-nan, parsed from
    20190301 dump.
*   **Download size**: `50.30 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 233,720

## wikipedia/20190301.zh-yue

*   **Config description**: Wikipedia dataset for zh-yue, parsed from 20190301
    dump.
*   **Download size**: `52.41 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 70,666

## wikipedia/20190301.zu

*   **Config description**: Wikipedia dataset for zu, parsed from 20190301 dump.
*   **Download size**: `1.50 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,184
