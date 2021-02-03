---
---

# Dataset Card for "cfq"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://github.com/google-research/google-research/tree/master/cfq](https://github.com/google-research/google-research/tree/master/cfq)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 2041.62 MB
- **Size of the generated dataset:** 345.30 MB
- **Total amount of disk used:** 2386.92 MB

### [Dataset Summary](#dataset-summary)

The CFQ dataset (and it's splits) for measuring compositional generalization.

See https://arxiv.org/abs/1912.09713.pdf for background.

Example usage:
data = datasets.load_dataset('cfq/mcd1')

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### mcd1

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 40.91 MB
- **Total amount of disk used:** 296.11 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

#### mcd2

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 42.70 MB
- **Total amount of disk used:** 297.91 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

#### mcd3

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 41.58 MB
- **Total amount of disk used:** 296.78 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

#### query_complexity_split

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 43.82 MB
- **Total amount of disk used:** 299.02 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

#### query_pattern_split

- **Size of downloaded dataset files:** 255.20 MB
- **Size of the generated dataset:** 43.98 MB
- **Total amount of disk used:** 299.19 MB

An example of 'train' looks as follows.
```
{
    "query": "SELECT /producer M0 . /director M0 . ",
    "question": "Who produced and directed M0?"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### mcd1
- `question`: a `string` feature.
- `query`: a `string` feature.

#### mcd2
- `question`: a `string` feature.
- `query`: a `string` feature.

#### mcd3
- `question`: a `string` feature.
- `query`: a `string` feature.

#### query_complexity_split
- `question`: a `string` feature.
- `query`: a `string` feature.

#### query_pattern_split
- `question`: a `string` feature.
- `query`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|         name         |train |test |
|----------------------|-----:|----:|
|mcd1                  | 95743|11968|
|mcd2                  | 95743|11968|
|mcd3                  | 95743|11968|
|query_complexity_split|100654| 9512|
|query_pattern_split   | 94600|12589|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```

@inproceedings{Keysers2020,
  title={Measuring Compositional Generalization: A Comprehensive Method on
         Realistic Data},
  author={Daniel Keysers and Nathanael Sch"{a}rli and Nathan Scales and
          Hylke Buisman and Daniel Furrer and Sergii Kashubin and
          Nikola Momchev and Danila Sinopalnikov and Lukasz Stafiniak and
          Tibor Tihon and Dmitry Tsarkov and Xiao Wang and Marc van Zee and
          Olivier Bousquet},
  booktitle={ICLR},
  year={2020},
  url={https://arxiv.org/abs/1912.09713.pdf},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@brainshawn](https://github.com/brainshawn) for adding this dataset.