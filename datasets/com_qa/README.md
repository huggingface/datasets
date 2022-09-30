---
language:
- en
paperswithcode_id: comqa
pretty_name: ComQA
---

# Dataset Card for "com_qa"

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

- **Homepage:** [http://qa.mpi-inf.mpg.de/comqa/](http://qa.mpi-inf.mpg.de/comqa/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1.59 MB
- **Size of the generated dataset:** 1.05 MB
- **Total amount of disk used:** 2.65 MB

### Dataset Summary

ComQA is a dataset of 11,214 questions, which were collected from WikiAnswers, a community question answering website.
By collecting questions from such a site we ensure that the information needs are ones of interest to actual users.
Moreover, questions posed there are often cannot be answered by commercial search engines or QA technology, making them
more interesting for driving future research compared to those collected from an engine's query log. The dataset contains
questions with various challenging phenomena such as the need for temporal reasoning, comparison (e.g., comparatives,
superlatives, ordinals), compositionality (multiple, possibly nested, subquestions with multiple entities), and
unanswerable questions (e.g., Who was the first human being on Mars?). Through a large crowdsourcing effort, questions
in ComQA are grouped into 4,834 paraphrase clusters that express the same information need. Each cluster is annotated
with its answer(s). ComQA answers come in the form of Wikipedia entities wherever possible. Wherever the answers are
temporal or measurable quantities, TIMEX3 and the International System of Units (SI) are used for normalization.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 1.59 MB
- **Size of the generated dataset:** 1.05 MB
- **Total amount of disk used:** 2.65 MB

An example of 'validation' looks as follows.
```
{
    "answers": ["https://en.wikipedia.org/wiki/north_sea"],
    "cluster_id": "cluster-922",
    "questions": ["what sea separates the scandinavia peninsula from britain?", "which sea separates britain from scandinavia?"]
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `cluster_id`: a `string` feature.
- `questions`: a `list` of `string` features.
- `answers`: a `list` of `string` features.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default| 3966|       966|2243|

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
@inproceedings{abujabal-etal-2019-comqa,
    title = "{ComQA: A Community-sourced Dataset for Complex Factoid Question Answering with Paraphrase Clusters",
    author = {Abujabal, Abdalghani  and
      Saha Roy, Rishiraj  and
      Yahya, Mohamed  and
      Weikum, Gerhard},
    booktitle = {Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)},
    month = {jun},
    year = {2019},
    address = {Minneapolis, Minnesota},
    publisher = {Association for Computational Linguistics},
    url = {https://www.aclweb.org/anthology/N19-1027},
    doi = {10.18653/v1/N19-1027{,
    pages = {307--317},
    }

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@patrickvonplaten](https://github.com/patrickvonplaten), [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.
