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
---

# Dataset Card for kannada_news dataset 

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)

## Dataset Description

- **Homepage:** [Kaggle link](https://www.kaggle.com/disisbig/kannada-news-dataset) for kannada news headlines dataset
- **Point of Contact:** More information about the dataset and the models can be found [here](https://github.com/goru001/nlp-for-kannada)

### Dataset Summary

The Kannada news dataset contains only the headlines of news article in three categories:
Entertainment, Tech, and Sports.

The data set contains around 6300 news article headlines which are collected from Kannada news websites.
The data set has been cleaned and contains train and test set using which can be used to benchmark topic classification models in Kannada.


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
NOTE: The data has very few examples on the technology (class label: 'tech') topic. 


### Data Fields

Data has two fields:
- headline: text headline in kannada (string)
- label : corresponding class label which the headlines pertains to in english (string)


### Data Splits

Describe and name the splits in the dataset if there are more than one.

Describe any criteria for splitting the data, if used. If their are differences between the splits (e.g. if the training annotations are machine-generated and the dev and test ones are created by humans, or if different numbers of annotators contributed to each example), describe them here.

Provide the sizes of each split. As appropriate, provide any descriptive statistics for the features, such as average length.  For example:

|                            | Tain   | Valid | 
| -----                      | ------ | ----- |
| Input Sentences            |  5167  | 1293  |


## Considerations for Using the Data

### Social Impact of Dataset

There are starkingly less amount of data for South Indian languages, especially Kannada, available in digital format which can be used for NLP purposes.
Though having roughly 38 million native speakers, it is a little under-represented language and will benifit from active contribution from the community.

This dataset, however, can just help people get exposed to Kannada and help proceed further active participation for enabling continuous progress and development.


## Additional Information

### Dataset Curators

[Gaurav Arora] (https://github.com/goru001/nlp-for-kannada) has also got some starter models an embeddings to help get started.
