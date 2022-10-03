---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
language:
- en
- hi
license:
- cc-by-sa-3.0
- gfdl
multilinguality:
- multilingual
- translation
pretty_name: CMU Document Grounded Conversations
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- translation
task_ids: []
---

# Dataset Card for CMU Document Grounded Conversations

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
{'rating': 2,
 'wikiDocumentIdx': 13,
 'utcTimestamp': '2018-03-16T17:48:22.037Z',
 'uid': 'user2',
 'date': '2018-03-16T17:47:21.964Z',
 'uid2response': {'response': [1, 2, 3, 5], 'type': 'finish'},
 'uid1LogInTime': '2018-03-16T17:47:21.964Z',
 'user2_id': 'USR664',
 'uid1LogOutTime': '2018-03-16T18:02:29.072Z',
 'whoSawDoc': ['user1', 'user2'],
 'status': 1,
 'docIdx': 0,
 'uid1response': {'response': [1, 2, 3, 4], 'type': 'finish'},
 'translation': {'en': 'The director is Zack Snyder, 27% Rotten Tomatoes, 4.9/10.',
  'hi_en': 'Zack Snyder director hai, 27% Rotten Tomatoes, 4.9/10.'}}
```

### Data Fields

- `date`: the time the file is created, as a string
- `docIdx`: the current section index of the wiki document when the utterance is said. There are in total 4 sections for each document.
- `translation`:
  - `hi_en`: The text in Hinglish
  - `en`: The text in English
- `uid`: the user id of this utterance.
- `utcTimestamp`: the server utc timestamp of this utterance, as a string
- `rating`: A number from 1 or 2 or 3. A larger number means the quality of the conversation is better.
- `status`: status as an integer
- `uid1LogInTime`: optional login time of user 1, as a string
- `uid1LogOutTime`: optional logout time of user 1, as a string
- `uid1response`: a json object contains the status and response of user after finishing the conversation. Fields in the object includes:
  - `type`: should be one of ['finish', 'abandon','abandonWithouAnsweringFeedbackQuestion']. 'finish' means the user successfully finishes the conversation, either by completing 12 or 15 turns or in the way that the other user leaves the conversation first. 'abandon' means the user abandons the conversation in the middle, but entering the feedback page. 'abandonWithouAnsweringFeedbackQuestion' means the user just disconnects or closes the web page without providing the feedback.
  - `response`: the answer to the post-conversation questions. The worker can choose multiple of them. The options presented to the user are as follows:
    For type 'finish'
      1: The conversation is understandable.
      2: The other user is actively responding me.
      3: The conversation goes smoothly.
    For type 'abandon'
      1: The other user is too rude.
      2: I don't know how to proceed with the conversation.
      3: The other user is not responding to me.
    For users given the document
      4: I have watched the movie before.
      5: I have not watched the movie before.
    For the users without the document
      4: I will watch the movie after the other user's introduction.
      5: I will not watch the movie after the other user's introduction.
- `uid2response`: same as uid1response
- `user2_id`: the generated user id of user 2
- `whoSawDoc`: Should be one of ['user1'], ['user2'], ['user1', 'user2']. Indicating which user read the document.
- `wikiDocumentId`: the index of the wiki document.

### Data Splits

|   name   |train|validation|test|
|----------|----:|---------:|---:|
|CMU DOG   | 8060|       942| 960| 

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

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset was initially created by Prof Alan W Black's group at CMU

### Licensing Information

[More Information Needed]

### Citation Information

```bibtex
@inproceedings{
	cmu_dog_emnlp18,
	title={A Dataset for Document Grounded Conversations},
	author={Zhou, Kangyan and Prabhumoye, Shrimai and Black, Alan W},
	year={2018},
	booktitle={Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing}
}
```

### Contributions

Thanks to [@Ishan-Kumar2](https://github.com/Ishan-Kumar2) for adding this dataset.