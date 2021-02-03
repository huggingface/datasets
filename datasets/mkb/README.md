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
- 1K<n<10K
licenses:
- cc-by-4.0
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

- **Homepage:** [Link](http://preon.iiit.ac.in/~jerin/bhasha/) 
- **Repository:**
- **Paper:** [ARXIV](https://arxiv.org/abs/2007.07691)
- **Leaderboard:** 
- **Point of Contact:** cvit-bhasha@googlegroups.com

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