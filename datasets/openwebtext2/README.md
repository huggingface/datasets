---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
pretty_name: OpenWebText2
size_categories:
- unknown
source_datasets: []
task_categories:
- sequence-modeling
- text-scoring
task_ids:
- language-modeling
- text-scoring-other-rating
---

# Dataset Card for openwebtext2

## Table of Contents
- [Dataset Card for openwebtext2](#dataset-card-for-openwebtext2)
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

## Dataset Description

- **Homepage:** https://openwebtext2.readthedocs.io/en/latest/
- **Repository:** [Needs More Information]
- **Paper:** https://arxiv.org/abs/2101.00027
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

OpenWebText2 is part of EleutherAi/The Pile dataset and is an enhanced version of the original OpenWebTextCorpus covering all Reddit submissions from 2005 up until April 2020, with further months becoming available after the corresponding PushShift dump files are released.

|download_size|27.3 Gib|
|dataset_size|63.8 Gib|

### Supported Tasks and Leaderboards

- `lm`

### Languages

- `en`

## Dataset Structure

### Data Instances

```
{'title': 'title',
'text': 'some text',
'reddit_scores': [6],}
```

### Data Fields

- `title`
- `text`
- `reddit_scores`

### Data Splits

|split|num examples|
--------------------------------
|train|17103059|

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

[Needs More Information]