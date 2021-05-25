---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
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
- question-answering
task_ids:
- multiple-choice-qa
- open-domain-qa
paperswithcode_id: qa-srl
---

# Dataset Card for QA-SRL

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

- **Homepage:** [Homepage](https://dada.cs.washington.edu/qasrl/#page-top)
- **Annotation Tool:** [Annotation tool](https://github.com/luheng/qasrl_annotation)
- **Repository:** [Repository](https://dada.cs.washington.edu/qasrl/#dataset)
- **Paper:**    [Qa_srl paper](https://www.aclweb.org/anthology/D15-1076.pdf)
- **Point of Contact:** [Luheng He](luheng@cs.washington.edu)


### Dataset Summary

we model predicate-argument structure of a sentence with a set of question-answer pairs. our method allows practical large-scale annotation of training data. We focus on semantic rather than syntactic annotation, and introduce a scalable method for gathering data that allows both training and evaluation.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

This dataset is in english language.

## Dataset Structure

### Data Instances


We use question-answer pairs to model verbal predicate-argument structure. The questions start with wh-words (Who, What, Where, What, etc.) and contains a verb predicate in the sentence; the answers are phrases in the sentence. For example:

`UCD finished the 2006 championship as Dublin champions , by beating St Vincents in the final .`

Predicate | Question | Answer
---|---|---|
|Finished|Who finished something? |	UCD
|Finished|What did someone finish?|the 2006 championship
|Finished|What did someone finish something as?	|Dublin champions
|Finished|How did someone finish something?	|by beating St Vincents in the final
|beating | Who beat someone? | UCD
|beating|When did someone beat someone?	|in the final
|beating|Who did someone beat?|	St Vincents

### Data Fields

Annotations provided are as follows:

- `sentence`: contains tokenized sentence
- `sent_id`: is the sentence identifier
- `predicate_idx`:the index of the predicate (its position in the sentence) 
- `predicate`: the predicate token
- `question`: contains the question which is a list of tokens. The question always consists of seven slots, as defined in the paper. The empty slots are represented with a marker “_”. The question ends with question mark.
- `answer`: list of answers to the question
               

### Data Splits

Dataset | Sentences | Verbs | QAs
--- | --- | --- |---|
**newswire-train**|744|2020|4904|
**newswire-dev**|249|664|1606|
**newswire-test**|248|652|1599
**Wikipedia-train**|`1174`|`2647`|`6414`|
**Wikipedia-dev**|`392`|`895`|`2183`|
**Wikipedia-test**|`393`|`898`|`2201`|

**Please note**
This dataset only has wikipedia data. Newswire dataset needs  CoNLL-2009 English training data to get the complete data. This training data is under license. Thus, newswire dataset is not included in this data.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

We annotated over 3000 sentences (nearly 8,000 verbs) in total across two domains: newswire (PropBank) and Wikipedia. 
#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

non-expert annotators were given a short tutorial and a small set of sample annotations (about 10 sentences). Annotators were hired if they showed good understanding of English and the task. The entire screening process usually took less than 2 hours.

#### Who are the annotators?

10 part-time, non-exper annotators from Upwork (Previously oDesk)

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

[Luheng He](luheng@cs.washington.edu)

### Licensing Information

[More Information Needed]

### Citation Information

```
@InProceedings{huggingface:dataset,
title = {QA-SRL: Question-Answer Driven Semantic Role Labeling},
authors={Luheng He, Mike Lewis, Luke Zettlemoyer},
year={2015}
publisher = {cs.washington.edu},
howpublished={\\url{https://dada.cs.washington.edu/qasrl/#page-top}},
}
```

### Contributions

Thanks to [@bpatidar](https://github.com/bpatidar) for adding this dataset.