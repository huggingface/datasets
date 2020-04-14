<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="kmnist" />
  <meta itemprop="description" content="Kuzushiji-MNIST is a drop-in replacement for the MNIST dataset (28x28 grayscale, 70,000 images), provided in the original MNIST format as well as a NumPy format. Since MNIST restricts us to 10 classes, we chose one character to represent each of the 10 rows of Hiragana when creating Kuzushiji-MNIST.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;kmnist&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/kmnist" />
  <meta itemprop="sameAs" content="http://codh.rois.ac.jp/kmnist/index.html.en" />
  <meta itemprop="citation" content="@online{clanuwat2018deep,&#10;  author       = {Tarin Clanuwat and Mikel Bober-Irizar and Asanobu Kitamoto and Alex Lamb and Kazuaki Yamamoto and David Ha},&#10;  title        = {Deep Learning for Classical Japanese Literature},&#10;  date         = {2018-12-03},&#10;  year         = {2018},&#10;  eprintclass  = {cs.CV},&#10;  eprinttype   = {arXiv},&#10;  eprint       = {cs.CV/1812.01718},&#10;}&#10;" />
</div>
# `kmnist`

*   **Description**:

Kuzushiji-MNIST is a drop-in replacement for the MNIST dataset (28x28 grayscale,
70,000 images), provided in the original MNIST format as well as a NumPy format.
Since MNIST restricts us to 10 classes, we chose one character to represent each
of the 10 rows of Hiragana when creating Kuzushiji-MNIST.

*   **Homepage**:
    [http://codh.rois.ac.jp/kmnist/index.html.en](http://codh.rois.ac.jp/kmnist/index.html.en)
*   **Source code**:
    [`tfds.image.mnist.KMNIST`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/mnist.py)
*   **Versions**:
    *   **`3.0.1`** (default): No release notes.
*   **Download size**: `20.26 MiB`
*   **Dataset size**: `31.76 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 10,000
'train' | 60,000

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@online{clanuwat2018deep,
  author       = {Tarin Clanuwat and Mikel Bober-Irizar and Asanobu Kitamoto and Alex Lamb and Kazuaki Yamamoto and David Ha},
  title        = {Deep Learning for Classical Japanese Literature},
  date         = {2018-12-03},
  year         = {2018},
  eprintclass  = {cs.CV},
  eprinttype   = {arXiv},
  eprint       = {cs.CV/1812.01718},
}
```
