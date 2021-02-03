---
---

# Dataset Card for "quoref"

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

- **Homepage:** [https://leaderboard.allenai.org/quoref/submissions/get-started](https://leaderboard.allenai.org/quoref/submissions/get-started)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 4.84 MB
- **Size of the generated dataset:** 47.51 MB
- **Total amount of disk used:** 52.36 MB

### [Dataset Summary](#dataset-summary)

Quoref is a QA dataset which tests the coreferential reasoning capability of reading comprehension systems. In this
span-selection benchmark containing 24K questions over 4.7K paragraphs from Wikipedia, a system must resolve hard
coreferences before selecting the appropriate span(s) in the paragraphs for answering questions.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 4.84 MB
- **Size of the generated dataset:** 47.51 MB
- **Total amount of disk used:** 52.36 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [1633],
        "text": ["Frankie"]
    },
    "context": "\"Frankie Bono, a mentally disturbed hitman from Cleveland, comes back to his hometown in New York City during Christmas week to ...",
    "id": "bfc3b34d6b7e73c0bd82a009db12e9ce196b53e6",
    "question": "What is the first name of the person who has until New Year's Eve to perform a hit?",
    "title": "Blast of Silence",
    "url": "https://en.wikipedia.org/wiki/Blast_of_Silence"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `id`: a `string` feature.
- `question`: a `string` feature.
- `context`: a `string` feature.
- `title`: a `string` feature.
- `url`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|validation|
|-------|----:|---------:|
|default|19399|      2418|

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
@article{allenai:quoref,
      author    = {Pradeep Dasigi and Nelson F. Liu and Ana Marasovic and Noah A. Smith and  Matt Gardner},
      title     = {Quoref: A Reading Comprehension Dataset with Questions Requiring Coreferential Reasoning},
      journal   = {arXiv:1908.05803v2 },
      year      = {2019},
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.