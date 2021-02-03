---
---

# Dataset Card for "ai2_arc"

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

- **Homepage:** [https://allenai.org/data/arc](https://allenai.org/data/arc)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1298.60 MB
- **Size of the generated dataset:** 2.17 MB
- **Total amount of disk used:** 1300.77 MB

### [Dataset Summary](#dataset-summary)

A new dataset of 7,787 genuine grade-school level, multiple-choice science questions, assembled to encourage research in
 advanced question-answering. The dataset is partitioned into a Challenge Set and an Easy Set, where the former contains
 only questions answered incorrectly by both a retrieval-based algorithm and a word co-occurrence algorithm. We are also
 including a corpus of over 14 million science sentences relevant to the task, and an implementation of three neural baseline models for this dataset. We pose ARC as a challenge to the community.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### ARC-Challenge

- **Size of downloaded dataset files:** 649.30 MB
- **Size of the generated dataset:** 0.79 MB
- **Total amount of disk used:** 650.09 MB

An example of 'train' looks as follows.
```
{
    "answerKey": "B",
    "choices": {
        "label": ["A", "B", "C", "D"],
        "text": ["Shady areas increased.", "Food sources increased.", "Oxygen levels increased.", "Available water increased."]
    },
    "id": "Mercury_SC_405487",
    "question": "One year, the oak trees in a park began producing more acorns than usual. The next year, the population of chipmunks in the park also increased. Which best explains why there were more chipmunks the next year?"
}
```

#### ARC-Easy

- **Size of downloaded dataset files:** 649.30 MB
- **Size of the generated dataset:** 1.38 MB
- **Total amount of disk used:** 650.68 MB

An example of 'train' looks as follows.
```
{
    "answerKey": "B",
    "choices": {
        "label": ["A", "B", "C", "D"],
        "text": ["Shady areas increased.", "Food sources increased.", "Oxygen levels increased.", "Available water increased."]
    },
    "id": "Mercury_SC_405487",
    "question": "One year, the oak trees in a park began producing more acorns than usual. The next year, the population of chipmunks in the park also increased. Which best explains why there were more chipmunks the next year?"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### ARC-Challenge
- `id`: a `string` feature.
- `question`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `answerKey`: a `string` feature.

#### ARC-Easy
- `id`: a `string` feature.
- `question`: a `string` feature.
- `choices`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `label`: a `string` feature.
- `answerKey`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|    name     |train|validation|test|
|-------------|----:|---------:|---:|
|ARC-Challenge| 1119|       299|1172|
|ARC-Easy     | 2251|       570|2376|

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
@article{allenai:arc,
      author    = {Peter Clark  and Isaac Cowhey and Oren Etzioni and Tushar Khot and
                    Ashish Sabharwal and Carissa Schoenick and Oyvind Tafjord},
      title     = {Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge},
      journal   = {arXiv:1803.05457v1},
      year      = {2018},
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.