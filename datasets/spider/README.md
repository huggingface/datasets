---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
- machine-generated
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- other-structured-to-text
paperswithcode_id: spider-1
pretty_name: Spider
---


# Dataset Card for Spider

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

- **Homepage:** https://yale-lily.github.io/spider
- **Repository:** https://github.com/taoyds/spider
- **Paper:** https://www.aclweb.org/anthology/D18-1425/
- **Point of Contact:** [Yale LILY](https://yale-lily.github.io/)

### Dataset Summary

Spider is a large-scale complex and cross-domain semantic parsing and text-to-SQL dataset annotated by 11 Yale students
The goal of the Spider challenge is to develop natural language interfaces to cross-domain databases

### Supported Tasks and Leaderboards

The leaderboard can be seen at https://yale-lily.github.io/spider

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

**What do the instances that comprise the dataset represent?**

Each instance is natural language question and the equivalent SQL query

**How many instances are there in total?**

**What data does each instance consist of?**

[More Information Needed]

### Data Fields

* **db_id**: Database name
* **question**: Natural language to interpret into SQL
* **query**: Target SQL query
* **query_toks**: List of tokens for the query
* **query_toks_no_value**: List of tokens for the query
* **question_toks**: List of tokens for the question

### Data Splits

**train**: 7000 questions and SQL query pairs
**dev**: 1034 question and SQL query pairs

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

#### Who are the source language producers?

[More Information Needed]

### Annotations

The dataset was annotated by 11 college students at Yale University

#### Annotation process

#### Who are the annotators?

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

## Additional Information

The listed authors in the homepage are maintaining/supporting the dataset. 

### Dataset Curators

[More Information Needed]

### Licensing Information

The spider dataset is licensed under 
the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode)

[More Information Needed]

### Citation Information

```
@article{yu2018spider,
  title={Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-sql task},
  author={Yu, Tao and Zhang, Rui and Yang, Kai and Yasunaga, Michihiro and Wang, Dongxu and Li, Zifan and Ma, James and Li, Irene and Yao, Qingning and Roman, Shanelle and others},
  journal={arXiv preprint arXiv:1809.08887},
  year={2018}
}
```

### Contributions

Thanks to [@olinguyen](https://github.com/olinguyen) for adding this dataset.
