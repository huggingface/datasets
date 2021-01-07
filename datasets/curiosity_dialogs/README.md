---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- sequence-modeling-other-conversational-curiosity
---

# Dataset Card for Curiosity Dataset

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

- **Homepage:** [Curiosity Dataset Homepage](https://www.pedro.ai/curiosity)
- **Repository:** [Curiosity Dataset Repository](https://github.com/facebookresearch/curiosity)
- **Paper:** [ACL Anthology](https://www.aclweb.org/anthology/2020.emnlp-main.655/)
- **Point of Contact:** [Pedro Rodriguez](https://mailhide.io/e/wbfjM)

### Dataset Summary

Curiosity dataset consists of 14K English dialogs (181K utterances) where users and assistants converse about geographic topics like geopolitical entities and locations. This dataset is annotated with pre-existing user knowledge, message-level dialog acts, grounding to Wikipedia, and user reactions to messages.

### Supported Tasks and Leaderboards

* `sequence-modeling-other-conversational-curiosity`: The dataset can be used to train a model for Conversational Curiosity, which consists in the testing of the hypothesis that engagement increases when users are presented with facts related to what they know. Success on this task is typically measured by achieving a *high* [Accuracy](https://huggingface.co/metrics/accuracy) and [F1 Score](https://huggingface.co/metrics/f1).

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

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

[Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/legalcode)

### Citation Information

```
@inproceedings{rodriguez2020curiosity,
    title = {Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity},
    author = {Pedro Rodriguez and Paul Crook and Seungwhan Moon and Zhiguang Wang},
    year = 2020,
    booktitle = {Empirical Methods in Natural Language Processing}
}
```

