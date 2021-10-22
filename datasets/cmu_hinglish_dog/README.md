---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages: []
licenses: []
multilinguality:
- multilingual
- translation
pretty_name: CMU_Hinglish_DoG
size_categories:
- unknown
source_datasets: []
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---

# Dataset Card for ELI5

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

- **Homepage:** [CMU Hinglish DoG](http://festvox.org/cedar/data/notyet/)
- **Repository:** [CMU Document Grounded Conversations (English version)](https://github.com/festvox/datasets-CMU_DoG)
- **Paper:** [CMU Document Grounded Conversations (English version)](https://arxiv.org/pdf/1809.07358.pdf)
- **Point of Contact:** 

### Dataset Summary

This is a collection of text conversations in Hinglish (code mixing between Hindi-English) and their corresponding English versions. Can be used for Translating between the two. The dataset has been provided by Prof. Alan Black's group from CMU.

### Supported Tasks and Leaderboards

- `abstractive-mt`

### Languages

## Dataset Structure

### Data Instances

A typical data point comprises a Hinglish text, with key `hi_en` and its English version with key `en`. The `docIdx` contains the current section index of the wiki document when the utterance is said. There are in total 4 sections for each document. The `uid` has the user id of this utterance.

An example from the CMU_Hinglish_DoG train set looks as follows:
```
{
	'hi_en': 'MAIN KUCHH MOVIE PASAND KARTHA HOON.AAP KYA PASAND KARTHE HO?', 
	'docIdx': 0, 
	'uid': 'user2', 
	'en': 'I like some action movies, yes.  Do you?'
}

```
An example from the CMU_Hinglish_DoG validation set looks as follows:
```
{
  'hi_en': 'Yes ek key scene to add hua hai,Wo scene hisme Kate k realize hota hai ki wah missing and use flight se ghar wapas bhejne ki koshish karti hai.', 
  'docIdx': 2, 
  'uid': 'user2', 
  'en': 'Yes it added a second key scene.  The one where Kate realizes he is missing and tries to get a flight home'
}
```

### Data Fields

- `hi_en`: The text in Hinglish
- `en`: The text in English
- `uid`: the user id of this utterance.
- `docIdx`: the current section index of the wiki document when the utterance is said. There are in total 4 sections for each document.

### Data Splits

Train, validation and test

## Dataset Creation

[More Information Needed]

### Curation Rationale

[More Information Needed]

### Source Data

The Hinglish dataset is derived from the original CMU DoG (Document Grounded Conversations Dataset). More info about that can be found in the [repo](https://github.com/festvox/datasets-CMU_DoG)

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop better question answering systems.


### Discussion of Biases


### Other Known Limitations

## Additional Information

### Dataset Curators

The dataset was initially created by Prof Alan W Black's group at CMU

### Licensing Information


### Citation Information

```
@inproceedings{
	cmu_dog_emnlp18,
	title={A Dataset for Document Grounded Conversations},
	author={Zhou, Kangyan and Prabhumoye, Shrimai and Black, Alan W},
	year={2018},
	booktitle={Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing}
}

```

### Contributions

