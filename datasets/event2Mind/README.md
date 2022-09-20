---
annotations_creators:
- crowdsourced
language:
- en
language_creators:
- found
license:
- unknown
multilinguality:
- monolingual
pretty_name: Event2Mind
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text2text-generation
task_ids:
- text2text-generation-other-common-sense-inference
paperswithcode_id: event2mind
---

# Dataset Card for "event2Mind"

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

- **Homepage:** [https://uwnlp.github.io/event2mind/](https://uwnlp.github.io/event2mind/)
- **Repository:** https://github.com/uwnlp/event2mind
- **Paper:** [Event2Mind: Commonsense Inference on Events, Intents, and Reactions](https://arxiv.org/abs/1805.06939)
- **Point of Contact:** [Hannah Rashkin](mailto:hrashkin@cs.washington.edu), [Maarten Sap](mailto:msap@cs.washington.edu)
- **Size of downloaded dataset files:** 1.24 MB
- **Size of the generated dataset:** 6.90 MB
- **Total amount of disk used:** 8.14 MB

### Dataset Summary

In Event2Mind, we explore the task of understanding stereotypical intents and reactions to events. Through crowdsourcing, we create a large corpus with 25,000 events and free-form descriptions of their intents and reactions, both of the event's subject and (potentially implied) other participants.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 1.24 MB
- **Size of the generated dataset:** 6.90 MB
- **Total amount of disk used:** 8.14 MB

An example of 'validation' looks as follows.
```
{
    "Event": "It shrinks in the wash",
    "Osent": "1",
    "Otheremotion": "[\"upset\", \"angry\"]",
    "Source": "it_events",
    "Xemotion": "[\"none\"]",
    "Xintent": "[\"none\"]",
    "Xsent": ""
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `Source`: a `string` feature.
- `Event`: a `string` feature.
- `Xintent`: a `string` feature.
- `Xemotion`: a `string` feature.
- `Otheremotion`: a `string` feature.
- `Xsent`: a `string` feature.
- `Osent`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|46472|      5401|5221|

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
@inproceedings{rashkin-etal-2018-event2mind,
    title = "{E}vent2{M}ind: Commonsense Inference on Events, Intents, and Reactions",
    author = "Rashkin, Hannah  and
      Sap, Maarten  and
      Allaway, Emily  and
      Smith, Noah A.  and
      Choi, Yejin",
    booktitle = "Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2018",
    address = "Melbourne, Australia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P18-1043",
    doi = "10.18653/v1/P18-1043",
    pages = "463--473",
}
```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.
