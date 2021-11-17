---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
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
- text-scoring
task_ids:
- sentiment-classification
- sentiment-scoring
paperswithcode_id: null
pretty_name: OCLAR
---

# Dataset Card for OCLAR

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

- **Homepage:** [OCLAR homepage](http://archive.ics.uci.edu/ml/datasets/Opinion+Corpus+for+Lebanese+Arabic+Reviews+%28OCLAR%29#)
- **Paper:** [paper link](https://www.semanticscholar.org/paper/Sentiment-Classifier%3A-Logistic-Regression-for-in-Omari-Al-Hajj/9319f4d9e8b3b7bfd0d214314911c071ba7ce1a0)
- **Point of Contact:** [Marwan Al Omari](marwanalomari@yahoo.com)

### Dataset Summary

The researchers of OCLAR Marwan et al. (2019), they gathered Arabic costumer reviews [Zomato website](https://www.zomato.com/lebanon)
on wide scope of domain, including restaurants, hotels, hospitals, local shops, etc.
The corpus finally contains 3916 reviews in 5-rating scale. For this research purpose, the positive class considers
rating stars from 5 to 3 of 3465 reviews, and the negative class is represented from values of 1 and 2 of about 451
texts.

### Supported Tasks and Leaderboards

Opinion Corpus for Lebanese Arabic Reviews (OCLAR) corpus is utilizable for Arabic sentiment classification on services
reviews, including hotels, restaurants, shops, and others.

### Languages

The text in the dataset is in Arabic, mainly in Lebanese (LB). The associated BCP-47 code is `ar-LB`.

## Dataset Structure

### Data Instances

A typical data point comprises a `pagename` which is the name of service / location being reviewed, a `review` which is
the review left by the user / client , and a `rating` which is a score between 1 and 5.

The authors consider a review to be positive if the score is greater or equal than `3`, else it is considered negative.

An example from the OCLAR data set looks as follows:

```
  "pagename": 'Ramlet Al Baida Beirut Lebanon',
  "review": 'مكان يطير العقل ويساعد على الاسترخاء',
  "rating": 5,
```

### Data Fields

- `pagename`: string name of the service / location being reviewed
- `review`: string review left by the user / costumer
- `rating`: number of stars left by the reviewer. It ranges from 1 to 5.

### Data Splits

The data set comes in a single csv file of a total `3916` reviews :
- `3465` are considered positive (a rating of 3 to 5)
- `451` are considered negative (a rating of 1 or 2)

## Dataset Creation

### Curation Rationale

This dataset was created for Arabic sentiment classification on services’ reviews in Lebanon country. 
Reviews are about public services, including hotels, restaurants, shops, and others.

### Source Data

#### Initial Data Collection and Normalization

The data was collected from Google Reviews and [Zomato website](https://www.zomato.com/lebanon)

#### Who are the source language producers?

The source language producers are people who posted their reviews on Google Reviews or [Zomato website](https://www.zomato.com/lebanon).
They're mainly Arabic speaking Lebanese people.

### Annotations

#### Annotation process

The dataset does not contain any additional annotations

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The author's research has tackled a highly important task of sentiment analysis for Arabic language in the Lebanese
context on 3916 reviews’ services from Google and Zomato. Experiments show three main findings: 
1) The classifier is confident when used to predict positive reviews,
2) while it is biased on predicting reviews with negative sentiment, and finally 
3) the low percentage of negative reviews in the corpus contributes to the diffidence of LR.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This dataset was curated by Marwan Al Omari, Moustafa Al-Hajj from Centre for Language Sciences and Communication,
Lebanese University, Beirut, Lebanon;  Nacereddine Hammami from college of Computer and Information Sciences, 
Jouf University, Aljouf, KSA; and Amani Sabra from Centre for Language Sciences and Communication, Lebanese University,
Beirut, Lebanon.

### Licensing Information

[More Information Needed]

### Citation Information
- Marwan Al Omari, Centre for Language Sciences and Communication, Lebanese University, Beirut, Lebanon, marwanalomari '@' yahoo.com
- Moustafa Al-Hajj, Centre for Language Sciences and Communication, Lebanese University, Beirut, Lebanon, moustafa.alhajj '@' ul.edu.lb
- Nacereddine Hammami, college of Computer and Information Sciences, Jouf University, Aljouf, KSA, n.hammami '@' ju.edu.sa
- Amani Sabra, Centre for Language Sciences and Communication, Lebanese University, Beirut, Lebanon, amani.sabra '@' ul.edu.lb
```
@misc{Dua:2019 ,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences" }

@InProceedings{AlOmari2019oclar,
title = {Sentiment Classifier: Logistic Regression for Arabic Services Reviews in Lebanon},
authors={Al Omari, M., Al-Hajj, M., Hammami, N., & Sabra, A.},
year={2019}
}
```

### Contributions

Thanks to [@alaameloh](https://github.com/alaameloh) for adding this dataset.