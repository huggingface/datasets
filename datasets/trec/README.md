---
---

# Dataset Card for "trec"

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

- **Homepage:** [https://cogcomp.seas.upenn.edu/Data/QA/QC/](https://cogcomp.seas.upenn.edu/Data/QA/QC/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.34 MB
- **Size of the generated dataset:** 0.39 MB
- **Total amount of disk used:** 0.74 MB

### [Dataset Summary](#dataset-summary)

The Text REtrieval Conference (TREC) Question Classification dataset contains 5500 labeled questions in training set and another 500 for test set. The dataset has 6 labels, 47 level-2 labels. Average length of each sentence is 10, vocabulary size of 8700.

Data are collected from four sources: 4,500 English questions published by USC (Hovy et al., 2001), about 500 manually constructed questions for a few rare classes, 894 TREC 8 and TREC 9 questions, and also 500 questions from TREC 10 which serves as the test set.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 0.34 MB
- **Size of the generated dataset:** 0.39 MB
- **Total amount of disk used:** 0.74 MB

An example of 'train' looks as follows.
```
{
    "label-coarse": 1,
    "label-fine": 2,
    "text": "What fowl grabs the spotlight after the Chinese Year of the Monkey ?"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `label-coarse`: a classification label, with possible values including `DESC` (0), `ENTY` (1), `ABBR` (2), `HUM` (3), `NUM` (4).
- `label-fine`: a classification label, with possible values including `manner` (0), `cremat` (1), `animal` (2), `exp` (3), `ind` (4).
- `text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|test|
|-------|----:|---:|
|default| 5452| 500|

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
@inproceedings{li-roth-2002-learning,
    title = "Learning Question Classifiers",
    author = "Li, Xin  and
      Roth, Dan",
    booktitle = "{COLING} 2002: The 19th International Conference on Computational Linguistics",
    year = "2002",
    url = "https://www.aclweb.org/anthology/C02-1150",
}
@inproceedings{hovy-etal-2001-toward,
    title = "Toward Semantics-Based Answer Pinpointing",
    author = "Hovy, Eduard  and
      Gerber, Laurie  and
      Hermjakob, Ulf  and
      Lin, Chin-Yew  and
      Ravichandran, Deepak",
    booktitle = "Proceedings of the First International Conference on Human Language Technology Research",
    year = "2001",
    url = "https://www.aclweb.org/anthology/H01-1069",
}

```


### Contributions

Thanks to [@lhoestq](https://github.com/lhoestq), [@thomwolf](https://github.com/thomwolf) for adding this dataset.