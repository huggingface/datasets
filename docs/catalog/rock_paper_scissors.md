<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="rock_paper_scissors" />
  <meta itemprop="description" content="Images of hands playing rock, paper, scissor game.&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;rock_paper_scissors&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/rock_paper_scissors" />
  <meta itemprop="sameAs" content="http://laurencemoroney.com/rock-paper-scissors-dataset" />
  <meta itemprop="citation" content="@ONLINE {rps,&#10;author = &quot;Laurence Moroney&quot;,&#10;title = &quot;Rock, Paper, Scissors Dataset&quot;,&#10;month = &quot;feb&quot;,&#10;year = &quot;2019&quot;,&#10;url = &quot;http://laurencemoroney.com/rock-paper-scissors-dataset&quot;&#10;}&#10;" />
</div>
# `rock_paper_scissors`

*   **Description**:

Images of hands playing rock, paper, scissor game.

*   **Homepage**:
    [http://laurencemoroney.com/rock-paper-scissors-dataset](http://laurencemoroney.com/rock-paper-scissors-dataset)
*   **Source code**:
    [`tfds.image.rock_paper_scissors.RockPaperScissors`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/rock_paper_scissors.py)
*   **Versions**:
    *   **`3.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `219.53 MiB`
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 372
'train' | 2,520

*   **Features**:

```python
FeaturesDict({
    'image': Image(shape=(300, 300, 3), dtype=tf.uint8),
    'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=3),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('image', 'label')`
*   **Citation**:

```
@ONLINE {rps,
author = "Laurence Moroney",
title = "Rock, Paper, Scissors Dataset",
month = "feb",
year = "2019",
url = "http://laurencemoroney.com/rock-paper-scissors-dataset"
}
```
