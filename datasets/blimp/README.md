---
---

# Dataset Card for "blimp"

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

- **Homepage:** [https://github.com/alexwarstadt/blimp/tree/master/](https://github.com/alexwarstadt/blimp/tree/master/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 28.21 MB
- **Size of the generated dataset:** 10.92 MB
- **Total amount of disk used:** 39.13 MB

### [Dataset Summary](#dataset-summary)

BLiMP is a challenge set for evaluating what language models (LMs) know about
major grammatical phenomena in English. BLiMP consists of 67 sub-datasets, each
containing 1000 minimal pairs isolating specific contrasts in syntax,
morphology, or semantics. The data is automatically generated according to
expert-crafted grammars.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### adjunct_island

- **Size of downloaded dataset files:** 0.34 MB
- **Size of the generated dataset:** 0.16 MB
- **Total amount of disk used:** 0.50 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### anaphor_gender_agreement

- **Size of downloaded dataset files:** 0.42 MB
- **Size of the generated dataset:** 0.13 MB
- **Total amount of disk used:** 0.54 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### anaphor_number_agreement

- **Size of downloaded dataset files:** 0.43 MB
- **Size of the generated dataset:** 0.13 MB
- **Total amount of disk used:** 0.56 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### animate_subject_passive

- **Size of downloaded dataset files:** 0.44 MB
- **Size of the generated dataset:** 0.14 MB
- **Total amount of disk used:** 0.58 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### animate_subject_trans

- **Size of downloaded dataset files:** 0.41 MB
- **Size of the generated dataset:** 0.12 MB
- **Total amount of disk used:** 0.54 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### adjunct_island
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### anaphor_gender_agreement
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### anaphor_number_agreement
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### animate_subject_passive
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### animate_subject_trans
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|          name          |train|
|------------------------|----:|
|adjunct_island          | 1000|
|anaphor_gender_agreement| 1000|
|anaphor_number_agreement| 1000|
|animate_subject_passive | 1000|
|animate_subject_trans   | 1000|

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

@article{warstadt2019blimp,
  title={BLiMP: A Benchmark of Linguistic Minimal Pairs for English},
  author={Warstadt, Alex and Parrish, Alicia and Liu, Haokun and Mohananey, Anhad and Peng, Wei, and Wang, Sheng-Fu and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1912.00582},
  year={2019}
}

```


### Contributions

Thanks to [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.