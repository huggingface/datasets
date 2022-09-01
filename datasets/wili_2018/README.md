---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- ace
- af
- als
- am
- an
- ang
- ar
- arz
- as
- ast
- av
- ay
- az
- azb
- ba
- bar
- bcl
- be
- bg
- bho
- bjn
- bn
- bo
- bpy
- br
- bs
- bxr
- ca
- cbk
- cdo
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
- diq
- dsb
- dty
- dv
- egl
- el
- en
- eo
- es
- et
- eu
- ext
- fa
- fi
- fo
- fr
- frp
- fur
- fy
- ga
- gag
- gd
- gl
- glk
- gn
- gu
- gv
- ha
- hak
- he
- hi
- hif
- hr
- hsb
- ht
- hu
- hy
- ia
- id
- ie
- ig
- ilo
- io
- is
- it
- ja
- jam
- jbo
- jv
- ka
- kaa
- kab
- kbd
- kk
- km
- kn
- ko
- koi
- kok
- krc
- ksh
- ku
- kv
- kw
- ky
- la
- lad
- lb
- lez
- lg
- li
- lij
- lmo
- ln
- lo
- lrc
- lt
- ltg
- lv
- lzh
- mai
- map
- mdf
- mg
- mhr
- mi
- min
- mk
- ml
- mn
- mr
- mrj
- ms
- mt
- mwl
- my
- myv
- mzn
- nan
- nap
- nb
- nci
- nds
- ne
- new
- nl
- nn
- nrm
- nso
- nv
- oc
- olo
- om
- or
- os
- pa
- pag
- pam
- pap
- pcd
- pdc
- pfl
- pl
- pnb
- ps
- pt
- qu
- rm
- ro
- roa
- ru
- rue
- rup
- rw
- sa
- sah
- sc
- scn
- sco
- sd
- sgs
- sh
- si
- sk
- sl
- sme
- sn
- so
- sq
- sr
- srn
- stq
- su
- sv
- sw
- szl
- ta
- tcy
- te
- tet
- tg
- th
- tk
- tl
- tn
- to
- tr
- tt
- tyv
- udm
- ug
- uk
- ur
- uz
- vec
- vep
- vi
- vls
- vo
- vro
- wa
- war
- wo
- wuu
- xh
- xmf
- yi
- yo
- zea
- zh
language_bcp47:
- be-tarask
- map-bms
- nds-nl
- roa-tara
- zh-yue
license:
- odbl
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
pretty_name: Wili2018
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
