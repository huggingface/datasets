---
---

# Dataset Card for "break_data"

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

- **Homepage:** [https://github.com/allenai/Break](https://github.com/allenai/Break)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 76.16 MB
- **Size of the generated dataset:** 148.34 MB
- **Total amount of disk used:** 224.49 MB

### [Dataset Summary](#dataset-summary)

Break is a human annotated dataset of natural language questions and their Question Decomposition Meaning Representations
(QDMRs). Break consists of 83,978 examples sampled from 10 question answering datasets over text, images and databases.
This repository contains the Break dataset along with information on the exact data format.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### QDMR

- **Size of downloaded dataset files:** 15.23 MB
- **Size of the generated dataset:** 15.19 MB
- **Total amount of disk used:** 30.42 MB

An example of 'validation' looks as follows.
```
{
    "decomposition": "return flights ;return #1 from  denver ;return #2 to philadelphia ;return #3 if  available",
    "operators": "['select', 'filter', 'filter', 'filter']",
    "question_id": "ATIS_dev_0",
    "question_text": "what flights are available tomorrow from denver to philadelphia ",
    "split": "dev"
}
```

#### QDMR-high-level

- **Size of downloaded dataset files:** 15.23 MB
- **Size of the generated dataset:** 6.24 MB
- **Total amount of disk used:** 21.47 MB

An example of 'train' looks as follows.
```
{
    "decomposition": "return ground transportation ;return #1 which  is  available ;return #2 from  the pittsburgh airport ;return #3 to downtown ;return the cost of #4",
    "operators": "['select', 'filter', 'filter', 'filter', 'project']",
    "question_id": "ATIS_dev_102",
    "question_text": "what ground transportation is available from the pittsburgh airport to downtown and how much does it cost ",
    "split": "dev"
}
```

#### QDMR-high-level-lexicon

- **Size of downloaded dataset files:** 15.23 MB
- **Size of the generated dataset:** 30.17 MB
- **Total amount of disk used:** 45.40 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "allowed_tokens": "\"['higher than', 'same as', 'what ', 'and ', 'than ', 'at most', 'he', 'distinct', 'House', 'two', 'at least', 'or ', 'date', 'o...",
    "source": "What office, also held by a member of the Maine House of Representatives, did James K. Polk hold before he was president?"
}
```

#### QDMR-lexicon

- **Size of downloaded dataset files:** 15.23 MB
- **Size of the generated dataset:** 73.61 MB
- **Total amount of disk used:** 88.84 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "allowed_tokens": "\"['higher than', 'same as', 'what ', 'and ', 'than ', 'at most', 'distinct', 'two', 'at least', 'or ', 'date', 'on ', '@@14@@', ...",
    "source": "what flights are available tomorrow from denver to philadelphia "
}
```

#### logical-forms

- **Size of downloaded dataset files:** 15.23 MB
- **Size of the generated dataset:** 23.13 MB
- **Total amount of disk used:** 38.36 MB

An example of 'train' looks as follows.
```
{
    "decomposition": "return ground transportation ;return #1 which  is  available ;return #2 from  the pittsburgh airport ;return #3 to downtown ;return the cost of #4",
    "operators": "['select', 'filter', 'filter', 'filter', 'project']",
    "program": "some program",
    "question_id": "ATIS_dev_102",
    "question_text": "what ground transportation is available from the pittsburgh airport to downtown and how much does it cost ",
    "split": "dev"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### QDMR
- `question_id`: a `string` feature.
- `question_text`: a `string` feature.
- `decomposition`: a `string` feature.
- `operators`: a `string` feature.
- `split`: a `string` feature.

#### QDMR-high-level
- `question_id`: a `string` feature.
- `question_text`: a `string` feature.
- `decomposition`: a `string` feature.
- `operators`: a `string` feature.
- `split`: a `string` feature.

#### QDMR-high-level-lexicon
- `source`: a `string` feature.
- `allowed_tokens`: a `string` feature.

#### QDMR-lexicon
- `source`: a `string` feature.
- `allowed_tokens`: a `string` feature.

#### logical-forms
- `question_id`: a `string` feature.
- `question_text`: a `string` feature.
- `decomposition`: a `string` feature.
- `operators`: a `string` feature.
- `split`: a `string` feature.
- `program`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|         name          |train|validation|test|
|-----------------------|----:|---------:|---:|
|QDMR                   |44321|      7760|8069|
|QDMR-high-level        |17503|      3130|3195|
|QDMR-high-level-lexicon|17503|      3130|3195|
|QDMR-lexicon           |44321|      7760|8069|
|logical-forms          |44098|      7719|8006|

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
@article{Wolfson2020Break,
  title={Break It Down: A Question Understanding Benchmark},
  author={Wolfson, Tomer and Geva, Mor and Gupta, Ankit and Gardner, Matt and Goldberg, Yoav and Deutch, Daniel and Berant, Jonathan},
  journal={Transactions of the Association for Computational Linguistics},
  year={2020},
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.