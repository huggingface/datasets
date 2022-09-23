---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- ur
license:
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
- fact-checking
- intent-classification
paperswithcode_id: null
pretty_name: Bend the Truth (Urdu Fake News)
dataset_info:
  features:
  - name: news
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: Fake
          1: Real
  - name: category
    dtype:
      class_label:
        names:
          0: bus
          1: hlth
          2: sp
          3: tch
          4: sbz
  splits:
  - name: test
    num_bytes: 799587
    num_examples: 262
  - name: train
    num_bytes: 1762905
    num_examples: 638
  download_size: 1042653
  dataset_size: 2562492
---

# Dataset Card for Bend the Truth (Urdu Fake News)

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

- **Homepage:** [Github](https://github.com/MaazAmjad/Datasets-for-Urdu-news/)
- **Repository:** [Github](https://github.com/MaazAmjad/Datasets-for-Urdu-news/)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [Maaz Amjad](https://github.com/MaazAmjad)

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- news: a string in urdu
- label: the label indicating whethere the provided news is real or fake.
- category: The intent of the news being presented. The available 5 classes are Sports, Health, Technology, Entertainment, and Business.

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

Thanks to [@chaitnayabasava](https://github.com/chaitnayabasava) for adding this dataset.