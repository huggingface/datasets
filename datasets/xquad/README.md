---
---

# Dataset Card for "xquad"

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

- **Homepage:** [https://github.com/deepmind/xquad](https://github.com/deepmind/xquad)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 139.53 MB
- **Size of the generated dataset:** 18.09 MB
- **Total amount of disk used:** 157.62 MB

### [Dataset Summary](#dataset-summary)

XQuAD (Cross-lingual Question Answering Dataset) is a benchmark dataset for evaluating cross-lingual question answering
performance. The dataset consists of a subset of 240 paragraphs and 1190 question-answer pairs from the development set
of SQuAD v1.1 (Rajpurkar et al., 2016) together with their professional translations into ten languages: Spanish, German,
Greek, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese, and Hindi. Consequently, the dataset is entirely parallel
across 11 languages.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### xquad.ar

- **Size of downloaded dataset files:** 12.68 MB
- **Size of the generated dataset:** 1.64 MB
- **Total amount of disk used:** 14.33 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [527],
        "text": ["136"]
    },
    "context": "\"Die Verteidigung der Panthers gab nur 308 Punkte ab und belegte den sechsten Platz in der Liga, während sie die NFL mit 24 Inte...",
    "id": "56beb4343aeaaa14008c925c",
    "question": "Wie viele Sacks erzielte Jared Allen in seiner Karriere?"
}
```

#### xquad.de

- **Size of downloaded dataset files:** 12.68 MB
- **Size of the generated dataset:** 1.23 MB
- **Total amount of disk used:** 13.91 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [527],
        "text": ["136"]
    },
    "context": "\"Die Verteidigung der Panthers gab nur 308 Punkte ab und belegte den sechsten Platz in der Liga, während sie die NFL mit 24 Inte...",
    "id": "56beb4343aeaaa14008c925c",
    "question": "Wie viele Sacks erzielte Jared Allen in seiner Karriere?"
}
```

#### xquad.el

- **Size of downloaded dataset files:** 12.68 MB
- **Size of the generated dataset:** 2.11 MB
- **Total amount of disk used:** 14.79 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [527],
        "text": ["136"]
    },
    "context": "\"Die Verteidigung der Panthers gab nur 308 Punkte ab und belegte den sechsten Platz in der Liga, während sie die NFL mit 24 Inte...",
    "id": "56beb4343aeaaa14008c925c",
    "question": "Wie viele Sacks erzielte Jared Allen in seiner Karriere?"
}
```

#### xquad.en

- **Size of downloaded dataset files:** 12.68 MB
- **Size of the generated dataset:** 1.07 MB
- **Total amount of disk used:** 13.75 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [527],
        "text": ["136"]
    },
    "context": "\"Die Verteidigung der Panthers gab nur 308 Punkte ab und belegte den sechsten Platz in der Liga, während sie die NFL mit 24 Inte...",
    "id": "56beb4343aeaaa14008c925c",
    "question": "Wie viele Sacks erzielte Jared Allen in seiner Karriere?"
}
```

#### xquad.es

- **Size of downloaded dataset files:** 12.68 MB
- **Size of the generated dataset:** 1.22 MB
- **Total amount of disk used:** 13.90 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [527],
        "text": ["136"]
    },
    "context": "\"Die Verteidigung der Panthers gab nur 308 Punkte ab und belegte den sechsten Platz in der Liga, während sie die NFL mit 24 Inte...",
    "id": "56beb4343aeaaa14008c925c",
    "question": "Wie viele Sacks erzielte Jared Allen in seiner Karriere?"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### xquad.ar
- `id`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### xquad.de
- `id`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### xquad.el
- `id`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### xquad.en
- `id`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### xquad.es
- `id`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|  name  |validation|
|--------|---------:|
|xquad.ar|      1190|
|xquad.de|      1190|
|xquad.el|      1190|
|xquad.en|      1190|
|xquad.es|      1190|

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
@article{Artetxe:etal:2019,
      author    = {Mikel Artetxe and Sebastian Ruder and Dani Yogatama},
      title     = {On the cross-lingual transferability of monolingual representations},
      journal   = {CoRR},
      volume    = {abs/1910.11856},
      year      = {2019},
      archivePrefix = {arXiv},
      eprint    = {1910.11856}
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.