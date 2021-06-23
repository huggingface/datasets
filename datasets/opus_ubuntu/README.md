---
annotations_creators:
- found
language_creators:
- found
languages:
- ace
- af
- ak
- am
- an
- ang
- ar
- ar_SY
- ary
- as
- ast
- az
- ba
- bal
- be
- bem
- ber
- bg
- bho
- bn
- bn_IN
- bo
- br
- brx
- bs
- bua
- byn
- ca
- ce
- ceb
- chr
- ckb
- co
- crh
- cs
- csb
- cv
- cy
- da
- de
- de_AT
- de_DE
- dsb
- dv
- dz
- el
- en
- en_AU
- en_CA
- en_GB
- en_NZ
- en_US
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
- fa_AF
- ff
- fi
- fil
- fo
- fr
- fr_CA
- fr_FR
- frm
- frp
- fur
- fy
- ga
- gd
- gl
- gn
- grc
- gu
- guc
- gv
- ha
- haw
- he
- hi
- hil
- hne
- hr
- hsb
- ht
- hu
- hy
- ia
- id
- ig
- io
- is
- it
- iu
- ja
- jbo
- jv
- ka
- kab
- kg
- kk
- kl
- km
- kn
- ko
- kok
- ks
- ksh
- ku
- kw
- ky
- la
- lb
- lg
- li
- lij
- lld
- ln
- lo
- lt
- ltg
- lv
- mai
- mg
- mh
- mhr
- mi
- miq
- mk
- ml
- mn
- mo
- mr
- ms
- mt
- mus
- my
- nan
- nap
- nb
- nds
- ne
- nhn
- nl
- nl_NL
- nn
- n/o
- nso
- ny
- oc
- oj
- om
- or
- os
- pa
- pam
- pap
- pl
- pms
- pmy
- ps
- pt
- pt_BR
- pt_PT
- qu
- rm
- ro
- rom
- ru
- rw
- sa
- sc
- sco
- sd
- se
- shn
- shs
- si
- sk
- sl
- sm
- sml
- sn
- so
- son
- sq
- sr
- st
- sv
- sw
- syr
- szl
- ta
- ta_LK
- te
- tet
- tg
- th
- ti
- tk
- tl
- tlh
- tr
- trv
- ts
- tt
- ug
- uk
- ur
- uz
- ve
- vec
- vi
- wa
- wae
- wo
- xal
- xh
- yi
- yo
- zh
- zh_CN
- zh_HK
- zh_TW
- zu
- zza
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
  as-bs:
  - 1K<n<10K
  az-cs:
  - n<1K
  bg-de:
  - n<1K
  bn-ga:
  - 1K<n<10K
  br-es_PR:
  - n<1K
  br-hi:
  - 10K<n<100K
  br-la:
  - n<1K
  br-uz:
  - 1K<n<10K
  br-yi:
  - 1K<n<10K
  bs-szl:
  - n<1K
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

- **Homepage:** http://opus.nlpl.eu/Ubuntu.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary


To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/Ubuntu.php
E.g.

`dataset = load_dataset("ubuntu", lang1="it", lang2="pl")`


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