---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- ar
licenses: []
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
---

# Dataset Card for CANER

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** 
- **Repository:** [Classical-Arabic-Named-Entity-Recognition-Corpus](https://github.com/RamziSalah)
- **Paper:** [Researchgate](https://www.researchgate.net/publication/330075080_BUILDING_THE_CLASSICAL_ARABIC_NAMED_ENTITY_RECOGNITION_CORPUS_CANERCORPUS)
- **Leaderboard:**
- **Point of Contact:** 

### Dataset Summary

The Classical Arabic Named Entity Recognition corpus is a new corpus of tagged data that can be useful for handling the issues in recognition of Arabic named entities.

### Supported Tasks and Leaderboards

- Named Entity Recognition

### Languages

Classical Arabic

## Dataset Structure

### Data Instances

An example from the dataset:
```
{'ner_tag': 1, 'token': 'الجامع'}
```
Where 1 stands for "Book"

### Data Fields

- `id`: id of the sample
 - `token`: the tokens of the example text
 - `ner_tag`: the NER tags of each token

The NER tags correspond to this list:
 ```
"Allah",
"Book",
"Clan",
"Crime",
"Date",
"Day",
"Hell",
"Loc",
"Meas",
"Mon",
"Month",
"NatOb",
"Number",
"O",
"Org",
"Para",
"Pers",
"Prophet",
"Rlig",
"Sect",
"Time"
 ```

### Data Splits

Training splits only

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

Ramzi Salah and Lailatul Qadri Zakaria

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

[More Information Needed]

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

@article{article,
author = {Salah, Ramzi and Zakaria, Lailatul},
year = {2018},
month = {12},
pages = {},
title = {BUILDING THE CLASSICAL ARABIC NAMED ENTITY RECOGNITION CORPUS (CANERCORPUS)},
volume = {96},
journal = {Journal of Theoretical and Applied Information Technology}
}

### Contributions

Thanks to [@KMFODA](https://github.com/KMFODA) for adding this dataset.