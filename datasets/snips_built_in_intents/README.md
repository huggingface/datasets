---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- cc0-1.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
paperswithcode_id: snips
---

# Dataset Card for Snips Built In Intents

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

- **Homepage:** https://github.com/sonos/nlu-benchmark/tree/master/2016-12-built-in-intents
- **Repository:** https://github.com/sonos/nlu-benchmark/tree/master/2016-12-built-in-intents
- **Paper:** https://arxiv.org/abs/1805.10190
- **Point of Contact:** The Snips team has joined Sonos in November 2019. These open datasets remain available and their access is now managed by the Sonos Voice Experience Team. Please email sve-research@sonos.com with any question.

### Dataset Summary

Snips' built in intents dataset was initially used to compare different voice assistants and released as a public dataset hosted at 
https://github.com/sonos/nlu-benchmark in folder 2016-12-built-in-intents. The dataset contains 328 utterances over 10 intent classes. 
A related Medium post is https://medium.com/snips-ai/benchmarking-natural-language-understanding-systems-d35be6ce568d.

### Supported Tasks and Leaderboards

There are no related shared tasks that we are aware of.

### Languages

English

## Dataset Structure

### Data Instances

The dataset contains 328 utterances over 10 intent classes. Each sample looks like:
`{'label': 8, 'text': 'Transit directions to Barcelona Pizza.'}`

### Data Fields

- `text`: The text utterance expressing some user intent.
- `label`: The intent label of the piece of text utterance.

### Data Splits

The source data is not split.

## Dataset Creation

### Curation Rationale

The dataset was originally created to compare the performance of a number of voice assistants. However, the labelled utterances are useful 
for developing and benchmarking text chatbots as well.

### Source Data

#### Initial Data Collection and Normalization

It is not clear how the data was collected. From the Medium post: `The benchmark relies on a set of 328 queries built by the business team 
at Snips, and kept secret from data scientists and engineers throughout the development of the solution.`

#### Who are the source language producers?

Originally prepared by snips.ai. The Snips team has since joined Sonos in November 2019. These open datasets remain available and their 
access is now managed by the Sonos Voice Experience Team. Please email sve-research@sonos.com with any question.

### Annotations

#### Annotation process

It is not clear how the data was collected. From the Medium post: `The benchmark relies on a set of 328 queries built by the business team 
at Snips, and kept secret from data scientists and engineers throughout the development of the solution.`

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

Originally prepared by snips.ai. The Snips team has since joined Sonos in November 2019. These open datasets remain available and their 
access is now managed by the Sonos Voice Experience Team. Please email sve-research@sonos.com with any question.

### Licensing Information

The source data is licensed under Creative Commons Zero v1.0 Universal.

### Citation Information

Any publication based on these datasets must include a full citation to the following paper in which the results were published by the Snips Team:

Coucke A. et al., "Snips Voice Platform: an embedded Spoken Language Understanding system for private-by-design voice interfaces." CoRR 2018, 
https://arxiv.org/abs/1805.10190 

### Contributions

Thanks to [@bduvenhage](https://github.com/bduvenhage) for adding this dataset.