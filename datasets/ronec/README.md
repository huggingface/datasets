---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
- found
languages:
- ro
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
---

# Dataset Card for [Needs More Information]

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

- **Homepage:** https://github.com/dumitrescustefan/ronec
- **Repository:** https://github.com/dumitrescustefan/ronec
- **Paper:** https://arxiv.org/abs/1909.01247
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** dumitrescu.stefan@gmail.com, avram.andreimarius@gmail.com

### Dataset Summary

The RONEC (Named Entity Corpus for the Romanian language) dataset  contains over 26000 entities in ~5000 annotated sentence,
belonging to 16 distinct classes. It represents the first initiative in the Romanian language space specifically targeted for named entity recognition.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Romanian (`ro`)

## Dataset Structure

### Data Instances

{'end': [19, 28, 42, 80], 
 'id': '1', 
 'ronec_class': [13, 4, 13, 8], 
 'sentence': ['Secretarul de stat al S.U.A., Colin Powell, începe un turneu în țările asiatice afectate de valurile seismice uriașe.'], 
 'start': [1, 22, 31, 72]
}

### Data Fields

- `id`: a `string` feature describing the index of the sentence in the dataset
- `sentence`: a `list` of `string` features.
- `start`: a `list` of `int32` features describing the start positions of each label in a sentence. Since a sentence can have more than one label, start will be a list with the starting offset of each label.
- `end`: a `list` of `int32` features describing the start positions of each label in a sentence. Since a sentence can have more than one label, start will be a list with the starting offset of each label.
- `ronec_class`: a `list` of classification labels, with possible values including `O`, `DATETIME`, `EVENT`, `FACILITY`, `GPE` etc.

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

The corpus creation process involved a small number ofpeople that have voluntarily joined the initiative, with theauthors of this paper directing the wor

#### Who are the annotators?

Stefan Dumitrescu, Marius Avram

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

MIT License

### Citation Information

@article{dumitrescu2019introducing,
  title={Introducing RONEC--the Romanian Named Entity Corpus},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei-Marius},
  journal={arXiv preprint arXiv:1909.01247},
  year={2019}
}
