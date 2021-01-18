---
---

# Dataset Card for "saudinewsnet"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://github.com/parallelfold/SaudiNewsNet](https://github.com/parallelfold/SaudiNewsNet)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 27.67 MB
- **Size of the generated dataset:** 98.85 MB
- **Total amount of disk used:** 126.52 MB

### [Dataset Summary](#dataset-summary)

The dataset contains a set of 31,030 Arabic newspaper articles alongwith metadata, extracted from various online Saudi newspapers and written in MSA.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 27.67 MB
- **Size of the generated dataset:** 98.85 MB
- **Total amount of disk used:** 126.52 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "author": "الرياض: محمد الحميدي",
    "content": "\"في وقت تتهيأ فيه السعودية لإطلاق الإصدار الثاني من العملات المعدنية، لا تزال التداول بمبالغ النقود المصنوعة من المعدن مستقرة عن...",
    "date_extracted": "2015-07-22 01:18:37",
    "source": "aawsat",
    "title": "\"«العملة المعدنية» السعودية تسجل انحسارًا تاريخيًا وسط تهيؤ لإطلاق الإصدار الثاني\"...",
    "url": "\"http://aawsat.com/home/article/411671/«العملة-المعدنية»-السعودية-تسجل-انحسارًا-تاريخيًا-وسط-تهيؤ-لإطلاق-الإصدار-الثاني\"..."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `source`: a `string` feature.
- `url`: a `string` feature.
- `date_extracted`: a `string` feature.
- `title`: a `string` feature.
- `author`: a `string` feature.
- `content`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|
|-------|----:|
|default|31030|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```
@misc{hagrima2015,
author = "M. Alhagri",
title = "Saudi Newspapers Arabic Corpus (SaudiNewsNet)",
year = 2015,
url = "http://github.com/ParallelMazen/SaudiNewsNet"
}

```

