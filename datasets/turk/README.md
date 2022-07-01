---
annotations_creators:
- machine-generated
language_creators:
- found
language:
- en
license:
- gpl-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text2text-generation
task_ids:
- text-simplification
paperswithcode_id: null
pretty_name: TURK
---

# Dataset Card for TURK

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

- **Homepage:** None 
- **Repository:** [TURK](https://github.com/cocoxu/simplification)
- **Paper:** [Optimizing Statistical Machine Translation for Text Simplification](https://www.aclweb.org/anthology/Q16-1029/)
- **Leaderboard:** N/A
- **Point of Contact:** [Wei Xu](mailto:wei.xu@cc.gatech.edu)


### Dataset Summary

TURK is a multi-reference dataset for the evaluation of sentence simplification in English. The dataset consists of 2,359 sentences from the [Parallel Wikipedia Simplification (PWKP) corpus](https://www.aclweb.org/anthology/C10-1152/). Each sentence is associated with 8 crowdsourced simplifications that focus on only lexical paraphrasing (no sentence splitting or deletion).

### Supported Tasks and Leaderboards

No Leaderboard for the task.

### Languages

TURK contains English text only (BCP-47: `en`).

## Dataset Structure

### Data Instances

An instance consists of an original sentence and 8 possible reference simplifications that focus on lexical paraphrasing.

```
{'original': 'one side of the armed conflicts is composed mainly of the sudanese military and the janjaweed , a sudanese militia group recruited mostly from the afro-arab abbala tribes of the northern rizeigat region in sudan .',
 'simplifications': ['one side of the armed conflicts is made of sudanese military and the janjaweed , a sudanese militia recruited from the afro-arab abbala tribes of the northern rizeigat region in sudan .', 'one side of the armed conflicts consist of the sudanese military and the sudanese militia group janjaweed .', 'one side of the armed conflicts is mainly sudanese military and the janjaweed , which recruited from the afro-arab abbala tribes .', 'one side of the armed conflicts is composed mainly of the sudanese military and the janjaweed , a sudanese militia group recruited mostly from the afro-arab abbala tribes in sudan .', 'one side of the armed conflicts is made up mostly of the sudanese military and the janjaweed , a sudanese militia group whose recruits mostly come from the afro-arab abbala tribes from the northern rizeigat region in sudan .', 'the sudanese military and the janjaweed make up one of the armed conflicts , mostly from the afro-arab abbal tribes in sudan .', 'one side of the armed conflicts is composed mainly of the sudanese military and the janjaweed , a sudanese militia group recruited mostly from the afro-arab abbala tribes of the northern rizeigat regime in sudan .', 'one side of the armed conflicts is composed mainly of the sudanese military and the janjaweed , a sudanese militia group recruited mostly from the afro-arab abbala tribes of the northern rizeigat region in sudan .']}
```


### Data Fields

- `original`: an original sentence from the source datasets
- `simplifications`:  a set of reference simplifications produced by crowd workers.

### Data Splits

TURK does not contain a training set; many models use [WikiLarge](https://github.com/XingxingZhang/dress) (Zhang and Lapata, 2017) or [Wiki-Auto](https://github.com/chaojiang06/wiki-auto) (Jiang et. al 2020) for training. 

Each input sentence has 8 associated reference simplified sentences. 2,359 input sentences are randomly split into 2,000 validation and 359 test sentences.

|                            | Dev    | Test | Total |
| -----                      | ------ | ---- | ----- |
| Input Sentences            | 2000   | 359  | 2359  |
| Reference Simplifications  | 16000  | 2872 | 18872 |


## Dataset Creation

### Curation Rationale

The TURK dataset was constructed to evaluate the task of text simplification.  It contains multiple human-written references that focus on only lexical simplification. 

### Source Data

#### Initial Data Collection and Normalization

 The input sentences in the dataset are extracted from the [Parallel Wikipedia Simplification (PWKP) corpus](https://www.aclweb.org/anthology/C10-1152/). 

#### Who are the source language producers?

The references are crowdsourced from Amazon Mechanical Turk. The annotators were asked to provide simplifications without losing any information or splitting the input sentence. No other demographic or compensation information is provided in the paper.

### Annotations

#### Annotation process

The instructions given to the annotators are available in the paper.

#### Who are the annotators?

The annotators are Amazon Mechanical Turk workers.

### Personal and Sensitive Information

Since the dataset is created from English Wikipedia (August 22, 2009 version), all the information contained in the dataset is already in the public domain.

## Considerations for Using the Data

### Social Impact of Dataset

The dataset helps move forward the research towards text simplification by creating a higher quality validation and test dataset. Progress in text simplification in turn has the potential to increase the accessibility of written documents to wider audiences.

### Discussion of Biases

The dataset may contain some social biases, as the input sentences are based on Wikipedia. Studies have shown that the English Wikipedia contains both gender biases [(Schmahl et al., 2020)](https://research.tudelft.nl/en/publications/is-wikipedia-succeeding-in-reducing-gender-bias-assessing-changes) and racial biases [(Adams et al., 2019)](https://journals.sagepub.com/doi/pdf/10.1177/2378023118823946).

### Other Known Limitations

Since the dataset contains only 2,359 sentences that are derived from Wikipedia, it is limited to a small subset of topics present on Wikipedia.


## Additional Information

### Dataset Curators

TURK was developed by researchers at the University of Pennsylvania. The work was  supported by the NSF under grant IIS-1430651 and the NSF GRFP under grant 1232825. 

### Licensing Information

[GNU General Public License v3.0](https://github.com/cocoxu/simplification/blob/master/LICENSE)

### Citation Information
```
 @article{Xu-EtAl:2016:TACL,
 author = {Wei Xu and Courtney Napoles and Ellie Pavlick and Quanze Chen and Chris Callison-Burch},
 title = {Optimizing Statistical Machine Translation for Text Simplification},
 journal = {Transactions of the Association for Computational Linguistics},
 volume = {4},
 year = {2016},
 url = {https://cocoxu.github.io/publications/tacl2016-smt-simplification.pdf},
 pages = {401--415}
 }
 ```
### Contributions

Thanks to [@mounicam](https://github.com/mounicam) for adding this dataset.
