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
- conditional-text-generation
task_ids:
- conditional-text-generation-other-dialogue-generation
---


# Dataset Card for Deal or No Deal Negotiator

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

- **Repository:** [Dataset Repository](https://github.com/facebookresearch/end-to-end-negotiator) 
- **Paper:** [Deal or No Deal? End-to-End Learning for Negotiation Dialogues](https://arxiv.org/abs/1706.05125)

### Dataset Summary

A large dataset of human-human negotiations on a multi-issue bargaining task, where agents who cannot observe each other’s reward functions must reach an agreement (or a deal) via natural language dialogue.

### Supported Tasks and Leaderboards

Train end-to-end models for negotiation

### Languages

The text in the dataset is in English

## Dataset Structure

### Data Instances

{'dialogue': 'YOU: i love basketball and reading <eos> THEM: no . i want the hat and the balls <eos> YOU: both balls ? <eos> THEM: yeah or 1 ball and 1 book <eos> YOU: ok i want the hat and you can have the rest <eos> THEM: okay deal ill take the books and the balls you can have only the hat <eos> YOU: ok <eos> THEM: <selection>',
 'input': {'count': [3, 1, 2], 'value': [0, 8, 1]},
 'output': 'item0=0 item1=1 item2=0 item0=3 item1=0 item2=2',
 'partner_input': {'count': [3, 1, 2], 'value': [1, 3, 2]}}

### Data Fields

`dialogue`: The dialogue between the agents. \
`input`: The input of the firt agent. \
`partner_input`: The input of the other agent. \
`count`: The count of the three available items. \
`value`: The value of the three available items. \
`output`: Describes how many of each of the three item typesare assigned to each agent
 

### Data Splits

|           | Tain   | Valid | Test |
| -----     | ------ | ----- | ---- |
| dialogues |  10095 |  1087 | 1052 |
| self_play |   8172 |  NA   | NA   |

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

Human workers using Amazon Mechanical Turk. They were paid $0.15 per dialogue, with a $0.05 bonus for maximal scores. Only workers based in the United States with a 95% approval rating and at least 5000 previous HITs were used.

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

The project is licenced under CC-by-NC

### Citation Information
```
@article{lewis2017deal,
  title={Deal or no deal? end-to-end learning for negotiation dialogues},
  author={Lewis, Mike and Yarats, Denis and Dauphin, Yann N and Parikh, Devi and Batra, Dhruv},
  journal={arXiv preprint arXiv:1706.05125},
  year={2017}
}
```
