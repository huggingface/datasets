---
---

# Dataset Card for "squadshifts"

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

- **Homepage:** [https://modestyachts.github.io/squadshifts-website/index.html](https://modestyachts.github.io/squadshifts-website/index.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 62.96 MB
- **Size of the generated dataset:** 35.82 MB
- **Total amount of disk used:** 98.78 MB

### [Dataset Summary](#dataset-summary)

SquadShifts consists of four new test sets for the Stanford Question Answering Dataset (SQuAD) from four different domains: Wikipedia articles, New York \
Times articles, Reddit comments, and Amazon product reviews. Each dataset was generated using the same data generating pipeline, Amazon Mechanical Turk interface, and data cleaning code as the original SQuAD v1.1 dataset. The "new-wikipedia" dataset measures overfitting on the original SQuAD v1.1 dataset.  The "new-york-times", "reddit", and "amazon" datasets measure robustness to natural distribution shifts. We encourage SQuAD model developers to also evaluate their methods on these new datasets!

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### amazon

- **Size of downloaded dataset files:** 15.74 MB
- **Size of the generated dataset:** 9.00 MB
- **Total amount of disk used:** 24.74 MB

An example of 'test' looks as follows.
```
{
    "answers": {
        "answer_start": [25],
        "text": ["amazon"]
    },
    "context": "This is a paragraph from amazon.",
    "id": "090909",
    "question": "Where is this paragraph from?",
    "title": "amazon dummy data"
}
```

#### new_wiki

- **Size of downloaded dataset files:** 15.74 MB
- **Size of the generated dataset:** 7.50 MB
- **Total amount of disk used:** 23.24 MB

An example of 'test' looks as follows.
```
{
    "answers": {
        "answer_start": [25],
        "text": ["wikipedia"]
    },
    "context": "This is a paragraph from wikipedia.",
    "id": "090909",
    "question": "Where is this paragraph from?",
    "title": "new_wiki dummy data"
}
```

#### nyt

- **Size of downloaded dataset files:** 15.74 MB
- **Size of the generated dataset:** 10.29 MB
- **Total amount of disk used:** 26.03 MB

An example of 'test' looks as follows.
```
{
    "answers": {
        "answer_start": [25],
        "text": ["new york times"]
    },
    "context": "This is a paragraph from new york times.",
    "id": "090909",
    "question": "Where is this paragraph from?",
    "title": "nyt dummy data"
}
```

#### reddit

- **Size of downloaded dataset files:** 15.74 MB
- **Size of the generated dataset:** 9.03 MB
- **Total amount of disk used:** 24.77 MB

An example of 'test' looks as follows.
```
{
    "answers": {
        "answer_start": [25],
        "text": ["reddit"]
    },
    "context": "This is a paragraph from reddit.",
    "id": "090909",
    "question": "Where is this paragraph from?",
    "title": "reddit dummy data"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### amazon
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### new_wiki
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### nyt
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### reddit
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|  name  |test |
|--------|----:|
|amazon  | 9885|
|new_wiki| 7938|
|nyt     |10065|
|reddit  | 9803|

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
@inproceedings{miller2020effect,
  author = {J. Miller and K. Krauth and B. Recht and L. Schmidt},
  booktitle = {International Conference on Machine Learning (ICML)},
  title = {The Effect of Natural Distribution Shift on Question Answering Models},
  year = {2020},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@millerjohnp](https://github.com/millerjohnp), [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.