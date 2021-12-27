---
annotations_creators:
- found
language_creators:
- found
languages:
- ar
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
paperswithcode_id: labr
pretty_name: LABR
---

# Dataset Card for LABR

## Table of Contents
- [Dataset Card for LABR](#dataset-card-for-labr)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
  - [|split|num examples|](#splitnum-examples)
  - [Dataset Creation](#dataset-creation)
    - [Curation Rationale](#curation-rationale)
    - [Source Data](#source-data)
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Repository:** [LABR](https://github.com/mohamedadaly/LABR)
- **Paper:** [LABR: Large-scale Arabic Book Reviews Dataset](https://aclanthology.org/P13-2088/)
- **Point of Contact:** [Mohammed Aly](mailto:mohamed@mohamedaly.info)

### Dataset Summary

This dataset contains over 63,000 book reviews in Arabic. It is the largest sentiment analysis dataset for Arabic to-date. The book reviews were harvested from the website Goodreads during the month or March 2013. Each book review comes with the goodreads review id, the user id, the book id, the rating (1 to 5) and the text of the review.

### Supported Tasks and Leaderboards

The dataset was published on this [paper](https://www.aclweb.org/anthology/P13-2088.pdf). 

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

A typical data point comprises a rating from 1 to 5 where the higher the rating the better the review.  

### Data Fields

- `text` (str): Review text.
- `label` (int): Review rating.

### Data Splits

The data is split into a training and testing. The split is organized as the following 

|           | Tain   | Test |
|---------- | ------ | ---- |
|data split | 11,760 | 2,935|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

downloaded over 220,000 reviews from the
book readers social network www.goodreads.com
during the month of March 2013

#### Who are the source language producers?

Reviews. 

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
@inproceedings{aly2013labr,
  title={Labr: A large scale arabic book reviews dataset},
  author={Aly, Mohamed and Atiya, Amir},
  booktitle={Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},
  pages={494--498},
  year={2013}
}
```

### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) for adding this dataset.