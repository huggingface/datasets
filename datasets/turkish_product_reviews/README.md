---
annotations_creators:
- found
language_creators:
- found
languages:
- tr
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text_classification
task_ids:
- sentiment-classification
---

# Dataset Card for Turkish Product Reviews

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
  - [Contributions](#contributions)

## Dataset Description

- **Repository:** [turkish-text-data](https://github.com/fthbrmnby/turkish-text-data)
- **Point of Contact:** [Fatih Barmanbay](https://github.com/fthbrmnby)

### Dataset Summary

This Turkish Product Reviews Dataset contains 235.165 product reviews collected online. There are 220.284 positive, 14881 negative reviews.

### Languages

The dataset is based on Turkish.

## Dataset Structure

### Data Instances

**Example 1:**

**sentence:** beklentimin altında bir ürün kaliteli değil

**sentiment:** 0 (negative)

**Example 2:**

**sentence:** fiyat ve performans olarak gayet iyi

**sentiment:** 1 (positive)


### Data Fields

- **sentence**(string) : Contatins turkish product review
- **sentiment**(int) : 0 (negative) or 1 (positive)

### Data Splits

It is not divided into Train set and Test set.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

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

The dataset was created by [Fatih Barmanbay](https://github.com/fthbrmnby).  

### Licensing Information

The data is under the [CC-BY-SA-4.0 License](https://github.com/fthbrmnby/turkish-text-data/blob/master/LICENCE)

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@basakbuluz](https://github.com/basakbuluz) for adding this dataset.