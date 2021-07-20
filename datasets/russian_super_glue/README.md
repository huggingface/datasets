---
YAML tags:

annotations_creators:

- crowdsourced
- expert-generated

language_creators:
  
- crowdsourced
- expert-generated

languages:

- ru-RU

licenses:
- mit

multilinguality:
- monolingual

pretty_name: Russian SuperGLUE

size_categories:

- unknown

source_datasets:

- original

task_categories:

- text-classification

task_ids:

- natural-language-inference
- multi-class-classification
---

# Dataset Card for [Russian SuperGLUE]

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** https://russiansuperglue.com/
- **Repository:** https://github.com/RussianNLP/RussianSuperGLUE
- **Paper:** https://russiansuperglue.com/download/main_article
- **Leaderboard:** https://russiansuperglue.com/leaderboard/2
- **Point of Contact:** [More Information Needed]

### Dataset Summary

Modern universal language models and transformers such as BERT, ELMo, XLNet, RoBERTa and others need to be properly
compared and evaluated. In the last year, new models and methods for pretraining and transfer learning have driven 
striking performance improvements across a range of language understanding tasks.


We offer testing methodology based on tasks, typically proposed for “strong AI” — logic, commonsense, reasoning.
Adhering to the GLUE and SuperGLUE methodology, we present a set of test tasks for general language understanding
and leaderboard models.


For the first time a complete test for Russian language was developed, which is similar to its English analog.
Many datasets were composed for the first time, and a leaderboard of models for the Russian language with comparable
results is also presented.

### Supported Tasks and Leaderboards

Supported tasks, barring a few additions, are equivalent to the original SuperGLUE tasks.

|Task Name|Equiv. to|
|----|---:|
|Linguistic Diagnostic for Russian|Broadcoverage Diagnostics (AX-b)|
|Russian Commitment Bank (RCB)|CommitmentBank (CB)|
|Choice of Plausible Alternatives for Russian language (PARus)|Choice of Plausible Alternatives (COPA)|
|Russian Multi-Sentence Reading Comprehension (MuSeRC)|Multi-Sentence Reading Comprehension (MultiRC)|
|Textual Entailment Recognition for Russian (TERRa)|Recognizing Textual Entailment (RTE)|
|Russian Words in Context (based on RUSSE)|Words in Context (WiC)|
|The Winograd Schema Challenge (Russian)|The Winograd Schema Challenge (WSC)|
|Yes/no Question Answering Dataset for the Russian (DaNetQA)|BoolQ|
|Russian Reading Comprehension with Commonsense Reasoning (RuCoS)|Reading Comprehension with Commonsense Reasoning (ReCoRD)|

### Languages

All tasks are in Russian.

## Dataset Structure

### Data Instances

#### LiDiRus

- **Size of downloaded dataset files:** 0.047 MB
- **Size of the generated dataset:** 0.47 MB
- **Total amount of disk used:** 0.517 MB

#### RCB

- **Size of downloaded dataset files:** 0.134 MB
- **Size of the generated dataset:** 0.504 MB
- **Total amount of disk used:** 0.641 MB

#### PARus

- **Size of downloaded dataset files:** 0.057 MB
- **Size of the generated dataset:** 0.187 MB
- **Total amount of disk used:**  0.245 MB

#### MuSeRC

- **Size of downloaded dataset files:** 1.2 MB
- **Size of the generated dataset:** 57 MB
- **Total amount of disk used:** 59 MB

#### TERRa

- **Size of downloaded dataset files:** 0.887 MB
- **Size of the generated dataset:** 3.28 MB
- **Total amount of disk used:** 4.19 MB

#### RUSSE

- **Size of downloaded dataset files:** 3.7 MB
- **Size of the generated dataset:** 20 MB
- **Total amount of disk used:** 24 MB

#### RWSD

- **Size of downloaded dataset files:** 0.04 MB
- **Size of the generated dataset:** 0.279 MB
- **Total amount of disk used:**  0.320 MB

#### DaNetQA

- **Size of downloaded dataset files:** 1.3 MB
- **Size of the generated dataset:** 4.6 MB
- **Total amount of disk used:**  5.9 MB

#### RuCoS

- **Size of downloaded dataset files:** 54 MB
- **Size of the generated dataset:** 193 MB
- **Total amount of disk used:** 249 MB

### Data Fields

#### LiDiRus

