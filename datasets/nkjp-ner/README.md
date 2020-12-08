---
annotations_creators:
- expert-generated
language_creators:
- other
languages:
- pl
licenses:
- gpl-3.0
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

- **Homepage:**
http://nkjp.pl/index.php?page=0&lang=1
- **Repository:**
- **Paper:**
@book{przepiorkowski2012narodowy,
title={Narodowy korpus j{\k{e}}zyka polskiego},
author={Przepi{\'o}rkowski, Adam},
year={2012},
publisher={Naukowe PWN}
- **Leaderboard:**
- **Point of Contact:**
adamp@ipipan.waw.pl

### Dataset Summary

A linguistic corpus is a collection of texts where one can find the typical use of a single word or a phrase, as well as their meaning and grammatical function. Nowadays, without access to a language corpus, it has become impossible to do linguistic research, to write dictionaries, grammars and language teaching books, to create search engines sensitive to Polish inflection, machine translation engines and software of advanced language technology. Language corpora have become an essential tool for linguists, but they are also helpful for software engineers, scholars of literature and culture, historians, librarians and other specialists of art and computer sciences.
The manually annotated 1-million word subcorpus of the NJKP, available on GNU GPL v.3

### Supported Tasks and Leaderboards

Named entity recognition

[More Information Needed]

### Languages

Polish

## Dataset Structure

### Data Instances

Two tsv files (train, dev) with two columns (sentence, target) and one (test) with just one (sentence). 

### Data Fields

- sentence
- target

### Data Splits

Data is splitted in train/dev/test split.

## Dataset Creation

### Curation Rationale

This dataset is one of nine evaluation tasks to improve polish language processing.

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

GNU GPL v.3

### Citation Information

@book{przepiorkowski2012narodowy,
title={Narodowy korpus j{\k{e}}zyka polskiego},
author={Przepi{\'o}rkowski, Adam},
year={2012},
publisher={Naukowe PWN}
}
