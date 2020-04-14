<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="diabetic_retinopathy_detection" />
  <meta itemprop="description" content="A large set of high-resolution retina images taken under a variety of imaging conditions.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;diabetic_retinopathy_detection&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/diabetic_retinopathy_detection" />
  <meta itemprop="sameAs" content="https://www.kaggle.com/c/diabetic-retinopathy-detection/data" />
  <meta itemprop="citation" content="@ONLINE {kaggle-diabetic-retinopathy,&#10;    author = &quot;Kaggle and EyePacs&quot;,&#10;    title  = &quot;Kaggle Diabetic Retinopathy Detection&quot;,&#10;    month  = &quot;jul&quot;,&#10;    year   = &quot;2015&quot;,&#10;    url    = &quot;https://www.kaggle.com/c/diabetic-retinopathy-detection/data&quot;&#10;}&#10;" />
</div>
# `diabetic_retinopathy_detection`

Warning: Manual download required. See instructions below.

*   **Description**:

A large set of high-resolution retina images taken under a variety of imaging
conditions.

*   **Homepage**:
    [https://www.kaggle.com/c/diabetic-retinopathy-detection/data](https://www.kaggle.com/c/diabetic-retinopathy-detection/data)
*   **Source code**:
    [`tfds.image.diabetic_retinopathy_detection.DiabeticRetinopathyDetection`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/diabetic_retinopathy_detection.py)
*   **Versions**:
    *   **`3.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `1.13 MiB`
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/diabetic_retinopathy_detection/`):<br/>
    You have to download this dataset from Kaggle.
    https://www.kaggle.com/c/diabetic-retinopathy-detection/data
    After downloading, unpack the test.zip file into test/ directory in manual_dir
    and sample.zip to sample/. Also unpack the sampleSubmissions.csv and
    trainLabels.csv.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | -------:
'sample'     | 10
'test'       | 42,670
'train'      | 35,126
'validation' | 10,906

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(None, None, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=5),
    'name': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@ONLINE {kaggle-diabetic-retinopathy,
    author = "Kaggle and EyePacs",
    title  = "Kaggle Diabetic Retinopathy Detection",
    month  = "jul",
    year   = "2015",
    url    = "https://www.kaggle.com/c/diabetic-retinopathy-detection/data"
}
```

## diabetic_retinopathy_detection/original (default config)

*   **Config description**: Images at their original resolution and quality.

## diabetic_retinopathy_detection/1M

*   **Config description**: Images have roughly 1,000,000 pixels, at 72 quality.

## diabetic_retinopathy_detection/250K

*   **Config description**: Images have roughly 250,000 pixels, at 72 quality.

## diabetic_retinopathy_detection/btgraham-300

*   **Config description**: Images have been preprocessed as the winner of the
    Kaggle competition did in 2015: first they are resized so that the radius of
    an eyeball is 300 pixels, then they are cropped to 90% of the radius, and
    finally they are encoded with 72 JPEG quality.
