---
pretty_name: Neural Code Search
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
  evaluation_dataset:
  - n<1K
  search_corpus:
  - 1M<n<10M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
  evaluation_dataset:
  - extractive-qa
  search_corpus:
  - extractive-qa
paperswithcode_id: neural-code-search-evaluation-dataset
---

# Dataset Card for Neural Code Search

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

- **Homepage:**
[facebookresearch
/
Neural-Code-Search-Evaluation-Dataset](https://github.com/facebookresearch/Neural-Code-Search-Evaluation-Dataset/tree/master/data)
- **Repository:**
[Github](https://github.com/facebookresearch/Neural-Code-Search-Evaluation-Dataset.git)
- **Paper:**
[arXiv](https://arxiv.org/pdf/1908.09804.pdf)

### Dataset Summary

Neural-Code-Search-Evaluation-Dataset presents an evaluation dataset consisting of natural language query and code snippet pairs, with the hope that future work in this area can use this dataset as a common benchmark. We also provide the results of two code search models (NCS, UNIF) from recent work.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

EN - English

## Dataset Structure

### Data Instances

#### Search Corpus
The search corpus is indexed using all method bodies parsed from the 24,549 GitHub repositories. In total, there are 4,716,814 methods in this corpus. The code search model will find relevant code snippets (i.e. method bodies) from this corpus given a natural language query. In this data release, we will provide the following information for each method in the corpus:

#### Evaluation Dataset
The evaluation dataset is composed of 287 Stack Overflow question and answer pairs

### Data Fields

#### Search Corpus
- id: Each method in the corpus has a unique numeric identifier. This ID number will also be referenced in our evaluation dataset.
- filepath: The file path is in the format of :owner/:repo/relative-file-path-to-the-repo
method_name
- start_line: Starting line number of the method in the file.
- end_line: Ending line number of the method in the file.
- url: GitHub link to the method body with commit ID and line numbers encoded.

#### Evaluation Dataset
- stackoverflow_id: Stack Overflow post ID.
- question: Title fo the Stack Overflow post.
- question_url: URL of the Stack Overflow post.
- answer: Code snippet answer to the question.

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The most popular Android repositories on GitHub (ranked by the number of stars) is used to create the search corpus. For each repository that we indexed, we provide the link, specific to the commit that was used.5 In total, there are 24,549 repositories.

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

Hongyu Li, Seohyun Kim and Satish Chandra

### Licensing Information

CC-BY-NC 4.0 (Attr Non-Commercial Inter.)

### Citation Information

arXiv:1908.09804 [cs.SE]
### Contributions

Thanks to [@vinaykudari](https://github.com/vinaykudari) for adding this dataset.