<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>

  <meta itemprop="name" content="abstract_reasoning" />
  <meta itemprop="description" content="Procedurally Generated Matrices (PGM) data from the paper Measuring Abstract Reasoning in Neural Networks, Barrett, Hill, Santoro et al. 2018. The goal is to infer the correct answer from the context panels based on abstract reasoning.&#10;&#10;To use this data set, please download all the *.tar.gz files from the data set page and place them in ~/tensorflow_datasets/abstract_reasoning/.&#10;&#10;$R$ denotes the set of relation types (progression, XOR, OR, AND, consistent union), $O$ denotes the object types (shape, line), and $A$ denotes the attribute types (size, colour, position, number). The structure of a matrix, $S$, is the set of triples $S={[r, o, a]}$ that determine the challenge posed by a particular matrix.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;abstract_reasoning&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/abstract_reasoning" />
  <meta itemprop="sameAs" content="https://github.com/deepmind/abstract-reasoning-matrices" />
  <meta itemprop="citation" content="@InProceedings{pmlr-v80-barrett18a,&#10;  title =   {Measuring abstract reasoning in neural networks},&#10;  author =   {Barrett, David and Hill, Felix and Santoro, Adam and Morcos, Ari and Lillicrap, Timothy},&#10;  booktitle =    {Proceedings of the 35th International Conference on Machine Learning},&#10;  pages =   {511--520},&#10;  year =    {2018},&#10;  editor =      {Dy, Jennifer and Krause, Andreas},&#10;  volume =      {80},&#10;  series =    {Proceedings of Machine Learning Research},&#10;  address =     {Stockholmsmassan, Stockholm Sweden},&#10;  month =     {10--15 Jul},&#10;  publisher =     {PMLR},&#10;  pdf =     {http://proceedings.mlr.press/v80/barrett18a/barrett18a.pdf},&#10;  url =   {http://proceedings.mlr.press/v80/barrett18a.html},&#10;  abstract =    {Whether neural networks can learn abstract reasoning or whetherthey merely rely on superficial statistics is a topic of recent debate. Here, we propose a dataset and challenge designed to probe abstract reasoning, inspired by a well-known human IQ test. To succeed at this challenge, models must cope with various generalisation &#x27;regimes&#x27; in which the training data and test questions differ in clearly-defined ways. We show that popular models such as ResNets perform poorly, even when the training and test sets differ only minimally, and we present a novel architecture, with structure designed to encourage reasoning, that does significantly better. When we vary the way in which the test questions and training data differ, we find that our model is notably proficient at certain forms of generalisation, but notably weak at others. We further show that the model&#x27;s ability to generalise improves markedly if it is trained to predict symbolic explanations for its answers. Altogether, we introduce and explore ways to both measure and induce stronger abstract reasoning in neural networks. Our freely-available dataset should motivate further progress in this direction.}&#10;}&#10;" />
</div>

# `abstract_reasoning`

Warning: Manual download required. See instructions below.

*   **Description**:

Procedurally Generated Matrices (PGM) data from the paper Measuring Abstract
Reasoning in Neural Networks, Barrett, Hill, Santoro et al. 2018. The goal is to
infer the correct answer from the context panels based on abstract reasoning.

To use this data set, please download all the *.tar.gz files from the data set
page and place them in ~/tensorflow_datasets/abstract_reasoning/.

$R$ denotes the set of relation types (progression, XOR, OR, AND, consistent
union), $O$ denotes the object types (shape, line), and $A$ denotes the
attribute types (size, colour, position, number). The structure of a matrix,
$S$, is the set of triples $S={[r, o, a]}$ that determine the challenge posed by
a particular matrix.

