<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="flores" />
  <meta itemprop="description" content="Evaluation datasets for low-resource machine translation: Nepali-English and Sinhala-English.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;flores&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/flores" />
  <meta itemprop="sameAs" content="https://github.com/facebookresearch/flores/" />
  <meta itemprop="citation" content="@misc{guzmn2019new,&#10;    title={Two New Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English},&#10;    author={Francisco Guzman and Peng-Jen Chen and Myle Ott and Juan Pino and Guillaume Lample and Philipp Koehn and Vishrav Chaudhary and Marc&#x27;Aurelio Ranzato},&#10;    year={2019},&#10;    eprint={1902.01382},&#10;    archivePrefix={arXiv},&#10;    primaryClass={cs.CL}&#10;}&#10;" />
</div>
# `flores`

*   **Description**:

Evaluation datasets for low-resource machine translation: Nepali-English and
Sinhala-English.

*   **Homepage**:
    [https://github.com/facebookresearch/flores/](https://github.com/facebookresearch/flores/)
*   **Source code**:
    [`tfds.translate.flores.Flores`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/translate/flores.py)
*   **Versions**:
    *   **`1.1.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `1.47 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
*   **Citation**:

```
@misc{guzmn2019new,
    title={Two New Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English},
    author={Francisco Guzman and Peng-Jen Chen and Myle Ott and Juan Pino and Guillaume Lample and Philipp Koehn and Vishrav Chaudhary and Marc'Aurelio Ranzato},
    year={2019},
    eprint={1902.01382},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

## flores/neen_plain_text (default config)

*   **Config description**: Translation dataset from ne to en, uses encoder
    plain_text.
*   **Dataset size**: `1.89 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 2,835
'validation' | 2,559

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'ne': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('ne', 'en')`

## flores/sien_plain_text

*   **Config description**: Translation dataset from si to en, uses encoder
    plain_text.
*   **Dataset size**: `2.05 MiB`
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 2,766
'validation' | 2,898

*   **Features**:

```python
Translation({
    'en': Text(shape=(), dtype=tf.string),
    'si': Text(shape=(), dtype=tf.string),
})
```

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('si', 'en')`
