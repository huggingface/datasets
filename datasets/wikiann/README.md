---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
  ace:
  - ace
  af:
  - af
  als:
  - als
  am:
  - am
  an:
  - an
  ang:
  - ang
  ar:
  - ar
  arc:
  - arc
  arz:
  - arz
  as:
  - as
  ast:
  - ast
  ay:
  - ay
  az:
  - az
  ba:
  - ba
  bar:
  - bar
  be:
  - be
  bg:
  - bg
  bh:
  - bh
  bn:
  - bn
  bo:
  - bo
  br:
  - br
  bs:
  - bs
  ca:
  - ca
  cdo:
  - cdo
  ce:
  - ce
  ceb:
  - ceb
  ckb:
  - ckb
  co:
  - co
  crh:
  - crh
  cs:
  - cs
  csb:
  - csb
  cv:
  - cv
  cy:
  - cy
  da:
  - da
  de:
  - de
  diq:
  - diq
  dv:
  - dv
  el:
  - el
  en:
  - en
  eo:
  - eo
  es:
  - es
  et:
  - et
  eu:
  - eu
  ext:
  - ext
  fa:
  - fa
  fi:
  - fi
  fo:
  - fo
  fr:
  - fr
  frr:
  - frr
  fur:
  - fur
  fy:
  - fy
  ga:
  - ga
  gan:
  - gan
  gd:
  - gd
  gl:
  - gl
  gn:
  - gn
  gu:
  - gu
  hak:
  - hak
  he:
  - he
  hi:
  - hi
  hr:
  - hr
  hsb:
  - hsb
  hu:
  - hu
  hy:
  - hy
  ia:
  - ia
  id:
  - id
  ig:
  - ig
  ilo:
  - ilo
  io:
  - io
  is:
  - is
  it:
  - it
  ja:
  - ja
  jbo:
  - jbo
  jv:
  - jv
  ka:
  - ka
  kk:
  - kk
  km:
  - km
  kn:
  - kn
  ko:
  - ko
  ksh:
  - ksh
  ku:
  - ku
  ky:
  - ky
  la:
  - la
  lb:
  - lb
  li:
  - li
  lij:
  - lij
  lmo:
  - lmo
  ln:
  - ln
  lt:
  - lt
  lv:
  - lv
  mg:
  - mg
  mhr:
  - mhr
  mi:
  - mi
  min:
  - min
  mk:
  - mk
  ml:
  - ml
  mn:
  - mn
  mr:
  - mr
  ms:
  - ms
  mt:
  - mt
  mwl:
  - mwl
  my:
  - my
  mzn:
  - mzn
  nap:
  - nap
  nds:
  - nds
  ne:
  - ne
  nl:
  - nl
  nn:
  - nn
  'no':
  - 'no'
  nov:
  - nov
  oc:
  - oc
  or:
  - or
  os:
  - os
  other-bat-smg:
  - other-bat-smg
  other-be-x-old:
  - other-be-x-old
  other-cbk-zam:
  - other-cbk-zam
  other-eml:
  - other-eml
  other-fiu-vro:
  - other-fiu-vro
  other-map-bms:
  - other-map-bms
  other-simple:
  - other-simple
  other-zh-classical:
  - other-zh-classical
  other-zh-min-nan:
  - other-zh-min-nan
  other-zh-yue:
  - other-zh-yue
  pa:
  - pa
  pdc:
  - pdc
  pl:
  - pl
  pms:
  - pms
  pnb:
  - pnb
  ps:
  - ps
  pt:
  - pt
  qu:
  - qu
  rm:
  - rm
  ro:
  - ro
  ru:
  - ru
  rw:
  - rw
  sa:
  - sa
  sah:
  - sah
  scn:
  - scn
  sco:
  - sco
  sd:
  - sd
  sh:
  - sh
  si:
  - si
  sk:
  - sk
  sl:
  - sl
  so:
  - so
  sq:
  - sq
  sr:
  - sr
  su:
  - su
  sv:
  - sv
  sw:
  - sw
  szl:
  - szl
  ta:
  - ta
  te:
  - te
  tg:
  - tg
  th:
  - th
  tk:
  - tk
  tl:
  - tl
  tr:
  - tr
  tt:
  - tt
  ug:
  - ug
  uk:
  - uk
  ur:
  - ur
  uz:
  - uz
  vec:
  - vec
  vep:
  - vep
  vi:
  - vi
  vls:
  - vls
  vo:
  - vo
  wa:
  - wa
  war:
  - war
  wuu:
  - wuu
  xmf:
  - xmf
  yi:
  - yi
  yo:
  - yo
  zea:
  - zea
  zh:
  - zh
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
---

