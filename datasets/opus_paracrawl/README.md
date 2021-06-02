---
annotations_creators:
- found
language_creators:
- found
languages:
- bg
- ca
- cs
- da
- de
- el
- en
- es
- et
- eu
- fi
- fr
- ga
- gl
- ha
- hr
- hu
- ig
- is
- it
- km
- lt
- lv
- mt
- my
- nb
- ne
- nl
- nn
- pl
- pt
- ro
- ru
- si
- sk
- sl
- so
- sv
- sw
- tl
licenses:
- cc0-1.0
multilinguality:
- multilingual
size_categories:
  de-pl:
  - 100K<n<1M
  el-en:
  - 1M<n<10M
  en-ha:
  - 10K<n<100K
  en-ig:
  - 10K<n<100K
  en-km:
  - 10K<n<100K
  en-so:
  - 10K<n<100K
  en-sw:
  - 100K<n<1M
  en-tl:
  - 100K<n<1M
  es-gl:
  - 1M<n<10M
  fr-nl:
  - 1M<n<10M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
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

- **Homepage:** http://opus.nlpl.eu/ParaCrawl.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/ParaCrawl.php
E.g.

`dataset = load_dataset("paracrawl", lang1="en", lang2="so")`

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

- Creative commons CC0 (no rights reserved)

### Citation Information

@InProceedings{TIEDEMANN12.463,
author = {J{\"o}rg Tiedemann},
title = {Parallel Data, Tools and Interfaces in OPUS},
booktitle = {Proceedings of the Eight International Conference on Language Resources and Evaluation (LREC'12)},
year = {2012},
month = {may},
date = {23-25},
address = {Istanbul, Turkey},
editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Mehmet Ugur Dogan and Bente Maegaard and Joseph Mariani and Jan Odijk and Stelios Piperidis},
publisher = {European Language Resources Association (ELRA)},
isbn = {978-2-9517408-7-7},
language = {english}
}

### Contributions

Thanks to [@rkc007](https://github.com/rkc007) for adding this dataset.