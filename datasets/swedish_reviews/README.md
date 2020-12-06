---
annotations_creators:
- found
language_creators:
- found
languages:
- sv
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for Swedish Reviews

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
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** [swedish_reviews homepage](https://github.com/timpal0l/swedish-sentiment)
- **Repository:** [swedish_reviews repository](https://github.com/timpal0l/swedish-sentiment)
- **Point of Contact:** [Tim Isbister](mailto:timisbisters@gmail.com)

### Dataset Summary

The dataset is scraped from various Swedish websites where reviews are present.

### Supported Tasks and Leaderboards

This dataset can be used to evaluate sentiment classification on Swedish.

### Languages

The text in the dataset is in Swedish.

## Dataset Structure

### Data Instances

What a sample looks like:
```
{
 'text': 'Jag tycker huggingface är ett grymt project!',
 'label': 1,
}
```

### Data Fields

- `text`:  A text where the sentiment expression is present.
- `label`: a int representing the label `0`for negative and `1`for positive.

### Data Splits

The data is split into a training, validation and test set. The final split sizes are as follow:

| Train   | Valid  | Test  |
| ------  | -----  | ----  |
| 62089   |  20696 | 20697 |

## Dataset Creation

### Curation Rationale

### Source Data

#### Initial Data Collection and Normalization

#### Who are the source language producers?

### Annotations

#### Annotation process

#### Who are the annotators?

### Personal and Sensitive Information

## Considerations for Using the Data

### Social Impact of Dataset

### Discussion of Biases

### Other Known Limitations

## Additional Information

### Dataset Curators

The corpus was scraped by @timpal0l

### Licensing Information

### Citation Information

