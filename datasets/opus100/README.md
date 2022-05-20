---
pretty_name: Opus100
task_categories:
- text-generation
- fill-mask
multilinguality:
- translation
task_ids:
- language-modeling
- masked-language-modeling
languages:
- 'no'
- af
- am
- an
- ar
- as
- az
- be
- bg
- bn
- br
- bs
- ca
- cs
- cy
- da
- de
- dz
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fr
- fy
- ga
- gd
- gl
- gu
- ha
- he
- hi
- hr
- hu
- hy
- id
- ig
- is
- it
- ja
- ka
- kk
- km
- kn
- ko
- ku
- ky
- li
- lt
- lv
- mg
- mk
- ml
- mn
- mr
- ms
- mt
- my
- nb
- ne
- nl
- nn
- oc
- or
- pa
- pl
- ps
- pt
- ro
- ru
- rw
- se
- sh
- si
- sk
- sl
- sq
- sr
- sv
- ta
- te
- tg
- th
- tk
- tr
- tt
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
annotations_creators:
- no-annotation
source_datasets:
- extended
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- 1M<n<10M
- n<1K
licenses:
- unknown
paperswithcode_id: opus-100
configs:
- af-en
- am-en
- an-en
- ar-de
- ar-en
- ar-fr
- ar-nl
- ar-ru
- ar-zh
- as-en
- az-en
- be-en
- bg-en
- bn-en
- br-en
- bs-en
- ca-en
- cs-en
- cy-en
- da-en
- de-en
- de-fr
- de-nl
- de-ru
- de-zh
- dz-en
- el-en
- en-eo
- en-es
- en-et
- en-eu
- en-fa
- en-fi
- en-fr
- en-fy
- en-ga
- en-gd
- en-gl
- en-gu
- en-ha
- en-he
- en-hi
- en-hr
- en-hu
- en-hy
- en-id
- en-ig
- en-is
- en-it
- en-ja
- en-ka
- en-kk
- en-km
- en-kn
- en-ko
- en-ku
- en-ky
- en-li
- en-lt
- en-lv
- en-mg
- en-mk
- en-ml
- en-mn
- en-mr
- en-ms
- en-mt
- en-my
- en-nb
- en-ne
- en-nl
- en-nn
- en-no
- en-oc
- en-or
- en-pa
- en-pl
- en-ps
- en-pt
- en-ro
- en-ru
- en-rw
- en-se
- en-sh
- en-si
- en-sk
- en-sl
- en-sq
- en-sr
- en-sv
- en-ta
- en-te
- en-tg
- en-th
- en-tk
- en-tr
- en-tt
- en-ug
- en-uk
- en-ur
- en-uz
- en-vi
- en-wa
- en-xh
- en-yi
- en-yo
- en-zh
- en-zu
- fr-nl
- fr-ru
- fr-zh
- nl-ru
- nl-zh
- ru-zh
---

# Dataset Card Creation Guide

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

- **Homepage:** [Link](http://opus.nlpl.eu/opus-100.php) 
- **Repository:** [GitHub](https://github.com/EdinburghNLP/opus-100-corpus)
- **Paper:** [ARXIV](https://arxiv.org/abs/2004.11867)
- **Leaderboard:** 
- **Point of Contact:** 

### Dataset Summary

OPUS-100 is English-centric, meaning that all training pairs include English on either the source or target side. The corpus covers 100 languages (including English). Selected the languages based on the volume of parallel data available in OPUS.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

OPUS-100 contains approximately 55M sentence pairs. Of the 99 language pairs, 44 have 1M sentence pairs of training data, 73 have at least 100k, and 95 have at least 10k.

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- `src_tag`: `string` text in source language
- `tgt_tag`: `string` translation of source language in target language

### Data Splits

The dataset is split into training, development, and test portions. Data was prepared by randomly sampled up to 1M sentence pairs per language pair for training and up to 2000 each for development and test. To ensure that there was no overlap (at the monolingual sentence level) between the training and development/test data, they applied a filter during sampling to exclude sentences that had already been sampled. Note that this was done cross-lingually so that, for instance, an English sentence in the Portuguese-English portion of the training data could not occur in the Hindi-English test set.

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

```
@misc{zhang2020improving,
      title={Improving Massively Multilingual Neural Machine Translation and Zero-Shot Translation}, 
      author={Biao Zhang and Philip Williams and Ivan Titov and Rico Sennrich},
      year={2020},
      eprint={2004.11867},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.
