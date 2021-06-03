---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- af
- am
- an
- as
- av
- ay
- bs
- ce
- co
- cv
- dv
- eo
- gl
- gn
- gu
- ha
- hr
- ht
- ia
- id
- ie
- ig
- io
- ja
- jv
- km
- ko
- ku
- kv
- ky
- lb
- lg
- li
- ln
- lo
- mg
- mi
- ml
- mn
- mr
- ms
- my
- ne
- om
- or
- os
- pa
- rm
- rw
- sc
- sd
- si
- sk
- sn
- so
- sr
- su
- sw
- ta
- th
- tl
- tn
- to
- ug
- vi
- vo
- wa
- wo
- xh
- yo
- zh
- ar
- az
- ba
- be
- bg
- bn
- bo
- br
- ca
- cs
- cy
- da
- de
- el
- en
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
- gv
- he
- hi
- hu
- hy
- is
- it
- ka
- kk
- kn
- kw
- la
- lt
- lv
- mk
- mt
- nb
- nl
- nn
- nv
- oc
- pl
- ps
- pt
- qu
- ro
- ru
- sa
- sh
- sl
- sq
- sv
- te
- tg
- tk
- tr
- tt
- uk
- ur
- uz
- yi
- ace
- als
- ang
- arz
- ast
- azb
- bar
- bcl
- bho
- bjn
- bpy
- bxr
- cbk
- cdo
- ceb
- chr
- ckb
- crh
- csb
- diq
- dsb
- dty
- egl
- ext
- frp
- fur
- gag
- glk
- hak
- hif
- hsb
- ilo
- jam
- jbo
- kaa
- kab
- kbd
- koi
- kok
- krc
- ksh
- lad
- lez
- lij
- lmo
- lrc
- ltg
- lzh
- mai
- mdf
- mhr
- min
- mrj
- mwl
- myv
- mzn
- nan
- nap
- nci
- nds
- new
- nrm
- nso
- olo
- pag
- pam
- pap
- pcd
- pdc
- pfl
- pnb
- rue
- rup
- sah
- scn
- sco
- sgs
- sme
- srn
- stq
- szl
- tcy
- tet
- tyv
- udm
- vec
- vep
- vls
- vro
- war
- wuu
- xmf
- zea
- other-roa-tara
- other-zh-yue
- other-map-bms
- other-nds-nl
- other-be-tarask
licenses:
- odbl-1.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-language-identification
paperswithcode_id: wili-2018
---

# Dataset Card for wili_2018

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

- **Homepage:** https://zenodo.org/record/841984
- **Repository:** [Needs More Information]
- **Paper:** https://arxiv.org/pdf/1801.07779
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** Thoma, Martin (Email: info@martin-thoma.de)

### Dataset Summary

WiLI-2018, the Wikipedia language identification benchmark dataset, contains 235000 paragraphs of 235 languages. The dataset is balanced and a train-test split is provided.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

235 Different Languages

## Dataset Structure

### Data Instances

```
{
    'label': 207,
    'sentence': 'Ti Turkia ket maysa a demokrata, sekular, unitario, batay-linteg a republika nga addaan ti taga-ugma a tinawtawid a kultura. Ti Turkia ket umadadu a naipatipon iti Laud babaen ti panagkameng kadagiti organisasion a kas ti Konsilo iti Europa, NATO, OECD, OSCE ken ti G-20 a dagiti kangrunaan nga ekonomia. Ti Turkia ket nangrugi a nakitulag ti napno a panagkameng iti Kappon ti Europa idi 2005, nga isu ket maysa idin a kumaduaan a kameng iti Europeano a Komunidad ti Ekonomia manipud idi 1963 ken nakadanon ti maysa a tulagan ti kappon ti aduana idi 1995. Ti Turkia ket nagtaraken iti asideg a kultural, politikal, ekonomiko ken industria a panakibiang iti Tengnga a Daya, dagiti Turko nga estado iti Tengnga nga Asia ken dagiti pagilian ti Aprika babaen ti panagkameng kadagiti organisasion a kas ti Turko a Konsilo, Nagsaupan nga Administrasion iti Turko nga Arte ken Kultura, Organisasion iti Islamiko a Panagtitinnulong ken ti Organisasion ti Ekonomiko a Panagtitinnulong.'
}
```

### Data Fields

[Needs More Information]

### Data Splits

175000 lines of text each for train and test data.

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

The dataset was initially created by Thomas Martin

### Licensing Information

ODC Open Database License v1.0

### Citation Information

```
@dataset{thoma_martin_2018_841984,
  author       = {Thoma, Martin},
  title        = {{WiLI-2018 - Wikipedia Language Identification database}},
  month        = jan,
  year         = 2018,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.841984},
  url          = {https://doi.org/10.5281/zenodo.841984}
}
```

### Contributions

Thanks to [@Shubhambindal2017](https://github.com/Shubhambindal2017) for adding this dataset.