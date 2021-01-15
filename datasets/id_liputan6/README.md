---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- id
licenses:
- 
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
---

# Dataset Card for Large-scale Indonesian Summarization

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

- **Homepage:** [IndoLEM (Indonesian Language Evaluation Montage)](https://indolem.github.io/)
- **Repository:** [Liputan6: Summarization Corpus for Indonesian](https://github.com/fajri91/sum_liputan6/)
- **Paper:** https://arxiv.org/abs/2011.00679
- **Leaderboard:**
- **Point of Contact:** [Fajri Koto](mailto:feryandi.n@gmail.com),
[Jey Han Lau](mailto:jeyhan.lau@gmail.com), [Timothy Baldwin](mailto:tbaldwin@unimelb.edu.au), 

### Dataset Summary

In this paper, we introduce a large-scale Indonesian summarization dataset. We harvest articles from this http URL,
an online news portal, and obtain 215,827 document-summary pairs. We leverage pre-trained language models to develop
benchmark extractive and abstractive summarization methods over the dataset with multilingual and monolingual
BERT-based models. We include a thorough error analysis by examining machine-generated summaries that have
low ROUGE scores, and expose both issues with ROUGE it-self, as well as with extractive and abstractive
summarization models.

You need to manually request the liputan6 dataset from https://github.com/fajri91/sum_liputan6/
and save it in a directory <path/to/folder>. The name of downloaded file is "liputan6_data.tar.gz".
The liputan6 dataset can then be loaded using the following command 
`datasets.load_dataset("id_liputan6", 'canonical', data_dir="<path/to/folder>")`.
### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
Indonesian

## Dataset Structure
```
{
  'id': 'string',
  'url': 'string',
  'clean_article': 'string',
  'clean_article': 'string',
  'extractive_summary': 'string'
}
```
### Data Instances

[More Information Needed]

### Data Fields
- `id`: id of the sample
- `url`: the url to the original article
- `clean_article`: the original article
- `clean_article`: the abstractive summarization
- `extractive_summary`: the extractive summarization

### Data Splits

The dataset is splitted in to train, validation and test sets.

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
@inproceedings{Koto2020Liputan6AL,
  title={Liputan6: A Large-scale Indonesian Dataset for Text Summarization},
  author={Fajri Koto and Jey Han Lau and Timothy Baldwin},
  booktitle={AACL/IJCNLP},
  year={2020}
}
