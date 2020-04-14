<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="scan" />
  <meta itemprop="description" content="SCAN tasks with various splits.&#10;&#10;SCAN is a set of simple language-driven navigation tasks for studying&#10;compositional learning and zero-shot generalization.&#10;&#10;See https://github.com/brendenlake/SCAN for a description of the splits.&#10;&#10;Example usage:&#10;data = tfds.load(&#x27;scan/length&#x27;)&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;scan&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/scan" />
  <meta itemprop="sameAs" content="https://github.com/brendenlake/SCAN" />
  <meta itemprop="citation" content="&#10;@inproceedings{Lake2018GeneralizationWS,&#10;  title={Generalization without Systematicity: On the Compositional Skills of&#10;         Sequence-to-Sequence Recurrent Networks},&#10;  author={Brenden M. Lake and Marco Baroni},&#10;  booktitle={ICML},&#10;  year={2018},&#10;  url={https://arxiv.org/pdf/1711.00350.pdf},&#10;}&#10;" />
</div>
# `scan`

*   **Description**:

SCAN tasks with various splits.

SCAN is a set of simple language-driven navigation tasks for studying
compositional learning and zero-shot generalization.

See https://github.com/brendenlake/SCAN for a description of the splits.

Example usage: data = tfds.load('scan/length')

*   **Config description**: SCAN tasks with various splits.

SCAN is a set of simple language-driven navigation tasks for studying
compositional learning and zero-shot generalization.

See https://github.com/brendenlake/SCAN for a description of the splits.

Example usage: data = tfds.load('scan/length') * **Homepage**:
[https://github.com/brendenlake/SCAN](https://github.com/brendenlake/SCAN) *
**Source code**:
[`tfds.text.scan.Scan`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/scan.py)
* **Versions**: * **`1.0.0`** (default): No release notes. * **Download size**:
`17.82 MiB` * **Dataset size**: `Unknown size` * **Auto-cached**
([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
No * **Features**:

```python
FeaturesDict({
    'actions': Text(shape=(), dtype=tf.string),
    'commands': Text(shape=(), dtype=tf.string),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('commands', 'actions')`
*   **Citation**:

```
@inproceedings{Lake2018GeneralizationWS,
  title={Generalization without Systematicity: On the Compositional Skills of
         Sequence-to-Sequence Recurrent Networks},
  author={Brenden M. Lake and Marco Baroni},
  booktitle={ICML},
  year={2018},
  url={https://arxiv.org/pdf/1711.00350.pdf},
}
```

## scan/simple (default config)

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 4,182
'train' | 16,728

## scan/addprim_jump

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 7,706
'train' | 14,670

## scan/addprim_turn_left

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,208
'train' | 21,890

## scan/filler_num0

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,173
'train' | 15,225

## scan/filler_num1

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,173
'train' | 16,290

## scan/filler_num2

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,173
'train' | 17,391

## scan/filler_num3

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,173
'train' | 18,528

## scan/length

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 3,920
'train' | 16,990

## scan/template_around_right

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 4,476
'train' | 15,225

## scan/template_jump_around_right

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 1,173
'train' | 18,528

## scan/template_opposite_right

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 4,476
'train' | 15,225

## scan/template_right

*   **Splits**:

Split   | Examples
:------ | -------:
'test'  | 4,476
'train' | 15,225
