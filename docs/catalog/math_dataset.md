<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="math_dataset" />
  <meta itemprop="description" content="&#10;Mathematics database.&#10;&#10;This dataset code generates mathematical question and answer pairs,&#10;from a range of question types at roughly school-level difficulty.&#10;This is designed to test the mathematical learning and algebraic&#10;reasoning skills of learning models.&#10;&#10;Original paper: Analysing Mathematical Reasoning Abilities of Neural Models&#10;(Saxton, Grefenstette, Hill, Kohli).&#10;&#10;Example usage:&#10;train_examples, val_examples = tfds.load(&#10;    &#x27;math_dataset/arithmetic__mul&#x27;,&#10;    split=[&#x27;train&#x27;, &#x27;test&#x27;],&#10;    as_supervised=True)&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;math_dataset&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/math_dataset" />
  <meta itemprop="sameAs" content="https://github.com/deepmind/mathematics_dataset" />
  <meta itemprop="citation" content="&#10;@article{2019arXiv,&#10;  author = {Saxton, Grefenstette, Hill, Kohli},&#10;  title = {Analysing Mathematical Reasoning Abilities of Neural Models},&#10;  year = {2019},&#10;  journal = {arXiv:1904.01557}&#10;}&#10;" />
</div>
# `math_dataset`

*   **Description**:

Mathematics database.

This dataset code generates mathematical question and answer pairs, from a range
of question types at roughly school-level difficulty. This is designed to test
the mathematical learning and algebraic reasoning skills of learning models.

Original paper: Analysing Mathematical Reasoning Abilities of Neural Models
(Saxton, Grefenstette, Hill, Kohli).

Example usage: train_examples, val_examples = tfds.load(
'math_dataset/arithmetic__mul', split=['train', 'test'], as_supervised=True)

*   **Config description**: Mathematics database.

This dataset code generates mathematical question and answer pairs, from a range
of question types at roughly school-level difficulty. This is designed to test
the mathematical learning and algebraic reasoning skills of learning models.

Original paper: Analysing Mathematical Reasoning Abilities of Neural Models
(Saxton, Grefenstette, Hill, Kohli).

Example usage: train_examples, val_examples = tfds.load(
'math_dataset/arithmetic__mul', split=['train', 'test'], as_supervised=True) *
**Homepage**:
[https://github.com/deepmind/mathematics_dataset](https://github.com/deepmind/mathematics_dataset)
* **Source code**:
[`tfds.text.math_dataset.MathDataset`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/math_dataset.py)
* **Versions**: * **`1.0.0`** (default): No release notes. * **Download size**:
`2.17 GiB` * **Dataset size**: `Unknown size` * **Auto-cached**
([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
No * **Splits**:

Split   | Examples
:------ | --------:
'test'  | 10,000
'train' | 1,999,998

*   **Features**:

```python
FeaturesDict({
    'answer': Text(shape=(), dtype=tf.string),
    'question': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('question', 'answer')`
*   **Citation**:

```
@article{2019arXiv,
  author = {Saxton, Grefenstette, Hill, Kohli},
  title = {Analysing Mathematical Reasoning Abilities of Neural Models},
  year = {2019},
  journal = {arXiv:1904.01557}
}
```

## math_dataset/algebra__linear_1d (default config)

## math_dataset/algebra__linear_1d_composed

## math_dataset/algebra__linear_2d

## math_dataset/algebra__linear_2d_composed

## math_dataset/algebra__polynomial_roots

## math_dataset/algebra__polynomial_roots_composed

## math_dataset/algebra__sequence_next_term

## math_dataset/algebra__sequence_nth_term

## math_dataset/arithmetic__add_or_sub

## math_dataset/arithmetic__add_or_sub_in_base

## math_dataset/arithmetic__add_sub_multiple

## math_dataset/arithmetic__div

## math_dataset/arithmetic__mixed

## math_dataset/arithmetic__mul

## math_dataset/arithmetic__mul_div_multiple

## math_dataset/arithmetic__nearest_integer_root

## math_dataset/arithmetic__simplify_surd

## math_dataset/calculus__differentiate

## math_dataset/calculus__differentiate_composed

## math_dataset/comparison__closest

## math_dataset/comparison__closest_composed

## math_dataset/comparison__kth_biggest

## math_dataset/comparison__kth_biggest_composed

## math_dataset/comparison__pair

## math_dataset/comparison__pair_composed

## math_dataset/comparison__sort

## math_dataset/comparison__sort_composed

## math_dataset/measurement__conversion

## math_dataset/measurement__time

## math_dataset/numbers__base_conversion

## math_dataset/numbers__div_remainder

## math_dataset/numbers__div_remainder_composed

## math_dataset/numbers__gcd

## math_dataset/numbers__gcd_composed

## math_dataset/numbers__is_factor

## math_dataset/numbers__is_factor_composed

## math_dataset/numbers__is_prime

## math_dataset/numbers__is_prime_composed

## math_dataset/numbers__lcm

## math_dataset/numbers__lcm_composed

## math_dataset/numbers__list_prime_factors

## math_dataset/numbers__list_prime_factors_composed

## math_dataset/numbers__place_value

## math_dataset/numbers__place_value_composed

## math_dataset/numbers__round_number

## math_dataset/numbers__round_number_composed

## math_dataset/polynomials__add

## math_dataset/polynomials__coefficient_named

## math_dataset/polynomials__collect

## math_dataset/polynomials__compose

## math_dataset/polynomials__evaluate

## math_dataset/polynomials__evaluate_composed

## math_dataset/polynomials__expand

## math_dataset/polynomials__simplify_power

## math_dataset/probability__swr_p_level_set

## math_dataset/probability__swr_p_sequence
