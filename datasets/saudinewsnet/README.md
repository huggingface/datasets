---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- ar
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: null
---

# Dataset Card for "saudinewsnet"

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

- **Homepage:** [SaudiNewsNet](https://github.com/parallelfold/SaudiNewsNet)
- **Repository:** [Website](https://github.com/parallelfold/SaudiNewsNet)
- **Paper:** [More Information Needed]
- **Point of Contact:** [Mazen Abdulaziz](mailto:mazen.abdulaziz@gmail.com)
- **Size of downloaded dataset files:** 27.67 MB
- **Size of the generated dataset:** 98.85 MB
- **Total amount of disk used:** 126.52 MB

### Dataset Summary

The dataset contains a set of 31,030 Arabic newspaper articles alongwith metadata, extracted from various online Saudi newspapers and written in MSA.

The dataset currently contains **31,030** Arabic articles (with a total number of **8,758,976 words**). The articles were extracted from the following Saudi newspapers (sorted by number of articles):

- [Al-Riyadh](http://www.alriyadh.com/) (4,852 articles)
- [Al-Jazirah](http://al-jazirah.com/) (3,690 articles)
- [Al-Yaum](http://alyaum.com/) (3,065 articles)
- [Al-Eqtisadiya](http://aleqt.com/) (2,964 articles)
- [Al-Sharq Al-Awsat](http://aawsat.com/) (2,947 articles)
- [Okaz](http://www.okaz.com.sa/) (2,846 articles)
- [Al-Watan](http://alwatan.com.sa/) (2,279 articles)
- [Al-Madina](http://www.al-madina.com/) (2,252 articles)
- [Al-Weeam](http://alweeam.com.sa/) (2,090 articles)
- [Ain Alyoum](http://3alyoum.com/) (2,080 articles)
- [Sabq](http://sabq.org/) (1,411 articles)
- [Saudi Press Agency](http://www.spa.gov.sa) (369 articles)
- [Arreyadi](http://www.arreyadi.com.sa/) (133 articles)
- [Arreyadiyah](http://www.arreyadiyah.com/) (52 articles)

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

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

### Data Fields

The data fields are the same among all splits.

- **`source`** (str): The source newspaper.
- **`url`** (str): The full URL from which the article was extracted.
- **`date_extracted`** (str): The timestamp of the date on which the article was extracted. It has the format `YYYY-MM-DD hh:mm:ss`. Notice that this field does not necessarily represent the date on which the article was authored (or made available online), however for articles stamped with a date of extraction after August 1, 2015, this field most probably represents the date of authoring.
- **`title`** (str): The title of the article. Contains missing values that were replaced with an empty string.
- **`author`** (str): The author of the article. Contains missing values that were replaced with an empty string.
- **`content`** (str): The content of the article.

### Data Splits

| name  |train|
|-------|----:|
|default|31030|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

    | String Identifier  | Newspaper |
    | ------------------ | --------- |
    | aawsat | [Al-Sharq Al-Awsat](http://aawsat.com/) |
    | aleqtisadiya | [Al-Eqtisadiya](http://aleqt.com/) |
    | aljazirah | [Al-Jazirah](http://al-jazirah.com/) |
    | almadina | [Al-Madina](http://www.al-madina.com/) |
    | alriyadh | [Al-Riyadh](http://www.alriyadh.com/) |
    | alwatan | [Al-Watan](http://alwatan.com.sa/) |
    | alweeam | [Al-Weeam](http://alweeam.com.sa/) |
    | alyaum | [Al-Yaum](http://alyaum.com/)  |
    | arreyadi | [Arreyadi](http://www.arreyadi.com.sa/) |
    | arreyadiyah | [Arreyadi](http://www.arreyadiyah.com/) |
    | okaz | [Okaz](http://www.okaz.com.sa/) |
    | sabq | [Sabq](http://sabq.org/) |
    | was | [Saudi Press Agency](http://www.spa.gov.sa/) |
    | 3alyoum | [Ain Alyoum](http://3alyoum.com/) |

#### Initial Data Collection and Normalization

The Modern Standard Arabic texts crawled from the Internet.

#### Who are the source language producers?

Newspaper Websites.

### Annotations

The dataset does not contain any additional annotations.

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

### Citation Information

```
@misc{hagrima2015,
author = "M. Alhagri",
title = "Saudi Newspapers Arabic Corpus (SaudiNewsNet)",
year = 2015,
url = "http://github.com/ParallelMazen/SaudiNewsNet"
}
```

### Contributions

Thanks to [@abdulelahsm](https://github.com/abdulelahsm) for adding this dataset.