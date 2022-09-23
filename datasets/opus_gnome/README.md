---
annotations_creators:
- found
language_creators:
- found
language:
- af
- am
- an
- ang
- ar
- as
- ast
- az
- bal
- be
- bem
- bg
- bn
- bo
- br
- brx
- bs
- ca
- crh
- cs
- csb
- cy
- da
- de
- dv
- dz
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fo
- fr
- fur
- fy
- ga
- gd
- gl
- gn
- gu
- gv
- ha
- he
- hi
- hr
- hu
- hy
- ia
- id
- ig
- io
- is
- it
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
- mt
- mus
- my
- nb
- nds
- ne
- nhn
- nl
- nn
- 'no'
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
- st
- sv
- sw
- szl
- ta
- te
- tg
- th
- tk
- tl
- tr
- ts
- tt
- tyj
- ug
- uk
- ur
- uz
- vi
- wa
- xh
- yi
- yo
- zh
- zu
language_bcp47:
- ar-TN
- az-IR
- bg-BG
- bn-IN
- da-DK
- de-CH
- en-AU
- en-CA
- en-GB
- en-NZ
- en-US
- en-ZA
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
- fa-IR
- hi-IN
- it-IT
- ms-MY
- nb-NO
- nn-NO
- no-NB
- pt-BR
- pt-PT
- sr-ME
- tg-TJ
- tl-PH
- tr-TR
- ur-PK
- vi-VN
- zh-CN
- zh-HK
- zh-TW
license:
- unknown
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
pretty_name: OpusGnome
configs:
- ar-bal
- bg-csb
- ca-en_GB
- cs-eo
- cs-tk
- da-vi
- de-ha
- de-tt
- el-sk
- en_GB-my
dataset_info:
- config_name: ar-bal
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - bal
  splits:
  - name: train
    num_bytes: 5150
    num_examples: 60
  download_size: 2503
  dataset_size: 5150
- config_name: bg-csb
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - csb
  splits:
  - name: train
    num_bytes: 172545
    num_examples: 1768
  download_size: 29706
  dataset_size: 172545
- config_name: ca-en_GB
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ca
        - en_GB
  splits:
  - name: train
    num_bytes: 1007488
    num_examples: 7982
  download_size: 188727
  dataset_size: 1007488
- config_name: cs-eo
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - eo
  splits:
  - name: train
    num_bytes: 2895
    num_examples: 73
  download_size: 3055
  dataset_size: 2895
- config_name: de-ha
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - ha
  splits:
  - name: train
    num_bytes: 22899
    num_examples: 216
  download_size: 5287
  dataset_size: 22899
- config_name: cs-tk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - tk
  splits:
  - name: train
    num_bytes: 1197731
    num_examples: 18686
  download_size: 98044
  dataset_size: 1197731
- config_name: da-vi
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - da
        - vi
  splits:
  - name: train
    num_bytes: 9372
    num_examples: 149
  download_size: 5432
  dataset_size: 9372
- config_name: en_GB-my
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en_GB
        - my
  splits:
  - name: train
    num_bytes: 3298074
    num_examples: 28232
  download_size: 362750
  dataset_size: 3298074
- config_name: el-sk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - sk
  splits:
  - name: train
    num_bytes: 12121
    num_examples: 150
  download_size: 6116
  dataset_size: 12121
- config_name: de-tt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - tt
  splits:
  - name: train
    num_bytes: 134978
    num_examples: 2169
  download_size: 15891
  dataset_size: 134978
---

# Dataset Card for Opus Gnome

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

`dataset = load_dataset("opus_gnome", lang1="it", lang2="pl")`


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances  
```
{
  'id': '0', 
  'translation': {
    'ar': 'إعداد سياسة القفل',
    'bal': 'تنظیم کتن سیاست کبل'
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
| ar-bal   |      60 |
| bg-csb   |      10 |
| ca-en_GB |    7982 |
| cs-eo    |      73 |
| de-ha    |     216 |
| cs-tk    |   18686 |
| da-vi    |     149 |
| en_GB-my |   28232 |
| el-sk    |     150 |
| de-tt    |    2169 |

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