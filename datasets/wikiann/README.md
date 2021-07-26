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
  - sgs
  other-be-x-old:
  - be-tarask
  other-cbk-zam:
  - cbk
  other-eml:
  - eml
  other-fiu-vro:
  - vro
  other-map-bms:
  - jv-x-bms
  other-simple:
  - en-basiceng
  other-zh-classical:
  - lzh
  other-zh-min-nan:
  - nan
  other-zh-yue:
  - yue
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
paperswithcode_id: wikiann-1
pretty_name: WikiANN
---

# Dataset Card for WikiANN

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

- **Homepage:** [Massively Multilingual Transfer for NER](https://github.com/afshinrahimi/mmner)
- **Repository:** [Massively Multilingual Transfer for NER](https://github.com/afshinrahimi/mmner)
- **Paper:** The original datasets come from the _Cross-lingual name tagging and linking for 282 languages_ [paper](https://www.aclweb.org/anthology/P17-1178/) by Xiaoman Pan et al. (2018). This version corresponds to the balanced train, dev, and test splits of the original data from the _Massively Multilingual Transfer for NER_ [paper](https://arxiv.org/abs/1902.00193) by Afshin Rahimi et al. (2019).
- **Leaderboard:**
- **Point of Contact:** [Afshin Rahimi](mailto:afshinrahimi@gmail.com) or [Lewis Tunstall](mailto:lewis.c.tunstall@gmail.com) or [Albert Villanova del Moral](albert@huggingface.co)

### Dataset Summary

WikiANN (sometimes called PAN-X) is a multilingual named entity recognition dataset consisting of Wikipedia articles annotated with LOC (location), PER (person), and ORG (organisation) tags in the IOB2 format. This version corresponds to the balanced train, dev, and test splits of Rahimi et al. (2019), which supports 176 of the 282 languages from the original WikiANN corpus.

### Supported Tasks and Leaderboards

- `named-entity-recognition`: The dataset can be used to train a model for named entity recognition in many languages, or evaluate the zero-shot cross-lingual capabilities of multilingual models.

### Languages

The dataset contains 176 languages, one in each of the configuration subsets. The corresponding BCP 47 language tags
are:

|                    | Language tag   |
|:-------------------|:---------------|
| ace                | ace            |
| af                 | af             |
| als                | als            |
| am                 | am             |
| an                 | an             |
| ang                | ang            |
| ar                 | ar             |
| arc                | arc            |
| arz                | arz            |
| as                 | as             |
| ast                | ast            |
| ay                 | ay             |
| az                 | az             |
| ba                 | ba             |
| bar                | bar            |
| be                 | be             |
| bg                 | bg             |
| bh                 | bh             |
| bn                 | bn             |
| bo                 | bo             |
| br                 | br             |
| bs                 | bs             |
| ca                 | ca             |
| cdo                | cdo            |
| ce                 | ce             |
| ceb                | ceb            |
| ckb                | ckb            |
| co                 | co             |
| crh                | crh            |
| cs                 | cs             |
| csb                | csb            |
| cv                 | cv             |
| cy                 | cy             |
| da                 | da             |
| de                 | de             |
| diq                | diq            |
| dv                 | dv             |
| el                 | el             |
| en                 | en             |
| eo                 | eo             |
| es                 | es             |
| et                 | et             |
| eu                 | eu             |
| ext                | ext            |
| fa                 | fa             |
| fi                 | fi             |
| fo                 | fo             |
| fr                 | fr             |
| frr                | frr            |
| fur                | fur            |
| fy                 | fy             |
| ga                 | ga             |
| gan                | gan            |
| gd                 | gd             |
| gl                 | gl             |
| gn                 | gn             |
| gu                 | gu             |
| hak                | hak            |
| he                 | he             |
| hi                 | hi             |
| hr                 | hr             |
| hsb                | hsb            |
| hu                 | hu             |
| hy                 | hy             |
| ia                 | ia             |
| id                 | id             |
| ig                 | ig             |
| ilo                | ilo            |
| io                 | io             |
| is                 | is             |
| it                 | it             |
| ja                 | ja             |
| jbo                | jbo            |
| jv                 | jv             |
| ka                 | ka             |
| kk                 | kk             |
| km                 | km             |
| kn                 | kn             |
| ko                 | ko             |
| ksh                | ksh            |
| ku                 | ku             |
| ky                 | ky             |
| la                 | la             |
| lb                 | lb             |
| li                 | li             |
| lij                | lij            |
| lmo                | lmo            |
| ln                 | ln             |
| lt                 | lt             |
| lv                 | lv             |
| mg                 | mg             |
| mhr                | mhr            |
| mi                 | mi             |
| min                | min            |
| mk                 | mk             |
| ml                 | ml             |
| mn                 | mn             |
| mr                 | mr             |
| ms                 | ms             |
| mt                 | mt             |
| mwl                | mwl            |
| my                 | my             |
| mzn                | mzn            |
| nap                | nap            |
| nds                | nds            |
| ne                 | ne             |
| nl                 | nl             |
| nn                 | nn             |
| no                 | no             |
| nov                | nov            |
| oc                 | oc             |
| or                 | or             |
| os                 | os             |
| other-bat-smg      | sgs            |
| other-be-x-old     | be-tarask      |
| other-cbk-zam      | cbk            |
| other-eml          | eml            |
| other-fiu-vro      | vro            |
| other-map-bms      | jv-x-bms       |
| other-simple       | en-basiceng    |
| other-zh-classical | lzh            |
| other-zh-min-nan   | nan            |
| other-zh-yue       | yue            |
| pa                 | pa             |
| pdc                | pdc            |
| pl                 | pl             |
| pms                | pms            |
| pnb                | pnb            |
| ps                 | ps             |
| pt                 | pt             |
| qu                 | qu             |
| rm                 | rm             |
| ro                 | ro             |
| ru                 | ru             |
| rw                 | rw             |
| sa                 | sa             |
| sah                | sah            |
| scn                | scn            |
| sco                | sco            |
| sd                 | sd             |
| sh                 | sh             |
| si                 | si             |
| sk                 | sk             |
| sl                 | sl             |
| so                 | so             |
| sq                 | sq             |
| sr                 | sr             |
| su                 | su             |
| sv                 | sv             |
| sw                 | sw             |
| szl                | szl            |
| ta                 | ta             |
| te                 | te             |
| tg                 | tg             |
| th                 | th             |
| tk                 | tk             |
| tl                 | tl             |
| tr                 | tr             |
| tt                 | tt             |
| ug                 | ug             |
| uk                 | uk             |
| ur                 | ur             |
| uz                 | uz             |
| vec                | vec            |
| vep                | vep            |
| vi                 | vi             |
| vls                | vls            |
| vo                 | vo             |
| wa                 | wa             |
| war                | war            |
| wuu                | wuu            |
| xmf                | xmf            |
| yi                 | yi             |
| yo                 | yo             |
| zea                | zea            |
| zh                 | zh             |

## Dataset Structure

### Data Instances

This is an example in the "train" split of the "af" (Afrikaans language) configuration subset:
```python
{
  'tokens': ['Sy', 'ander', 'seun', ',', 'Swjatopolk', ',', 'was', 'die', 'resultaat', 'van', '’n', 'buite-egtelike', 'verhouding', '.'],
  'ner_tags': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  'langs': ['af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af'],
  'spans': ['PER: Swjatopolk']
}
```

### Data Fields

- `tokens`: a `list` of `string` features.
- `langs`: a `list` of `string` features that correspond to the language of each token.
- `ner_tags`: a `list` of classification labels, with possible values including `O` (0), `B-PER` (1), `I-PER` (2), `B-ORG` (3), `I-ORG` (4), `B-LOC` (5), `I-LOC` (6).
- `spans`: a `list` of `string` features, that is the list of named entities in the input text formatted as ``<TAG>: <mention>``

### Data Splits

For each configuration subset, the data is split into "train", "validation" and "test" sets, each containing the
following number of examples:

|              |   Train |   Validation |   Test |
|:-------------|--------:|-------------:|-------:|
| ace          |     100 |          100 |    100 |
| af           |    5000 |         1000 |   1000 |
| als          |     100 |          100 |    100 |
| am           |     100 |          100 |    100 |
| an           |    1000 |         1000 |   1000 |
| ang          |     100 |          100 |    100 |
| ar           |   20000 |        10000 |  10000 |
| arc          |     100 |          100 |    100 |
| arz          |     100 |          100 |    100 |
| as           |     100 |          100 |    100 |
| ast          |    1000 |         1000 |   1000 |
| ay           |     100 |          100 |    100 |
| az           |   10000 |         1000 |   1000 |
| ba           |     100 |          100 |    100 |
| bar          |     100 |          100 |    100 |
| bat-smg      |     100 |          100 |    100 |
| be           |   15000 |         1000 |   1000 |
| be-x-old     |    5000 |         1000 |   1000 |
| bg           |   20000 |        10000 |  10000 |
| bh           |     100 |          100 |    100 |
| bn           |   10000 |         1000 |   1000 |
| bo           |     100 |          100 |    100 |
| br           |    1000 |         1000 |   1000 |
| bs           |   15000 |         1000 |   1000 |
| ca           |   20000 |        10000 |  10000 |
| cbk-zam      |     100 |          100 |    100 |
| cdo          |     100 |          100 |    100 |
| ce           |     100 |          100 |    100 |
| ceb          |     100 |          100 |    100 |
| ckb          |    1000 |         1000 |   1000 |
| co           |     100 |          100 |    100 |
| crh          |     100 |          100 |    100 |
| cs           |   20000 |        10000 |  10000 |
| csb          |     100 |          100 |    100 |
| cv           |     100 |          100 |    100 |
| cy           |   10000 |         1000 |   1000 |
| da           |   20000 |        10000 |  10000 |
| de           |   20000 |        10000 |  10000 |
| diq          |     100 |          100 |    100 |
| dv           |     100 |          100 |    100 |
| el           |   20000 |        10000 |  10000 |
| eml          |     100 |          100 |    100 |
| en           |   20000 |        10000 |  10000 |
| eo           |   15000 |        10000 |  10000 |
| es           |   20000 |        10000 |  10000 |
| et           |   15000 |        10000 |  10000 |
| eu           |   10000 |        10000 |  10000 |
| ext          |     100 |          100 |    100 |
| fa           |   20000 |        10000 |  10000 |
| fi           |   20000 |        10000 |  10000 |
| fiu-vro      |     100 |          100 |    100 |
| fo           |     100 |          100 |    100 |
| fr           |   20000 |        10000 |  10000 |
| frr          |     100 |          100 |    100 |
| fur          |     100 |          100 |    100 |
| fy           |    1000 |         1000 |   1000 |
| ga           |    1000 |         1000 |   1000 |
| gan          |     100 |          100 |    100 |
| gd           |     100 |          100 |    100 |
| gl           |   15000 |        10000 |  10000 |
| gn           |     100 |          100 |    100 |
| gu           |     100 |          100 |    100 |
| hak          |     100 |          100 |    100 |
| he           |   20000 |        10000 |  10000 |
| hi           |    5000 |         1000 |   1000 |
| hr           |   20000 |        10000 |  10000 |
| hsb          |     100 |          100 |    100 |
| hu           |   20000 |        10000 |  10000 |
| hy           |   15000 |         1000 |   1000 |
| ia           |     100 |          100 |    100 |
| id           |   20000 |        10000 |  10000 |
| ig           |     100 |          100 |    100 |
| ilo          |     100 |          100 |    100 |
| io           |     100 |          100 |    100 |
| is           |    1000 |         1000 |   1000 |
| it           |   20000 |        10000 |  10000 |
| ja           |   20000 |        10000 |  10000 |
| jbo          |     100 |          100 |    100 |
| jv           |     100 |          100 |    100 |
| ka           |   10000 |        10000 |  10000 |
| kk           |    1000 |         1000 |   1000 |
| km           |     100 |          100 |    100 |
| kn           |     100 |          100 |    100 |
| ko           |   20000 |        10000 |  10000 |
| ksh          |     100 |          100 |    100 |
| ku           |     100 |          100 |    100 |
| ky           |     100 |          100 |    100 |
| la           |    5000 |         1000 |   1000 |
| lb           |    5000 |         1000 |   1000 |
| li           |     100 |          100 |    100 |
| lij          |     100 |          100 |    100 |
| lmo          |     100 |          100 |    100 |
| ln           |     100 |          100 |    100 |
| lt           |   10000 |        10000 |  10000 |
| lv           |   10000 |        10000 |  10000 |
| map-bms      |     100 |          100 |    100 |
| mg           |     100 |          100 |    100 |
| mhr          |     100 |          100 |    100 |
| mi           |     100 |          100 |    100 |
| min          |     100 |          100 |    100 |
| mk           |   10000 |         1000 |   1000 |
| ml           |   10000 |         1000 |   1000 |
| mn           |     100 |          100 |    100 |
| mr           |    5000 |         1000 |   1000 |
| ms           |   20000 |         1000 |   1000 |
| mt           |     100 |          100 |    100 |
| mwl          |     100 |          100 |    100 |
| my           |     100 |          100 |    100 |
| mzn          |     100 |          100 |    100 |
| nap          |     100 |          100 |    100 |
| nds          |     100 |          100 |    100 |
| ne           |     100 |          100 |    100 |
| nl           |   20000 |        10000 |  10000 |
| nn           |   20000 |         1000 |   1000 |
| no           |   20000 |        10000 |  10000 |
| nov          |     100 |          100 |    100 |
| oc           |     100 |          100 |    100 |
| or           |     100 |          100 |    100 |
| os           |     100 |          100 |    100 |
| pa           |     100 |          100 |    100 |
| pdc          |     100 |          100 |    100 |
| pl           |   20000 |        10000 |  10000 |
| pms          |     100 |          100 |    100 |
| pnb          |     100 |          100 |    100 |
| ps           |     100 |          100 |    100 |
| pt           |   20000 |        10000 |  10000 |
| qu           |     100 |          100 |    100 |
| rm           |     100 |          100 |    100 |
| ro           |   20000 |        10000 |  10000 |
| ru           |   20000 |        10000 |  10000 |
| rw           |     100 |          100 |    100 |
| sa           |     100 |          100 |    100 |
| sah          |     100 |          100 |    100 |
| scn          |     100 |          100 |    100 |
| sco          |     100 |          100 |    100 |
| sd           |     100 |          100 |    100 |
| sh           |   20000 |        10000 |  10000 |
| si           |     100 |          100 |    100 |
| simple       |   20000 |         1000 |   1000 |
| sk           |   20000 |        10000 |  10000 |
| sl           |   15000 |        10000 |  10000 |
| so           |     100 |          100 |    100 |
| sq           |    5000 |         1000 |   1000 |
| sr           |   20000 |        10000 |  10000 |
| su           |     100 |          100 |    100 |
| sv           |   20000 |        10000 |  10000 |
| sw           |    1000 |         1000 |   1000 |
| szl          |     100 |          100 |    100 |
| ta           |   15000 |         1000 |   1000 |
| te           |    1000 |         1000 |   1000 |
| tg           |     100 |          100 |    100 |
| th           |   20000 |        10000 |  10000 |
| tk           |     100 |          100 |    100 |
| tl           |   10000 |         1000 |   1000 |
| tr           |   20000 |        10000 |  10000 |
| tt           |    1000 |         1000 |   1000 |
| ug           |     100 |          100 |    100 |
| uk           |   20000 |        10000 |  10000 |
| ur           |   20000 |         1000 |   1000 |
| uz           |    1000 |         1000 |   1000 |
| vec          |     100 |          100 |    100 |
| vep          |     100 |          100 |    100 |
| vi           |   20000 |        10000 |  10000 |
| vls          |     100 |          100 |    100 |
| vo           |     100 |          100 |    100 |
| wa           |     100 |          100 |    100 |
| war          |     100 |          100 |    100 |
| wuu          |     100 |          100 |    100 |
| xmf          |     100 |          100 |    100 |
| yi           |     100 |          100 |    100 |
| yo           |     100 |          100 |    100 |
| zea          |     100 |          100 |    100 |
| zh           |   20000 |        10000 |  10000 |
| zh-classical |     100 |          100 |    100 |
| zh-min-nan   |     100 |          100 |    100 |
| zh-yue       |   20000 |        10000 |  10000 |

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

Thanks to [@lewtun](https://github.com/lewtun) and [@rabeehk](https://github.com/rabeehk) for adding this dataset.
