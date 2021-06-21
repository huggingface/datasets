---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- af
- an
- ar
- az
- be
- bg
- bn
- br
- bs
- ca
- cs
- cy
- da
- de
- el
- eo
- es
- et
- eu
- fa
- fi
- fo
- fr
- fy
- ga
- gd
- gl
- gu
- he
- hi
- hr
- ht
- hu
- hy
- ia
- id
- io
- is
- it
- ja
- ka
- km
- kn
- ko
- ku
- ky
- la
- lb
- lt
- lv
- mk
- mr
- ms
- mt
- nl
- nn
- 'no'
- pl
- pt
- rm
- ro
- ru
- sk
- sl
- sq
- sr
- sv
- sw
- ta
- te
- th
- tk
- tl
- tr
- uk
- ur
- uz
- vi
- vo
- wa
- yi
- zh
- zhw
licenses:
- gpl-3.0
multilinguality:
- multilingual
size_categories:
  af:
  - 1K<n<10K
  an:
  - n<1K
  ar:
  - 1K<n<10K
  az:
  - 1K<n<10K
  be:
  - 1K<n<10K
  bg:
  - 1K<n<10K
  bn:
  - 1K<n<10K
  br:
  - n<1K
  bs:
  - 1K<n<10K
  ca:
  - 1K<n<10K
  cs:
  - 1K<n<10K
  cy:
  - 1K<n<10K
  da:
  - 1K<n<10K
  de:
  - 1K<n<10K
  el:
  - 1K<n<10K
  eo:
  - 1K<n<10K
  es:
  - 1K<n<10K
  et:
  - 1K<n<10K
  eu:
  - 1K<n<10K
  fa:
  - 1K<n<10K
  fi:
  - 1K<n<10K
  fo:
  - n<1K
  fr:
  - 1K<n<10K
  fy:
  - n<1K
  ga:
  - 1K<n<10K
  gd:
  - n<1K
  gl:
  - 1K<n<10K
  gu:
  - 1K<n<10K
  he:
  - 1K<n<10K
  hi:
  - 1K<n<10K
  hr:
  - 1K<n<10K
  ht:
  - n<1K
  hu:
  - 1K<n<10K
  hy:
  - 1K<n<10K
  ia:
  - n<1K
  id:
  - 1K<n<10K
  io:
  - n<1K
  is:
  - 1K<n<10K
  it:
  - 1K<n<10K
  ja:
  - 1K<n<10K
  ka:
  - 1K<n<10K
  km:
  - n<1K
  kn:
  - 1K<n<10K
  ko:
  - 1K<n<10K
  ku:
  - n<1K
  ky:
  - n<1K
  la:
  - 1K<n<10K
  lb:
  - n<1K
  lt:
  - 1K<n<10K
  lv:
  - 1K<n<10K
  mk:
  - 1K<n<10K
  mr:
  - 1K<n<10K
  ms:
  - 1K<n<10K
  mt:
  - n<1K
  nl:
  - 1K<n<10K
  nn:
  - 1K<n<10K
  'no':
  - 1K<n<10K
  pl:
  - 1K<n<10K
  pt:
  - 1K<n<10K
  rm:
  - n<1K
  ro:
  - 1K<n<10K
  ru:
  - 1K<n<10K
  sk:
  - 1K<n<10K
  sl:
  - 1K<n<10K
  sq:
  - 1K<n<10K
  sr:
  - 1K<n<10K
  sv:
  - 1K<n<10K
  sw:
  - 1K<n<10K
  ta:
  - 1K<n<10K
  te:
  - 1K<n<10K
  th:
  - 1K<n<10K
  tk:
  - n<1K
  tl:
  - 1K<n<10K
  tr:
  - 1K<n<10K
  uk:
  - 1K<n<10K
  ur:
  - 1K<n<10K
  uz:
  - n<1K
  vi:
  - 1K<n<10K
  vo:
  - n<1K
  wa:
  - n<1K
  yi:
  - n<1K
  zh:
  - 1K<n<10K
  zhw:
  - 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
---

# Dataset Card for SentiWS

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

- **Homepage:** https://sites.google.com/site/datascienceslab/projects/multilingualsentiment
- **Repository:** https://www.kaggle.com/rtatman/sentiment-lexicons-for-81-languages
- **Paper:** [Needs More Information]
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
Japanese
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
Zhoa

## Dataset Structure

### Data Instances

```
{
"word":"die",
"sentiment": 0, #"negative"
}
``` 

### Data Fields

- word: one word as a string,
- sentiment-score: the sentiment classification of the word as a string either negative (0) or positive (1)

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
### Contributions

Thanks to [@KMFODA](https://github.com/KMFODA) for adding this dataset.
