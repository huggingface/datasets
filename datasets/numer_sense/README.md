---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other
task_categories:
- sequence-modeling
task_ids:
- slot-filling
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** https://inklab.usc.edu/NumerSense/
- **Repository:** https://github.com/INK-USC/NumerSense
- **Paper:** https://arxiv.org/abs/2005.00683
- **Leaderboard:** https://inklab.usc.edu/NumerSense/#exp
- **Point of Contact:** Author emails listed in [paper](https://arxiv.org/abs/2005.00683)

### Dataset Summary

NumerSense is a new numerical commonsense reasoning probing task, with a diagnostic dataset consisting of 3,145
masked-word-prediction probes. The general idea is to mask numbers between 0-10 in sentences mined from a commonsense
corpus and evaluate whether a language model can correctly predict the masked value.

### Supported Tasks and Leaderboards

The dataset supports the task of slot-filling, specifically as an evaluation of numerical common sense. A leaderboard
is included on the [dataset webpage](https://inklab.usc.edu/NumerSense/#exp) with included benchmarks for GPT-2,
RoBERTa, BERT, and human performance. Leaderboards are included for both the core set and the adversarial set
discussed below.

### Languages

This dataset is in English.

## Dataset Structure

### Data Instances

Each instance consists of a sentence with a masked numerical value between 0-10 and (in the train set) a target.
Example from the training set:

```
sentence: Black bears are about <mask> metres tall.
target: two
```

### Data Fields

Each value of the training set consists of:
- `sentence`: The sentence with a number masked out with the `<mask>` token.
- `target`: The ground truth target value. Since the test sets do not include the ground truth, the `target` field
values are empty strings in the `test_core` and `test_all` splits.

### Data Splits

The dataset includes the following pre-defined data splits:

- A train set with >10K labeled examples (i.e. containing a ground truth value)
- A core test set (`test_core`) with 1,132 examples (no ground truth provided)
- An expanded test set (`test_all`) encompassing `test_core` with the addition of adversarial examples for a total of
3,146 examples. See section 2.2 of [the paper] for a discussion of how these examples are constructed.

## Dataset Creation

### Curation Rationale

The purpose of this dataset is "to study whether PTLMs capture numerical commonsense knowledge, i.e., commonsense
knowledge that provides an understanding of the numeric relation between entities." This work is motivated by the
prior research exploring whether language models possess _commonsense knowledge_.

### Source Data

#### Initial Data Collection and Normalization

The dataset is an extension of the [Open Mind Common Sense](https://huggingface.co/datasets/open_mind_common_sense)
corpus. A query was performed to discover sentences containing numbers between 0-12, after which the resulting
sentences were manually evaluated for inaccuracies, typos, and the expression of commonsense knowledge. The numerical
values were then masked.

#### Who are the source language producers?

The [Open Mind Common Sense](https://huggingface.co/datasets/open_mind_common_sense) corpus, from which this dataset
is sourced, is a crowdsourced dataset maintained by the MIT Media Lab.

### Annotations

#### Annotation process

No annotations are present in this dataset beyond the `target` values automatically sourced from the masked
sentences, as discussed above.

#### Who are the annotators?

The curation and inspection was done in two rounds by graduate students.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The motivation of measuring a model's ability to associate numerical values with real-world concepts appears
relatively innocuous. However, as discussed in the following section, the source dataset may well have biases encoded
from crowdworkers, particularly in terms of factoid coverage. A model's ability to perform well on this benchmark
should therefore not be considered evidence that it is more unbiased or objective than a human performing similar
tasks.

[More Information Needed]

### Discussion of Biases

This dataset is sourced from a crowdsourced commonsense knowledge base. While the information contained in the graph
is generally considered to be of high quality, the coverage is considered to very low as a representation of all
possible commonsense knowledge. The representation of certain factoids may also be skewed by the demographics of the
crowdworkers. As one possible example, the term "homophobia" is connected with "Islam" in the ConceptNet knowledge
base, but not with any other religion or group, possibly due to the biases of crowdworkers contributing to the
project.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This dataset was collected by Bill Yuchen Lin, Seyeon Lee, Rahul Khanna, and Xiang Ren, Computer Science researchers
at the at the University of Southern California.

### Licensing Information

The data is hosted in a GitHub repositor with the
[MIT License](https://github.com/INK-USC/NumerSense/blob/main/LICENSE).

### Citation Information

```
@inproceedings{lin2020numersense,
  title={Birds have four legs?! NumerSense: Probing Numerical Commonsense Knowledge of Pre-trained Language Models},
  author={Bill Yuchen Lin and Seyeon Lee and Rahul Khanna and Xiang Ren}, 
  booktitle={Proceedings of EMNLP},
  year={2020},
  note={to appear}
}
```
