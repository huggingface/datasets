<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="big_patent" />
  <meta itemprop="description" content="&#10;BIGPATENT, consisting of 1.3 million records of U.S. patent documents&#10;along with human written abstractive summaries.&#10;Each US patent application is filed under a Cooperative Patent Classification&#10;(CPC) code. There are nine such classification categories:&#10;A (Human Necessities), B (Performing Operations; Transporting),&#10;C (Chemistry; Metallurgy), D (Textiles; Paper), E (Fixed Constructions),&#10;F (Mechanical Engineering; Lightning; Heating; Weapons; Blasting),&#10;G (Physics), H (Electricity), and&#10;Y (General tagging of new or cross-sectional technology)&#10;&#10;There are two features:&#10;  - description: detailed description of patent.&#10;  - summary: Patent abastract.&#10;&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;big_patent&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/big_patent" />
  <meta itemprop="sameAs" content="https://evasharma.github.io/bigpatent/" />
  <meta itemprop="citation" content="&#10;@misc{sharma2019bigpatent,&#10;    title={BIGPATENT: A Large-Scale Dataset for Abstractive and Coherent Summarization},&#10;    author={Eva Sharma and Chen Li and Lu Wang},&#10;    year={2019},&#10;    eprint={1906.03741},&#10;    archivePrefix={arXiv},&#10;    primaryClass={cs.CL}&#10;}&#10;" />
</div>
# `big_patent`

*   **Description**:

BIGPATENT, consisting of 1.3 million records of U.S. patent documents along with
human written abstractive summaries. Each US patent application is filed under a
Cooperative Patent Classification (CPC) code. There are nine such classification
categories: A (Human Necessities), B (Performing Operations; Transporting), C
(Chemistry; Metallurgy), D (Textiles; Paper), E (Fixed Constructions), F
(Mechanical Engineering; Lightning; Heating; Weapons; Blasting), G (Physics), H
(Electricity), and Y (General tagging of new or cross-sectional technology)

There are two features: - description: detailed description of patent. -
summary: Patent abastract.

*   **Homepage**:
    [https://evasharma.github.io/bigpatent/](https://evasharma.github.io/bigpatent/)
*   **Source code**:
    [`tfds.summarization.big_patent.BigPatent`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/summarization/big_patent.py)
*   **Versions**:
    *   **`2.0.0`** (default): Updated to cased raw strings.
    *   `1.0.0`: No release notes.
*   **Download size**: `Unknown size`
*   **Features**:

```python
FeaturesDict({
    'abstract': Text(shape=(), dtype=tf.string),
    'description': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('description', 'abstract')`
*   **Citation**:

```
@misc{sharma2019bigpatent,
    title={BIGPATENT: A Large-Scale Dataset for Abstractive and Coherent Summarization},
    author={Eva Sharma and Chen Li and Lu Wang},
    year={2019},
    eprint={1906.03741},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

## big_patent/all (default config)

*   **Config description**: Patents under all categories.
*   **Dataset size**: `24.22 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | --------:
'test'       | 67,072
'train'      | 1,207,222
'validation' | 67,068

## big_patent/a

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)a: Human Necessities
*   **Dataset size**: `3.45 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 9,675
'train'      | 174,134
'validation' | 9,674

## big_patent/b

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)b: Performing Operations; Transporting
*   **Dataset size**: `2.67 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 8,974
'train'      | 161,520
'validation' | 8,973

## big_patent/c

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)c: Chemistry; Metallurgy
*   **Dataset size**: `2.74 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 5,614
'train'      | 101,042
'validation' | 5,613

## big_patent/d

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)d: Textiles; Paper
*   **Dataset size**: `170.08 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes (test, validation), Only when `shuffle_files=False` (train)
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 565
'train'      | 10,164
'validation' | 565

## big_patent/e

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)e: Fixed Constructions
*   **Dataset size**: `568.03 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1,914
'train'      | 34,443
'validation' | 1,914

## big_patent/f

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)f: Mechanical Engineering; Lightning; Heating; Weapons; Blasting
*   **Dataset size**: `1.35 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 4,754
'train'      | 85,568
'validation' | 4,754

## big_patent/g

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)g: Physics
*   **Dataset size**: `5.78 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 14,386
'train'      | 258,935
'validation' | 14,385

## big_patent/h

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)h: Electricity
*   **Dataset size**: `5.17 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 14,279
'train'      | 257,019
'validation' | 14,279

## big_patent/y

*   **Config description**: Patents under Cooperative Patent Classification
    (CPC)y: General tagging of new or cross-sectional technology
*   **Dataset size**: `2.35 GiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 6,911
'train'      | 124,397
'validation' | 6,911
