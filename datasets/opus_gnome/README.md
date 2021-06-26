---
annotations_creators:
- found
language_creators:
- found
languages:
- af
- am
- an
- ang
- ar
- ar_TN
- ara
- as
- ast
- az
- az_IR
- bal
- be
- bem
- bg
- bg_BG
- bn
- bn_IN
- bo
- br
- brx
- bs
- ca
- cat
- crh
- cs
- csb
- cy
- da
- da_DK
- de
- de_CH
- dv
- dz
- el
- en
- en_AU
- en_CA
- en_GB
- en_NZ
- en_US
- en_ZA
- eo
- es
- es_AR
- es_CL
- es_CO
- es_CR
- es_DO
- es_EC
- es_ES
- es_GT
- es_HN
- es_MX
- es_NI
- es_PA
- es_PE
- es_PR
- es_SV
- es_UY
- es_VE
- et
- eu
- fa
- fa_IR
- fi
- fo
- foo
- fr
- fur
- fy
- ga
- gd
- gl
- gn
- gr
- gu
- gv
- ha
- he
- hi
- hi_IN
- hr
- hu
- hy
- ia
- id
- ig
- io
- is
- it
- it_IT
- ja
- jbo
- ka
- kg
- kk
- km
- kn
- ko
- kr
- ks
- ku
- ky
- la
- lg
- li
- lo
- lt
- lv
- mai
- mg
- mi
- mk
- ml
- mn
- mr
- ms
- ms_MY
- mt
- mus
- my
- nb
- nb_NO
- nds
- ne
- nhn
- nl
- nn
- nn_NO
- n/o
- no_nb
- nqo
- nr
- nso
- oc
- or
- os
- pa
- pl
- ps
- pt
- pt_BR
- pt_PT
- quz
- ro
- ru
- rw
- si
- sk
- sl
- so
- sq
- sr
- sr_ME
- st
- sv
- sw
- szl
- ta
- te
- tg
- tg_TJ
- th
- tk
- tl
- tl_PH
- tmp
- tr
- tr_TR
- ts
- tt
- ug
- uk
- ur
- ur_PK
- uz
- vi
- vi_VN
- wa
- xh
- yi
- yo
- zh_CN
- zh_HK
- zh_TW
- zu
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
  ar-bal:
  - n<1K
  bg-csb:
  - 1K<n<10K
  ca-en_GB:
  - 1K<n<10K
  cs-eo:
  - n<1K
  cs-tk:
  - 10K<n<100K
  da-vi:
  - n<1K
  de-ha:
  - n<1K
  de-tt:
  - 1K<n<10K
  el-sk:
  - n<1K
  en_GB-my:
  - 10K<n<100K
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

- **Homepage:** http://opus.nlpl.eu/GNOME.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary


To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/GNOME.php
E.g.

`dataset = load_dataset("gnome", lang1="it", lang2="pl")`


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

[More Information Needed]

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