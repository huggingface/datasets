---
task_categories:
- sequence-modeling
multilinguality:
- translation
task_ids:
- language-modeling
languages:
- 99 languages
annotations_creators:
- no-annotation
source_datasets:
- extended
size_categories:
- 10K<n<1M
licenses:
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

[MORE INFORMATION NEEDED]

### Languages

OPUS-100 contains approximately 55M sentence pairs. Of the 99 language pairs, 44 have 1M sentence pairs of training data, 73 have at least 100k, and 95 have at least 10k.

Following language pairs are available:
['ar-de', 'ar-fr', 'ar-nl', 'ar-ru', 'ar-zh', 'de-fr', 'de-nl', 'de-ru', 'de-zh', 'fr-nl', 'fr-ru', 'fr-zh', 'nl-ru', 'nl-zh', 'ru-zh', 'af-en', 'am-en', 'an-en', 'ar-en', 'as-en', 'az-en', 'be-en', 'bg-en', 'bn-en', 'br-en', 'bs-en', 'ca-en', 'cs-en', 'cy-en', 'da-en', 'de-en', 'dz-en', 'el-en', 'en-eo', 'en-es', 'en-et', 'en-eu', 'en-fa', 'en-fi', 'en-fr', 'en-fy', 'en-ga', 'en-gd', 'en-gl', 'en-gu', 'en-ha', 'en-he', 'en-hi', 'en-hr', 'en-hu', 'en-hy', 'en-id', 'en-ig', 'en-is', 'en-it', 'en-ja', 'en-ka', 'en-kk', 'en-km', 'en-ko', 'en-kn', 'en-ku', 'en-ky', 'en-li', 'en-lt', 'en-lv', 'en-mg', 'en-mk', 'en-ml', 'en-mn', 'en-mr', 'en-ms', 'en-mt', 'en-my', 'en-nb', 'en-ne', 'en-nl', 'en-nn', 'en-no', 'en-oc', 'en-or', 'en-pa', 'en-pl', 'en-ps', 'en-pt', 'en-ro', 'en-ru', 'en-rw', 'en-se', 'en-sh', 'en-si', 'en-sk', 'en-sl', 'en-sq', 'en-sr', 'en-sv', 'en-ta', 'en-te', 'en-tg', 'en-th', 'en-tk', 'en-tr', 'en-tt', 'en-ug', 'en-uk', 'en-ur', 'en-uz', 'en-vi', 'en-wa', 'en-xh', 'en-yi', 'en-yo', 'en-zh', 'en-zu']

## Dataset Structure

### Data Instances

[MORE INFORMATION NEEDED]

### Data Fields

- `src_tag`: `string` text in source language
- `tgt_tag`: `string` translation of source language in target language

### Data Splits

The dataset is split into training, development, and test portions. Data was prepared by randomly sampled up to 1M sentence pairs per language pair for training and up to 2000 each for development and test. To ensure that there was no overlap (at the monolingual sentence level) between the training and development/test data, they applied a filter during sampling to exclude sentences that had already been sampled. Note that this was done cross-lingually so that, for instance, an English sentence in the Portuguese-English portion of the training data could not occur in the Hindi-English test set.

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

[MORE INFORMATION NEEDED]

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
