---
language:
- en
paperswithcode_id: wikiqa
pretty_name: Wikipedia open-domain Question Answering
---

# Dataset Card for "wiki_qa"

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

- **Homepage:** [https://www.microsoft.com/en-us/download/details.aspx?id=52419](https://www.microsoft.com/en-us/download/details.aspx?id=52419)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 6.77 MB
- **Size of the generated dataset:** 6.10 MB
- **Total amount of disk used:** 12.87 MB

### Dataset Summary

Wiki Question Answering corpus from Microsoft

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 6.77 MB
- **Size of the generated dataset:** 6.10 MB
- **Total amount of disk used:** 12.87 MB

An example of 'train' looks as follows.
```
{
    "answer": "Glacier caves are often called ice caves , but this term is properly used to describe bedrock caves that contain year-round ice.",
    "document_title": "Glacier cave",
    "label": 0,
    "question": "how are glacier caves formed?",
    "question_id": "Q1"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `question_id`: a `string` feature.
- `question`: a `string` feature.
- `document_title`: a `string` feature.
- `answer`: a `string` feature.
- `label`: a classification label, with possible values including `0` (0), `1` (1).

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|20360|      2733|6165|

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
@InProceedings{YangYihMeek:EMNLP2015:WikiQA,
       author = {{Yi}, Yang and {Wen-tau},  Yih and {Christopher} Meek},
        title = "{WikiQA: A Challenge Dataset for Open-Domain Question Answering}",
      journal = {Association for Computational Linguistics},
         year = 2015,
          doi = {10.18653/v1/D15-1237},
        pages = {2013–2018},
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
