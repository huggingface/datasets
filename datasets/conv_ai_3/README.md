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
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
- text-scoring
task_ids:
- text-scoring-other-evaluating-dialogue-systems
paperswithcode_id: null
---

# Dataset Card for [More Information Needed]

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

- **Homepage:** https://github.com/aliannejadi/ClariQ
- **Repository:** https://github.com/aliannejadi/ClariQ
- **Paper:** https://arxiv.org/abs/2009.11352
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

The Conv AI 3 challenge is organized as part of the Search-oriented Conversational AI (SCAI) EMNLP workshop in 2020. The main aim of the conversational systems is to return an appropriate answer in response to the user requests. However, some user requests might be ambiguous. In Information Retrieval (IR) settings such a situation is handled mainly through the diversification of search result page. It is however much more challenging in dialogue settings. Hence, we aim to study the following situation for dialogue settings:

- a user is asking an ambiguous question (where ambiguous question is a question to which one can return > 1 possible answers)
- the system must identify that the question is ambiguous, and, instead of trying to answer it directly, ask a good clarifying question.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

Here are a few examples from the dataset:
```
{'topic_id': 8,
'facet_id': 'F0968',
'initial_request': 'I want to know about appraisals.',
'topic_desc': 'Find information about the appraisals in nearby companies.',
'clarification_need': 2,
'question_id': 'F0001',
'question': 'are you looking for a type of appraiser',
'answer': 'im looking for nearby companies that do home appraisals',
'facet_desc': 'Get the TYPE of Appraisals'
'conversation_context': [],
'context_id': 968}
```

```
{'topic_id': 8,
'facet_id': 'F0969',
'initial_request': 'I want to know about appraisals.',
'topic_desc': 'Find information about the type of appraisals.',
'clarification_need': 2,
'question_id': 'F0005',
'question': 'are you looking for a type of appraiser',
'facet_desc': 'Get the TYPE of Appraisals'
'answer': 'yes jewelry',
'conversation_context': [],
'context_id': 969}
```

```
{'topic_id': 293,
'facet_id': 'F0729',
'initial_request': 'Tell me about the educational advantages of social networking sites.',
'topic_desc': 'Find information about the educational benefits of the social media sites',
'clarification_need': 2,
'question_id': 'F0009'
'question': 'which social networking sites would you like information on',
'answer': 'i don have a specific one in mind just overall educational benefits to social media sites',
'facet_desc': 'Detailed information about the Networking Sites.'
'conversation_context': [{'question': 'what level of schooling are you interested in gaining the advantages to social networking sites', 'answer': 'all levels'}, {'question': 'what type of educational advantages are you seeking from social networking', 'answer': 'i just want to know if there are any'}],
'context_id': 976573}
```
### Data Fields

- `topic_id`: the ID of the topic (`initial_request`).
- `initial_request`: the query (text) that initiates the conversation.
- `topic_desc`: a full description of the topic as it appears in the TREC Web Track data.
- `clarification_need`: a label from 1 to 4, indicating how much it is needed to clarify a topic. If an `initial_request` is self-contained and would not need any clarification, the label would be 1. While if a `initial_request` is absolutely ambiguous, making it impossible for a search engine to guess the user's right intent before clarification, the label would be 4.
- `facet_id`: the ID of the facet.
- `facet_desc`: a full description of the facet (information need) as it appears in the TREC Web Track data.
- `question_id`: the ID of the question..
- `question`: a clarifying question that the system can pose to the user for the current topic and facet.
- `answer`: an answer to the clarifying question, assuming that the user is in the context of the current row (i.e., the user's initial query is `initial_request`, their information need is `facet_desc`, and `question` has been posed to the user).

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

@misc{aliannejadi2020convai3,
title={ConvAI3: Generating Clarifying Questions for Open-Domain Dialogue Systems (ClariQ)},
author={Mohammad Aliannejadi and Julia Kiseleva and Aleksandr Chuklin and Jeff Dalton and Mikhail Burtsev},
year={2020},
eprint={2009.11352},
archivePrefix={arXiv},
primaryClass={cs.CL}
}

### Contributions

Thanks to [@rkc007](https://github.com/rkc007) for adding this dataset.