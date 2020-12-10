---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- rn
- rw
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  kinnews_cleaned:
  - 10K<n<100K
  kinnews_raw:
  - 10K<n<100K
  kirnews_cleaned:
  - 1K<n<10K
  kirnews_raw:
  - 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- topic-classification
---
# Dataset Card for kinnews_kirnews

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

- **Homepage:** [Needs More Information]
- **Repository:** https://github.com/Andrews2017/KINNEWS-and-KIRNEWS-Corpus
- **Paper:** [KINNEWS and KIRNEWS: Benchmarking Cross-Lingual Text Classification for Kinyarwanda and Kirundi](https://arxiv.org/abs/2010.12174)
- **Leaderboard:** NA
- **Point of Contact:** [Rubungo Andre Niyongabo1](mailto:niyongabor.andre@std.uestc.edu.cn)

### Dataset Summary

Kinyarwanda and Kirundi news classification datasets (KINNEWS and KIRNEWS,respectively), which were both collected from Rwanda and Burundi news websites and newspapers, for low-resource monolingual and cross-lingual multiclass classification tasks.

### Supported Tasks and Leaderboards

NA

### Languages

Kinyarwanda and Kirundi

## Dataset Structure

### Data Instances

Each dataset is in comma-separated-value (csv) format, with columns that are described bellow (Note that in the cleaned versions we only remain with 'label','title', and 'content' columns):
| Field | Description |
| ----- | ----------- |
| label | Numerical labels that range from 1 to 14 |
| en_label | English labels |
| kin_label | Kinyarwanda labels |
| kir_label | Kirundi labels |
| url | The link to the news source |
| title | The title of the news article |
| content | The full content of the news article |

### Data Fields

The raw version of the data for Kinyarwanda language consists of these fields
-label: The category of the news article
-kin_label: The associated label in Kinyarwanda language
-en_label: The associated label in English
-url: The URL of the news article
-title: The title of the news article
-content: The content of the news article

The cleaned version contains only the `label`, `title` and the `content` fields
 

### Data Splits

Lang| Train | Test |
|---| ----- | ---- |
|Kinyarwanda|17014|4254|
|Kirundi|3689|923|

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

[Needs More Information]
i
