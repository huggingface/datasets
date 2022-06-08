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
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
pretty_name: SentiWS
configs:
- 'no'
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