*   **Homepage**:
    [https://github.com/deepmind/abstract-reasoning-matrices](https://github.com/deepmind/abstract-reasoning-matrices)
*   **Source code**:
    [`tfds.image.abstract_reasoning.AbstractReasoning`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/image/abstract_reasoning.py)
*   **Versions**:
    *   **`1.0.0`** (default): New split API
        (https://tensorflow.org/datasets/splits)
*   **Download size**: `Unknown size`
*   **Dataset size**: `Unknown size`
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/abstract_reasoning/`):<br/>
    Data can be downloaded from
    https://console.cloud.google.com/storage/browser/ravens-matrices
    Please put all the tar.gz files in manual_dir.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Splits**:

Split        | Examples
:----------- | --------:
'test'       | 200,000
'train'      | 1,200,000
'validation' | 20,000

*   **Features**:

```python
FeaturesDict({
    'answers': Video(Image(shape=(160, 160, 1), dtype=tf.uint8)),
    'context': Video(Image(shape=(160, 160, 1), dtype=tf.uint8)),
    'filename': Text(shape=(), dtype=tf.string),
    'meta_target': Tensor(shape=(12,), dtype=tf.int64),
    'relation_structure_encoded': Tensor(shape=(4, 12), dtype=tf.int64),
    'target': ClassLabel(shape=(), dtype=tf.int64, num_classes=8),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@InProceedings{pmlr-v80-barrett18a,
  title =    {Measuring abstract reasoning in neural networks},
  author =   {Barrett, David and Hill, Felix and Santoro, Adam and Morcos, Ari and Lillicrap, Timothy},
  booktitle =    {Proceedings of the 35th International Conference on Machine Learning},
  pages =    {511--520},
  year =     {2018},
  editor =   {Dy, Jennifer and Krause, Andreas},
  volume =   {80},
  series =   {Proceedings of Machine Learning Research},
  address =      {Stockholmsmassan, Stockholm Sweden},
  month =    {10--15 Jul},
  publisher =    {PMLR},
  pdf =      {http://proceedings.mlr.press/v80/barrett18a/barrett18a.pdf},
  url =      {http://proceedings.mlr.press/v80/barrett18a.html},
  abstract =     {Whether neural networks can learn abstract reasoning or whetherthey merely rely on superficial statistics is a topic of recent debate. Here, we propose a dataset and challenge designed to probe abstract reasoning, inspired by a well-known human IQ test. To succeed at this challenge, models must cope with various generalisation 'regimes' in which the training data and test questions differ in clearly-defined ways. We show that popular models such as ResNets perform poorly, even when the training and test sets differ only minimally, and we present a novel architecture, with structure designed to encourage reasoning, that does significantly better. When we vary the way in which the test questions and training data differ, we find that our model is notably proficient at certain forms of generalisation, but notably weak at others. We further show that the model's ability to generalise improves markedly if it is trained to predict symbolic explanations for its answers. Altogether, we introduce and explore ways to both measure and induce stronger abstract reasoning in neural networks. Our freely-available dataset should motivate further progress in this direction.}
}
```

## abstract_reasoning/neutral (default config)

*   **Config description**: The structures encoding the matrices in both the \
    training and testing sets contain any triples $[r, o, a]$ for $r \\in R$, \
    $o \\in O$, and $a \\in A$. Training and testing sets are disjoint, with \
    separation occurring at the level of the input variables (i.e. pixel \
    manifestations).

## abstract_reasoning/interpolation

*   **Config description**: As in the neutral split, $S$ consisted of any \
    triples $[r, o, a]$. For interpolation, in the training set, when the \
    attribute was "colour" or "size" (i.e., the ordered attributes), the values
    of \
    the attributes were restricted to even-indexed members of a discrete set, \
    whereas in the test set only odd-indexed values were permitted. Note that
    all \
    $S$ contained some triple $[r, o, a]$ with the colour or size attribute . \
    Thus, generalisation is required for every question in the test set.

## abstract_reasoning/extrapolation

*   **Config description**: Same as in interpolation, but the values of \
    the attributes were restricted to the lower half of the discrete set during
    \
    training, whereas in the test set they took values in the upper half.

## abstract_reasoning/attr.rel.pairs

*   **Config description**: All $S$ contained at least two triples, \
    $([r_1,o_1,a_1],[r_2,o_2,a_2]) = (t_1, t_2)$, of which 400 are viable. We \
    randomly allocated 360 to the training set and 40 to the test set. Members \
    $(t_1, t_2)$ of the 40 held-out pairs did not occur together in structures
    $S$ \
    in the training set, and all structures $S$ had at least one such pair \
    $(t_1, t_2)$ as a subset.

## abstract_reasoning/attr.rels

*   **Config description**: In our dataset, there are 29 possible unique \
    triples $[r,o,a]$. We allocated seven of these for the test set, at random,
    \
    but such that each of the attributes was represented exactly once in this
    set. \
    These held-out triples never occurred in questions in the training set, and
    \
    every $S$ in the test set contained at least one of them.

## abstract_reasoning/attrs.pairs

*   **Config description**: $S$ contained at least two triples. There are 20 \
    (unordered) viable pairs of attributes $(a_1, a_2)$ such that for some \
    $r_i, o_i, ([r_1,o_1,a_1],[r_2,o_2,a_2])$ is a viable triple pair \
    $([r_1,o_1,a_1],[r_2,o_2,a_2]) = (t_1, t_2)$. We allocated 16 of these pairs
    \
    for training and four for testing. For a pair $(a_1, a_2)$ in the test set,
    \
    $S$ in the training set contained triples with $a_1$ or $a_2$. In the test \
    set, all $S$ contained triples with $a_1$ and $a_2$.

## abstract_reasoning/attrs.shape.color

*   **Config description**: Held-out attribute shape-colour. $S$ in \
    the training set contained no triples with $o$=shape and $a$=colour. \
    All structures governing puzzles in the test set contained at least one
    triple \
    with $o$=shape and $a$=colour.

## abstract_reasoning/attrs.line.type

*   **Config description**: Held-out attribute line-type. $S$ in \
    the training set contained no triples with $o$=line and $a$=type. \
    All structures governing puzzles in the test set contained at least one
    triple \
    with $o$=line and $a$=type.
