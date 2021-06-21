---
annotations_creators:
- found
language_creators:
- found
multilinguality:
- multilingual
languages:
- en
- vi
licenses:
- unknown
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
---

# Dataset Card for mt_eng_vietnamese

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

- **Homepage:** https://nlp.stanford.edu/projects/nmt/data/iwslt15.en-vi/
- **Repository:** [Needs More Information]
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

Preprocessed Dataset from IWSLT'15 English-Vietnamese machine translation: English-Vietnamese.

### Supported Tasks and Leaderboards

Machine Translation 

### Languages

English, Vietnamese

## Dataset Structure

### Data Instances

An example from the dataset:
```
{
  'translation': {
    'en': 'In 4 minutes , atmospheric chemist Rachel Pike provides a glimpse of the massive scientific effort behind the bold headlines on climate change , with her team -- one of thousands who contributed -- taking a risky flight over the rainforest in pursuit of data on a key molecule .', 
    'vi': 'Trong 4 phút , chuyên gia hoá học khí quyển Rachel Pike giới thiệu sơ lược về những nỗ lực khoa học miệt mài đằng sau những tiêu đề táo bạo về biến đổi khí hậu , cùng với đoàn nghiên cứu của mình -- hàng ngàn người đã cống hiến cho dự án này -- một chuyến bay mạo hiểm qua rừng già để tìm kiếm thông tin về một phân tử then chốt .'
    }
}
```


### Data Fields

- translation:
  - en: text in english
  - vi: text in vietnamese


### Data Splits

train: 133318, validation: 1269, test: 1269

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

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
@inproceedings{Luong-Manning:iwslt15,
        Address = {Da Nang, Vietnam}
        Author = {Luong, Minh-Thang  and Manning, Christopher D.},
        Booktitle = {International Workshop on Spoken Language Translation},
        Title = {Stanford Neural Machine Translation Systems for Spoken Language Domain},
        Year = {2015}}

```

### Contributions

Thanks to [@Nilanshrajput](https://github.com/Nilanshrajput) for adding this dataset.