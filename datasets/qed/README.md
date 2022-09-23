---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|natural_questions
task_categories:
- question-answering
task_ids:
- extractive-qa
- question-answering-other-explanations-in-question-answering
paperswithcode_id: qed
pretty_name: QED
dataset_info:
  features:
  - name: example_id
    dtype: int64
  - name: title_text
    dtype: string
  - name: url
    dtype: string
  - name: question
    dtype: string
  - name: paragraph_text
    dtype: string
  - name: sentence_starts
    sequence: int32
  - name: original_nq_answers
    list:
    - name: start
      dtype: int32
    - name: end
      dtype: int32
    - name: string
      dtype: string
  - name: annotation
    struct:
    - name: referential_equalities
      list:
      - name: question_reference
        struct:
        - name: start
          dtype: int32
        - name: end
          dtype: int32
        - name: string
          dtype: string
      - name: sentence_reference
        struct:
        - name: start
          dtype: int32
        - name: end
          dtype: int32
        - name: bridge
          dtype: string
        - name: string
          dtype: string
    - name: answer
      list:
      - name: sentence_reference
        struct:
        - name: start
          dtype: int32
        - name: end
          dtype: int32
        - name: bridge
          dtype: string
        - name: string
          dtype: string
      - name: paragraph_reference
        struct:
        - name: start
          dtype: int32
        - name: end
          dtype: int32
        - name: string
          dtype: string
    - name: explanation_type
      dtype: string
    - name: selected_sentence
      struct:
      - name: start
        dtype: int32
      - name: end
        dtype: int32
      - name: string
        dtype: string
  config_name: qed
  splits:
  - name: train
    num_bytes: 8602094
    num_examples: 7638
  - name: validation
    num_bytes: 1584139
    num_examples: 1355
  download_size: 14083968
  dataset_size: 10186233
---

# Dataset Card for QED

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

- **Homepage:** N/A
- **Repository:** [GitHub](https://github.com/google-research-datasets/QED)
- **Paper:** [QED: A Framework and Dataset for Explanations in Question Answering](https://arxiv.org/abs/2009.06354)
- **Leaderboard:** N/A
- **Point of Contact:** -

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