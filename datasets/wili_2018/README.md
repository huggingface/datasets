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
dataset_info:
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: cdo
          1: glk
          2: jam
          3: lug
          4: san
          5: rue
          6: wol
          7: new
          8: mwl
          9: bre
          10: ara
          11: hye
          12: xmf
          13: ext
          14: cor
          15: yor
          16: div
          17: asm
          18: lat
          19: cym
          20: hif
          21: ace
          22: kbd
          23: tgk
          24: rus
          25: nso
          26: mya
          27: msa
          28: ava
          29: cbk
          30: urd
          31: deu
          32: swa
          33: pus
          34: bxr
          35: udm
          36: csb
          37: yid
          38: vro
          39: por
          40: pdc
          41: eng
          42: tha
          43: hat
          44: lmo
          45: pag
          46: jav
          47: chv
          48: nan
          49: sco
          50: kat
          51: bho
          52: bos
          53: kok
          54: oss
          55: mri
          56: fry
          57: cat
          58: azb
          59: kin
          60: hin
          61: sna
          62: dan
          63: egl
          64: mkd
          65: ron
          66: bul
          67: hrv
          68: som
          69: pam
          70: nav
          71: ksh
          72: nci
          73: khm
          74: sgs
          75: srn
          76: bar
          77: cos
          78: ckb
          79: pfl
          80: arz
          81: roa-tara
          82: fra
          83: mai
          84: zh-yue
          85: guj
          86: fin
          87: kir
          88: vol
          89: hau
          90: afr
          91: uig
          92: lao
          93: swe
          94: slv
          95: kor
          96: szl
          97: srp
          98: dty
          99: nrm
          100: dsb
          101: ind
          102: wln
          103: pnb
          104: ukr
          105: bpy
          106: vie
          107: tur
          108: aym
          109: lit
          110: zea
          111: pol
          112: est
          113: scn
          114: vls
          115: stq
          116: gag
          117: grn
          118: kaz
          119: ben
          120: pcd
          121: bjn
          122: krc
          123: amh
          124: diq
          125: ltz
          126: ita
          127: kab
          128: bel
          129: ang
          130: mhr
          131: che
          132: koi
          133: glv
          134: ido
          135: fao
          136: bak
          137: isl
          138: bcl
          139: tet
          140: jpn
          141: kur
          142: map-bms
          143: tyv
          144: olo
          145: arg
          146: ori
          147: lim
          148: tel
          149: lin
          150: roh
          151: sqi
          152: xho
          153: mlg
          154: fas
          155: hbs
          156: tam
          157: aze
          158: lad
          159: nob
          160: sin
          161: gla
          162: nap
          163: snd
          164: ast
          165: mal
          166: mdf
          167: tsn
          168: nds
          169: tgl
          170: nno
          171: sun
          172: lzh
          173: jbo
          174: crh
          175: pap
          176: oci
          177: hak
          178: uzb
          179: zho
          180: hsb
          181: sme
          182: mlt
          183: vep
          184: lez
          185: nld
          186: nds-nl
          187: mrj
          188: spa
          189: ceb
          190: ina
          191: heb
          192: hun
          193: que
          194: kaa
          195: mar
          196: vec
          197: frp
          198: ell
          199: sah
          200: eus
          201: ces
          202: slk
          203: chr
          204: lij
          205: nep
          206: srd
          207: ilo
          208: be-tarask
          209: bod
          210: orm
          211: war
          212: glg
          213: mon
          214: gle
          215: min
          216: ibo
          217: ile
          218: epo
          219: lav
          220: lrc
          221: als
          222: mzn
          223: rup
          224: fur
          225: tat
          226: myv
          227: pan
          228: ton
          229: kom
          230: wuu
          231: tcy
          232: tuk
          233: kan
          234: ltg
  config_name: WiLI-2018 dataset
  splits:
  - name: test
    num_bytes: 66491260
    num_examples: 117500
  - name: train
    num_bytes: 65408201
    num_examples: 117500
  download_size: 130516351
  dataset_size: 131899461
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