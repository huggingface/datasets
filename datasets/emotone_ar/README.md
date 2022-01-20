---
annotations_creators:
- found
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
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
pretty_name: Emotional Tone in Arabic
---

# Dataset Card for Emotional Tone in Arabic

## Table of Contents
- [Dataset Card for Emotional Tone in Arabic](#dataset-card-for-emotional-tone-in-arabic)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
  - [|split|num examples|](#splitnum-examples)
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
    - [Contributions](#contributions)

## Dataset Description

- **Repository:** [Repository](https://github.com/AmrMehasseb/Emotional-Tone)
- **Paper:** [Emotional Tone Detection in Arabic Tweets](https://www.researchgate.net/publication/328164296_Emotional_Tone_Detection_in_Arabic_Tweets_18th_International_Conference_CICLing_2017_Budapest_Hungary_April_17-23_2017_Revised_Selected_Papers_Part_II)
- **Point of Contact:** [Amr Al-Khatib](https://github.com/AmrMehasseb)

### Dataset Summary

Dataset of 10065 tweets in Arabic for Emotion detection in Arabic text

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

example: 
```
    >>> {'label': 0, 'tweet': 'الاوليمبياد الجايه هكون لسه ف الكليه ..'}
```

### Data Fields

- "tweet": plain text tweet in Arabic

- "label": emotion class label

the dataset distribution and balance for each class looks like the following

|label||Label description |  Count    |
|---------|---------|  -------  | 
|0        |none     |   1550    |
|1        |anger    |   1444    |
|2        |joy      |   1281    |
|3        |sadness  |   1256    |
|4        |love     |   1220    |
|5        |sympathy |   1062    |
|6        |surprise |   1045    |
|7        |fear     |   1207    |

### Data Splits

The dataset is not split. 

|           | Tain   | 
|---------- | ------ | 
|no split   | 10,065  | 

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

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

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```
@inbook{inbook,
author = {Al-Khatib, Amr and El-Beltagy, Samhaa},
year = {2018},
month = {01},
pages = {105-114},
title = {Emotional Tone Detection in Arabic Tweets: 18th International Conference, CICLing 2017, Budapest, Hungary, April 17–23, 2017, Revised Selected Papers, Part II},
isbn = {978-3-319-77115-1},
doi = {10.1007/978-3-319-77116-8_8}
}
```

### Contributions

Thanks to [@abdulelahsm](https://github.com/abdulelahsm) for adding this dataset.