---
annotations_creators:
- crowdsourced
- expert-generated
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
- ar-SY
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
- bn-IN
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
- de-AT
- de-DE
- dsb
- dv
- dz
- el
- en
- en-AU
- en-CA
- en-GB
- en-NZ
- en-US
- eo
- es
- es-AR
- es-CL
- es-CO
- es-CR
- es-DO
- es-EC
- es-ES
- es-GT
- es-HN
- es-MX
- es-NI
- es-PA
- es-PE
- es-PR
- es-SV
- es-UY
- es-VE
- et
- eu
- fa
- fa-AF
- ff
- fi
- fil
- fo
- fr
- fr-CA
- fr-FR
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
- nl-NL
- nn
- "no"
- nso
- ny
- oc
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
- pt-BR
- pt-PT
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
- ta-LK
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
- zh-CN
- zh-HK
- zh-TW
- zu
- zza
licenses:
- bsd-3-clause
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: Opus Ubuntu
configs:
- as-bs
- az-cs
- bg-de
- bn-ga
- br-es_PR
- br-hi
- br-la
- br-uz
- br-yi
- bs-szl
---

# Dataset Card for Opus Ubuntu

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

These are translations of the Ubuntu software package messages, donated by the Ubuntu community.

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/Ubuntu.php
E.g.

`dataset = load_dataset("opus_ubuntu", lang1="it", lang2="pl")`


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

Example instance:

```
{
  'id': '0', 
  'translation': {
    'it': 'Comprende Gmail, Google Docs, Google+, YouTube e Picasa',
    'pl': 'Zawiera Gmail, Google Docs, Google+, YouTube oraz Picasa'
  }
}
```

### Data Fields

Each instance has two fields:
- **id**: the id of the example
- **translation**: a dictionary containing translated texts in two languages.

### Data Splits

Each subset simply consists in a train set. We provide the number of examples for certain language pairs:

|          |   train |
|:---------|--------:|
| as-bs    |    8583 |
| az-cs    |     293 |
| bg-de    |     184 |
| br-es_PR |     125 |
| bn-ga    |    7324 |
| br-hi    |   15551 |
| br-la    |     527 |
| bs-szl   |     646 |
| br-uz    |    1416 |
| br-yi    |    2799 |

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

BSD "Revised" license (see (https://help.launchpad.net/Legal#Translations_copyright)[https://help.launchpad.net/Legal#Translations_copyright])

### Citation Information

```bibtex
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
```

### Contributions

Thanks to [@rkc007](https://github.com/rkc007) for adding this dataset.
