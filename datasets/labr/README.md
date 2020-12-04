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
- 10k<n<100k
source_datasets:
- original
task_categories:
- text_classification
task_ids:
- multi-class-classification
---

# Dataset Card for MetRec

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Discussion of Social Impact and Biases](#discussion-of-social-impact-and-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** [LABR](https://github.com/mohamedadaly/LABR)
- **Repository:** [LABR](https://github.com/mohamedadaly/LABR)
- **Paper:** [LABR: Large-scale Arabic Book Reviews Dataset](https://www.aclweb.org/anthology/P13-2088.pdf)
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

[More Information Needed]

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

### Discussion of Social Impact and Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]
