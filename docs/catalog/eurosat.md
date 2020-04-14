<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="eurosat" />
  <meta itemprop="description" content="EuroSAT dataset is based on Sentinel-2 satellite images covering 13 spectral&#10;bands and consisting of 10 classes with 27000 labeled and&#10;geo-referenced samples.&#10;&#10;Two datasets are offered:&#10;- rgb: Contains only the optical R, G, B frequency bands encoded as JPEG image.&#10;- all: Contains all 13 bands in the original value range (float32).&#10;&#10;URL: https://github.com/phelber/eurosat&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;eurosat&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/eurosat" />
  <meta itemprop="sameAs" content="https://github.com/phelber/eurosat" />
  <meta itemprop="citation" content="&#10;@misc{helber2017eurosat,&#10;    title={EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification},&#10;    author={Patrick Helber and Benjamin Bischke and Andreas Dengel and Damian Borth},&#10;    year={2017},&#10;    eprint={1709.00029},&#10;    archivePrefix={arXiv},&#10;    primaryClass={cs.CV}&#10;}&#10;" />
</div>
# `eurosat`

*   **Description**:

EuroSAT dataset is based on Sentinel-2 satellite images covering 13 spectral
bands and consisting of 10 classes with 27000 labeled and geo-referenced
samples.

Two datasets are offered: - rgb: Contains only the optical R, G, B frequency
bands encoded as JPEG image. - all: Contains all 13 bands in the original value
range (float32).

URL: https://github.com/phelber/eurosat

*   **Homepage**:
    [https://github.com/phelber/eurosat](https://github.com/phelber/eurosat)
*   **Source code**:
    [`tfds.image.eurosat.Eurosat`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/eurosat.py)
*   **Versions**:
    *   **`2.0.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 27,000

*   **Citation**:

```
@misc{helber2017eurosat,
    title={EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification},
    author={Patrick Helber and Benjamin Bischke and Andreas Dengel and Damian Borth},
    year={2017},
    eprint={1709.00029},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```

## eurosat/rgb (default config)

*   **Config description**: Sentinel-2 RGB channels
*   **Download size**: `89.91 MiB`
*   **Features**:

```python
FeaturesDict({
    'filename': Text(shape=(), dtype=tf.string),
    'image': Image(shape=(64, 64, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`

## eurosat/all

*   **Config description**: 13 Sentinel-2 channels
*   **Download size**: `1.93 GiB`
*   **Features**:

```python
FeaturesDict({
    'filename': Text(shape=(), dtype=tf.string),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
    'sentinel2': Tensor(shape=(64, 64, 13), dtype=tf.float32),
})
```

*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('sentinel2', 'label')`
