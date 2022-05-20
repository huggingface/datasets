---
task_categories:
- text-generation
- fill-mask
multilinguality:
- translation
task_ids:
- language-modeling
- masked-language-modeling
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
- n<1K
licenses:
- cc-by-4.0
paperswithcode_id: null
pretty_name: CVIT MKB
configs:
- bn-en
- bn-gu
- bn-hi
- bn-ml
- bn-mr
- bn-or
- bn-ta
- bn-te
- bn-ur
- en-gu
- en-hi
- en-ml
- en-mr
- en-or
- en-ta
- en-te
- en-ur
- gu-hi
- gu-ml
- gu-mr
- gu-or
- gu-ta
- gu-te
- gu-ur
- hi-ml
- hi-mr
- hi-or
- hi-ta
- hi-te
- hi-ur
- ml-mr
- ml-or
- ml-ta
- ml-te
- ml-ur
- mr-or
- mr-ta
- mr-te
- mr-ur
- or-ta
- or-te
- or-ur
- ta-te
- ta-ur
- te-ur
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