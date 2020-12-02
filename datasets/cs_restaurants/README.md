---
annotations_creators:
- found
language_creators:
- expert-generated
- machine-generated
languages:
- cs
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-san-francisco-restaurants
task_categories:
- conditional-text-generation
- sequence-modeling
task_ids:
- dialogue-modeling
- language-modeling
- other-stuctured-to-text
---

# Dataset Card Creation Guide

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

- **Repository:** [Czech restaurants homepage](https://github.com/UFAL-DSG/cs_restaurant_dataset)
- **Paper:** [Czech restaurants on Arxiv](https://arxiv.org/abs/1910.05298)

### Dataset Summary

This is a dataset for NLG in task-oriented spoken dialogue systems with Czech as the target language. It originated as a translation of the [English San Francisco Restaurants dataset](https://www.repository.cam.ac.uk/handle/1810/251304) by Wen et al. (2015). The domain is restaurant information in Prague, with random/fictional values. It includes input dialogue acts and the corresponding outputs in Czech.

### Supported Tasks and Leaderboards

- `other-stuctured-to-text`: The dataset can be used to train a model for data-to-text generation: from a desired dialogue act, the model must produce textual output that conveys this intention.

### Languages

The entire dataset is in Czech, translated from the English San Francisco dataset by professional translators.

## Dataset Structure

### Data Instances

Example of a data instance:

```
{
  "da": "?request(area)",
  "delex_da": "?request(area)",
  "text": "Jakou lokalitu hledáte ?",
  "delex_text": "Jakou lokalitu hledáte ?"
}
```

### Data Fields

- `da`: input dialogue act
- `delex_da`: input dialogue act, delexicalized
- `text`: output text
- `delex_text`: output text, delexicalized

### Data Splits

The order of the instances is random; the split is roughly 3:1:1 between train, development, and test, ensuring that the different sections don't share the same DAs (so the generators need to generalize to unseen DAs), but they share as many generic different DA types as possible (e.g., confirm, inform_only_match etc.). DA types that only have a single corresponding DA (e.g., bye()) are included in the training set.

The training, development, and test set contain 3569, 781, and 842 instances, respectively.

## Dataset Creation

### Curation Rationale

While most current neural NLG systems do not explicitly contain language-specific components and are thus capable of multilingual generation in principle, there has been little work to test these capabilities experimentally. This goes hand in hand with the scarcity of non-English training datasets for NLG – the only data-to-text NLG set known to us is a small sportscasting Korean dataset (Chenet al., 2010), which only contains a limited number of named entities, reducing the need for their inflection. Since  most  generators  are  only  tested  on  English, they do not need to handle grammar complexities not present in English.  A prime example is the delexicalization technique used by most current generators. We create a novel dataset for Czech delexicalized generation; this extends the typical task of data-to-text  NLG  by  requiring  attribute  value inflection. We  choose  Czech  as an example of a morphologically complex language with a large set of NLP tools readily available.

### Source Data

#### Initial Data Collection and Normalization

The original data was collected from the [English San Francisco Restaurants dataset](https://www.repository.cam.ac.uk/handle/1810/251304) by Wen et al. (2015).

#### Who are the source language producers?

The original data was produced in interactions between Amazon Mechanical Turk workers and themed around San Francisco restaurants. This data was then translated into Czech and localized to Prague restaurants by professional translators.

### Annotations

No annotations.

### Personal and Sensitive Information

This data does not contain personal information.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Ondřej Dušek, Filip Jurčíček, Josef Dvořák, Petra Grycová, Matěj Hejda, Jana Olivová, Michal Starý, Eva Štichová, Charles University. This work was funded by the Ministry of Education, Youth and Sports of the Czech Republic under the grant agreement LK11221 and core research funding, SVV project 260 333, and GAUK grant 2058214 of Charles University in Prague. It used language resources stored and distributed by the LINDAT/CLARIN project of the Ministry of Education, Youth and Sports of the Czech Republic (project LM2015071).

### Licensing Information

[Creative Commons 4.0 BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)

### Citation Information

```
@article{DBLP:journals/corr/abs-1910-05298,
  author    = {Ondrej Dusek and
               Filip Jurcicek},
  title     = {Neural Generation for Czech: Data and Baselines},
  journal   = {CoRR},
  volume    = {abs/1910.05298},
  year      = {2019},
  url       = {http://arxiv.org/abs/1910.05298},
  archivePrefix = {arXiv},
  eprint    = {1910.05298},
  timestamp = {Wed, 16 Oct 2019 16:25:53 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1910-05298.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
