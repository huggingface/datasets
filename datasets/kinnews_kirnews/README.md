---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- rn
- rw
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  kinnews_cleaned:
  - 10K<n<100K
  kinnews_raw:
  - 10K<n<100K
  kirnews_cleaned:
  - 1K<n<10K
  kirnews_raw:
  - 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- topic-classification
paperswithcode_id: kinnews-and-kirnews
---
# Dataset Card for kinnews_kirnews

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

- **Homepage:** [More Information Needed]
- **Repository:** https://github.com/Andrews2017/KINNEWS-and-KIRNEWS-Corpus
- **Paper:** [KINNEWS and KIRNEWS: Benchmarking Cross-Lingual Text Classification for Kinyarwanda and Kirundi](https://arxiv.org/abs/2010.12174)
- **Leaderboard:** NA
- **Point of Contact:** [Rubungo Andre Niyongabo1](mailto:niyongabor.andre@std.uestc.edu.cn)

### Dataset Summary

Kinyarwanda and Kirundi news classification datasets (KINNEWS and KIRNEWS,respectively), which were both collected from Rwanda and Burundi news websites and newspapers, for low-resource monolingual and cross-lingual multiclass classification tasks.

### Supported Tasks and Leaderboards
This dataset can be used for text classification of news articles in Kinyarwadi and Kirundi languages. Each news article can be classified into one of the 14 possible classes. The classes are:

- politics
- sport
- economy
- health
- entertainment
- history
- technology
- culture
- religion
- environment
- education
- relationship


### Languages

Kinyarwanda and Kirundi

## Dataset Structure

### Data Instances

Here is an example from the dataset:

| Field | Value |
| ----- | ----------- |
| label | 1 |
| kin_label/kir_label | 'inkino' |
| url | 'https://nawe.bi/Primus-Ligue-Imirwi-igiye-guhura-gute-ku-ndwi-ya-6-y-ihiganwa.html' |
| title | 'Primus Ligue\xa0: Imirwi igiye guhura gute ku ndwi ya 6 y’ihiganwa\xa0?'|
| content | ' Inkino zitegekanijwe kuruno wa gatandatu igenekerezo rya 14 Nyakanga umwaka wa 2019...'|
| en_label| 'sport'|




### Data Fields

The raw version of the data for Kinyarwanda language consists of these fields
- label: The category of the news article
- kin_label/kir_label: The associated label in Kinyarwanda/Kirundi language
- en_label: The associated label in English
- url: The URL of the news article
- title: The title of the news article
- content: The content of the news article

The cleaned version contains only the `label`, `title` and the `content` fields
 

### Data Splits

Lang| Train | Test |
|---| ----- | ---- |
|Kinyarwandai Raw|17014|4254|
|Kinyarwandai Clean|17014|4254|
|Kirundi Raw|3689|923|
|Kirundi Clean|3689|923|

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

[More Information Needed]

### Contributions

Thanks to [@saradhix](https://github.com/saradhix) for adding this dataset.