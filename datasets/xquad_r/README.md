---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
  ar:
  - ar
  de:
  - de
  el:
  - el
  en:
  - en
  es:
  - es
  hi:
  - hi
  ru:
  - ru
  th:
  - th
  tr:
  - tr
  vi:
  - vi
  zh:
  - zh
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|squad
- extended|xquad
task_categories:
- question-answering
task_ids:
- extractive-qa
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [LAReQA](https://github.com/google-research-datasets/lareqa)
- **Repository:** [XQuAD-R](https://github.com/google-research-datasets/lareqa)
- **Paper:** [LAReQA: Language-agnostic answer retrieval from a multilingual pool](https://arxiv.org/pdf/2004.05484.pdf)
- **Point of Contact:** [Noah Constant](mailto:nconstant@google.com)


### Dataset Summary
 
XQuAD-R is a retrieval version of the XQuAD dataset (a cross-lingual extractive
QA dataset). Like XQuAD, XQUAD-R is an 11-way parallel dataset,  where each
question appears in 11 different languages and has 11 parallel correct answers
across the languages.


### Supported Tasks and Leaderboards



### Languages

The dataset can be found with the following languages:
* Arabic: `xquad-r/ar.json`
* German: `xquad-r/de.json`
* Greek: `xquad-r/el.json`
* English: `xquad-r/en.json`
* Spanish: `xquad-r/es.json`
* Hindi: `xquad-r/hi.json`
* Russian: `xquad-r/ru.json`
* Thai: `xquad-r/th.json`
* Turkish: `xquad-r/tr.json`
* Vietnamese: `xquad-r/vi.json`
* Chinese: `xquad-r/zh.json`

## Dataset Structure

### Data Instances

The number of questions and candidate sentences for each language for XQuAD-R is shown in the table below.

|     | XQuAD-R   |            |
|-----|-----------|------------|
|     | questions | candidates |
| ar |      1190 |       1222 |
| de |      1190 |       1276 |
| el |      1190 |       1234 |
| en |      1190 |       1180 |
| es |      1190 |       1215 |
| hi |      1190 |       1244 |
| ru |      1190 |       1219 |
| th |      1190 |        852 |
| tr |      1190 |       1167 |
| vi |      1190 |       1209 |
| zh |      1190 |       1196 |

### Data Fields



### Data Splits



## Dataset Creation

### Curation Rationale



### Source Data

#### Initial Data Collection and Normalization



#### Who are the source language producers?



### Annotations

#### Annotation process



#### Who are the annotators?



### Personal and Sensitive Information



## Considerations for Using the Data

### Social Impact of Dataset



### Discussion of Biases



### Other Known Limitations



## Additional Information

### Dataset Curators

The dataset was initially created by Uma Roy, Noah Constant, Rami Al-Rfou, Aditya Barua, Aaron Phillips and Yinfei Yang, during work done at Google Research.

### Licensing Information

XQuAD-R is distributed under the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/legalcode).

### Citation Information

```
@article{roy2020lareqa,
  title={LAReQA: Language-agnostic answer retrieval from a multilingual pool},
  author={Roy, Uma and Constant, Noah and Al-Rfou, Rami and Barua, Aditya and Phillips, Aaron and Yang, Yinfei},
  journal={arXiv preprint arXiv:2004.05484},
  year={2020}
}
```
