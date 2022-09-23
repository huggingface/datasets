---
annotations_creators:
- found
language_creators:
- found
language:
- ab
- acm
- ady
- af
- afb
- afh
- aii
- ain
- ajp
- akl
- aln
- am
- an
- ang
- aoz
- apc
- ar
- arq
- ary
- arz
- as
- ast
- avk
- awa
- ayl
- az
- ba
- bal
- bar
- be
- ber
- bg
- bho
- bjn
- bm
- bn
- bo
- br
- brx
- bs
- bua
- bvy
- bzt
- ca
- cay
- cbk
- ce
- ceb
- ch
- chg
- chn
- cho
- chr
- cjy
- ckb
- ckt
- cmn
- co
- code
- cpi
- crh
- crk
- cs
- csb
- cv
- cy
- da
- de
- dng
- drt
- dsb
- dtp
- dv
- dws
- ee
- egl
- el
- emx
- en
- enm
- eo
- es
- et
- eu
- ext
- fi
- fj
- fkv
- fo
- fr
- frm
- fro
- frr
- fuc
- fur
- fuv
- fy
- ga
- gag
- gan
- gbm
- gcf
- gd
- gil
- gl
- gn
- gom
- gos
- got
- grc
- gsw
- gu
- gv
- ha
- hak
- haw
- hbo
- he
- hi
- hif
- hil
- hnj
- hoc
- hr
- hrx
- hsb
- hsn
- ht
- hu
- hy
- ia
- iba
- id
- ie
- ig
- ii
- ike
- ilo
- io
- is
- it
- izh
- ja
- jam
- jbo
- jdt
- jpa
- jv
- ka
- kaa
- kab
- kam
- kek
- kha
- kjh
- kk
- kl
- km
- kmr
- kn
- ko
- koi
- kpv
- krc
- krl
- ksh
- ku
- kum
- kw
- kxi
- ky
- la
- laa
- lad
- lb
- ldn
- lfn
- lg
- lij
- liv
- lkt
- lld
- lmo
- ln
- lo
- lt
- ltg
- lut
- lv
- lzh
- lzz
- mad
- mai
- max
- mdf
- mfe
- mg
- mgm
- mh
- mhr
- mi
- mic
- min
- mk
- ml
- mn
- mni
- mnw
- moh
- mr
- mt
- mvv
- mwl
- mww
- my
- myv
- na
- nah
- nan
- nb
- nch
- nds
- ngt
- ngu
- niu
- nl
- nlv
- nn
- nog
- non
- nov
- npi
- nst
- nus
- nv
- ny
- nys
- oar
- oc
- ofs
- ood
- or
- orv
- os
- osp
- ota
- otk
- pa
- pag
- pal
- pam
- pap
- pau
- pcd
- pdc
- pes
- phn
- pi
- pl
- pms
- pnb
- ppl
- prg
- ps
- pt
- qu
- quc
- qya
- rap
- rif
- rm
- rn
- ro
- rom
- ru
- rue
- rw
- sa
- sah
- sc
- scn
- sco
- sd
- sdh
- se
- sg
- sgs
- shs
- shy
- si
- sjn
- sl
- sm
- sma
- sn
- so
- sq
- sr
- stq
- su
- sux
- sv
- swg
- swh
- syc
- ta
- te
- tet
- tg
- th
- thv
- ti
- tig
- tk
- tl
- tlh
- tly
- tmr
- tmw
- tn
- to
- toi
- tok
- tpi
- tpw
- tr
- ts
- tt
- tts
- tvl
- ty
- tyv
- tzl
- udm
- ug
- uk
- umb
- ur
- uz
- vec
- vep
- vi
- vo
- vro
- wa
- war
- wo
- wuu
- xal
- xh
- xqa
- yi
- yo
- yue
- zlm
- zsm
- zu
- zza
license:
- cc-by-2.0
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: tatoeba
pretty_name: Tatoeba
dataset_info:
- config_name: en-mr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mr
  splits:
  - name: train
    num_bytes: 6190484
    num_examples: 53462
  download_size: 1436200
  dataset_size: 6190484
- config_name: eo-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - eo
        - nl
  splits:
  - name: train
    num_bytes: 8150048
    num_examples: 93650
  download_size: 3020382
  dataset_size: 8150048
- config_name: es-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - pt
  splits:
  - name: train
    num_bytes: 6180464
    num_examples: 67782
  download_size: 2340361
  dataset_size: 6180464
- config_name: fr-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ru
  splits:
  - name: train
    num_bytes: 19775390
    num_examples: 195161
  download_size: 5509784
  dataset_size: 19775390
