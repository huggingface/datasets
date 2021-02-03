---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
---

# Dataset Card for Big Patent

## Table of Contents

- [Dataset Card for Big Patent](#dataset-card-for-big-patent)
  - [Table of Contents](#table-of-contents)
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

## Dataset Description

- **Homepage:[Big Patent](https://evasharma.github.io/bigpatent/)**
- **Repository:**
- **Paper:[BIGPATENT: A Large-Scale Dataset for Abstractive and Coherent Summarization](https://arxiv.org/abs/1906.03741)**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

BIGPATENT, consisting of 1.3 million records of U.S. patent documents along with human written abstractive summaries. Each US patent application is filed under a Cooperative Patent Classification (CPC) code. There are nine such classification categories:

- A (Human Necessities)
- B (Performing Operations; Transporting)
- C (Chemistry; Metallurgy)
- D (Textiles; Paper)
- E (Fixed Constructions)
- F (Mechanical Engineering; Lightning; Heating; Weapons; Blasting)
- G (Physics)
- H (Electricity)
- Y (General tagging of new or cross-sectional technology)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

Each instance contains a pair of `description` and `abstract`. `description` is extracted from the Description section of the Patent while `abstract` is extracted from the Abstract section.

### Data Fields

- `description`: detailed description of patent.
- `abstract`: Patent abastract.

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.