---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- other-LDC User Agreement for Non-Members
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: null
---

# Dataset Card for Penn Treebank

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

- **Homepage:** https://catalog.ldc.upenn.edu/LDC99T42

- **Repository:** 'https://raw.githubusercontent.com/wojzaremba/lstm/master/data/ptb.train.txt',
  'https://raw.githubusercontent.com/wojzaremba/lstm/master/data/ptb.valid.txt',
  'https://raw.githubusercontent.com/wojzaremba/lstm/master/data/ptb.test.txt'
- **Paper:** https://www.aclweb.org/anthology/J93-2004.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

This is the Penn Treebank Project: Release 2 CDROM, featuring a million words of 1989 Wall Street Journal material. 
The rare words in this version are already replaced with <unk> token. The numbers are replaced with <N> token.

### Supported Tasks and Leaderboards

Language Modelling

### Languages

The text in the dataset is in American English

## Dataset Structure

### Data Instances

[Needs More Information]

### Data Fields

[Needs More Information]

### Data Splits

[Needs More Information]

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

@article{marcus-etal-1993-building,
    title = "Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank",
    author = "Marcus, Mitchell P.  and
      Santorini, Beatrice  and
      Marcinkiewicz, Mary Ann",
    journal = "Computational Linguistics",
    volume = "19",
    number = "2",
    year = "1993",
    url = "https://www.aclweb.org/anthology/J93-2004",
    pages = "313--330",
}
### Contributions

Thanks to [@harshalmittal4](https://github.com/harshalmittal4) for adding this dataset.