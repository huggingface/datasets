---
annotations_creators:
- found
language_creators:
- found
languages:
- tr
licenses:
- found
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-offensive-language-classification
paperswithcode_id: null
---

# Dataset Card for OffensEval-TR 2020

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

- **Homepage:** [offensive-turkish](https://coltekin.github.io/offensive-turkish/)
- **Paper:** [A Corpus of Turkish Offensive Language on Social Media](https://coltekin.github.io/offensive-turkish/troff.pdf)
- **Point of Contact:** [Çağrı Çöltekin](ccoltekin@sfs.uni-tuebingen.de)

### Dataset Summary

The file offenseval-tr-training-v1.tsv contains 31,756 annotated tweets. 

The file offenseval-annotation.txt contains a short summary of the annotation guidelines.

Twitter user mentions were substituted by @USER and URLs have been substitute by URL.

Each instance contains up to 1 labels corresponding to one of the following sub-task:

- Sub-task A: Offensive language identification; 

### Supported Tasks and Leaderboards

The dataset was published on this [paper](https://coltekin.github.io/offensive-turkish/troff.pdf). 

### Languages

The dataset is based on Turkish.

## Dataset Structure

### Data Instances

A binary dataset with with (NOT) Not Offensive and (OFF) Offensive tweets.  

### Data Fields

Instances are included in TSV format as follows:

ID	INSTANCE	SUBA

The column names in the file are the following:

id	tweet	subtask_a

The labels used in the annotation are listed below.

#### Task and Labels

(A) Sub-task A: Offensive language identification

- (NOT) Not Offensive - This post does not contain offense or profanity.
- (OFF) Offensive - This post contains offensive language or a targeted (veiled or direct) offense

In our annotation, we label a post as offensive (OFF) if it contains any form of non-acceptable language (profanity) or a targeted offense, which can be veiled or direct. 

### Data Splits

| Tain  | Test  | 
|-------| ----- | 
| 31756 | 3528  | 

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

From tweeter.  

### Annotations

[More Information Needed]

#### Annotation process

We describe the labels above in a “flat” manner. However, the annotation process we follow is hierarchical. The following QA pairs give a more flowchart-like procedure to follow

1. Is the tweet in Turkish and understandable?
    * No: mark tweet X for exclusion, and go to next tweet
    * Yes: continue to step 2
2. Is the tweet include offensive/inappropriate language?
    * No: mark the tweet non go to step 4
    * Yes: continue to step 3
3. Is the offense in the tweet targeted?
    * No: mark the tweet prof go to step 4
    * Yes: chose one (or more) of grp, ind, *oth based on the definitions above. Please try to limit the number of labels unless it is clear that the tweet includes offense against multiple categories.
4. Was the labeling decision difficult (precise answer needs more context, tweets includes irony, or for another reason)?
    * No: go to next tweet
    * Yes: add the label X, go to next tweet


#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Discussion of Social Impact and Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

The annotations are distributed under the terms of [Creative Commons Attribution License (CC-BY)](https://creativecommons.org/licenses/by/2.0/). Please cite the following paper, if you use this resource.

### Citation Information

```
@inproceedings{coltekin2020lrec,
 author  = {\c{C}\"{o}ltekin, \c{C}a\u{g}r{\i}},
 year  = {2020},
 title  = {A Corpus of Turkish Offensive Language on Social Media},
 booktitle  = {Proceedings of The 12th Language Resources and Evaluation Conference},
 pages  = {6174--6184},
 address  = {Marseille, France},
 url  = {https://www.aclweb.org/anthology/2020.lrec-1.758},
}
```

### Contributions

Thanks to [@yavuzKomecoglu](https://github.com/yavuzKomecoglu) for adding this dataset.