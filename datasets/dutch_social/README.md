---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
- en
- nl
licenses:
- cc-by-nc-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
- multi-label-classification
paperswithcode_id: null
---

# Dataset Card for Dutch Social Media Collection

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

- **Homepage:[Dutch Social Media Collection](http://datasets.coronawhy.org/dataset.xhtml?persistentId=doi:10.5072/FK2/MTPTL7)**
- **Repository: **
- **Paper:*(in-progress)* https://doi.org/10.5072/FK2/MTPTL7**
- **Leaderboard:**
- **Point of Contact: [Aakash Gupta](mailto:aakashg80@gmail.com)**

### Dataset Summary

The dataset contains 10 files with around 271,342 tweets. The tweets are filtered via the official Twitter API to contain tweets in Dutch language or by users who have specified their location information within Netherlands geographical boundaries. Using natural language processing we have classified the tweets for their HISCO codes. If the user has provided their location within Dutch boundaries, we have also classified them to their respective provinces The objective of this dataset is to make research data available publicly in a FAIR (Findable, Accessible, Interoperable, Reusable) way. Twitter's Terms of Service Licensed under Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) (2020-10-27)

### Supported Tasks and Leaderboards

`sentiment analysis`, `multi-label classification`, `entity-extraction`

### Languages

The text is primarily in Dutch with some tweets in English and other languages. The BCP 47 code is `nl` and `en`

## Dataset Structure

### Data Instances

An example of the data field will be: 

```
{
  "full_text": "@pflegearzt @Friedelkorn @LAguja44 Pardon, wollte eigentlich das zitieren: \nhttps://t.co/ejO7bIMyj8\nMeine mentions sind inzw komplett undurchschaubar weil da Leute ihren supporterclub zwecks Likes zusammengerufen haben.",
  "text_translation": "@pflegearzt @Friedelkorn @ LAguja44 Pardon wollte zitieren eigentlich das:\nhttps://t.co/ejO7bIMyj8\nMeine mentions inzw sind komplett undurchschaubar weil da Leute ihren supporter club Zwecks Likes zusammengerufen haben.",
  "created_at": 1583756789000,
  "screen_name": "TheoRettich",
  "description": "I ❤️science, therefore a Commie.   ☭ FALGSC: Part of a conspiracy which wants to achieve world domination. Tankie-Cornucopian. Ecology is a myth",
  "desc_translation": "I ❤️science, Therefore a Commie. ☭ FALGSC: Part of a conspiracy How many followers wants to Achieve World Domination. Tankie-Cornucopian. Ecology is a myth",
  "weekofyear": 11,
  "weekday": 0,
  "day": 9,
  "month": 3,
  "year": 2020,
  "location": "Netherlands",
  "point_info": "Nederland",
  "point": "(52.5001698, 5.7480821, 0.0)",
  "latitude": 52.5001698,
  "longitude": 5.7480821,
  "altitude": 0,
  "province": "Flevoland",
  "hisco_standard": null,
  "hisco_code": null,
  "industry": false,
  "sentiment_pattern": 0,
  "subjective_pattern": 0
}
```

### Data Fields


| Column Name | Description |
| --- | --- |
| full_text | Original text in the tweet |
| text_translation | English translation of the full text |
| created_at | Date of tweet creation | 
| screen_name | username of the tweet author |
| description | description as provided in the users bio | 
| desc_translation | English translation of user's bio/ description | 
| location | Location information as provided in the user's bio |
| weekofyear | week of the year |
| weekday | Day of the week information; Monday=0....Sunday = 6| 
| month | Month of tweet creation |
| year | year of tweet creation |
| day | day of tweet creation |
| point_info | point information from location columnd |
| point | tuple giving lat, lon & altitude information |
| latitude | geo-referencing information derived from location data | 
| longitude | geo-referencing information derived from location data |
| altitude | geo-referencing information derived from location data|
| province | Province given location data of user |
| hisco_standard | HISCO standard key word; if available in tweet |
| hisco_code| HISCO standard code as derived from `hisco_standard`|
| industry | Whether the tweet talks about industry `(True/False)` |
| sentiment_score | Sentiment score -1.0 to 1.0 |
| subjectivity_score | Subjectivity scores 0 to 1 |

Missing values are replaced with empty strings or -1 (-100 for missing sentiment_score).


### Data Splits

Data has been split into Train: 60%, Validation: 20% and Test: 20%

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The tweets were hydrated using Twitter's API and then filtered for those which were in Dutch language and/or for users who had mentioned that they were from within Netherlands geographical borders. 

#### Who are the source language producers?

The language producers are twitter users who have identified their location within the geographical boundaries of Netherland. Or those who have tweeted in the dutch language!

### Annotations

Using Natural language processing, we have classified the tweets on industry and for HSN HISCO codes. 
Depending on the user's location, their provincial information is also added. Please check the file/column for detailed information. 

The tweets are also classified on the sentiment & subjectivity scores. 
Sentiment scores are between -1 to +1 
Subjectivity scores are between 0 to 1

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

As of writing this data card no anonymization has been carried out on the tweets or user data. As such, if the twitter user has shared any personal & sensitive information, then it may be available in this dataset. 

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[Aakash Gupta](mailto:aakashg80@gmail.com) 
*Th!nkEvolve Consulting* and Researcher at CoronaWhy

### Licensing Information

CC BY-NC 4.0

### Citation Information

@data{FK2/MTPTL7_2020,
author = {Gupta, Aakash},
publisher = {COVID-19 Data Hub},
title = {{Dutch social media collection}},
year = {2020},
version = {DRAFT VERSION},
doi = {10.5072/FK2/MTPTL7},
url = {https://doi.org/10.5072/FK2/MTPTL7}
}

### Contributions

Thanks to [@skyprince999](https://github.com/skyprince999) for adding this dataset.