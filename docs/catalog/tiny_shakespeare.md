<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="tiny_shakespeare" />
  <meta itemprop="description" content="40,000 lines of Shakespeare from a variety of Shakespeare&#x27;s plays. Featured in Andrej Karpathy&#x27;s blog post &#x27;The Unreasonable Effectiveness of Recurrent Neural Networks&#x27;: http://karpathy.github.io/2015/05/21/rnn-effectiveness/.&#10;&#10;To use for e.g. character modelling:&#10;&#10;```&#10;d = tfds.load(name=&#x27;tiny_shakespeare&#x27;)[&#x27;train&#x27;]&#10;d = d.map(lambda x: tf.strings.unicode_split(x[&#x27;text&#x27;], &#x27;UTF-8&#x27;))&#10;# train split includes vocabulary for other splits&#10;vocabulary = sorted(set(next(iter(d)).numpy()))&#10;d = d.map(lambda x: {&#x27;cur_char&#x27;: x[:-1], &#x27;next_char&#x27;: x[1:]})&#10;d = d.unbatch()&#10;seq_len = 100&#10;batch_size = 2&#10;d = d.batch(seq_len)&#10;d = d.batch(batch_size)&#10;```&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;tiny_shakespeare&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/tiny_shakespeare" />
  <meta itemprop="sameAs" content="https://github.com/karpathy/char-rnn/blob/master/data/tinyshakespeare/input.txt" />
  <meta itemprop="citation" content="@misc{&#10;  author={Karpathy, Andrej},&#10;  title={char-rnn},&#10;  year={2015},&#10;  howpublished={\url{https://github.com/karpathy/char-rnn}}&#10;}" />
</div>
# `tiny_shakespeare`

*   **Description**:

40,000 lines of Shakespeare from a variety of Shakespeare's plays. Featured in
Andrej Karpathy's blog post 'The Unreasonable Effectiveness of Recurrent Neural
Networks': http://karpathy.github.io/2015/05/21/rnn-effectiveness/.

To use for e.g. character modelling:

```
d = tfds.load(name='tiny_shakespeare')['train']
d = d.map(lambda x: tf.strings.unicode_split(x['text'], 'UTF-8'))
# train split includes vocabulary for other splits
vocabulary = sorted(set(next(iter(d)).numpy()))
d = d.map(lambda x: {'cur_char': x[:-1], 'next_char': x[1:]})
d = d.unbatch()
seq_len = 100
batch_size = 2
d = d.batch(seq_len)
d = d.batch(batch_size)
```

*   **Homepage**:
    [https://github.com/karpathy/char-rnn/blob/master/data/tinyshakespeare/input.txt](https://github.com/karpathy/char-rnn/blob/master/data/tinyshakespeare/input.txt)
*   **Source code**:
    [`tfds.text.tiny_shakespeare.TinyShakespeare`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/tiny_shakespeare.py)
*   **Versions**:
    *   **`1.0.0`** (default): No release notes.
*   **Download size**: `Unknown size`
*   **Dataset size**: `1.06 MiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
*   **Splits**:

Split        | Examples
:----------- | -------:
'test'       | 1
'train'      | 1
'validation' | 1

*   **Features**:

```python
FeaturesDict({
    'text': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@misc{
  author={Karpathy, Andrej},
  title={char-rnn},
  year={2015},
  howpublished={\url{https://github.com/karpathy/char-rnn}}
}
```
