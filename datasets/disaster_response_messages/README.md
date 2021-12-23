---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
- es
- fr
- ht
- ur
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
- text-classification
task_ids:
- intent-classification
- sentiment-classification
- text-simplification
paperswithcode_id: null
---

# Dataset Card for Disaster Response Messages 

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

- **Homepage: [HomePage](https://appen.com/datasets/combined-disaster-response-data/)
- **Repository: [Repo to Download the Dataset](https://datasets.appen.com/appen_datasets/disaster_response_data/disaster_response_messages_training.csv)
- **Paper:
- **Leaderboard:
- **Point of Contact:[Darshan Gandhi](darshangandhi1151@gmail.com)

### Dataset Summary

This dataset contains 30,000 messages drawn from events including an earthquake in Haiti in 2010, an earthquake in Chile in 2010, floods in Pakistan in 2010, super-storm Sandy in the U.S.A. in 2012, and news articles spanning a large number of years and 100s of different disasters. The data has been encoded with 36 different categories related to disaster response and has been stripped of messages with sensitive information in their entirety. Upon release, this is the featured dataset of a new Udacity course on Data Science and the AI4ALL summer school and is especially utile for text analytics and natural language processing (NLP) tasks and models.The input data in this job contains thousands of untranslated disaster-related messages and their English translations. In the “Data” tab above, you’ll find the annotated data, with 40 class labels for intent and content.

### Supported Tasks and Leaderboards

The input data in this job contains thousands of untranslated disaster-related messages and their English translations. In the dataset, you’ll find the annotated data, with 40 class labels for intent and content. This dataset contains the original message in its original language, the English translation, and dozens of classes for message content. These classes are noted in column titles with a simple binary 1= yes, 0=no.

### Languages

The dataset is a multilingual dataset which has the messages in the original language and also it's translated English form.

## Dataset Structure

### Data Instances

The dataset consists of a message in English and also it's original language form. Adding on, there are 40 labels which help to understand more about the exact essence of the message.

Example of a Disaster Response : { 'split': 'train', 'message': 'Weather update - a cold front from Cuba that could pass over Haiti', 'original': 'Un front froid se retrouve sur Cuba ce matin. Il pourrait traverser Haiti demain. Des averses de pluie isolee sont encore prevues sur notre region ce soi', 'genre': 'direct', 'related': 1, 'PII': 0, 'request': 0, 'offer': 0, 'aid_related': 0, 'medical_help': 0, 'medical_products': 0, 'search_and_rescue': 0, 'security': 0, 'military': 0, 'child_alone': 0, 'water': 0, 'food': 0, 'shelter': 0, 'clothing': 0, 'money': 0, 'missing_people': 0, 'refugees': 0, 'death': 0, 'other_aid': 0, 'infrastructure_related': 0, 'transport': 0, 'buildings': 0, 'electricity': 0, 'tools': 0, 'hospitals': 0, 'shops': 0, 'aid_centers': 0, 'other_infrastructure': 0, 'weather_related': 0, 'floods': 0, 'storm': 0, 'fire': 0, 'earthquake': 0, 'cold': 0, 'other_weather': 0, 'direct_report': 0}

### Data Fields

*split: Train, Test split</br>
*message: English text of actual messages related to disaster </br>
*original: Text of column 3 in native language as originally written</br>
*genre: Type of message, including direct messages, social posting, and news stories or bulletins</br>
*related: Is the message disaster related? 1= yes, 0=no, 2=maybe</br>
*PII: Does the message contain PII? 1= yes, 0=no </br>
*request: Does the message contain a request? 1= yes, 0=no </br>
*offer: Does the message contain an offer? 1= yes, 0=no </br>
*aid_related: Is the message aid related? 1= yes, 0=no </br>
*medical_help: Does the message concern medical help? 1= yes, 0=no </br>
*medical_products: Does the message concern medical products? 1= yes, 0=no </br>
*search_and_rescue: Does the message concern search and rescue? 1= yes, 0=no </br>
*security: Does the message concern security? 1= yes, 0=no </br>
*military: Does the message concern military? 1= yes, 0=no </br>
*child_alone: Does the message mention a child alone? 1= yes, 0=no</br>
*water: Does the message concern water? 1= yes, 0=no</br>
*food: Does the message concern food? 1= yes, 0=no </br>
*shelter: Does the message concern shelter? 1= yes, 0=no </br>
*clothing: Does the message concern clothing? 1= yes, 0=no </br>
*money: Does the message concern money? 1= yes, 0=no </br>
*missing_people: Does the message indicate missing people? 1= yes, 0=no</br>
*refugees: Does the message concern refugess? 1= yes, 0=no</br>
*death: Does the message imply death? 1= yes, 0=no </br>
*other_aid: Is there any other aid needed? 1=yes, 0=no </br>
*infrastructure_related: Does the message concern infrastructure? 1= yes, 0=no </br>
*transport: Does the message concern transport? 1= yes, 0=no </br>
*buildings: Does the message concern buildings? 1= yes, 0=no </br>
*electricity: Does the message concern electricity? 1= yes, 0=no </br>
*tools: Does the message concern tools? 1= yes, 0=no </br>
*hospitals: Does the message concern clothing? 1= yes, 0=no </br>
*shops: Does the message concern clothing? 1= yes, 0=no </br>
*aid_centers:Does the message concern clothing? 1= yes, 0=no </br>
*other_infrastructure:Does the message concern clothing? 1= yes, 0=no </br>
*weather_related: Does the message concern weather? 1= yes, 0=no</br>
*floods: Does the message indicate there was a flood? 1= yes, 0=no</br>
*storm: Does the message indicate there was a storm? 1= yes, 0=no </br>
*fire: Does the message indicate there was a fire? 1= yes, 0=no</br>
*earthquake: Does the message indicate there was an earthquake? 1= yes, 0=no</br>
*cold: Does the message indicate there was a cold? 1= yes, 0=no</br>
*other_weather: Does the message indicate there was other weather issues? 1= yes, 0=no</br>
*direct_report: Does the show a direct report? 1= yes, 0=no

### Data Splits

|train|test |validation|
|:----:|:-----------:|:----:|
|21046|2629|2573|

## Dataset Creation

### Curation Rationale

The dataset was built to understand about the sentiments of the citizens and also more about want was the emergency about and what kind of help they were seeking

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

The dataset has a great usecase of understand more about the sentiments of the citizens around the globe during a disaster and how their responses are. Also, it helps the government to understand their citizens better and would eventually help to draft better policies accordingly.

### Discussion of Biases

The messages since have been translated in English may not be able to judically imply the exact significance of the individual when they would have posted the message

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset was initially created by [Appen](https://appen.com/)

### Licensing Information

[More Information Needed]

### Citation Information

[Multilingual Disaster Response Messages](https://appen.com/datasets/combined-disaster-response-data/)


### Contributions

Thanks to [@darshan-gandhi](https://github.com/darshan-gandhi) for adding this dataset.