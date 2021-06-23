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
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
---

# Dataset Card for ArRestReviews

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

- **Homepage:** [Large Arabic Sentiment Analysis Resources](https://github.com/hadyelsahar/large-arabic-sentiment-analysis-resouces)
- **Repository:** [Large Arabic Sentiment Analysis Resources](https://github.com/hadyelsahar/large-arabic-sentiment-analysis-resouces)
- **Paper:** [ Building Large Arabic Multi-domain Resources for Sentiment Analysis](https://github.com/hadyelsahar/large-arabic-sentiment-analysis-resouces/blob/master/Paper%20-%20Building%20Large%20Arabic%20Multi-domain%20Resources%20for%20Sentiment%20Analysis.pdf)
- **Point of Contact:** [hady elsahar](hadyelsahar@gmail.com)

### Dataset Summary

Dataset of 8364 restaurant reviews from qaym.com in Arabic for sentiment analysis

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

A typical data point comprises of the following:

- "polarity": which is a string value of either 0 or 1 indicating the sentiment around the review    

- "text": is the review plain text of a restaurant in Arabic

- "restaurant_id": the restaurant ID on the website

- "user_id": the user ID on the website

example:
``` 
{
    'polarity': 0,  # negative
    'restaurant_id': '1412',
    'text': 'عادي جدا مامن زود',
    'user_id': '21294'
}
```

### Data Fields

- "polarity": is a string value of either 0 or 1 indicating the sentiment around the review    

- "text": is the review plain text of a restaurant in Arabic

- "restaurant_id": the restaurant ID on the website (string)

- "user_id": the user ID on the website (string)

### Data Splits

The dataset is not split. 

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

Contains 8364 restaurant reviews from qaym.com

#### Who are the source language producers?

From tweeter.  

### Annotations

The polarity field provides a label of 1 or -1 pertaining to the sentiment of the review

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Discussion of Social Impact and Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

@InProceedings{10.1007/978-3-319-18117-2_2,
author="ElSahar, Hady
and El-Beltagy, Samhaa R.",
editor="Gelbukh, Alexander",
title="Building Large Arabic Multi-domain Resources for Sentiment Analysis",
booktitle="Computational Linguistics and Intelligent Text Processing",
year="2015",
publisher="Springer International Publishing",
address="Cham",
pages="23--34",
isbn="978-3-319-18117-2"
}

### Contributions

Thanks to [@abdulelahsm](https://github.com/abdulelahsm) for adding this dataset.