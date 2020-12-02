---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- crowdsourced
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
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

- **Homepage:** [MC-TACO](https://cogcomp.seas.upenn.edu/page/resource_view/125)
- **Repository:** [Github repository](https://github.com/CogComp/MCTACO)
- **Paper:** ["Going on a vacation" takes longer than "Going for a walk": A Study of Temporal Commonsense Understanding](https://arxiv.org/abs/1909.03065)
- **Leaderboard:** [AI2 Leaderboard](https://leaderboard.allenai.org/mctaco)

### Dataset Summary

MC-TACO (Multiple Choice TemporAl COmmonsense) is a dataset of 13k question-answer pairs that require temporal commonsense comprehension. A system receives a sentence providing context information, a question designed to require temporal commonsense knowledge, and multiple candidate answers. More than one candidate answer can be plausible.

### Supported Tasks and Leaderboards

The task is framed as binary classification: givent he context, the question, and the candidate answer, the task is to determine whether the candidate answer is plausible ("yes") or not ("no").

Performance is measured using two metrics:

- Exact Match -- the average number of questions for which all the candidate answers are predicted correctly.
- F1 -- is slightly more relaxed than EM. It measures the overlap between one’s predictions and the ground truth, by computing the geometric mean of Precision and Recall.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

An example looks like this:

```
{
  "sentence": "However, more recently, it has been suggested that it may date from earlier than Abdalonymus' death.",
  "question": "How often did Abdalonymus die?",
  "answer": "every two years",
  "label": "no",
  "category": "Frequency",
}
```

### Data Fields

All fields are strings:
- `sentence`: a sentence (or context) on which the question is based
- `question`: a question querying some temporal commonsense knowledge
- `answer`: a potential answer to the question (all lowercased)
- `label`: whether the answer is a correct. "yes" indicates the answer is correct/plaussible, "no" otherwise
- `category`: the temporal category the question belongs to (among "Event Ordering", "Event Duration", "Frequency", "Stationarity", and "Typical Time")

### Data Splits

The development set contains 561 questions and 3,783 candidate answers. The test set contains 1,332 questions and 9,442 candidate answers.

From the original repository:

*Note that there is no training data, and we provide the dev set as the only source of supervision. The rationale is that we believe a successful system has to bring in a huge amount of world knowledge and derive commonsense understandings prior to the current task evaluation. We therefore believe that it is not reasonable to expect a system to be trained solely on this data, and we think of the development data as only providing a definition of the task.*

## Dataset Creation

### Curation Rationale

MC-TACO is used as a testbed to study the temporal commonsense understanding on NLP systems.

### Source Data

From the original paper:

*The context sentences are randomly selected from [MultiRC](https://www.aclweb.org/anthology/N18-1023/) (from each of its 9 domains). For each sentence, we use crowdsourcing on Amazon Mechanical Turk to collect questions and candidate answers (both correct and wrong ones).*

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

From the original paper:

*To ensure the quality of the results, we limit the annotations to native speakers and use qualification tryouts.*

#### Annotation process

The crowdsourced construction/annotation of the dataset follows 4 steps described in Section 3 of the [paper](https://arxiv.org/abs/1909.03065): question generation, question verification, candidate answer expansion and answer labeling.

#### Who are the annotators?

Paid crowdsourcers.

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

Unknwon

### Citation Information

```
@inproceedings{ZKNR19,
    author = {Ben Zhou, Daniel Khashabi, Qiang Ning and Dan Roth},
    title = {“Going on a vacation” takes longer than “Going for a walk”: A Study of Temporal Commonsense Understanding },
    booktitle = {EMNLP},
    year = {2019},
}
```
