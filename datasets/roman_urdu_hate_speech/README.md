---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- ur
licenses:
- mit
multilinguality:
- monolingual
pretty_name: roman_urdu_hate_speech
size_categories:
- unknown
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- text-classification-other-binary classification
---

# Dataset Card for roman_urdu_hate_speech

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** [roman_urdu_hate_speech homepage](https://aclanthology.org/2020.emnlp-main.197/)
- **Repository:** [roman_urdu_hate_speech repository](https://github.com/haroonshakeel/roman_urdu_hate_speech)
- **Paper:** [Hate-Speech and Offensive Language Detection in Roman Urdu](https://aclanthology.org/2020.emnlp-main.197.pdf)
- **Leaderboard:** [N/A]
- **Point of Contact:** [M. Haroon Shakeel](mailto:m.shakeel@lums.edu.pk)

### Dataset Summary

The Roman Urdu Hate-Speech and Offensive Language Detection (RUHSOLD) dataset is a Roman Urdu dataset of tweets annotated by experts in the relevant language. The authors develop the gold-standard for two sub-tasks. First sub-task is based on binary labels of Hate-Offensive content and Normal content (i.e., inoffensive language). These labels are self-explanatory. The authors refer to this sub-task as coarse-grained classification. Second sub-task defines Hate-Offensive content with four labels at a granular level. These labels are the most relevant for the demographic of users who converse in RU and are defined in related literature. The authors refer to this sub-task as fine-grained classification. The objective behind creating two gold-standards is to enable the researchers to evaluate the hate speech detection approaches on both easier (coarse-grained) and challenging (fine-grained) scenarios.  

### Supported Tasks and Leaderboards

- 'multi-class-classification', 'text-classification-other-binary classification': The dataset can be used for both multi class classification as well as for binary classification as it contains both coarse grained and fine grained labels.

### Languages

The text of this dataset is Roman Urdu. The associated BCP-47 code is 'ur'.

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

MIT License from the GitHub repository

### Citation Information

@inproceedings{rizwan2020hate,
  title={Hate-speech and offensive language detection in roman Urdu},
  author={Rizwan, Hammad and Shakeel, Muhammad Haroon and Karim, Asim},
  booktitle={Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  pages={2512--2522},
  year={2020}
}