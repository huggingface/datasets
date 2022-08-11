---
annotations_creators:
- found
language_creators:
- found
language:
- aa
- ab
- ae
- aeb
- af
- ak
- am
- an
- ar
- arq
- arz
- as
- ase
- ast
- av
- ay
- az
- ba
- be
- ber
- bg
- bh
- bi
- bm
- bn
- bnt
- bo
- br
- bs
- bug
- ca
- ce
- ceb
- ch
- cho
- cku
- cnh
- co
- cr
- cs
- cu
- cv
- cy
- da
- de
- dv
- dz
- ee
- efi
- el
- en
- eo
- es
- et
- eu
- fa
- ff
- fi
- fil
- fj
- fo
- fr
- ga
- gd
- gl
- gn
- gu
- ha
- hai
- haw
- haz
- hch
- he
- hi
- ho
- hr
- ht
- hu
- hup
- hus
- hy
- hz
- ia
- id
- ie
- ig
- ik
- inh
- io
- iro
- is
- it
- iu
- ja
- jv
- ka
- kar
- ki
- kj
- kk
- kl
- km
- kn
- ko
- kr
- ksh
- ku
- kv
- kw
- ky
- la
- lb
- lg
- li
- lkt
- lld
- ln
- lo
- lt
- ltg
- lu
- luo
- luy
- lv
- mad
- mfe
- mg
- mi
- mk
- ml
- mn
- mni
- moh
- mos
- mr
- ms
- mt
- mus
- my
- nb
- nci
- nd
- ne
- nl
- nn
- nso
- nv
- ny
- oc
- om
- or
- pa
- pam
- pap
- pi
- pl
- pnb
- prs
- ps
- pt
- qu
- rm
- rn
- ro
- ru
- rup
- rw
- sa
- sc
- scn
- sco
- sd
- sg
- sgn
- sh
- si
- sk
- sl
- sm
- sn
- so
- sq
- sr
- st
- sv
- sw
- szl
- ta
- te
- tet
- tg
- th
- ti
- tk
- tl
- tlh
- to
- tr
- ts
- tt
- tw
- ug
- uk
- umb
- ur
- uz
- ve
- vi
- vls
- vo
- wa
- wo
- xh
- yaq
- yi
- yo
- za
- zam
- zh
- zu
license:
- unknown
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: QedAmara
---

# Dataset Card for QedAmara

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

- **Homepage:** http://opus.nlpl.eu/QED.php
- **Repository:** None
- **Paper:** https://www.aclweb.org/anthology/L14-1675/
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary


To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/QED.php
E.g.

`dataset = load_dataset("qed_amara", lang1="cs", lang2="nb")`


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The languages in the dataset are:
- aa
- ab
- ae
- aeb
- af
- aka: `ak`
- amh: `am`
- an
- ar
- arq
- arz
- as
- ase
- ast
- av
- ay
- az
- ba
- bam: `bm`
- be
- ber
- bg
- bh
- bi
- bn
- bnt
- bo
- br
- bs
- bug
- ca
- ce
- ceb
- ch
- cho
- cku
- cnh
- co
- cr
- cs
- cu
- cv
- cy
- da
- de
- dv
- dz
- ee
- efi
- el
- en
- eo
- es
- et
- eu
- fa
- ff
- fi
- fil
- fj
- fo
- fr
- ful: `ff`
- ga
- gd
- gl
- gn
- gu
- hai
- hau: `ha`
- haw
- haz
- hb: ?
- hch
- he
- hi
- ho
- hr
- ht
- hu
- hup
- hus
- hy
- hz
- ia
- ibo: `ig`
- id
- ie
- ik
- inh
- io
- iro
- is
- it
- iu
- ja
- jv
- ka
- kar
- kau: `kr`
- kik: `ki`
- kin: `rw`
- kj
- kk
- kl
- km
- kn
- ko
- ksh
- ku
- kv
- kw
- ky
- la
- lb
- lg
- li
- lin: `ln`
- lkt
- lld
- lo
- lt
- ltg
- lu
- luo
- luy
- lv
- mad
- mfe
- mi
- mk
- ml
- mlg: `mg`
- mn
- mni
- mo: Moldavian (deprecated tag; preferred value: Romanian; Moldavian; Moldovan (`ro`))
- moh
- mos
- mr
- ms
- mt
- mus
- my
- nb
- nci
- nd
- ne
- nl
- nn
- nso
- nv
- nya: `ny`
- oc
- or
- orm: `om`
- pam
- pan: `pa`
- pap
- pi
- pl
- pnb
- prs
- ps
- pt
- que: `qu`
- rm
- ro
- ru
- run: `rn`
- rup
- ry: ?
- sa
- sc
- scn
- sco
- sd
- sg
- sgn
- sh
- si
- sk
- sl
- sm
- sna: `sn`
- som: `so`
- sot: `st`
- sq
- sr
- srp: `sr`
- sv
- swa: `sw`
- szl
- ta
- te
- tet
- tg
- th
- tir: `ti`
- tk
- tl
- tlh
- to
- tr
- ts
- tt
- tw
- ug
- uk
- umb
- ur
- uz
- ve
- vi
- vls
- vo
- wa
- wol: `wo`
- xh
- yaq
- yi
- yor: `yo`
- za
- zam
- zh
- zul: `zu`

## Dataset Structure

### Data Instances

Here are some examples of questions and facts:


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
