---
task_categories:
- sequence-modeling
task_ids:
- language-modeling
multilinguality:
- translation
languages:
- en
- hi
- ta
- te
- ml
- ur
- bn
- mr
- gu
- or
- pa
language_creators:
- other
annotations_creators:
- no-annotation
source_datasets:
- original
size_categories:
  bn-en:
  - 10K<n<100K
  bn-gu:
  - 1K<n<10K
  bn-hi:
  - 10K<n<100K
  bn-ml:
  - 1K<n<10K
  bn-mr:
  - 1K<n<10K
  bn-or:
  - n<1K
  bn-pa:
  - 1K<n<10K
  bn-ta:
  - 1K<n<10K
  bn-te:
  - n<1K
  bn-ur:
  - 1K<n<10K
  en-gu:
  - 10K<n<100K
  en-hi:
  - 100K<n<1M
  en-ml:
  - 10K<n<100K
  en-mr:
  - 10K<n<100K
  en-or:
  - 1K<n<10K
  en-pa:
  - 10K<n<100K
  en-ta:
  - 10K<n<100K
  en-te:
  - 1K<n<10K
  en-ur:
  - 10K<n<100K
  gu-hi:
  - 10K<n<100K
  gu-ml:
  - 1K<n<10K
  gu-mr:
  - 1K<n<10K
  gu-or:
  - n<1K
  gu-pa:
  - 1K<n<10K
  gu-ta:
  - 1K<n<10K
  gu-te:
  - 1K<n<10K
  gu-ur:
  - 1K<n<10K
  hi-ml:
  - 1K<n<10K
  hi-mr:
  - 10K<n<100K
  hi-or:
  - 1K<n<10K
  hi-pa:
  - 1K<n<10K
  hi-ta:
  - 10K<n<100K
  hi-te:
  - 1K<n<10K
  hi-ur:
  - 1K<n<10K
  ml-mr:
  - 1K<n<10K
  ml-or:
  - n<1K
  ml-pa:
  - 1K<n<10K
  ml-ta:
  - 1K<n<10K
  ml-te:
  - 1K<n<10K
  ml-ur:
  - 1K<n<10K
  mr-or:
  - n<1K
  mr-pa:
  - 1K<n<10K
  mr-ta:
  - 10K<n<100K
  mr-te:
  - n<1K
  mr-ur:
  - 1K<n<10K
  or-pa:
  - n<1K
  or-ta:
  - n<1K
  or-te:
  - n<1K
  or-ur:
  - n<1K
  pa-ta:
  - 1K<n<10K
  pa-te:
  - 1K<n<10K
  pa-ur:
  - 1K<n<10K
  ta-te:
  - 1K<n<10K
  ta-ur:
  - 1K<n<10K
  te-ur:
  - n<1K
licenses:
- cc-by-4.0
paperswithcode_id: null
pretty_name: CVIT PIB
---

# Dataset Card for CVIT PIB

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

### Dataset Description

- **Homepage:** http://preon.iiit.ac.in/~jerin/bhasha/
- **Paper:** https://arxiv.org/abs/2008.04860
- **Point of Contact:** [Mailing List](cvit-bhasha@googlegroups.com)

### Dataset Summary

This dataset is the large scale sentence aligned corpus in 11 Indian languages, viz. CVIT-PIB corpus that is the largest multilingual corpus available for Indian languages.

### Languages

Parallel data for following languages [en, bn, gu, hi, ml, mr, pa, or, ta, te, ur] are covered.

### Citation Information

```
@InProceedings{cvit-pib:multilingual-corpus,
title = {Revisiting Low Resource Status of Indian Languages in Machine Translation},
authors={Jerin Philip, Shashank Siripragada, Vinay P. Namboodiri, C.V. Jawahar
},
year={2020}
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.