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
task_ids:
- other-other-Coached Conversation Preference
---

# Dataset Card for Coached Conversational Preference Elicitation

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:**
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

Each conversation has the following fields:

* conversationId: A unique random ID for the conversation. The ID has no meaning.
* utterances: An array of utterances by the workers.

Each utterance has the following fields:

* index: A 0-based index indicating the order of the utterances in the conversation.
* speaker: Either USER or ASSISTANT, indicating which role generated this utterance.
* text: The raw text as written by the ASSISTANT, or transcribed from the spoken recording of USER.
* segments: An array of semantic annotations of spans in the text.  

Each semantic annotation segment has the following fields:

* startIndex: The position of the start of the annotation in the utterance text.
* endIndex: The position of the end of the annotation in the utterance text.
* text: The raw text that has been annotated.
* annotations: An array of annotation details for this segment.

Each annotation has two fields:

* annotationType: The class of annotation (see ontology below).
* entityType: The class of the entity to which the text refers (see ontology below).

**EXPLANATION OF ONTOLOGY**

In the corpus, preferences and the entities that these preferences refer to are annotated with an annotation type as well as an entity type.

Annotation types fall into four categories:

* ENTITY_NAME: These mark the names of relevant entities mentioned.
* ENTITY_PREFERENCE: These are defined as statements indicating that the dialog participant does or does not like the relevant entity in general, or that they do or do not like some aspect of the entity. This may also be thought of the participant having some sentiment about what is being discussed.
* ENTITY_DESCRIPTION: Neutral descriptions that describe an entity but do not convey an explicit liking or disliking.
* ENTITY_OTHER: Other relevant statements about an entity that convey relevant information of how the participant relates to the entity but do not provide a sentiment. Most often, these relate to whether a participant has seen a particular movie, or knows a lot about a given entity.

Entity types are marked as belonging to one of four categories:

* MOVIE_GENRE_OR_CATEGORY for genres or general descriptions that capture a particular type or style of movie.
* MOVIE_OR_SERIES for the full or partial name of a movie or series of movies.
* PERSON for the full or partial name of an actual person.
* SOMETHING_ELSE for other important proper nouns, such as the names of characters or locations.


### Data Splits

[More Information Needed]

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

[More Information Needed]

### Citation Information

[More Information Needed]
