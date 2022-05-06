---
pretty_name: Mathematics Dataset
languages:
- en
paperswithcode_id: mathematics
---

# Dataset Card for "math_dataset"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [https://github.com/deepmind/mathematics_dataset](https://github.com/deepmind/mathematics_dataset)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 124600.07 MB
- **Size of the generated dataset:** 8656.79 MB
- **Total amount of disk used:** 133256.87 MB

### Dataset Summary

Mathematics database.

This dataset code generates mathematical question and answer pairs,
from a range of question types at roughly school-level difficulty.
This is designed to test the mathematical learning and algebraic
reasoning skills of learning models.

Original paper: Analysing Mathematical Reasoning Abilities of Neural Models
(Saxton, Grefenstette, Hill, Kohli).

Example usage:
train_examples, val_examples = datasets.load_dataset(
    'math_dataset/arithmetic__mul',
    split=['train', 'test'],
    as_supervised=True)

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### algebra__linear_1d

- **Size of downloaded dataset files:** 2225.00 MB
- **Size of the generated dataset:** 88.31 MB
- **Total amount of disk used:** 2313.31 MB

An example of 'train' looks as follows.
```

```

#### algebra__linear_1d_composed

- **Size of downloaded dataset files:** 2225.00 MB
- **Size of the generated dataset:** 191.29 MB
- **Total amount of disk used:** 2416.29 MB

An example of 'train' looks as follows.
```

```

#### algebra__linear_2d

- **Size of downloaded dataset files:** 2225.00 MB
- **Size of the generated dataset:** 121.51 MB
- **Total amount of disk used:** 2346.51 MB

An example of 'train' looks as follows.
```

```

#### algebra__linear_2d_composed

- **Size of downloaded dataset files:** 2225.00 MB
- **Size of the generated dataset:** 224.68 MB
- **Total amount of disk used:** 2449.68 MB

An example of 'train' looks as follows.
```

```

#### algebra__polynomial_roots

- **Size of downloaded dataset files:** 2225.00 MB
- **Size of the generated dataset:** 156.41 MB
- **Total amount of disk used:** 2381.41 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### algebra__linear_1d
- `question`: a `string` feature.
- `answer`: a `string` feature.

#### algebra__linear_1d_composed
- `question`: a `string` feature.
- `answer`: a `string` feature.

#### algebra__linear_2d
- `question`: a `string` feature.
- `answer`: a `string` feature.

#### algebra__linear_2d_composed
- `question`: a `string` feature.
- `answer`: a `string` feature.

#### algebra__polynomial_roots
- `question`: a `string` feature.
- `answer`: a `string` feature.

### Data Splits

|           name            | train |test |
|---------------------------|------:|----:|
|algebra__linear_1d         |1999998|10000|
|algebra__linear_1d_composed|1999998|10000|
|algebra__linear_2d         |1999998|10000|
|algebra__linear_2d_composed|1999998|10000|
|algebra__polynomial_roots  |1999998|10000|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```

@article{2019arXiv,
  author = {Saxton, Grefenstette, Hill, Kohli},
  title = {Analysing Mathematical Reasoning Abilities of Neural Models},
  year = {2019},
  journal = {arXiv:1904.01557}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.