---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- ady
- ang
- ar
- arn
- ast
- az
- ba
- be
- bg
- bn
- bo
- br
- ca
- ckb
- crh
- cs
- csb
- cu
- cy
- da
- de
- dsb
- el
- en
- es
- et
- eu
- fa
- fi
- fo
- fr
- frm
- fro
- frr
- fur
- fy
- ga
- gal
- gd
- gmh
- gml
- got
- grc
- gv
- hai
- he
- hi
- hu
- hy
- is
- it
- izh
- ka
- kbd
- kjh
- kk
- kl
- klr
- kmr
- kn
- krl
- kw
- la
- liv
- lld
- lt
- lud
- lv
- mk
- mt
- mwf
- nap
- nb
- nds
- nl
- nn
- nv
- oc
- olo
- osx
- pl
- ps
- pt
- qu
- ro
- ru
- sa
- sga
- sh
- sl
- sme
- sq
- sv
- swc
- syc
- te
- tg
- tk
- tr
- tt
- uk
- ur
- uz
- vec
- vep
- vot
- xcl
- xno
- yi
- zu
license:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- token-classification
- text-classification
task_ids:
- multi-class-classification
- multi-label-classification
- token-classification-other-morphology
paperswithcode_id: null
pretty_name: UniversalMorphologies
configs:
- ady
- ang
- ara
- arn
- ast
- aze
- bak
- bel
- ben
- bod
- bre
- bul
- cat
- ces
- chu
- ckb
- cor
- crh
- csb
- cym
- dan
- deu
- dsb
- ell
- eng
- est
- eus
- fao
- fas
- fin
- fra
- frm
- fro
- frr
- fry
- fur
- gal
- gla
- gle
- glv
- gmh
- gml
- got
- grc
- hai
- hbs
- heb
- hin
- hun
- hye
- isl
- ita
- izh
- kal
- kan
- kat
- kaz
- kbd
- kjh
- klr
- kmr
- krl
- lat
- lav
- lit
- liv
- lld
- lud
- mkd
- mlt
- mwf
- nap
- nav
- nds
- nld
- nno
- nob
- oci
- olo
- osx
- pol
- por
- pus
- que
- ron
- rus
- san
- sga
- slv
- sme
- spa
- sqi
- swc
- swe
- syc
- tat
- tel
- tgk
- tuk
- tur
- ukr
- urd
- uzb
- vec
- vep
- vot
- xcl
- xno
- yid
- zul
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [UniMorph Homepage](https://unimorph.github.io/)
- **Repository:** [List of UniMorph repositories](https://github.com/unimorph)
- **Paper:** [The Composition and Use of the Universal Morphological Feature Schema (UniMorph Schema)](https://unimorph.github.io/doc/unimorph-schema.pdf)
- **Point of Contact:** [Arya McCarthy](mailto:arya@jhu.edu)

### Dataset Summary

The Universal Morphology (UniMorph) project is a collaborative effort to improve how NLP handles complex morphology in the world’s languages.
The goal of UniMorph is to annotate morphological data in a universal schema that allows an inflected word from any language to be defined by its lexical meaning,
typically carried by the lemma, and by a rendering of its inflectional form in terms of a bundle of morphological features from our schema.
The specification of the schema is described in Sylak-Glassman (2016).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The current version of the UniMorph dataset covers 110 languages.

## Dataset Structure

### Data Instances

Each data instance comprises of a lemma and a set of possible realizations with morphological and meaning annotations. For example:
```
{'forms': {'Aktionsart': [[], [], [], [], []],
  'Animacy': [[], [], [], [], []],
  ...
  'Finiteness': [[], [], [], [1], []],
  ...
  'Number': [[], [], [0], [], []],
  'Other': [[], [], [], [], []],
  'Part_Of_Speech': [[7], [10], [7], [7], [10]],
  ...
  'Tense': [[1], [1], [0], [], [0]],
  ...
  'word': ['ablated', 'ablated', 'ablates', 'ablate', 'ablating']},
 'lemma': 'ablate'}
```

### Data Fields

Each instance in the dataset has the following fields:
- `lemma`: the common lemma for all all_forms
- `forms`: all annotated forms for this lemma, with:
  - `word`: the full word form
  - [`category`]: a categorical variable denoting one or several tags in a category (several to represent composite tags, originally denoted with `A+B`). The full list of categories and possible tags for each can be found [here](https://github.com/unimorph/unimorph.github.io/blob/master/unimorph-schema-json/dimensions-to-features.json)


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

[More Information Needed]

### Contributions

Thanks to [@yjernite](https://github.com/yjernite) for adding this dataset.
