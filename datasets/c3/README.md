---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- zh
license:
- other
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
paperswithcode_id: c3
pretty_name: C3
dataset_info:
- config_name: mixed
  features:
  - name: documents
    sequence: string
  - name: document_id
    dtype: string
  - name: questions
    sequence:
    - name: question
      dtype: string
    - name: answer
      dtype: string
    - name: choice
      sequence: string
  splits:
  - name: test
    num_bytes: 891619
    num_examples: 1045
  - name: train
    num_bytes: 2710513
    num_examples: 3138
  - name: validation
    num_bytes: 910799
    num_examples: 1046
  download_size: 5481785
  dataset_size: 4512931
- config_name: dialog
  features:
  - name: documents
    sequence: string
  - name: document_id
    dtype: string
  - name: questions
    sequence:
    - name: question
      dtype: string
    - name: answer
      dtype: string
    - name: choice
      sequence: string
  splits:
  - name: test
    num_bytes: 646995
    num_examples: 1627
  - name: train
    num_bytes: 2039819
    num_examples: 4885
  - name: validation
    num_bytes: 611146
    num_examples: 1628
  download_size: 4352392
  dataset_size: 3297960
---
# Dataset Card for C3

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

- **Homepage:** []()
- **Repository:** [link]()
- **Paper:** []()
- **Leaderboard:** []()
- **Point of Contact:** []()

### Dataset Summary

Machine reading comprehension tasks require a machine reader to answer questions relevant to the given document. In this paper, we present the first free-form multiple-Choice Chinese machine reading Comprehension dataset (C^3), containing 13,369 documents (dialogues or more formally written mixed-genre texts) and their associated 19,577 multiple-choice free-form questions collected from Chinese-as-a-second-language examinations.
We present a comprehensive analysis of the prior knowledge (i.e., linguistic, domain-specific, and general world knowledge) needed for these real-world problems. We implement rule-based and popular neural methods and find that there is still a significant performance gap between the best performing model (68.5%) and human readers (96.0%), especially on problems that require prior knowledge. We further study the effects of distractor plausibility and data augmentation based on translated relevant datasets for English on model performance. We expect C^3 to present great challenges to existing systems as answering 86.8% of questions requires both knowledge within and beyond the accompanying document, and we hope that C^3 can serve as a platform to study how to leverage various kinds of prior knowledge to better understand a given written or orally oriented text.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

[More Information Needed]

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

Dataset provided for research purposes only. Please check dataset license for additional information.

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
@article{sun2019investigating,
  title={Investigating Prior Knowledge for Challenging Chinese Machine Reading Comprehension},
  author={Sun, Kai and Yu, Dian and Yu, Dong and Cardie, Claire},
  journal={Transactions of the Association for Computational Linguistics},
  year={2020},
  url={https://arxiv.org/abs/1904.09679v3}
}
```


### Contributions

Thanks to [@Narsil](https://github.com/Narsil) for adding this dataset.