---
task_categories:
- sequence-modeling
multilinguality:
- translation
task_ids:
- language-modeling
languages:
- hi
- te
- ta
- ml
- gu
- ur
- bn
- or
- mr
- pa
- en
annotations_creators:
- no-annotation
source_datasets:
- original
size_categories:
  bn-en:
  - 1K<n<10K
  bn-gu:
  - 1K<n<10K
  bn-hi:
  - 1K<n<10K
  bn-ml:
  - 1K<n<10K
  bn-mr:
  - 1K<n<10K
  bn-or:
  - n<1K
  bn-ta:
  - 1K<n<10K
  bn-te:
  - 1K<n<10K
  bn-ur:
  - n<1K
  en-gu:
  - 1K<n<10K
  en-hi:
  - 1K<n<10K
  en-ml:
  - 1K<n<10K
  en-mr:
  - 1K<n<10K
  en-or:
  - n<1K
  en-ta:
  - 1K<n<10K
  en-te:
  - 1K<n<10K
  en-ur:
  - 1K<n<10K
  gu-hi:
  - 1K<n<10K
  gu-ml:
  - 1K<n<10K
  gu-mr:
  - 1K<n<10K
  gu-or:
  - n<1K
  gu-ta:
  - 1K<n<10K
  gu-te:
  - 1K<n<10K
  gu-ur:
  - n<1K
  hi-ml:
  - 1K<n<10K
  hi-mr:
  - 1K<n<10K
  hi-or:
  - n<1K
  hi-ta:
  - 1K<n<10K
  hi-te:
  - 1K<n<10K
  hi-ur:
  - n<1K
  ml-mr:
  - 1K<n<10K
  ml-or:
  - n<1K
  ml-ta:
  - 1K<n<10K
  ml-te:
  - 1K<n<10K
  ml-ur:
  - n<1K
  mr-or:
  - n<1K
  mr-ta:
  - 1K<n<10K
  mr-te:
  - 1K<n<10K
  mr-ur:
  - n<1K
  or-ta:
  - n<1K
  or-te:
  - n<1K
  or-ur:
  - n<1K
  ta-te:
  - 1K<n<10K
  ta-ur:
  - n<1K
  te-ur:
  - n<1K
licenses:
- cc-by-4.0
paperswithcode_id: null
pretty_name: CVIT MKB
---

# Dataset Card for CVIT MKB

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

- **Homepage:** [Link](http://preon.iiit.ac.in/~jerin/bhasha/) 
- **Repository:**
- **Paper:** [ARXIV](https://arxiv.org/abs/2007.07691)
- **Leaderboard:** 
- **Point of Contact:** [email](cvit-bhasha@googlegroups.com)

### Dataset Summary

Indian Prime Minister's speeches - Mann Ki Baat, on All India Radio, translated into many languages.

### Supported Tasks and Leaderboards

[MORE INFORMATION NEEDED]

### Languages

Hindi, Telugu, Tamil, Malayalam, Gujarati, Urdu, Bengali, Oriya, Marathi, Punjabi, and English

## Dataset Structure

### Data Instances

[MORE INFORMATION NEEDED]

### Data Fields

- `src_tag`: `string` text in source language
- `tgt_tag`: `string` translation of source language in target language

### Data Splits

[MORE INFORMATION NEEDED]

## Dataset Creation

### Curation Rationale

[MORE INFORMATION NEEDED]

### Source Data

[MORE INFORMATION NEEDED]

#### Initial Data Collection and Normalization

[MORE INFORMATION NEEDED]

#### Who are the source language producers?

[MORE INFORMATION NEEDED]

### Annotations

#### Annotation process

[MORE INFORMATION NEEDED]

#### Who are the annotators?

[MORE INFORMATION NEEDED]

### Personal and Sensitive Information

[MORE INFORMATION NEEDED]

## Considerations for Using the Data

### Social Impact of Dataset

[MORE INFORMATION NEEDED]

### Discussion of Biases

[MORE INFORMATION NEEDED]

### Other Known Limitations

[MORE INFORMATION NEEDED]

## Additional Information

### Dataset Curators

[MORE INFORMATION NEEDED]

### Licensing Information

The datasets and pretrained models provided here are licensed under Creative Commons Attribution-ShareAlike 4.0 International License.

### Citation Information

```
@misc{siripragada2020multilingual,
      title={A Multilingual Parallel Corpora Collection Effort for Indian Languages},
      author={Shashank Siripragada and Jerin Philip and Vinay P. Namboodiri and C V Jawahar},
      year={2020},
      eprint={2007.07691},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.