---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- es
licenses:
- cc-by-2.1
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
---

# Dataset Card for Muchocine

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

- **Homepage:** http://www.lsi.us.es/~fermin/index.php/Datasets

### Dataset Summary

The Muchocine reviews dataset contains 3,872 longform movie reviews in Spanish language,
each with a shorter summary review, and a rating on a 1-5 scale.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Spanish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- review_body - longform review
- review_summary - shorter-form review
- star_rating - an integer star rating (1-5)

The original source also includes part-of-speech tagging for body and summary fields.

### Data Splits

One split (train) with 3,872 reviews

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Data was collected from www.muchocine.net and uploaded by Dr. Fermín L. Cruz Mata
of La Universidad de Sevilla

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

The text reviews and star ratings came directly from users, so no additional annotation was needed.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

- Dr. Fermín L. Cruz Mata

### Licensing Information

CC-BY-2.1

### Citation Information

See http://www.lsi.us.es/~fermin/index.php/Datasets

### Contributions

Thanks to [@mapmeld](https://github.com/mapmeld) for adding this dataset.