---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- other
- sequence-modeling
- structure-prediction
task_ids:
- other-other-Conversational Recommendation
- dialogue-modeling
- parsing
paperswithcode_id: coached-conversational-preference-elicitation
---

# Dataset Card for Coached Conversational Preference Elicitation

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

- **Homepage:** [Coached Conversational Preference Elicitation Homepage](https://research.google/tools/datasets/coached-conversational-preference-elicitation/)
- **Repository:** [Coached Conversational Preference Elicitation Repository](https://github.com/google-research-datasets/ccpe)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/W19-5941/)

### Dataset Summary

A dataset consisting of 502 English dialogs with 12,000 annotated utterances between a user and an assistant discussing movie preferences in natural language. It was collected using a Wizard-of-Oz  methodology between two paid crowd-workers, where one worker plays the role of an 'assistant', while the other plays the role of a 'user'. The 'assistant' elicits the 'user’s' preferences about movies following a Coached Conversational Preference Elicitation (CCPE) method. The assistant asks questions designed to minimize the bias in the terminology the 'user' employs to convey his or her preferences as much as possible, and to obtain these preferences in natural language. Each dialog is annotated with entity mentions, preferences expressed about entities, descriptions of entities provided, and other statements of entities.

### Supported Tasks and Leaderboards

* `other-other-Conversational Recommendation`:  The dataset can be used to train a model for Conversational recommendation, which consists in Coached Conversation Preference Elicitation. 

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

A typical data point comprises of a series of utterances between the 'assistant' and the 'user'. Each such utterance is annotated into categories mentioned in data fields.

An example from the Coached Conversational Preference Elicitation dataset looks as follows:

```
{'conversationId': 'CCPE-6faee',
 'utterances': {'index': [0,
   1,
   2,
   3,
   4,
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   15],
  'segments': [{'annotations': [{'annotationType': [], 'entityType': []}],
    'endIndex': [0],
    'startIndex': [0],
    'text': ['']},
   {'annotations': [{'annotationType': [0], 'entityType': [0]},
     {'annotationType': [1], 'entityType': [0]}],
    'endIndex': [20, 27],
    'startIndex': [14, 0],
    'text': ['comedy', 'I really like comedy movies']},
   {'annotations': [{'annotationType': [0], 'entityType': [0]}],
    'endIndex': [24],
    'startIndex': [16],
    'text': ['comedies']},
   {'annotations': [{'annotationType': [1], 'entityType': [0]}],
    'endIndex': [15],
    'startIndex': [0],
    'text': ['I love to laugh']},
   {'annotations': [{'annotationType': [], 'entityType': []}],
    'endIndex': [0],
    'startIndex': [0],
    'text': ['']},
   {'annotations': [{'annotationType': [0], 'entityType': [1]},
     {'annotationType': [1], 'entityType': [1]}],
    'endIndex': [21, 21],
    'startIndex': [8, 0],
    'text': ['Step Brothers', 'I liked Step Brothers']},
   {'annotations': [{'annotationType': [], 'entityType': []}],
    'endIndex': [0],
    'startIndex': [0],
    'text': ['']},
   {'annotations': [{'annotationType': [1], 'entityType': [1]}],
    'endIndex': [32],
    'startIndex': [0],
    'text': ['Had some amazing one-liners that']},
   {'annotations': [{'annotationType': [], 'entityType': []}],
    'endIndex': [0],
    'startIndex': [0],
    'text': ['']},
   {'annotations': [{'annotationType': [0], 'entityType': [1]},
     {'annotationType': [1], 'entityType': [1]}],
    'endIndex': [15, 15],
    'startIndex': [13, 0],
    'text': ['RV', "I don't like RV"]},
   {'annotations': [{'annotationType': [], 'entityType': []}],
    'endIndex': [0],
    'startIndex': [0],
    'text': ['']},
   {'annotations': [{'annotationType': [1], 'entityType': [1]},
     {'annotationType': [1], 'entityType': [1]}],
    'endIndex': [48, 66],
    'startIndex': [18, 50],
    'text': ['It was just so slow and boring', "I didn't like it"]},
   {'annotations': [{'annotationType': [0], 'entityType': [1]}],
    'endIndex': [63],
    'startIndex': [33],
    'text': ['Jurassic World: Fallen Kingdom']},
   {'annotations': [{'annotationType': [0], 'entityType': [1]},
     {'annotationType': [3], 'entityType': [1]}],
    'endIndex': [52, 52],
    'startIndex': [22, 0],
    'text': ['Jurassic World: Fallen Kingdom',
     'I have seen the movie Jurassic World: Fallen Kingdom']},
   {'annotations': [{'annotationType': [], 'entityType': []}],
    'endIndex': [0],
    'startIndex': [0],
    'text': ['']},
   {'annotations': [{'annotationType': [1], 'entityType': [1]},
     {'annotationType': [1], 'entityType': [1]},
     {'annotationType': [1], 'entityType': [1]}],
    'endIndex': [24, 125, 161],
    'startIndex': [0, 95, 135],
    'text': ['I really like the actors',
     'I just really like the scenery',
     'the dinosaurs were awesome']}],
  'speaker': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
  'text': ['What kinds of movies do you like?',
   'I really like comedy movies.',
   'Why do you like comedies?',
   "I love to laugh and comedy movies, that's their whole purpose. Make you laugh.",
   'Alright, how about a movie you liked?',
   'I liked Step Brothers.',
   'Why did you like that movie?',
   'Had some amazing one-liners that still get used today even though the movie was made awhile ago.',
   'Well, is there a movie you did not like?',
   "I don't like RV.",
   'Why not?',
   "And I just didn't It was just so slow and boring. I didn't like it.",
   'Ok, then have you seen the movie Jurassic World: Fallen Kingdom',
   'I have seen the movie Jurassic World: Fallen Kingdom.',
   'What is it about these kinds of movies that you like or dislike?',
   'I really like the actors. I feel like they were doing their best to make the movie better. And I just really like the scenery, and the the dinosaurs were awesome.']}}
```



### Data Fields

Each conversation has the following fields:

* `conversationId`: A unique random ID for the conversation. The ID has no meaning.
* `utterances`: An array of utterances by the workers.

Each utterance has the following fields:

* `index`: A 0-based index indicating the order of the utterances in the conversation.
* `speaker`: Either USER or ASSISTANT, indicating which role generated this utterance.
* `text`: The raw text as written by the ASSISTANT, or transcribed from the spoken recording of USER.
* `segments`: An array of semantic annotations of spans in the text.  

Each semantic annotation segment has the following fields:

* `startIndex`: The position of the start of the annotation in the utterance text.
* `endIndex`: The position of the end of the annotation in the utterance text.
* `text`: The raw text that has been annotated.
* `annotations`: An array of annotation details for this segment.

Each annotation has two fields:

* `annotationType`: The class of annotation (see ontology below).
* `entityType`: The class of the entity to which the text refers (see ontology below).

**EXPLANATION OF ONTOLOGY**

In the corpus, preferences and the entities that these preferences refer to are annotated with an annotation type as well as an entity type.

Annotation types fall into four categories:

* `ENTITY_NAME` (0): These mark the names of relevant entities mentioned.
* `ENTITY_PREFERENCE` (1): These are defined as statements indicating that the dialog participant does or does not like the relevant entity in general, or that they do or do not like some aspect of the entity. This may also be thought of the participant having some sentiment about what is being discussed.
* `ENTITY_DESCRIPTION` (2): Neutral descriptions that describe an entity but do not convey an explicit liking or disliking.
* `ENTITY_OTHER` (3): Other relevant statements about an entity that convey relevant information of how the participant relates to the entity but do not provide a sentiment. Most often, these relate to whether a participant has seen a particular movie, or knows a lot about a given entity.

Entity types are marked as belonging to one of four categories:

* `MOVIE_GENRE_OR_CATEGORY` (0): For genres or general descriptions that capture a particular type or style of movie.
* `MOVIE_OR_SERIES` (1): For the full or partial name of a movie or series of movies.
* `PERSON` (2): For the full or partial name of an actual person.
* `SOMETHING_ELSE ` (3):  For other important proper nouns, such as the names of characters or locations.

### Data Splits

There is a single split of the dataset named 'train' which contains the whole datset.

|                     | Train |
| ------------------- | ----- |
| Input Conversations | 502   |

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

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)

### Citation Information

```
@inproceedings{radlinski-etal-2019-ccpe,
  title = {Coached Conversational Preference Elicitation: A Case Study in Understanding Movie Preferences},
  author = {Filip Radlinski and Krisztian Balog and Bill Byrne and Karthik Krishnamoorthi},
  booktitle = {Proceedings of the Annual Meeting of the Special Interest Group on Discourse and Dialogue ({SIGDIAL})},
  year = 2019
}
```


### Contributions

Thanks to [@vineeths96](https://github.com/vineeths96) for adding this dataset.