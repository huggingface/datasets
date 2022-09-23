---
annotations_creators:
- expert-generated
- machine-generated
language_creators:
- expert-generated
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
paperswithcode_id: pubmedqa
pretty_name: PubMedQA
configs:
- pqa_artificial
- pqa_labeled
- pqa_unlabeled
dataset_info:
- config_name: pqa_labeled
  features:
  - name: pubid
    dtype: int32
  - name: question
    dtype: string
  - name: context
    sequence:
    - name: contexts
      dtype: string
    - name: labels
      dtype: string
    - name: meshes
      dtype: string
    - name: reasoning_required_pred
      dtype: string
    - name: reasoning_free_pred
      dtype: string
  - name: long_answer
    dtype: string
  - name: final_decision
    dtype: string
  splits:
  - name: train
    num_bytes: 2089200
    num_examples: 1000
  download_size: 687882700
  dataset_size: 2089200
- config_name: pqa_unlabeled
  features:
  - name: pubid
    dtype: int32
  - name: question
    dtype: string
  - name: context
    sequence:
    - name: contexts
      dtype: string
    - name: labels
      dtype: string
    - name: meshes
      dtype: string
  - name: long_answer
    dtype: string
  splits:
  - name: train
    num_bytes: 125938502
    num_examples: 61249
  download_size: 687882700
  dataset_size: 125938502
- config_name: pqa_artificial
  features:
  - name: pubid
    dtype: int32
  - name: question
    dtype: string
  - name: context
    sequence:
    - name: contexts
      dtype: string
    - name: labels
      dtype: string
    - name: meshes
      dtype: string
  - name: long_answer
    dtype: string
  - name: final_decision
    dtype: string
  splits:
  - name: train
    num_bytes: 443554667
    num_examples: 211269
  download_size: 687882700
  dataset_size: 443554667
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

- **Homepage:** [PUBMED_QA homepage](https://pubmedqa.github.io/ )
- **Repository:** [PUBMED_QA repository](https://github.com/pubmedqa/pubmedqa)
- **Paper:** [PUBMED_QA: A Dataset for Biomedical Research Question Answering](https://arxiv.org/abs/1909.06146)
- **Leaderboard:**  [PUBMED_QA: Leaderboard](https://pubmedqa.github.io/)

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

Thanks to [@tuner007](https://github.com/tuner007) for adding this dataset.