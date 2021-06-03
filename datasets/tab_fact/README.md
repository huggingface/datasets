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
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- fact-checking
paperswithcode_id: tabfact
---

# Dataset Card Creation Guide

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

- **Homepage:** [TabFact](https://tabfact.github.io/index.html)
- **Repository:** [GitHub](https://github.com/wenhuchen/Table-Fact-Checking)
- **Paper:** [TabFact: A Large-scale Dataset for Table-based Fact Verification](https://arxiv.org/abs/1909.02164)
- **Leaderboard:** [Leaderboard](https://competitions.codalab.org/competitions/21611)
- **Point of Contact:** [Wenhu Chen](wenhuchen@cs.ucsb.edu)

### Dataset Summary

The problem of verifying whether a textual hypothesis holds the truth based on the given evidence, also known as fact verification, plays an important role in the study of natural language understanding and semantic representation. However, existing studies are restricted to dealing with unstructured textual evidence (e.g., sentences and passages, a pool of passages), while verification using structured forms of evidence, such as tables, graphs, and databases, remains unexplored. TABFACT is large scale dataset with 16k Wikipedia tables as evidence for 118k human annotated statements designed for fact verification with semi-structured evidence. The statements are labeled as either ENTAILED or REFUTED. TABFACT is challenging since it involves both soft linguistic reasoning and hard symbolic reasoning.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

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
@inproceedings{2019TabFactA,
  title={TabFact : A Large-scale Dataset for Table-based Fact Verification},
  author={Wenhu Chen, Hongmin Wang, Jianshu Chen, Yunkai Zhang, Hong Wang, Shiyang Li, Xiyou Zhou and William Yang Wang},
  booktitle = {International Conference on Learning Representations (ICLR)},
  address = {Addis Ababa, Ethiopia},
  month = {April},
  year = {2020}
}
```

### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.