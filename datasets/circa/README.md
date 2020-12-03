---
annotations_creators:
- expert-generated
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
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- text-classification-other-question-answer-pair-classification
---

# Dataset Card Creation Guide

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

- **Homepage:** [CIRCA homepage](https://github.com/google-research-datasets/circa)
- **Repository:** [CIRCA repository](https://github.com/google-research-datasets/circa)
- **Paper:** ["I’d rather just go to bed”: Understanding Indirect Answers](https://arxiv.org/abs/2010.03450)
- **Point of Contact:** [Circa team, Google](circa@google.com)

### Dataset Summary

The Circa (meaning ‘approximately’) dataset aims to help machine learning systems to solve the problem of interpreting indirect answers to polar questions.

The dataset contains pairs of yes/no questions and indirect answers, together with annotations for the interpretation of the answer. The data is collected in 10 different social conversational situations (eg. food preferences of a friend).

The following are the situational contexts for the dialogs in the data.

```
1. X wants to know about Y’s food preferences
2. X wants to know what activities Y likes to do during weekends.
3. X wants to know what sorts of books Y likes to read.
4. Y has just moved into a neighbourhood and meets his/her new neighbour X.
5. X and Y are colleagues who are leaving work on a Friday at the same time.
6. X wants to know about Y's music preferences.
7. Y has just travelled from a different city to meet X.
8. X and Y are childhood neighbours who unexpectedly run into each other at a cafe.
9. Y has just told X that he/she is thinking of buying a flat in New York.
10. Y has just told X that he/she is considering switching his/her job.
```

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

The columns indicate:

```
1. id             : unique id for the question-answer pair

2. context        : the social situation for the dialogue. One of 10 situations (see next section). Each
                    situation is a dialogue between a person who poses the question (X) and the person who
		    answers (Y).

3. question-X     : the question posed by X

4. canquestion-X  : a (automatically) rewritten version of question into declarative form
                    Eg. Do you like Italian? --> I like Italian. See the paper for details.

5. answer-Y       : the answer given by Y to X

6. judgements     : the interpretations for the QA pair from 5 annotators. The value is a list of 5 strings,
                    separated by the token ‘#’

7. goldstandard1  : a gold standard majority judgement from the annotators. The value is the most common
                    interpretation and picked by at least 3 (out of 5 annotators). When a majority
		    judgement was not reached by the above criteria, the value is ‘NA’

8. goldstandard2  : Here the labels ‘Probably yes / sometimes yes’, ‘Probably no', and 'I am not sure how
                    X will interpret Y’s answer' are mapped respectively to ‘Yes’, ‘No’, and 'In the
		    middle, neither yes nor no’ before computing the majority. Still the label must be given
		    at least 3 times to become the majority choice. This method represents a less strict way
		    of analyzing the interpretations.
```

### Data Fields

```
id		        :	1
context		    :	X wants to know about Y's food preferences.
question-X	    :	Are you vegan?
canquestion-X   :   I am vegan.
answer-Y	    :	I love burgers too much.
judgements	    :	no#no#no#no#no
goldstandard1	:	no (label(s) used for the classification task)
goldstandard2	:	no (label(s) used for the classification task)
```

### Data Splits

There are no explicit train/val/test splits in this dataset.

## Dataset Creation

### Curation Rationale

They revisited a pragmatic inference problem in dialog: Understanding indirect responses to questions. Humans can interpret ‘I’m starving.’ in response to ‘Hungry?’, even without direct cue words such as ‘yes’ and ‘no’. In dialog systems, allowing natural responses rather than closed vocabularies would be similarly beneficial. However, today’s systems are only as sensitive to these pragmatic moves as their language model allows. They create and release the first large-scale English language corpus ‘Circa’ with 34,268 (polar question, indirect answer) pairs to enable progress on this task.

### Source Data

#### Initial Data Collection and Normalization

The QA pairs and judgements were collected using crowd annotations in three phases. They recruited English native speakers. The full descriptions of the data collection and quality control are present in [EMNLP 2020 paper](https://arxiv.org/pdf/2010.03450.pdf). Below is a brief overview only.

Phase 1: In the first phase, they collected questions only. They designed 10 imaginary social situations which give the annotator a context for the conversation. Examples are:
```
	‘asking a friend for food preferences’
	‘meeting your childhood neighbour’
	‘your friend wants to buy a flat in New York’
```
Annotators were asked to suggest questions which could be asked in each situation, such that each question only requires a ‘yes’ or ‘no’ answer. 100 annotators produced 5 questions each for the 10 situations, resulting in 5000 questions.

Phase 2: Here they focused on eliciting answers to the questions. They sampled 3500 questions from our previous set. For each question, They collected possible answers from 10 different annotators. The annotators were instructed to provide a natural phrase or a sentence as the answer and to avoid the use of explicit ‘yes’ and ‘no’ words.

Phase 3: Finally the QA pairs (34,268) were given to a third set of annotators who were asked how the question seeker would likely interpret a particular answer. These annotators had the following options to choose from:
```
	* 'Yes'
	* 'Probably yes' / 'sometimes yes'
	* 'Yes, subject to some conditions'
	* 'No'
	* 'Probably no'
	* 'In the middle, neither yes nor no'
	* 'I am not sure how X will interpret Y's answer'
```

#### Who are the source language producers?

The rest of the data apart from 10 initial questions was collected using crowd workers. They ran pilots for each step of data collection, and perused their results manually to ensure clarity in guidelines, and quality of the data. They also recruited native English speakers, mostly from the USA, and a few from the UK and Canada. They did not collect any further information about the crowd workers.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

The rest of the data apart from 10 initial questions was collected using crowd workers. They ran pilots for each step of data collection, and perused their results manually to ensure clarity in guidelines, and quality of the data. They also recruited native English speakers, mostly from the USA, and a few from the UK and Canada. They did not collect any further information about the crowd workers.

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

This dataset is the work of Annie Louis, Dan Roth, and Filip Radlinski from Google LLC.

### Licensing Information

This dataset was made available under the Creative Commons Attribution 4.0 License. A full copy of the license can be found at https://creativecommons.org/licenses/by-sa/4.0/e and link to the license webpage if available.

### Citation Information
```
@InProceedings{louis_emnlp2020,
  author =      "Annie Louis and Dan Roth and Filip Radlinski",
  title =       ""{I}'d rather just go to bed": {U}nderstanding {I}ndirect {A}nswers",
  booktitle =   "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing",
  year =        "2020",
}
```