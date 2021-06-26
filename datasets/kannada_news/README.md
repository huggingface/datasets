---
annotations_creators:
- other
language_creators:
- other
languages:
- kn
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- topic-classification
paperswithcode_id: null
---

# Dataset Card for kannada_news dataset 

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

- **Homepage:** [Kaggle link](https://www.kaggle.com/disisbig/kannada-news-dataset) for kannada news headlines dataset
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** More information about the dataset and the models can be found [here](https://github.com/goru001/nlp-for-kannada)

### Dataset Summary

The Kannada news dataset contains only the headlines of news article in three categories:
Entertainment, Tech, and Sports.

The data set contains around 6300 news article headlines which are collected from Kannada news websites.
The data set has been cleaned and contains train and test set using which can be used to benchmark topic classification models in Kannada.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Kannada (kn)

## Dataset Structure

### Data Instances

The data has two files. A train.csv and valid.csv. An example row of the dataset is as below:

```
{
  'headline': 'ಫಿಫಾ ವಿಶ್ವಕಪ್ ಫೈನಲ್: ಅತಿರೇಕಕ್ಕೇರಿದ ಸಂಭ್ರಮಾಚರಣೆ; ಅಭಿಮಾನಿಗಳ ಹುಚ್ಚು ವರ್ತನೆಗೆ ವ್ಯಾಪಕ ಖಂಡನೆ',
  'label':'sports'
}
```
NOTE: The data has very few examples on the technology (class label: 'tech') topic. [More Information Needed]

### Data Fields

Data has two fields:
- headline: text headline in kannada (string)
- label : corresponding class label which the headlines pertains to in english (string)

### Data Splits

The dataset is divided into two splits. All the headlines are scraped from news websites on the internet.
|                            | Tain   | Valid | 
| -----                      | ------ | ----- |
| Input Sentences            |  5167  | 1293  |

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

There are starkingly less amount of data for South Indian languages, especially Kannada, available in digital format which can be used for NLP purposes.
Though having roughly 38 million native speakers, it is a little under-represented language and will benefit from active contribution from the community.

This dataset, however, can just help people get exposed to Kannada and help proceed further active participation for enabling continuous progress and development.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[Gaurav Arora] (https://github.com/goru001/nlp-for-kannada). Has also got some starter models an embeddings to help get started.

### Licensing Information

cc-by-sa-4.0

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@vrindaprabhu](https://github.com/vrindaprabhu) for adding this dataset.