- config_name: es-gl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - gl
  splits:
  - name: train
    num_bytes: 287683
    num_examples: 3135
  download_size: 128506
  dataset_size: 287683
---
# Dataset Card for Tatoeba

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

- **Homepage:** http://opus.nlpl.eu/Tatoeba.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

Tatoeba is a collection of sentences and translations.

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/Tatoeba.php
E.g.

`dataset = load_dataset("tatoeba", lang1="en", lang2="he")`

The default date is v2021-07-22, but you can also change the date with

`dataset = load_dataset("tatoeba", lang1="en", lang2="he", date="v2020-11-09")`


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The languages in the dataset are:
- ab
- acm
- ady
- af
- afb
- afh
- aii
- ain
- ajp
- akl
- aln
- am
- an
- ang
- aoz
- apc
- ar
- arq
- ary
- arz
- as
- ast
- avk
- awa
- ayl
- az
- ba
- bal
- bar
- be
- ber
- bg
- bho
- bjn
- bm
- bn
- bo
- br
- brx
- bs
- bua
- bvy
- bzt
- ca
- cay
- cbk
- ce
- ceb
- ch
- chg
- chn
- cho
- chr
- cjy
- ckb
- ckt
- cmn
- co
- code
- cpi
- crh
- crk
- cs
- csb
- cv
- cy
- da
- de
- dng
- drt
- dsb
- dtp
- dv
- dws
- ee
- egl
- el
- emx
- en
- enm
- eo
- es
- et
- eu
- ext
- fi
- fj
- fkv
- fo
- fr
- frm
- fro
- frr
- fuc
- fur
- fuv
- fy
- ga
- gag
- gan
- gbm
- gcf
- gd
- gil
- gl
- gn
- gom
- gos
- got
- grc
- gsw
- gu
- gv
- ha
- hak
- haw
- hbo
- he
- hi
- hif
- hil
- hnj
- hoc
- hr
- hrx
- hsb
- hsn
- ht
- hu
- hy
- ia
- iba
- id
- ie
- ig
- ii
- ike
- ilo
- io
- is
- it
- izh
- ja
- jam
- jbo
- jdt
- jpa
- jv
- ka
- kaa
- kab
- kam
- kek
- kha
- kjh
- kk
- kl
- km
- kmr
- kn
- ko
- koi
- kpv
- krc
- krl
- ksh
- ku
- kum
- kw
- kxi
- ky
- kzj: Coastal Kadazan (deprecated tag; preferred value: Kadazan Dusun; Central Dusun (`dtp`))
- la
- laa
- lad
- lb
- ldn
- lfn
- lg
- lij
- liv
- lkt
- lld
- lmo
- ln
- lo
- lt
- ltg
- lut
- lv
- lzh
- lzz
- mad
- mai
- max
- mdf
- mfe
- mg
- mgm
- mh
- mhr
- mi
- mic
- min
- mk
- ml
- mn
- mni
- mnw
- moh
- mr
- mt
- mvv
- mwl
- mww
- my
- myv
- na
- nah
- nan
- nb
- nch
- nds
- ngt
- ngu
- niu
- nl
- nlv
- nn
- nog
- non
- nov
- npi
- nst
- nus
- nv
- ny
- nys
- oar
- oc
- ofs
- ood
- or
- orv
- os
- osp
- ota
- otk
- pa
- pag
- pal
- pam
- pap
- pau
- pcd
- pdc
- pes
- phn
- pi
- pl
- pms
- pnb
- ppl
- prg
- ps
- pt
- qu
- quc
- qya
- rap
- rif
- rm
- rn
- ro
- rom
- ru
- rue
- rw
- sa
- sah
- sc
- scn
- sco
- sd
- sdh
- se
- sg
- sgs
- shs
- shy
- si
- sjn
- sl
- sm
- sma
- sn
- so
- sq
- sr
- stq
- su
- sux
- sv
- swg
- swh
- syc
- ta
- te
- tet
- tg
- th
- thv
- ti
- tig
- tk
- tl
- tlh
- tly
- tmr
- tmw
- tn
- to
- toi
- tok
- tpi
- tpw
- tr
- ts
- tt
- tts
- tvl
- ty
- tyv
- tzl
- udm
- ug
- uk
- umb
- ur
- uz
- vec
- vep
- vi
- vo
- vro
- wa
- war
- wo
- wuu
- xal
- xh
- xqa
- yi
- yo
- yue
- zlm
- zsm
- zu
- zza

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

[More Information Needed]

### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.