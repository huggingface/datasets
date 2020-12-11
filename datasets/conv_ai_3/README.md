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
- 1K<n<10K
source_datasets:
- original
task_categories:
- conditional-text-generation
- text-scoring
task_ids:
- text-scoring-other-evaluating-dialogue-systems
---

# Dataset Card for [Needs More Information]

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

- **Homepage:** https://github.com/aliannejadi/ClariQ
- **Repository:** https://github.com/aliannejadi/ClariQ
- **Paper:** https://arxiv.org/abs/2009.11352
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The Conv AI 3 challenge is organized as part of the Search-oriented Conversational AI (SCAI) EMNLP workshop in 2020. The main aim of the conversational systems is to return an appropriate answer in response to the user requests. However, some user requests might be ambiguous. In Information Retrieval (IR) settings such a situation is handled mainly through the diversification of search result page. It is however much more challenging in dialogue settings. Hence, we aim to study the following situation for dialogue settings: 
- a user is asking an ambiguous question (where ambiguous question is a question to which one can return > 1 possible answers)
- the system must identify that the question is ambiguous, and, instead of trying to answer it directly, ask a good clarifying question.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

[Needs More Information]

## Dataset Structure

### Data Instances

topic_id	initial_request	topic_desc	clarification_need	facet_id	facet_desc	question_id	question	answer
1	Tell me about Obama family tree.	Find information on President Barack Obama\'s family history, including genealogy, national origins, places and dates of birth, etc.	2	F0001	"Find the TIME magazine photo essay ""Barack Obama's Family Tree""."	Q00384	are you interested in seeing barack obamas family	yes am interested in obamas family
105 	Tell me about sonoma county medical services.	What medical services are available in Sonoma County, California?	2	F0025	What medical services are available in Sonoma County, California?	Q03267	would you like the different services that are provided	yes please


### Data Fields

- topic_id: Unique Id referring to topic
- initial_request: Topic request initially generated
- topic_desc: Description of the given topic
- clarification_need: Is clarification required for the topic
- facet_id: Facet Id for the topic
- facet_desc: Facet description for the topic
- question_id: Question Id for the topic
- question: Question for the topic
- answer: Answer for the topic

### Data Splits

[Needs More Information]

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

@misc{aliannejadi2020convai3,
      title={ConvAI3: Generating Clarifying Questions for Open-Domain Dialogue Systems (ClariQ)}, 
      author={Mohammad Aliannejadi and Julia Kiseleva and Aleksandr Chuklin and Jeff Dalton and Mikhail Burtsev},
      year={2020},
      eprint={2009.11352},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}