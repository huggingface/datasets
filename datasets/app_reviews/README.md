---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-scoring
task_ids:
- sentiment-scoring
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage: [Home Page](https://github.com/sealuzh/user_quality)
- **Repository: [Repo Link](https://github.com/sealuzh/user_quality)
- **Paper: [Link](https://giograno.me/assets/pdf/workshop/wama17.pdf)
- **Leaderboard:
- **Point of Contact: [Darshan Gandhi](darshangandhi1151@gmail.com)

### Dataset Summary

It is a large dataset of Android applications belonging to 23 differentapps categories, which provides an overview of the types of feedback users report on the apps and documents the evolution of the related code metrics. The dataset contains about 395 applications of the F-Droid repository, including around 600 versions, 280,000 user reviews (extracted with specific text mining approaches)

### Supported Tasks and Leaderboards

The dataset we provide comprises 395 different apps from F-Droid repository, including code quality indicators of 629 versions of these
apps. It also encloses app reviews related to each of these versions, which have been automatically categorized classifying types of user feedback from a software maintenance and evolution perspective.

### Languages

The dataset is a monolingual dataset which has the messages English.

## Dataset Structure

### Data Instances

The dataset consists of a message in English.

{'package_name': 'com.mantz_it.rfanalyzer',
 'review': "Great app! The new version now works on my Bravia Android TV which is great as it's right by my rooftop aerial cable. The scan feature would be useful...any ETA on when this will be available? Also the option to import a list of bookmarks e.g. from a simple properties file would be useful.",
 'date': 'October 12 2016',
 'star': 4}

### Data Fields

* package_name : Name of the Software Application Package
* review : Message of the user 
* date : date when the user posted the review 
* star : rating provied by the user for the application

### Data Splits

There is training data, with a total of : 288065

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

With the help of this dataset one can try to understand more about software applications and what are the views and opinions of the users about them. This helps to understand more about which type of software applications are prefeered by the users and how do these applications facilitate the user to help them solve their problems and issues. 

### Discussion of Biases

The reviews are only for applications which are in the open-source software applications, the other sectors have not been considered here 

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Giovanni Grano - (University of Zurich), Sebastiano Panichella - (University of Zurich), Andrea di Sorbo - (University of Sannio)

### Licensing Information

[More Information Needed]

### Citation Information

@InProceedings{Zurich Open Repository and
Archive:dataset,
title = {Software Applications User Reviews},
authors={Grano, Giovanni; Di Sorbo, Andrea; Mercaldo, Francesco; Visaggio, Corrado A; Canfora, Gerardo;
Panichella, Sebastiano},
year={2017}
}

### Contributions

Thanks to [@darshan-gandhi](https://github.com/darshan-gandhi) for adding this dataset.