---
---

# Dataset Card for "glue"

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

- **Homepage:** [https://nyu-mll.github.io/CoLA/](https://nyu-mll.github.io/CoLA/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 955.33 MB
- **Size of the generated dataset:** 229.68 MB
- **Total amount of disk used:** 1185.01 MB

### [Dataset Summary](#dataset-summary)

GLUE, the General Language Understanding Evaluation benchmark
(https://gluebenchmark.com/) is a collection of resources for training,
evaluating, and analyzing natural language understanding systems.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### ax

- **Size of downloaded dataset files:** 0.21 MB
- **Size of the generated dataset:** 0.23 MB
- **Total amount of disk used:** 0.44 MB

An example of 'test' looks as follows.
```

```

#### cola

- **Size of downloaded dataset files:** 0.36 MB
- **Size of the generated dataset:** 0.58 MB
- **Total amount of disk used:** 0.94 MB

An example of 'train' looks as follows.
```

```

#### mnli

- **Size of downloaded dataset files:** 298.29 MB
- **Size of the generated dataset:** 78.65 MB
- **Total amount of disk used:** 376.95 MB

An example of 'train' looks as follows.
```

```

#### mnli_matched

- **Size of downloaded dataset files:** 298.29 MB
- **Size of the generated dataset:** 3.52 MB
- **Total amount of disk used:** 301.82 MB

An example of 'validation' looks as follows.
```

```

#### mnli_mismatched

- **Size of downloaded dataset files:** 298.29 MB
- **Size of the generated dataset:** 3.73 MB
- **Total amount of disk used:** 302.02 MB

An example of 'validation' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### ax
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

#### cola
- `sentence`: a `string` feature.
- `label`: a classification label, with possible values including `unacceptable` (0), `acceptable` (1).
- `idx`: a `int32` feature.

#### mnli
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

#### mnli_matched
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

#### mnli_mismatched
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

#### ax

|   |test|
|---|---:|
|ax |1104|

#### cola

|    |train|validation|test|
|----|----:|---------:|---:|
|cola| 8551|      1043|1063|

#### mnli

|    |train |validation_matched|validation_mismatched|test_matched|test_mismatched|
|----|-----:|-----------------:|--------------------:|-----------:|--------------:|
|mnli|392702|              9815|                 9832|        9796|           9847|

#### mnli_matched

|            |validation|test|
|------------|---------:|---:|
|mnli_matched|      9815|9796|

#### mnli_mismatched

|               |validation|test|
|---------------|---------:|---:|
|mnli_mismatched|      9832|9847|

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
@article{warstadt2018neural,
  title={Neural Network Acceptability Judgments},
  author={Warstadt, Alex and Singh, Amanpreet and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1805.12471},
  year={2018}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```


### Contributions

Thanks to [@patpizio](https://github.com/patpizio), [@jeswan](https://github.com/jeswan), [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.