---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- other
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
- open-domain-qa
paperswithcode_id: protoqa
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

- **Interactive Demo:** [Interactive demo](http://protoqa.com)
- **Repository:** [proto_qa repository](https://github.com/iesl/protoqa-data)
- **Paper:** [proto_qa paper](https://arxiv.org/pdf/2005.00771.pdf)
- **Point of Contact:** [Michael Boratko](mailto:mboratko@cs.umass.edu) 
                        [Xiang Lorraine Li](mailto:xiangl@cs.umass.edu)
                        [Tim O’Gorman](mailto:togorman@cs.umass.edu)
                        [Rajarshi Das](mailto:rajarshi@cs.umass.edu)
                        [Dan Le](mailto:dhle@cs.umass.edu)
                        [Andrew McCallum](mailto:mccallum@cs.umass.edu)
                        

### Dataset Summary

This dataset is for studying computational models trained to reason about prototypical situations. It is anticipated that still would not lead to usage in a downstream task, but as a way of studying the knowledge (and biases) of prototypical situations already contained in pre-trained models. The data it is partially based on (Family Feud).
Using deterministic filtering a sampling from a larger set of all transcriptions was built.  Scraped data was acquired through fan transcriptions at [family feud](https://www.familyfeudinfo.com) and [family feud friends](http://familyfeudfriends.arjdesigns.com/); crowdsourced data was acquired with FigureEight (now Appen)

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English

## Dataset Structure

### Data Instances

**What do the instances that comprise the dataset represent?**<br>
Each represents a survey question from Family Feud game and reported answer clusters

**How many instances are there in total?**<br>
9789 instances

**What data does each instance consist of?**<br>
Each instance is a question, a set of answers, and a count associated with each answer.


### Data Fields

**Data Files**<br>
Each line is a json dictionary, in which:<br>
**question** contains the question (in original and a normalized form)<br>
**answerstrings** contains the original answers provided by survey respondents (when available), along with the counts for each string. Because the FamilyFeud data has only cluster names rather than strings, those cluster names are included with 0 weight.<br>
**answer-clusters** list of clusters, with the count of each cluster and the strings included in that cluster. Each cluster is given a unique ID that can be linked to in the assessment files.

The simplified configuration includes:
- `question`: contains the original question
- `normalized-question`: contains the question in normalized form
- `totalcount`: unique identifier of the comment (can be used to look up the entry in the raw dataset)
- `id`: unique identifier of the commen
- `source`: unique identifier of the commen
- `answerstrings`: unique identifier of the commen
- `answer-clusters | answers-cleaned`: list clusters of:
    * `clusterid`: Each cluster is given a unique ID that can be linked to in the assessment files
    * `count`: the count of each cluster
    * `answers`: the strings included in that cluster
    

In addition to the above, there is crowdsourced assessments file. The config "proto_qa_cs_assessments" provides mappings from additional human and model answers to clusters, to evaluate different assessment methods.


**Assessment files**<br>

The file **data/dev/crowdsource_dev.assessments.jsonl** contains mappings from additional human and model answers to clusters, to evaluate different assessment methods.
Each line contains:<br>
* `question`: contains the ID of the question
* `assessments`: maps individual strings to one of three options, either the answer cluster id, "invalid" if the answer is judged to be bad, or "valid_new_cluster" if the answer is valid but does not match any existing clusters.

### Data Splits

* proto_qa `Train` : 8781 instances for training or fine-tuning scraped from Family Feud fan sites (see paper). Scraped data has answer clusters with sizes, but only has a single string per cluster (corresponding to the original cluster name
* proto_qa `Validation` : 979 instances sampled from the same Family Feud data, for use in model validation and development.

* proto_qa_cs `Validation` :: 51 questions collected with exhaustive answer collection and manual clustering, matching the details of the eval test set (roughly 100 human answers per question)

**data/dev/crowdsource_dev.assessments.jsonl**: assessment file (format described above) for study of assessment methods.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

**How was the data associated with each instance acquired?**<br>
Scraped data was acquired through fan transcriptions at https://www.familyfeudinfo.com and http://familyfeudfriends.arjdesigns.com/ ; crowdsourced data was acquired with FigureEight (now Appen)

**If the dataset is a sample from a larger set, what was the sampling strategy?**<br>
Deterministic filtering was used (noted elsewhere), but no probabilistic sampling was used.

**Who was involved in the data collection process (e.g., students,crowdworkers , contractors) and how were they compensated?**<br>
Crowdworkers were used in the evalaution dataset. Time per task was calculated and per-task cost was set to attempt to provide a living wage

**Over what timeframe was the data collected?**<br>
Crowdsource answers were collected between Fall of 2018 and Spring of 2019. Scraped data covers question-answer pairs collected since the origin of the show in 1976


#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

**Was any preprocessing/cleaning/labeling of the data done?**<br> 
Obvious typos in the crowdsourced answer set were corrected

#### Who are the annotators?

The original question-answer pairs were generated by surveys of US English-speakers in a period from 1976 to present day. Crowd-sourced evaluation was constrained geographically to US English speakers but not otherwise constrained. Additional demographic data was not collected.

### Personal and Sensitive Information

**Does the dataset contain data that might be considered sensitive in any way?**<br>
As the questions address prototypical/stereotypical activities, models trained on more offensive material (such as large language models) may provide offensive answers to such questions. While we had found a few questions which we worried would actually encourage models to provide offensive answers, we cannot guarantee that the data is clean of such questions. Even a perfectly innocent version of this dataset would be encouraging models to express generalizations about situations, and therefore may provoke offensive material that is oontained in language models

**Does the dataset contain data that might be considered confidential?**<br>
The data does not concern individuals and thus does not contain any information to identify persons. Crowdsourced answers do not provide any user identifiers.

## Considerations for Using the Data

### Social Impact of Dataset

**Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?**<br>
Not egregiously so (questions are all designed to be shown on television or replications thereof),

### Discussion of Biases

**Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?**
<br>All original questions were written with US television audiences in mind, and therefore characterize prototypical situations with a specific lens. Any usages which deploy this to actually model prototypical situations globally will carry that bias.

**Are there tasks for which the dataset should not be used?**
<br>We caution regarding free-form use of this dataset for interactive "commonsense question answering" purposes without more study of the biases and stereotypes learned by such models.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The listed authors are maintaining/supporting the dataset. They pledge to help support issues, but cannot guarantee long-term support

### Licensing Information

The Proto_qa dataset is licensed under the [Creative Commons Attribution 4.0 International](https://github.com/iesl/protoqa-data/blob/master/LICENSE)

### Citation Information
```
@InProceedings{
huggingface:dataset,
title        = {ProtoQA: A Question Answering Dataset for Prototypical Common-Sense Reasoning},
authors      = {Michael Boratko, Xiang Lorraine Li, Tim O’Gorman, Rajarshi Das, Dan Le, Andrew McCallum},
year         = {2020},
publisher    = {GitHub},
journal      = {GitHub repository},
howpublished = {https://github.com/iesl/protoqa-data},
}
```

### Contributions

Thanks to [@bpatidar](https://github.com/bpatidar) for adding this dataset.