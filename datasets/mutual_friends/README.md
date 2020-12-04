---
TODO
---

# Dataset Card Creation Guide

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

- **Homepage:** [)](https://stanfordnlp.github.io/cocoa/)
- **Repository:** [Github repository](https://github.com/stanfordnlp/cocoa)
- **Paper:** [Learning Symmetric Collaborative Dialogue Agents with Dynamic Knowledge Graph Embeddings (ACL 2017)](https://arxiv.org/abs/1704.07130)

### Dataset Summary

Our goal is to build systems that collaborate with people by exchanging information through natural language and reasoning over structured knowledge base. In the MutualFriend task, two agents, A and B, each have a private knowledge base, which contains a list of friends with multiple attributes (e.g., name, school, major, etc.). The agents must chat with each other to find their unique mutual friend.

### Supported Tasks and Leaderboards

We consider two agents, each with a private knowledge base of items, who must communicate their knowlege to achieve a common goal. Specifically, we designed the MutualFriends task (see the figure below). Each agent has a list of friends with attributes like school, major etc. They must chat with each other to find the unique mutual friend.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

TODO

Provide an JSON-formatted example and brief description of a typical instance in the dataset. If available, provide a link to further examples.

```
{
  'example_field': ...,
  ...
}
```

Provide any additional information that is not covered in the other sections about the data here. In particular describe any relationships between data points and if these relationships are made explicit.

### Data Fields

TODO

List and describe the fields present in the dataset. Mention their data type, and whether they are used as input or output in any of the tasks the dataset currently supports. If the data has span indices, describe their attributes, such as whether they are at the character level or word level, whether they are contiguous or not, etc. If the datasets contains example IDs, state whether they have an inherent meaning, such as a mapping to other datasets or pointing to relationships between data points.

- `example_field`: description of `example_field`

### Data Splits

TODO

Describe and name the splits in the dataset if there are more than one.

Describe any criteria for splitting the data, if used. If their are differences between the splits (e.g. if the training annotations are machine-generated and the dev and test ones are created by humans, or if different numbers of annotators contributed to each example), describe them here.

Provide the sizes of each split. As appropriate, provide any descriptive statistics for the features, such as average length.  For example:

|                            | Tain   | Valid | Test |
| -----                      | ------ | ----- | ---- |
| Input Sentences            |        |       |      |
| Average Sentence Length    |        |       |      |

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

```
@inproceedings{he-etal-2017-learning,
    title = "Learning Symmetric Collaborative Dialogue Agents with Dynamic Knowledge Graph Embeddings",
    author = "He, He  and
      Balakrishnan, Anusha  and
      Eric, Mihail  and
      Liang, Percy",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1162",
    doi = "10.18653/v1/P17-1162",
    pages = "1766--1776",
    abstract = "We study a \textit{symmetric collaborative dialogue} setting in which two agents, each with private knowledge, must strategically communicate to achieve a common goal. The open-ended dialogue state in this setting poses new challenges for existing dialogue systems. We collected a dataset of 11K human-human dialogues, which exhibits interesting lexical, semantic, and strategic elements. To model both structured knowledge and unstructured language, we propose a neural model with dynamic knowledge graph embeddings that evolve as the dialogue progresses. Automatic and human evaluations show that our model is both more effective at achieving the goal and more human-like than baseline neural and rule-based models.",
}
```
