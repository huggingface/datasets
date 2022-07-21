---
language:
- en
paperswithcode_id: superglue
pretty_name: SuperGLUE
---

# Dataset Card for "super_glue"

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

- **Homepage:** [https://github.com/google-research-datasets/boolean-questions](https://github.com/google-research-datasets/boolean-questions)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 55.66 MB
- **Size of the generated dataset:** 238.01 MB
- **Total amount of disk used:** 293.67 MB

### Dataset Summary

SuperGLUE (https://super.gluebenchmark.com/) is a new benchmark styled after
GLUE with a new set of more difficult language understanding tasks, improved
resources, and a new public leaderboard.

BoolQ (Boolean Questions, Clark et al., 2019a) is a QA task where each example consists of a short
passage and a yes/no question about the passage. The questions are provided anonymously and
unsolicited by users of the Google search engine, and afterwards paired with a paragraph from a
Wikipedia article containing the answer. Following the original work, we evaluate with accuracy.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### axb

- **Size of downloaded dataset files:** 0.03 MB
- **Size of the generated dataset:** 0.23 MB
- **Total amount of disk used:** 0.26 MB

An example of 'test' looks as follows.
```

```

#### axg

- **Size of downloaded dataset files:** 0.01 MB
- **Size of the generated dataset:** 0.05 MB
- **Total amount of disk used:** 0.06 MB

An example of 'test' looks as follows.
```

```

#### boolq

- **Size of downloaded dataset files:** 3.93 MB
- **Size of the generated dataset:** 9.92 MB
- **Total amount of disk used:** 13.85 MB

An example of 'train' looks as follows.
```

```

#### cb

- **Size of downloaded dataset files:** 0.07 MB
- **Size of the generated dataset:** 0.19 MB
- **Total amount of disk used:** 0.27 MB

An example of 'train' looks as follows.
```

```

#### copa

- **Size of downloaded dataset files:** 0.04 MB
- **Size of the generated dataset:** 0.12 MB
- **Total amount of disk used:** 0.16 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### axb
- `sentence1`: a `string` feature.
- `sentence2`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `entailment` (0), `not_entailment` (1).

#### axg
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `entailment` (0), `not_entailment` (1).

#### boolq
- `question`: a `string` feature.
- `passage`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `False` (0), `True` (1).

#### cb
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `entailment` (0), `contradiction` (1), `neutral` (2).

#### copa
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `idx`: a `int32` feature.
- `label`: a classification label, with possible values including `choice1` (0), `choice2` (1).

### Data Splits

#### axb

|   |test|
|---|---:|
|axb|1104|

#### axg

|   |test|
|---|---:|
|axg| 356|

#### boolq

|     |train|validation|test|
|-----|----:|---------:|---:|
|boolq| 9427|      3270|3245|

#### cb

|   |train|validation|test|
|---|----:|---------:|---:|
|cb |  250|        56| 250|

#### copa

|    |train|validation|test|
|----|----:|---------:|---:|
|copa|  400|       100| 500|

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
@inproceedings{clark2019boolq,
  title={BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions},
  author={Clark, Christopher and Lee, Kenton and Chang, Ming-Wei, and Kwiatkowski, Tom and Collins, Michael, and Toutanova, Kristina},
  booktitle={NAACL},
  year={2019}
}
@article{wang2019superglue,
  title={SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems},
  author={Wang, Alex and Pruksachatkun, Yada and Nangia, Nikita and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1905.00537},
  year={2019}
}

Note that each SuperGLUE dataset has its own citation. Please see the source to
get the correct citation for each contained dataset.

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.
