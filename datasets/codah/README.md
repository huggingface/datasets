---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
paperswithcode_id: codah
pretty_name: COmmonsense Dataset Adversarially-authored by Humans
dataset_info:
- config_name: codah
  features:
  - name: id
    dtype: int32
  - name: question_category
    dtype:
      class_label:
        names:
          0: Idioms
          1: Reference
          2: Polysemy
          3: Negation
          4: Quantitative
          5: Others
  - name: question_propmt
    dtype: string
  - name: candidate_answers
    sequence: string
  - name: correct_answer_idx
    dtype: int32
  splits:
  - name: train
    num_bytes: 571208
    num_examples: 2776
  download_size: 485130
  dataset_size: 571208
- config_name: fold_0
  features:
  - name: id
    dtype: int32
  - name: question_category
    dtype:
      class_label:
        names:
          0: Idioms
          1: Reference
          2: Polysemy
          3: Negation
          4: Quantitative
          5: Others
  - name: question_propmt
    dtype: string
  - name: candidate_answers
    sequence: string
  - name: correct_answer_idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 112109
    num_examples: 555
  - name: train
    num_bytes: 344912
    num_examples: 1665
  - name: validation
    num_bytes: 114211
    num_examples: 556
  download_size: 485130
  dataset_size: 571232
- config_name: fold_1
  features:
  - name: id
    dtype: int32
  - name: question_category
    dtype:
      class_label:
        names:
          0: Idioms
          1: Reference
          2: Polysemy
          3: Negation
          4: Quantitative
          5: Others
  - name: question_propmt
    dtype: string
  - name: candidate_answers
    sequence: string
  - name: correct_answer_idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 116031
    num_examples: 555
  - name: train
    num_bytes: 340990
    num_examples: 1665
  - name: validation
    num_bytes: 114211
    num_examples: 556
  download_size: 485130
  dataset_size: 571232
- config_name: fold_2
  features:
  - name: id
    dtype: int32
  - name: question_category
    dtype:
      class_label:
        names:
          0: Idioms
          1: Reference
          2: Polysemy
          3: Negation
          4: Quantitative
          5: Others
  - name: question_propmt
    dtype: string
  - name: candidate_answers
    sequence: string
  - name: correct_answer_idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 114728
    num_examples: 555
  - name: train
    num_bytes: 342293
    num_examples: 1665
  - name: validation
    num_bytes: 114211
    num_examples: 556
  download_size: 485130
  dataset_size: 571232
- config_name: fold_3
  features:
  - name: id
    dtype: int32
  - name: question_category
    dtype:
      class_label:
        names:
          0: Idioms
          1: Reference
          2: Polysemy
          3: Negation
          4: Quantitative
          5: Others
  - name: question_propmt
    dtype: string
  - name: candidate_answers
    sequence: string
  - name: correct_answer_idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 114177
    num_examples: 555
  - name: train
    num_bytes: 342844
    num_examples: 1665
  - name: validation
    num_bytes: 114211
    num_examples: 556
  download_size: 485130
  dataset_size: 571232
- config_name: fold_4
  features:
  - name: id
    dtype: int32
  - name: question_category
    dtype:
      class_label:
        names:
          0: Idioms
          1: Reference
          2: Polysemy
          3: Negation
          4: Quantitative
          5: Others
  - name: question_propmt
    dtype: string
  - name: candidate_answers
    sequence: string
  - name: correct_answer_idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 114211
    num_examples: 556
  - name: train
    num_bytes: 342844
    num_examples: 1665
  - name: validation
    num_bytes: 114177
    num_examples: 555
  download_size: 485130
  dataset_size: 571232
---

# Dataset Card for COmmonsense Dataset Adversarially-authored by Humans

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

- **Homepage:** [Add homepage URL here if available (unless it's a GitHub repository)]()
- **Repository:** [If the dataset is hosted on github or has a github homepage, add URL here]()
- **Paper:** [If the dataset was introduced by a paper or there was a paper written describing the dataset, add URL here (landing page for Arxiv paper preferred)]()
- **Leaderboard:** [If the dataset supports an active leaderboard, add link here]()
- **Point of Contact:** [If known, name and email of at least one person the reader can contact for questions about the dataset.]()

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