- `idx`: an `int32` feature
- `label`: a classification label, with possible values `entailment` (0), `not_entailment` (1)
- `sentence1`: a `string` feature
- `sentence2`: a `string` feature
- `knowledge`: a `string` feature with possible values `''`, `'World knowledge'`, `'Common sense'`
- `lexical-semantics`: a `string` feature
- `logic`: a `string` feature
- `predicate-argument-structure`: a `string` feature


#### RCB

- `idx`: an `int32` feature
- `label`: a classification label, with possible values `entailment` (0), `contraditction` (1), `neutral` (2)
- `premise`: a `string` feature
- `hypothesis`: a `string` feature
- `verb`: a `string` feature
- `negation`: a `string` feature with possible values `'no_negation'`, `'negation'`, `''`, `'double_negation'`

#### PARus

- `idx`: an `int32` feature
- `label`: a classification label, with possible values `choice1` (0), `choice2` (1)
- `premise`: a `string` feature
- `choice1`: a `string` feature
- `choice2`: a `string` feature
- `question`: a `string` feature with possible values `'cause'`, `'effect'`

#### MuSeRC
- `idx`: an `int32` feature
- `label` : a classification label, with possible values `0`, `1`
- `paragraph`: a `string` feature
- `question`: a `string` feature
- `answer`: a `string` feature


#### TERRa
- `idx`: an `int32` feature
- `label`: a classification label, with possible values `entailment` (0), `not_entailment` (1)
- `premise`: a `string` feature
- `hypothesis`: a `string` feature

#### RUSSE
- `idx`: an `int32` feature
- `label` : a classification label, with possible values `0`, `1`
- `word`: a `string` feature
- `sentence1`: a `string` feature
- `sentence2`: a `string` feature
- `gold_sense1`: an `int32` feature
- `gold_sense2`: an `int32` feature
- `start1`: an `int32` feature
- `start2`: an `int32` feature
- `end1`: an `int32` feature
- `end2`: an `int32` feature

#### RWSD

- `idx`: an `int32` feature
- `label` : a classification label, with possible values `0`, `1`
- `text`: a `string` feature
- `span1_index`: an `int32` feature
- `span2_index`: an `int32` feature
- `span1_text`: a `string` feature
- `span2_text`: a `string` feature


#### DaNetQA
- `idx`: an `int32` feature
- `label` : a classification label, with possible values `false` (0), `true` (1)
- `question`: a `string` feature
- `passage`: a `string` feature

#### RuCoS

- `idx`: an `int32` feature
- `passage`: a `string` feature
- `query`: a `string` feature
- `entities`: a `list of strings` feature
- `answers`: a `list of strings` feature


[More Information Needed]

### Data Splits

#### 	LiDiRus
|   |test|
|---|---:|
|LiDiRus|1104|

#### RCB

| |train|validation|test|
|----|---:|----:|---:|
|RCB|438|220|438|

#### PARus

| |train|validation|test|
|----|---:|----:|---:|
|PARus|400|100|500|

#### MuSeRC

| |train|validation|test|
|----|---:|----:|---:|
|MuSeRC|500|100|322|


#### TERRa

| |train|validation|test|
|----|---:|----:|---:|
|TERRa|2616|307|3198|


#### RUSSE

| |train|validation|test|
|----|---:|----:|---:|
|RUSSE|19845|8508|18892|


#### RWSD

| |train|validation|test|
|----|---:|----:|---:|
|RWSD|606|204|154|


#### DaNetQA

| |train|validation|test|
|----|---:|----:|---:|
|DaNetQA|1749|821|805|


#### RuCoS

| |train|validation|test|
|----|---:|----:|---:|
|RuCoS|72193|7577|7257|

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

All our datasets are published by MIT License.

### Citation Information
```
@article{shavrina2020russiansuperglue,
                  title={RussianSuperGLUE: A Russian Language Understanding Evaluation Benchmark},
                  author={Shavrina, Tatiana and Fenogenova, Alena and Emelyanov, Anton and Shevelev, Denis and Artemova, Ekaterina and Malykh, Valentin and Mikhailov, Vladislav and Tikhonova, Maria and Chertok, Andrey and Evlampiev, Andrey},
                  journal={arXiv preprint arXiv:2010.15925},
                  year={2020}
                  }
```
### Contributions

Thanks to [@slowwavesleep](https://github.com/slowwavesleep) for adding this dataset.
