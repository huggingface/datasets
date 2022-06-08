---
pretty_name: NoReC
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- nb
- nn
- 'no'
licenses:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: norec
---

# Dataset Card Creation Guide

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

- **Repository:** https://github.com/ltgoslo/norec
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2018/pdf/851.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

This dataset contains Norwegian Review Corpus (NoReC), created for the purpose of training and evaluating models for document-level sentiment analysis. More than 43,000 full-text reviews have been collected from major Norwegian news sources and cover a range of different domains, including literature, movies, video games, restaurants, music and theater, in addition to product reviews across a range of categories. Each review is labeled with a manually assigned score of 1–6, as provided by the rating of the original author.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The sentences in the dataset are in Norwegian (nb, nn, no).

## Dataset Structure

### Data Instances

A sample from training set is provided below:

```
{'deprel': ['det',
  'amod',
  'cc',
  'conj',
  'nsubj',
  'case',
  'nmod',
  'cop',
  'case',
  'case',
  'root',
  'flat:name',
  'flat:name',
  'punct'],
 'deps': ['None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None'],
 'feats': ["{'Gender': 'Masc', 'Number': 'Sing', 'PronType': 'Dem'}",
  "{'Definite': 'Def', 'Degree': 'Pos', 'Number': 'Sing'}",
  'None',
  "{'Definite': 'Def', 'Degree': 'Pos', 'Number': 'Sing'}",
  "{'Definite': 'Def', 'Gender': 'Masc', 'Number': 'Sing'}",
  'None',
  'None',
  "{'Mood': 'Ind', 'Tense': 'Pres', 'VerbForm': 'Fin'}",
  'None',
  'None',
  'None',
  'None',
  'None',
  'None'],
 'head': ['5',
  '5',
  '4',
  '2',
  '11',
  '7',
  '5',
  '11',
  '11',
  '11',
  '0',
  '11',
  '11',
  '11'],
 'idx': '000000-02-01',
 'lemmas': ['den',
  'andre',
  'og',
  'sist',
  'sesong',
  'av',
  'Rome',
  'være',
  'ute',
  'på',
  'DVD',
  'i',
  'Norge',
  '$.'],
 'misc': ['None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  "{'SpaceAfter': 'No'}",
  'None'],
 'pos_tags': [5, 0, 4, 0, 7, 1, 11, 3, 1, 1, 11, 1, 11, 12],
 'text': 'Den andre og siste sesongen av Rome er ute på DVD i Norge.',
 'tokens': ['Den',
  'andre',
  'og',
  'siste',
  'sesongen',
  'av',
  'Rome',
  'er',
  'ute',
  'på',
  'DVD',
  'i',
  'Norge',
  '.'],
 'xpos_tags': ['None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None',
  'None']}

```


### Data Fields

The data instances have the following fields:

- deprel: [More Information Needed]
- deps: [More Information Needed]
- feats: [More Information Needed]
- head: [More Information Needed]
- idx: index
- lemmas: lemmas of all tokens
- misc: [More Information Needed]
- pos_tags: part of speech tags
- text: text string
- tokens: tokens
- xpos_tags: [More Information Needed]

The part of speech taggs correspond to these labels: "ADJ" (0), "ADP" (1), "ADV" (2), "AUX" (3), "CCONJ" (4), "DET" (5), "INTJ" (6), "NOUN" (7), "NUM" (8), "PART" (9), "PRON" (10), "PROPN" (11), "PUNCT" (12), "SCONJ" (13), "SYM" (14), "VERB" (15), "X" (16),

### Data Splits

The training, validation, and test set contain `680792`, `101106`, and `101594` sentences respectively.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

```
@InProceedings{VelOvrBer18,
  author = {Erik Velldal and Lilja {\O}vrelid and 
            Eivind Alexander Bergem and  Cathrine Stadsnes and 
            Samia Touileb and Fredrik J{\o}rgensen},
  title = {{NoReC}: The {N}orwegian {R}eview {C}orpus},
  booktitle = {Proceedings of the 11th edition of the 
               Language Resources and Evaluation Conference},
  year = {2018},
  address = {Miyazaki, Japan},
  pages = {4186--4191}
}
```

### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.
