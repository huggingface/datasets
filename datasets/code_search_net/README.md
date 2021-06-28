---
annotations_creators:
- no-annotation
language_creators:
- machine-generated
languages:
- code
licenses:
- other-several-licenses
multilinguality:
- multilingual
size_categories:
  all:
  - 1M<n<10M
  go:
  - 100K<n<1M
  java:
  - 100K<n<1M
  javascript:
  - 100K<n<1M
  php:
  - 100K<n<1M
  python:
  - 100K<n<1M
  ruby:
  - 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: codesearchnet
pretty_name: CodeSearchNet
---

# Dataset Card for CodeSearchNet corpus

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
- **Homepage:** https://wandb.ai/github/CodeSearchNet/benchmark
- **Repository:** https://github.com/github/CodeSearchNet
- **Paper:** https://arxiv.org/abs/1909.09436
- **Leaderboard:** https://wandb.ai/github/CodeSearchNet/benchmark/leaderboard

### Dataset Summary

CodeSearchNet corpus is a dataset of 2 milllion (comment, code) pairs from opensource libraries hosted on GitHub. It contains code and documentation for several programming languages.

CodeSearchNet corpus was gathered to support the [CodeSearchNet challenge](https://wandb.ai/github/CodeSearchNet/benchmark), to explore the problem of code retrieval using natural language.

### Supported Tasks and Leaderboards

- `language-modeling`: The dataset can be used to train a model for modelling programming languages, which consists in building language models for programming languages.

### Languages

- Go **programming** language
- Java **programming** language
- Javascript **programming** language
- PHP **programming** language
- Python **programming** language
- Ruby **programming** language

## Dataset Structure

### Data Instances

A data point consists of a function code along with its documentation. Each data point also contains meta data on the function, such as the repository it was extracted from.
```
{
  'id': '0',
  'repository_name': 'organisation/repository',
  'func_path_in_repository': 'src/path/to/file.py',
  'func_name': 'func',
  'whole_func_string': 'def func(args):\n"""Docstring"""\n [...]',
  'language': 'python', 
  'func_code_string': '[...]',
  'func_code_tokens': ['def', 'func', '(', 'args', ')', ...],
  'func_documentation_string': 'Docstring',
  'func_documentation_string_tokens': ['Docstring'],
  'split_name': 'train',
  'func_code_url': 'https://github.com/<org>/<repo>/blob/<hash>/src/path/to/file.py#L111-L150'
}
```
### Data Fields

- `id`: Arbitrary number
- `repository_name`: name of the GitHub repository
- `func_path_in_repository`: tl;dr: path to the file which holds the function in the repository
- `func_name`: name of the function in the file
- `whole_func_string`: Code + documentation of the function
- `language`: Programming language in whoch the function is written
- `func_code_string`: Function code
- `func_code_tokens`: Tokens yielded by Treesitter
- `func_documentation_string`: Function documentation
- `func_documentation_string_tokens`: Tokens yielded by Treesitter
- `split_name`: Name of the split to which the example belongs (one of train, test or valid)
- `func_code_url`: URL to the function code on Github

### Data Splits

Three splits are available:
- train
- test
- valid

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

All information can be retrieved in the [original technical review](https://arxiv.org/pdf/1909.09436.pdf)

**Corpus collection**:

Corpus has been collected from publicly available open-source non-fork GitHub repositories, using libraries.io to identify all projects which are used by at least one other project, and sort them by “popularity” as indicated by the number of stars and forks. 

Then, any projects that do not have a license or whose license does not explicitly permit the re-distribution of parts of the project were removed. Treesitter - GitHub's universal parser - has been used to then tokenize all Go, Java, JavaScript, Python, PHP and Ruby functions (or methods) using and, where available, their respective documentation text using a heuristic regular expression.

**Corpus filtering**:

Functions without documentation are removed from the corpus. This yields a set of pairs ($c_i$, $d_i$) where ci is some function documented by di. Pairs ($c_i$, $d_i$) are passed through the folllowing preprocessing tasks:

- Documentation $d_i$ is truncated to the first full paragraph to remove in-depth discussion of function arguments and return values
- Pairs in which $d_i$ is shorter than three tokens are removed
- Functions $c_i$ whose implementation is shorter than three lines are removed
- Functions whose name contains the substring “test” are removed
- Constructors and standard extenion methods (eg `__str__` in Python or `toString` in Java) are removed
- Duplicates and near duplicates functions are removed, in order to keep only one version of the function

#### Who are the source language producers?

OpenSource contributors produced the code and documentations.

The dataset was gatherered and preprocessed automatically.

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

Each example in the dataset has is extracted from a GitHub repository, and each repository has its own license. Example-wise license information is not (yet) included in this dataset: you will need to find out yourself which license the code is using.

### Citation Information

@article{husain2019codesearchnet,
  title={{CodeSearchNet} challenge: Evaluating the state of semantic code search},
  author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
  journal={arXiv preprint arXiv:1909.09436},
  year={2019}
}

### Contributions

Thanks to [@SBrandeis](https://github.com/SBrandeis) for adding this dataset.