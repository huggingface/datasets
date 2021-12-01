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
pretty_name: Arabic Jordanian General Tweets
---

# Dataset Card for Arabic Jordanian General Tweets

## Table of Contents
- [Dataset Card for Arabic Jordanian General Tweets](#dataset-card-for-arabic-jordanian-general-tweets)
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

- **Repository:** [Arabic Jordanian General Tweets](https://github.com/komari6/Arabic-twitter-corpus-AJGT)
- **Paper:** [Arabic Tweets Sentimental Analysis Using Machine Learning](https://link.springer.com/chapter/10.1007/978-3-319-60042-0_66)
- **Point of Contact:** [Khaled Alomari](khaled.alomari@adu.ac.ae)

### Dataset Summary

Arabic Jordanian General Tweets (AJGT) Corpus consisted of 1,800 tweets annotated as positive and negative. Modern Standard Arabic (MSA) or Jordanian dialect.

### Supported Tasks and Leaderboards

The dataset was published on this [paper](https://link.springer.com/chapter/10.1007/978-3-319-60042-0_66). 

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

A binary datset with with negative and positive sentiments.  

### Data Fields

- `text` (str): Tweet text.
- `label` (int): Sentiment.

### Data Splits

The dataset is not split. 

|           | Tain   | 
|---------- | ------ | 
|no split   | 1,800  | 

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

Contains 1,800 tweets collected from twitter. 

#### Who are the source language producers?

From tweeter.  

### Annotations

The dataset does not contain any additional annotations.

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
@inproceedings{alomari2017arabic,
  title={Arabic tweets sentimental analysis using machine learning},
  author={Alomari, Khaled Mohammad and ElSherif, Hatem M and Shaalan, Khaled},
  booktitle={International Conference on Industrial, Engineering and Other Applications of Applied Intelligent Systems},
  pages={602--610},
  year={2017},
  organization={Springer}
}
```

### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai), [@lhoestq](https://github.com/lhoestq) for adding this dataset.