---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
- structure-prediction
task_ids:
- closed-domain-qa
- extractive-qa
- question-answering-other-yes-no-qa
- structure-prediction-other-output-structure
---

# Dataset Card for "ZEST: ZEroShot learning from Task descriptions"

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

- **Homepage:** https://allenai.org/data/zest
- **Repository:** https://github.com/allenai/zest
- **Paper:** https://arxiv.org/abs/2011.08115
- **Leaderboard:** https://leaderboard.allenai.org/zest/submissions/public
- **Point of Contact:**

### Dataset Summary

ZEST tests whether NLP systems can perform unseen tasks in a zero-shot way, given a natural language description of
the task. It is an instantiation of our proposed framework "learning from task descriptions". The tasks include
classification, typed entity extraction and relationship extraction, and each task is paired with 20 different
annotated (input, output) examples. ZEST's structure allows us to systematically test whether models can generalize
in five different ways.

### Supported Tasks and Leaderboards

A [leaderboard](https://leaderboard.allenai.org/zest/submissions/public) is included with accepatbility metrics for
each of the four generalization types outlined in the paper. The metrics are novel acceptability metrics also
proposed by the authors.

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

To evaluate the ability of a model to generalize to unseen tasks based only on a task description in a zero-shot
manner.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Mechanical Turk crowdsource workers.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

Mechanical Turk crowdsource workers.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The dataset emphasizes a model's ability to generalize to unseen tasks with only a natural language description of
the task. The long-term vision of this type of evaluation is to facilitate the creation of models which can perform
arbitrary tasks with only a prompt from a non-technical user. This could broaden the frontier of what a user can
ask something like a chatbot to do for them, but it is unclear how restrictions would be put in place to prevent
users from prompting a system to perform unethical tasks.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

This dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Citation Information

```
@inproceedings{weller-etal-2020-learning,
    title = "Learning from Task Descriptions",
    author = "Weller, Orion  and
      Lourie, Nicholas  and
      Gardner, Matt  and
      Peters, Matthew",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.105",
    pages = "1361--1375",
    abstract = "Typically, machine learning systems solve new tasks by training on thousands of examples. In contrast, humans can solve new tasks by reading some instructions, with perhaps an example or two. To take a step toward closing this gap, we introduce a framework for developing NLP systems that solve new tasks after reading their descriptions, synthesizing prior work in this area. We instantiate this frame- work with a new English language dataset, ZEST, structured for task-oriented evaluation on unseen tasks. Formulating task descriptions as questions, we ensure each is general enough to apply to many possible inputs, thus comprehensively evaluating a model{'}s ability to solve each task. Moreover, the dataset{'}s structure tests specific types of systematic generalization. We find that the state-of-the-art T5 model achieves a score of 12% on ZEST, leaving a significant challenge for NLP researchers.",
}
```