# Dataset Card for WikiANN

## Table of Contents
- [Dataset Card for WikiANN](#dataset-card-for-wikiann)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
    - [Personal and Sensitive Information](#personal-and-sensitive-information)
  - [Considerations for Using the Data](#considerations-for-using-the-data)
    - [Social Impact of Dataset](#social-impact-of-dataset)
    - [Discussion of Biases](#discussion-of-biases)
    - [Other Known Limitations](#other-known-limitations)
  - [Additional Information](#additional-information)
    - [Dataset Curators](#dataset-curators)
    - [Licensing Information](#licensing-information)
    - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** [Massively Multilingual Transfer for NER](https://github.com/afshinrahimi/mmner)
- **Repository:** [Massively Multilingual Transfer for NER](https://github.com/afshinrahimi/mmner)
- **Paper:** The original datasets come from the _Cross-lingual name tagging and linking for 282 languages_ [paper](https://www.aclweb.org/anthology/P17-1178/) by Xiaoman Pan et al. (2018). This version corresponds to the balanced train, dev, and test splits of the original data from the _Massively Multilingual Transfer for NER_ [paper](https://arxiv.org/abs/1902.00193) by Afshin Rahimi et al. (2019).
- **Leaderboard:**
- **Point of Contact:** [Afshin Rahimi](mailto:afshinrahimi@gmail.com) or [Lewis Tunstall](mailto:lewis.c.tunstall@gmail.com)

### Dataset Summary

WikiANN (sometimes called PAN-X) is a multilingual named entity recognition dataset consisting of Wikipedia articles annotated with LOC (location), PER (person), and ORG (organisation) tags in the IOB2 format. This version corresponds to the balanced train, dev, and test splits of Rahimi et al. (2019), which supports 176 of the 282 languages from the original WikiANN corpus.

### Supported Tasks and Leaderboards

- `named-entity-recognition`: The dataset can be used to train a model for named entity recognition in many languages, or evaluate the zero-shot cross-lingual capabilities of multilingual models.

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

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

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

The original 282 datasets are associated with this article

```
@inproceedings{pan-etal-2017-cross,
    title = "Cross-lingual Name Tagging and Linking for 282 Languages",
    author = "Pan, Xiaoman  and
      Zhang, Boliang  and
      May, Jonathan  and
      Nothman, Joel  and
      Knight, Kevin  and
      Ji, Heng",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1178",
    doi = "10.18653/v1/P17-1178",
    pages = "1946--1958",
    abstract = "The ambitious goal of this work is to develop a cross-lingual name tagging and linking framework for 282 languages that exist in Wikipedia. Given a document in any of these languages, our framework is able to identify name mentions, assign a coarse-grained or fine-grained type to each mention, and link it to an English Knowledge Base (KB) if it is linkable. We achieve this goal by performing a series of new KB mining methods: generating {``}silver-standard{''} annotations by transferring annotations from English to other languages through cross-lingual links and KB properties, refining annotations through self-training and topic selection, deriving language-specific morphology features from anchor links, and mining word translation pairs from cross-lingual links. Both name tagging and linking results for 282 languages are promising on Wikipedia data and on-Wikipedia data.",
}
```

while the 176 languages supported in this version are associated with the following article

```
@inproceedings{rahimi-etal-2019-massively,
    title = "Massively Multilingual Transfer for {NER}",
    author = "Rahimi, Afshin  and
      Li, Yuan  and
      Cohn, Trevor",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1015",
    pages = "151--164",
}
```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun) for adding this dataset.