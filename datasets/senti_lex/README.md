---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- af
- an
- az
licenses:
- gpl-3.0
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for SentiWS

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

- **Homepage:** https://wortschatz.uni-leipzig.de/en/download
- **Repository:** [Needs More Information]
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2010/pdf/490_Paper.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

This dataset add sentiment lexicons for 81 languages generated via graph propagation based on a knowledge graph--a graphical representation of real-world entities and the links between them

### Supported Tasks and Leaderboards

Sentiment-Classification

### Languages

Afrikaans
Aragonese
Arabic
Azerbaijani
Belarusian
Bulgarian
Bengali
Breton
Bosnian
Catalan; Valencian
Czech
Welsh
Danish
German
Greek, Modern
Esperanto
Spanish; Castilian
Estonian
Basque
Persian
Finnish
Faroese
French
Western Frisian
Irish
Scottish Gaelic; Gaelic
Galician
Gujarati
Hebrew (modern)
Hindi
Croatian
Haitian; Haitian Creole
Hungarian
Armenian
Interlingua
Indonesian
Ido
Icelandic
Italian
Georgian
Khmer
Kannada
Korean
Kurdish
Kirghiz, Kyrgyz
Latin
Luxembourgish, Letzeburgesch
Lithuanian
Latvian
Macedonian
Marathi (Marāṭhī)
Malay
Maltese
Dutch
Norwegian Nynorsk
Norwegian
Polish
Portuguese
Romansh
Romanian, Moldavian, Moldovan
Russian
Slovak
Slovene
Albanian
Serbian
Swedish
Swahili
Tamil
Telugu
Thai
Turkmen
Tagalog
Turkish
Ukrainian
Urdu
Uzbek
Vietnamese
Volapük
Walloon
Yiddish
Chinese

## Dataset Structure

### Data Instances

```
{
"word":"die"
"sentimen":"negative"
}
``` 

### Data Fields

- word: one word as a string,
- sentiment-score: the sentiment classifcation of the word as a string either negative or positive

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

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

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

GNU General Public License v3

### Citation Information
@inproceedings{inproceedings,
author = {Chen, Yanqing and Skiena, Steven},
year = {2014},
month = {06},
pages = {383-389},
title = {Building Sentiment Lexicons for All Major Languages},
volume = {2},
journal = {52nd Annual Meeting of the Association for Computational Linguistics, ACL 2014 - Proceedings of the Conference},
doi = {10.3115/v1/P14-2063}
}