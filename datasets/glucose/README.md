---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-ROC-stories
task_categories:
- sequence-modeling
task_ids:
- sequence-modeling-other-common-sense-inference
---

# Dataset Card for [Dataset Name]

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

- **[Repository](https://github.com/TevenLeScao/glucose)**
- **[Paper](https://arxiv.org/abs/2009.07758)**
- **Point of Contact: [glucose@elementalcognition.com](mailto:glucose@elementalcognition.com)**

### Dataset Summary

GLUCOSE: GeneraLized and COntextualized Story Explanations, is a novel conceptual framework and dataset for commonsense reasoning. Given a short story and a sentence X in the story, GLUCOSE captures ten dimensions of causal explanation related to X. These dimensions, inspired by human cognitive psychology, cover often-implicit causes and effects of X, including events, location, possession, and other attributes.

### Supported Tasks and Leaderboards

Common sense inference of:
1. Causes
2. Emotions motivating an event
3. Locations enabling an event
4. Possession states enabling an event
5. Other attributes enabling an event
6. Consequences
7. Emotions caused by an event
8. Changes in location caused by an event
9. Changes in possession caused by an event
10. Other attributes that may be changed by an event

### Languages

English, monolingual

## Dataset Structure

### Data Instances

```
{
  "experiment_id": "e56c7c3e-4660-40fb-80d0-052d566d676a__4",
  "story_id": "e56c7c3e-4660-40fb-80d0-052d566d676a",
  "worker_id": 19,
  "submission_time_normalized": "20190930",
  "worker_quality_rating": 3,
  "selected_sentence_index": 4,
  "story": "It was bedtime at our house. Two of the three kids hit the pillow and fall asleep. The third is a trouble maker. For two hours he continues to get out of bed and want to play. Finally he becomes tired and falls asleep."
  selected_sentence: "Finally he becomes tired and falls asleep.",
  "1_specificNL": "The third kid continues to  get out of bed and wants to play >Causes/Enables> The kid finally becomes tired and falls asleep",
  "1_specificStructured": "{The third kid}_[subject] {continues}_[verb] {to }_[preposition1] {get out of bed}_[object1] {and wants to play}_[object2] >Causes/Enables> {The kid}_[subject] {finally becomes}_[verb] {tired}_[object1] {and falls asleep}_[object2]",
  "1_generalNL": "Someone_A doesn't want to  go to sleep >Causes/Enables> Someone_A finally falls asleep",
  "1_generalStructured": "{Someone_A}_[subject] {doesn't want}_[verb] {to }_[preposition1] {go to sleep}_[object1] >Causes/Enables> {Someone_A}_[subject] {finally falls}_[verb] {asleep}_[object1]",
  "2_specificNL": "escaped",
  "2_specificStructured": "escaped",
  "2_generalNL": "escaped",
  "2_generalStructured": "escaped",
  "3_specificNL": "The third kid is in bed >Enables> The kid finally becomes tired and falls asleep",
  "3_specificStructured": "{The third kid}_[subject] {is}_[verb] {in}_[preposition] {bed}_[object] >Enables> {The kid}_[subject] {finally becomes}_[verb] {tired}_[object1] {and falls asleep}_[object2]",
  "3_generalNL": "Someone_A is in bed >Enables> Someone_A falls asleep",
  "3_generalStructured": "{Someone_A}_[subject] {is}_[verb] {in}_[preposition] {bed}_[object] >Enables> {Someone_A}_[subject] {falls}_[verb] {asleep}_[object1]",
  "4_specificNL": "escaped",
  "4_specificStructured": "escaped",
  "4_generalNL": "escaped",
  "4_generalStructured": "escaped",
  "5_specificNL": "escaped",
  "5_specificStructured": "escaped",
  "5_generalNL": "escaped",
  "5_generalStructured": "escaped",
  "6_specificNL": "escaped",
  "6_specificStructured": "escaped",
  "6_generalNL": "escaped",
  "6_generalStructured": "escaped",
  "7_specificNL": "escaped",
  "7_specificStructured": "escaped",
  "7_generalNL": "escaped",
  "7_generalStructured": "escaped",
  "8_specificNL": "escaped",
  "8_specificStructured": "escaped",
  "8_generalNL": "escaped",
  "8_generalStructured": "escaped",
  "9_specificNL": "escaped",
  "9_specificStructured": "escaped",
  "9_generalNL": "escaped",
  "9_generalStructured": "escaped",
  "10_specificNL": "escaped",
  "10_specificStructured": "escaped",
  "10_generalNL": "escaped",
  "10_generalStructured": "escaped",
  "number_filled_in": 7
}
```

### Data Fields

- __experiment_id__: a randomly generated alphanumeric sequence for a given story with the sentence index appended at the end after two underscores. Example: cbee2b5a-f2f9-4bca-9630-6825b1e36c13__0

- __story_id__: a random alphanumeric identifier for the story. Example: e56c7c3e-4660-40fb-80d0-052d566d676a

- __worker_id__: each worker has a unique identificaiton number. Example: 21

- __submission_time_normalized__: the time of submission in the format YYYYMMDD. Example: 20200115

- __worker_quality_assessment__: rating for the worker on the assignment in the row. Example: 2

- __selected_sentence_index__: the index of a given sentence in a story. Example: 0

- __story__: contains the full text of the ROC story that was used for the HIT. Example: It was bedtime at our house. Two of the three kids hit the pillow and fall asleep. The third is a trouble maker. For two hours he continues to get out of bed and want to play. Finally he becomes tired and falls asleep.

- __selected_sentence__: the sentence from the story that is being annotated. Example: It was bedtime at our house.

- __[1-10]\_[specific/general][NL/Structured]__: This is the primary data collected. It provides the common sense knowledge about the related stories and those general rules about the world derived from the specific statements. For each of the ten relationships, there are four columns. The specific columns give the specific statements from the story. The general statements give the corresponding generalization. The NL columns are formatted in natural language, whereas the structured columns contain indications of the slots used to fill in the data. Example: 
  - __1_specificNL__: "The school has a football team >Causes/Enables> The football game was last weekend" 
  - __1_specificStructured__: "{The school }\_[subject] {has }\_[verb] {a football team }\_[object1] >Causes/Enables> {The football game }\_[subject] {was last weekend }\_[verb]"
  - __1_generalNL__: "Somewhere_A (that is a school ) has Something_A (that is a sports team ) >Causes/Enables> The game was last weekend" 
  - __1_generalStructured__: "{Somewhere_A ||that is a school ||}\_[subject] {has }\_[verb] {Something_A ||that is a sports team ||}\_[object1] >Causes/Enables> {The game }\_[subject] {was last weekend }\_[verb]" 

- __number\_filled\_in__: number of dimensions filled in for the assignment. Example: 4


### Data Splits

Train split: 65,521 examples
Test splits: 500 examples, without worker id and rating, number filled in, and structured text.

## Dataset Creation

### Curation Rationale

When humans read or listen, they make implicit commonsense inferences that frame their understanding of what happened and why. As a step toward AI systems that can build similar mental models, we introduce GLUCOSE, a large-scale dataset of implicit commonsense causal knowledge, encoded as causal mini-theories about the world, each grounded in a narrative context.

### Source Data

#### Initial Data Collection and Normalization

Initial text from ROCStories

#### Who are the source language producers?

Amazon Mechanical Turk.

### Annotations

#### Annotation process

To enable developing models that can build mental models of narratives, we aimed to crowdsource a large, quality-monitored dataset. Beyond the scalability benefits, using crowd workers (as opposed to a small set of expert annotators) ensures diversity of thought, thus broadening coverage of a common-sense knowledge resource. The annotation task is complex: it requires annotators to understand different causal dimensions in a variety of contexts and to come up with generalized  theories beyond  the  story  context.   For
strict quality control,  we designed a three-stage knowledge  acquisition  pipeline  for  crowdsourcing the GLUCOSE dataset on the Amazon Mechanical Turk Platform. The workers first go through a qualification test where they must score at least 90% on 10 multiple-choice questions on select GLUCOSE dimensions. Next, qualified workers can work on the main GLUCOSE data collection task:  given a story S and a story sentence X, they are asked to fill in (allowing for non-applicable) all ten GLUCOSE dimensions, getting step-by-step guidance from the GLUCOSE data acquisition. To ensure data consistency,  the same workers answer all dimensions for an S, X pair. Finally, the submissions are reviewed by an expert who rates each worker on a scale from 0 to 3, and provides feedback on how to improve. Our final UIs are the result of more than six rounds of pilot studies, iteratively improving the interaction elements, functionality, dimension definitions, instructions, and examples.

#### Who are the annotators?

Amazon Mechanical Turk workers, with feedback from an expert.

### Personal and Sensitive Information

No personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Nasrin Mostafazadeh, Aditya Kalyanpur, Lori Moon, David Buchanan, Lauren Berkowitz, Or Biran, Jennifer Chu-Carroll, from Elemental Cognition

### Licensing Information

Creative Commons Attribution-NonCommercial 4.0 International Public License

### Citation Information

```
@inproceedings{mostafazadeh2020glucose,
      title={GLUCOSE: GeneraLized and COntextualized Story Explanations}, 
      author={Nasrin Mostafazadeh and Aditya Kalyanpur and Lori Moon and David Buchanan and Lauren Berkowitz and Or Biran and Jennifer Chu-Carroll},
      year={2020},
      booktitle={The Conference on Empirical Methods in Natural Language Processing},
      publisher={Association for Computational Linguistics}
}
```