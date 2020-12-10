---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- id
licenses:
- other-nergrit-license
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
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

- **Homepage:** [Nergrit](https://ner.grit.id/)
- **Repository:** [Nergrit Corpus](https://github.com/grit-id/nergrit-corpus)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Nergrit Corpus is a dataset collection of Indonesian Named Entity Recognition, Statement Extraction, 
and Sentiment Analysis developed by [Gria Inovasi Teknologi (GRIT)](https://grit.id/). 
This `id_nergrit_ner` dataset contains the Named Entity Recognition part of the collection.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Indonesian

## Dataset Structure

A data point consists of sentences seperated by empty line and tab-seperated tokens and tags. 
{'id': '0',
 'ner_tags': [9, 28, 28, 38, 38, 38],
 'tokens': ['Gubernur', 'Bank', 'Indonesia', 'menggelar', 'konferensi', 'pers']
}

### Data Instances

[More Information Needed]

### Data Fields
- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

The NER tags correspond to this list:
```
"B-CRD", "B-DAT", "B-EVT", "B-FAC", "B-GPE", "B-LAN", "B-LAW", "B-LOC", "B-MON", "B-NOR", 
"B-ORD", "B-ORG", "B-PER", "B-PRC", "B-PRD", "B-QTY", "B-REG", "B-TIM", "B-WOA",
"I-CRD", "I-DAT", "I-EVT", "I-FAC", "I-GPE", "I-LAN", "I-LAW", "I-LOC", "I-MON", "I-NOR",
"I-ORD", "I-ORG", "I-PER", "I-PRC", "I-PRD", "I-QTY", "I-REG", "I-TIM", "I-WOA", "O",
```
The NER tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any 
non-initial word. The dataset contains 19 following entities
```
    'CRD': Cardinal
    'DAT': Date
    'EVT': Event
    'FAC': Facility
    'GPE': Geopolitical Entity
    'LAW': Law Entity (such as Undang-Undang)
    'LOC': Location
    'MON': Money
    'NOR': Political Organization
    'ORD': Ordinal
    'ORG': Organization
    'PER': Person
    'PRC': Percent
    'PRD': Product
    'QTY': Quantity
    'REG': Religion
    'TIM': Time
    'WOA': Work of Art
    'LAN': Language
```

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
The annotators are listed in the
[Nergrit Corpus repository](https://github.com/grit-id/nergrit-corpus)

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

[More Information Needed]
