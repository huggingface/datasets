---
task_categories:
- sequence-modeling
multilinguality:
- translation
task_ids:
- language-modeling
languages:
  af-en:
  - af
  - en
  am-en:
  - am
  - en
  an-en:
  - an
  - en
  ar-en:
  - ar
  - en
  as-en:
  - as
  - en
  az-en:
  - az
  - en
  be-en:
  - be
  - en
  bg-en:
  - bg
  - en
  bn-en:
  - bn
  - en
  br-en:
  - br
  - en
  bs-en:
  - bs
  - en
  ca-en:
  - ca
  - en
  cs-en:
  - cs
  - en
  cy-en:
  - cy
  - en
  da-en:
  - da
  - en
  de-en:
  - de
  - en
  dz-en:
  - dz
  - en
  el-en:
  - el
  - en
  en-eo:
  - en
  - eo
  en-es:
  - en
  - es
  en-et:
  - en
  - et
  en-eu:
  - en
  - eu
  en-fa:
  - en
  - fa
  en-fi:
  - en
  - fi
  en-fr:
  - en
  - fr
  en-fy:
  - en
  - fy
  en-ga:
  - en
  - ga
  en-gd:
  - en
  - gd
  en-gl:
  - en
  - gl
  en-gu:
  - en
  - gu
  en-ha:
  - en
  - ha
  en-he:
  - en
  - he
  en-hi:
  - en
  - hi
  en-hr:
  - en
  - hr
  en-hu:
  - en
  - hu
  en-hy:
  - en
  - hy
  en-id:
  - en
  - id
  en-ig:
  - en
  - ig
  en-is:
  - en
  - is
  en-it:
  - en
  - it
  en-ja:
  - en
  - ja
  en-ka:
  - en
  - ka
  en-kk:
  - en
  - kk
  en-km:
  - en
  - km
  en-ko:
  - en
  - ko
  en-kn:
  - en
  - kn
  en-ku:
  - en
  - ku
  en-ky:
  - en
  - ky
  en-li:
  - en
  - li
  en-lt:
  - en
  - lt
  en-lv:
  - en
  - lv
  en-mg:
  - en
  - mg
  en-mk:
  - en
  - mk
  en-ml:
  - en
  - ml
  en-mn:
  - en
  - mn
  en-mr:
  - en
  - mr
  en-ms:
  - en
  - ms
  en-mt:
  - en
  - mt
  en-my:
  - en
  - my
  en-nb:
  - en
  - nb
  en-ne:
  - en
  - ne
  en-nl:
  - en
  - nl
  en-nn:
  - en
  - nn
  en-no:
  - en
  - no
  en-oc:
  - en
  - oc
  en-or:
  - en
  - or
  en-pa:
  - en
  - pa
  en-pl:
  - en
  - pl
  en-ps:
  - en
  - ps
  en-pt:
  - en
  - pt
  en-ro:
  - en
  - ro
  en-ru:
  - en
  - ru
  en-rw:
  - en
  - rw
  en-se:
  - en
  - se
  en-sh:
  - en
  - sh
  en-si:
  - en
  - si
  en-sk:
  - en
  - sk
  en-sl:
  - en
  - sl
  en-sq:
  - en
  - sq
  en-sr:
  - en
  - sr
  en-sv:
  - en
  - sv
  en-ta:
  - en
  - ta
  en-te:
  - en
  - te
  en-tg:
  - en
  - tg
  en-th:
  - en
  - th
  en-tk:
  - en
  - tk
  en-tr:
  - en
  - tr
  en-tt:
  - en
  - tt
  en-ug:
  - en
  - ug
  en-uk:
  - en
  - uk
  en-ur:
  - en
  - ur
  en-uz:
  - en
  - uz
  en-vi:
  - en
  - vi
  en-wa:
  - en
  - wa
  en-xh:
  - en
  - xh
  en-yi:
  - en
  - yi
  en-yo:
  - en
  - yo
  en-zh:
  - en
  - zh
  en-zu:
  - en
  - zu
annotations_creators:
- no-annotation
source_datasets:
- extended
size_categories:
- 10K<n<1M
licenses:
- unknown
---

# Dataset Card Creation Guide

## Table of Contents
- [Dataset Card Creation Guide](#dataset-card-creation-guide)
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