---
annotations_creators:
  monolingual:
  - no-annotation
  monolingual_raw:
  - found
  parallel:
  - expert-generated
  parallel_raw:
  - expert-generated
language_creators:
- found
languages:
  monolingual:
  - chr
  - en
  monolingual_raw:
  - chr
  parallel:
  - chr
  - en
  parallel_raw:
  - chr
  - en
licenses:
- other-different-license-per-source
multilinguality:
  monolingual:
  - multilingual
  monolingual_raw:
  - monolingual
  parallel:
  - translation
  parallel_raw:
  - translation
size_categories:
  monolingual:
  - 100K<n<1M
  monolingual_raw:
  - 1K<n<10K
  parallel:
  - 10K<n<100K
  parallel_raw:
  - 10K<n<100K
source_datasets:
- original
task_categories:
  monolingual:
  - conditional-text-generation
  monolingual_raw:
  - sequence-modeling
  parallel:
  - conditional-text-generation
  parallel_raw:
  - conditional-text-generation
task_ids:
  monolingual:
  - machine-translation
  monolingual_raw:
  - language-modeling
  parallel:
  - machine-translation
  parallel_raw:
  - machine-translation
---

# Dataset Card for ChrEn

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Repository:** [Github repository for ChrEn](https://github.com/ZhangShiyue/ChrEn)
- **Paper:** [ChrEn: Cherokee-English Machine Translation for Endangered Language Revitalization](https://arxiv.org/abs/2010.04791)
- **Point of Contact:** [benfrey@email.unc.edu](benfrey@email.unc.edu)

### Dataset Summary

ChrEn is a Cherokee-English parallel dataset to facilitate machine translation research between Cherokee and English.
ChrEn is extremely low-resource contains 14k sentence pairs in total, split in ways that facilitate both in-domain and out-of-domain evaluation.
ChrEn also contains 5k Cherokee monolingual data to enable semi-supervised learning.

### Supported Tasks and Leaderboards

The dataset is intended to use for `machine-translation` between Enlish (`en`) and Cherokee (`chr`).

### Languages

The dataset contains Enlish (`en`) and Cherokee (`chr`) text. The data encompasses both existing dialects of Cherokee: the Overhill dialect, mostly spoken in Oklahoma (OK), and the Middle dialect, mostly used in North Carolina (NC).

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Many of the source texts were translations of English materials, which means that the Cherokee structures may not be 100% natural in terms of what a speaker might spontaneously produce. Each text was translated by people who speak Cherokee as the first language, which means there is a high probability of grammaticality. These data were originally available in PDF version. We apply the Optical Character Recognition (OCR) via Tesseract OCR engine to extract the Cherokee and English text.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

The sentences were manually aligned by Dr. Benjamin Frey a proficient second-language speaker of Cherokee, who also fixed the errors introduced by OCR. This process is time-consuming and took several months.

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

The dataset was gathered and annotated by Shiyue Zhang, Benjamin Frey, and Mohit Bansal at UNC Chapel Hill.

### Licensing Information

The copyright of the data belongs to original book/article authors or translators (hence, used for research purpose; and please contact Dr. Benjamin Frey for other copyright questions).

### Citation Information

```
@inproceedings{zhang2020chren,
  title={ChrEn: Cherokee-English Machine Translation for Endangered Language Revitalization},
  author={Zhang, Shiyue and Frey, Benjamin and Bansal, Mohit},
  booktitle={EMNLP2020},
  year={2020}
}
```
