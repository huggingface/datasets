---
annotations_creators:
- crowdsourced
language_creators:
- expert-generated
language:
- en
license:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
- question-answering-other-multi-hop
paperswithcode_id: medhop
pretty_name: MedHop
dataset_info:
- config_name: original
  features:
  - name: id
    dtype: string
  - name: query
    dtype: string
  - name: answer
    dtype: string
  - name: candidates
    sequence: string
  - name: supports
    sequence: string
  splits:
  - name: train
    num_bytes: 93937322
    num_examples: 1620
  - name: validation
    num_bytes: 16461640
    num_examples: 342
  download_size: 339843061
  dataset_size: 110398962
- config_name: masked
  features:
  - name: id
    dtype: string
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: candidates
    sequence: string
  - name: supports
    sequence: string
  splits:
  - name: train
    num_bytes: 95813584
    num_examples: 1620
  - name: validation
    num_bytes: 16800570
    num_examples: 342
  download_size: 339843061
  dataset_size: 112614154
---

# Dataset Card for MedHop

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

- **Homepage:** [QAngaroo](http://qangaroo.cs.ucl.ac.uk/)
- **Repository:** [If the dataset is hosted on github or has a github homepage, add URL here]()
- **Paper:** [Constructing Datasets for Multi-hop Reading Comprehension Across Documents](https://arxiv.org/abs/1710.06481)
- **Leaderboard:** [leaderboard](http://qangaroo.cs.ucl.ac.uk/leaderboard.html)
- **Point of Contact:** [Johannes Welbl](j.welbl@cs.ucl.ac.uk)

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

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.