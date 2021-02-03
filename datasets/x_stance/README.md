---
---

# Dataset Card for "x_stance"

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

- **Homepage:** [https://github.com/ZurichNLP/xstance](https://github.com/ZurichNLP/xstance)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 6.11 MB
- **Size of the generated dataset:** 24.54 MB
- **Total amount of disk used:** 30.65 MB

### [Dataset Summary](#dataset-summary)

The x-stance dataset contains more than 150 political questions, and 67k comments written by candidates on those questions.

It can be used to train and evaluate stance detection systems.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 6.11 MB
- **Size of the generated dataset:** 24.54 MB
- **Total amount of disk used:** 30.65 MB

An example of 'train' looks as follows.
```
{
    "author": "f27b54a137b4",
    "comment": "Das Arbeitsgesetz regelt die Arbeitszeiten und schützt den Arbeitnehmer. Es macht doch Sinn, dass wenn eine Nachfrage besteht, die Läden öffnen dürfen und wenn es keine Nachfrage gibt, diese geschlossen bleiben.",
    "id": 10045,
    "label": "FAVOR",
    "language": "de",
    "numerical_label": 100,
    "question": "Sind Sie für eine vollständige Liberalisierung der Geschäftsöffnungszeiten (Geschäfte können die Öffnungszeiten nach freiem Ermessen festlegen)?",
    "question_id": 739,
    "topic": "Economy"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `question`: a `string` feature.
- `id`: a `int32` feature.
- `question_id`: a `int32` feature.
- `language`: a `string` feature.
- `comment`: a `string` feature.
- `label`: a `string` feature.
- `numerical_label`: a `int32` feature.
- `author`: a `string` feature.
- `topic`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|validation|test |
|-------|----:|---------:|----:|
|default|45640|      3926|17705|

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
@inproceedings{vamvas2020xstance,
    author    = "Vamvas, Jannis and Sennrich, Rico",
    title     = "{X-Stance}: A Multilingual Multi-Target Dataset for Stance Detection",
    booktitle = "Proceedings of the 5th Swiss Text Analytics Conference (SwissText) \& 16th Conference on Natural Language Processing (KONVENS)",
    address   = "Zurich, Switzerland",
    year      = "2020",
    month     = "jun",
    url       = "http://ceur-ws.org/Vol-2624/paper9.pdf"
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@jvamvas](https://github.com/jvamvas) for adding this dataset.