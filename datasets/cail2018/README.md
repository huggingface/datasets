---
annotations_creators:
- found
language_creators:
- found
language:
- zh
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-judgement-prediction
paperswithcode_id: chinese-ai-and-law-cail-2018
pretty_name: CAIL 2018
dataset_info:
  features:
  - name: fact
    dtype: string
  - name: relevant_articles
    sequence: int32
  - name: accusation
    sequence: string
  - name: punish_of_money
    dtype: float32
  - name: criminals
    sequence: string
  - name: death_penalty
    dtype: bool
  - name: imprisonment
    dtype: float32
  - name: life_imprisonment
    dtype: bool
  splits:
  - name: exercise_contest_test
    num_bytes: 41057634
    num_examples: 32508
  - name: exercise_contest_train
    num_bytes: 220112732
    num_examples: 154592
  - name: exercise_contest_valid
    num_bytes: 21702157
    num_examples: 17131
  - name: final_test
    num_bytes: 44194707
    num_examples: 35922
  - name: first_stage_test
    num_bytes: 244335194
    num_examples: 217016
  - name: first_stage_train
    num_bytes: 1779657510
    num_examples: 1710856
  download_size: 984551626
  dataset_size: 2351059934
---
---
# Dataset Card for CAIL 2018

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

- **Homepage:** [Github](https://github.com/thunlp/CAIL/blob/master/README_en.md)
- **Repository:** [Github](https://github.com/thunlp/CAIL)
- **Paper:** [Arxiv](https://arxiv.org/abs/1807.02478)
- **Leaderboard:**
- **Point of Contact:**

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

[More Information Needed]

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

Thanks to [@JetRunner](https://github.com/JetRunner) for adding this dataset.