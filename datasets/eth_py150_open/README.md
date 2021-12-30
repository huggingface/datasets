---
annotations_creators:
- no-annotations
language_creators:
- machine-generated
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-contextual-embeddings
paperswithcode_id: eth-py150-open
---

# Dataset Card for ethpy150open

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

- **Homepage:** https://www.sri.inf.ethz.ch/py150
- **Repository:** https://github.com/google-research-datasets/eth_py150_open
- **Paper:** https://proceedings.icml.cc/static/paper_files/icml/2020/5401-Paper.pdf
- **Leaderboard:** None
- **Point of Contact:** Aditya Kanade <kanade@iisc.ac.in>, Petros Maniatis <maniatis@google.com> 

### Dataset Summary

A redistributable subset of the [ETH Py150 corpus](https://www.sri.inf.ethz.ch/py150), introduced in the ICML 2020 paper ['Learning and Evaluating Contextual Embedding of Source Code'](https://proceedings.icml.cc/static/paper_files/icml/2020/5401-Paper.pdf)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure
List of dicts of
  {
    "filepath": The relative URL containing the path to the file on GitHub
    "license": The license used for that specific file or repository
  }

### Data Instances

{
  "filepath": "0rpc/zerorpc-python/setup.py",
  "license": "mit"
},
{
  "filepath": "0rpc/zerorpc-python/zerorpc/heartbeat.py",
  "license": "mit"
},

### Data Fields

- `filepath`: The relative URL containing the path to the file on GitHub
- `license`: The license used for that specific file or repository

### Data Splits

|                            | Train   | Valid | Test  |
| -----                      | ------- | ----- | ----- |
| Dataset Split              | 74749   | 8302  | 41457 |

## Dataset Creation
The original dataset is at https://www.sri.inf.ethz.ch/py150
### Curation Rationale

To generate a more redistributable version of the dataset

### Source Data

#### Initial Data Collection and Normalization

All the urls are filepaths relative to GitHub and the master branch was used as available at the time

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

[More Information Needed]

### Licensing Information

Apache License 2.0

### Citation Information

@inproceedings{kanade2020learning,
  title={Learning and Evaluating Contextual Embedding of Source Code},
  author={Kanade, Aditya and Maniatis, Petros and Balakrishnan, Gogul and Shi, Kensen},
  booktitle={International Conference on Machine Learning},
  pages={5110--5121},
  year={2020},
  organization={PMLR}
}

### Contributions

Thanks to [@Bharat123rox](https://github.com/Bharat123rox) for adding this dataset.