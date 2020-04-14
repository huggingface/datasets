<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="cmaterdb" />
  <meta itemprop="description" content="This dataset contains images of -&#10;  Handwritten Bangla numerals - balanced dataset of total 6000 Bangla numerals (32x32 RGB coloured, 6000 images), each having 600 images per class(per digit). &#10;  Handwritten Devanagari numerals - balanced dataset of total 3000 Devanagari numerals (32x32 RGB coloured, 3000 images), each having 300 images per class(per digit). &#10;  Handwritten Telugu numerals - balanced dataset of total 3000 Telugu numerals (32x32 RGB coloured, 3000 images), each having 300 images per class(per digit). &#10;&#10;CMATERdb is the pattern recognition database repository created at the &#x27;Center for Microprocessor Applications for Training Education and Research&#x27; (CMATER) research lab, Jadavpur University, India.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;cmaterdb&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/cmaterdb" />
  <meta itemprop="sameAs" content="https://code.google.com/archive/p/cmaterdb/" />
  <meta itemprop="citation" content="@article{Das:2012:GAB:2161007.2161320,&#10;  author = {Das, Nibaran and Sarkar, Ram and Basu, Subhadip and Kundu, Mahantapas &#10;            and Nasipuri, Mita and Basu, Dipak Kumar},&#10;  title = {A Genetic Algorithm Based Region Sampling for Selection of Local Features &#10;          in Handwritten Digit Recognition Application},&#10;  journal = {Appl. Soft Comput.},&#10;  issue_date = {May, 2012},&#10;  volume = {12},&#10;  number = {5},&#10;  month = may,&#10;  year = {2012},&#10;  issn = {1568-4946},&#10;  pages = {1592--1606},&#10;  numpages = {15},&#10;  url = {http://dx.doi.org/10.1016/j.asoc.2011.11.030},&#10;  doi = {10.1016/j.asoc.2011.11.030},&#10;  acmid = {2161320},&#10;  publisher = {Elsevier Science Publishers B. V.},&#10;  address = {Amsterdam, The Netherlands, The Netherlands},&#10;  keywords = {Feature selection, Genetic algorithm, N-Quality consensus, &#10;  Optimal local regions, Region sampling, Variable sized local regions},&#10;}&#10;@article{Das:2012:SFC:2240301.2240421,&#10;  author = {Das, Nibaran and Reddy, Jagan Mohan and Sarkar, Ram and Basu, Subhadip and Kundu, &#10;            Mahantapas and Nasipuri, Mita and Basu, Dipak Kumar},&#10;  title = {A Statistical-topological Feature Combination for Recognition of Handwritten Numerals},&#10;  journal = {Appl. Soft Comput.},&#10;  issue_date = {August, 2012},&#10;  volume = {12},&#10;  number = {8},&#10;  month = aug,&#10;  year = {2012},&#10;  issn = {1568-4946},&#10;  pages = {2486--2495},&#10;  numpages = {10},&#10;  url = {http://dx.doi.org/10.1016/j.asoc.2012.03.039},&#10;  doi = {10.1016/j.asoc.2012.03.039},&#10;  acmid = {2240421},&#10;  publisher = {Elsevier Science Publishers B. V.},&#10;  address = {Amsterdam, The Netherlands, The Netherlands},&#10;  keywords = {Character recognition, Feature combination, MPCA, PCA, SVM, Statistical, Topological},&#10;}&#10;" />
</div>
# `cmaterdb`

*   **Description**:

This dataset contains images of - Handwritten Bangla numerals - balanced dataset
of total 6000 Bangla numerals (32x32 RGB coloured, 6000 images), each having 600
images per class(per digit). Handwritten Devanagari numerals - balanced dataset
of total 3000 Devanagari numerals (32x32 RGB coloured, 3000 images), each having
300 images per class(per digit). Handwritten Telugu numerals - balanced dataset
of total 3000 Telugu numerals (32x32 RGB coloured, 3000 images), each having 300
images per class(per digit).

CMATERdb is the pattern recognition database repository created at the 'Center
for Microprocessor Applications for Training Education and Research' (CMATER)
research lab, Jadavpur University, India.

*   **Homepage**:
    [https://code.google.com/archive/p/cmaterdb/](https://code.google.com/archive/p/cmaterdb/)
*   **Source code**:
    [`tfds.image.cmaterdb.Cmaterdb`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/cmaterdb.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(32, 32, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@article{Das:2012:GAB:2161007.2161320,
  author = {Das, Nibaran and Sarkar, Ram and Basu, Subhadip and Kundu, Mahantapas
            and Nasipuri, Mita and Basu, Dipak Kumar},
  title = {A Genetic Algorithm Based Region Sampling for Selection of Local Features
          in Handwritten Digit Recognition Application},
  journal = {Appl. Soft Comput.},
  issue_date = {May, 2012},
  volume = {12},
  number = {5},
  month = may,
  year = {2012},
  issn = {1568-4946},
  pages = {1592--1606},
  numpages = {15},
  url = {http://dx.doi.org/10.1016/j.asoc.2011.11.030},
  doi = {10.1016/j.asoc.2011.11.030},
  acmid = {2161320},
  publisher = {Elsevier Science Publishers B. V.},
  address = {Amsterdam, The Netherlands, The Netherlands},
  keywords = {Feature selection, Genetic algorithm, N-Quality consensus,
  Optimal local regions, Region sampling, Variable sized local regions},
}
@article{Das:2012:SFC:2240301.2240421,
  author = {Das, Nibaran and Reddy, Jagan Mohan and Sarkar, Ram and Basu, Subhadip and Kundu,
            Mahantapas and Nasipuri, Mita and Basu, Dipak Kumar},
  title = {A Statistical-topological Feature Combination for Recognition of Handwritten Numerals},
  journal = {Appl. Soft Comput.},
  issue_date = {August, 2012},
  volume = {12},
  number = {8},
  month = aug,
  year = {2012},
  issn = {1568-4946},
  pages = {2486--2495},
  numpages = {10},
  url = {http://dx.doi.org/10.1016/j.asoc.2012.03.039},
  doi = {10.1016/j.asoc.2012.03.039},
  acmid = {2240421},
  publisher = {Elsevier Science Publishers B. V.},
  address = {Amsterdam, The Netherlands, The Netherlands},
  keywords = {Character recognition, Feature combination, MPCA, PCA, SVM, Statistical, Topological},
}
```

## cmaterdb/bangla (default config)

*   **Config description**: CMATERdb Bangla Numerals
*   **Download size**: `573.81 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,000
'train' | 5,000

## cmaterdb/devanagari

*   **Config description**: CMATERdb Devangari Numerals
*   **Download size**: `275.29 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 500
'train' | 2,500

## cmaterdb/telugu

*   **Config description**: CMATERdb Telugu Numerals
*   **Download size**: `283.90 KiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 500
'train' | 2,500
