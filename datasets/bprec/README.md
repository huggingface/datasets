---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- pl
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-retrieval
task_ids:
- entity-linking-retrieval
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [bprec homepage](https://clarin-pl.eu/dspace/handle/11321/736)
- **Repository:** [bprec repository](https://gitlab.clarin-pl.eu/team-semantics/semrel-extraction)
- **Paper:** [bprec paper](https://www.aclweb.org/anthology/2020.lrec-1.233.pdf)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Brand-Product Relation Extraction Corpora in Polish

### Supported Tasks and Leaderboards

NER, Entity linking

### Languages

Polish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- id: int identifier of a text
- text: string text, for example a consumer comment on the social media
- ner: extracted entities and their relationship
    - source and target: a pair of entities identified in the text
        - from: int value representing starting character of the entity
        - text: string value with the entity text
        - to: int value representing end character of the entity
        - type: one of pre-identified entity types:
            - PRODUCT_NAME
            - PRODUCT_NAME_IMP
            - PRODUCT_NO_BRAND
            - BRAND_NAME
            - BRAND_NAME_IMP
            - VERSION
            - PRODUCT_ADJ
            - BRAND_ADJ
            - LOCATION
            - LOCATION_IMP


### Data Splits

No train/validation/test split provided. Current dataset configurations point to 4 domain categories for the texts:
- tele
- electro
- cosmetics
- banking

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
```
@inproceedings{inproceedings,
author = {Janz, Arkadiusz and Kopociński, Łukasz and Piasecki, Maciej and Pluwak, Agnieszka},
year = {2020},
month = {05},
pages = {},
title = {Brand-Product Relation Extraction Using Heterogeneous Vector Space Representations}
}
```

### Contributions

Thanks to [@kldarek](https://github.com/kldarek) for adding this dataset.