---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- en
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
pretty_name: Stack Exchange
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
---

# Dataset Card for Stack Exchange

## Table of Contents
- [Dataset Card for Stack Exchange](#dataset-card-for-the_pile_stack_exchange)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
  - [|split|num examples|](#splitnum-examples)
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
    - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [GitHub](https://github.com/EleutherAI/stackexchange-dataset)
- **Repository:** [Needs More Information]
- **Paper:** [arXiv](https://arxiv.org/abs/2101.00027)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

This dataset is part of EleutherAI/The Pile dataset and is a dataset for Language Models from processing stackexchange data dump, which is an anonymized dump of all user-contributed content on the Stack Exchange network.

|download_size|34.28 Gib|
|dataset_size|10.3 Gib|

### Supported Tasks and Leaderboards

The dataset is used for Language Modeling.

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

```
{'domain': 'chemistry',
'text':"\nQ:                                                                                                                                            \n                                                                                                                                              \nReviving old questions or asking a new one?                                                                                                   \n                                                                                                                                              \nI'm relatively new to the Chemistry SE community, and sometimes when I go to ask a question, I notice that the same (or similar) question has \nalready been asked. However, the previous question doesn't have a good answer (or is unanswered). In this case, is it better to ask the questi\non again in a new post (which might be marked as duplicate) or comment on the old post (which might be several years old)? In other words, wha\nt are the customs of this site in regards to reviving old questions/discussions?\n\nA:\n\nAs Martin commented, it really depends on the type of question. In any case, you always have the following possibilities:\n\nAsk a new question\nEdit the question to bump it to the first page\nAdd a bounty\nBring it to the attention of people in chat\n\nConsider the following cases:\n\nI have exactly the same question as asked and unanswered before!\n\nIf you ask a new question which turns out to be the same question, it may be closed as a dupe (depending on whether users remember the old que\nstion). Not the ideal option.\nIf you can find something substantial to edit and bump the question, do so. Maybe add a comment that you would really love an answer.\nIf you can spare some rep for a bounty (50 is usually enough), do so.\nYou can always bring it to the attention of people in chat.\n",}
```

### Data Fields

- `domain`: Stack Exchange domain of the sample
- `text`: Text content containing both the question and the answer

### Data Splits

|split|num examples|
--------------------------------
|train|5096117|

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

```
@article{pile,
    title={The {P}ile: An 800GB Dataset of Diverse Text for Language Modeling},
    author={Gao, Leo and Biderman, Stella and Black, Sid and Golding, Laurence and Hoppe, Travis and Foster, Charles and Phang, Jason and He, Horace and Thite, Anish and Nabeshima, Noa and Presser, Shawn and Leahy, Connor},
    journal={arXiv preprint arXiv:2101.00027},
    year={2020}
}
```

### Contributions
Thanks to [sdtblck](https://github.com/sdtblck) for creating the dataset.
Thanks to [richarddwang](https://github.com/richarddwang) for adding the dataset.
