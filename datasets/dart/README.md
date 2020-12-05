---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- crowdsourced
- machine-generated
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|wikitable_questions
- extended|wikisql
- extended|web_nlg
- extended|cleaned_e2e
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-rdf-to-text
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

- **Homepage:** [homepahe](https://github.com/Yale-LILY/dart)
- **Repository:** [github](https://github.com/Yale-LILY/dart)
- **Paper:** [paper](https://arxiv.org/abs/2007.02871)
- **Leaderboard:** [leaderboard](https://github.com/Yale-LILY/dart#leaderboard)

### Dataset Summary

DART is a large dataset for open-domain structured data record to text generation. We consider the structured data record input as a set of RDF entity-relation triples, a format widely used for knowledge representation and semantics description. DART consists of 82,191 examples across different domains with each input being a semantic RDF triple set derived from data records in tables and the tree ontology of the schema, annotated with sentence descriptions that cover all facts in the triple set. This hierarchical, structured format with its open-domain nature differentiates DART from other existing table-to-text corpora.

### Supported Tasks and Leaderboards

The task associated to DART is text generation from data records that are RDF triplets:

- `conditional-text-generation-other-rdf-to-text`: The dataset can be used to train a model for text generation from RDF triplets, which consists in generating textual description of structured data. Success on this task is typically measured by achieving a *high* [BLEU](https://huggingface.co/metrics/bleu), [METEOR](https://huggingface.co/metrics/meteor), [BLEURT](https://huggingface.co/metrics/bleurt), [TER](https://huggingface.co/metrics/ter), [MoverScore](https://huggingface.co/metrics/mover_score), and [BERTScore](https://huggingface.co/metrics/bert_score). The ([BART-large model](https://huggingface.co/facebook/bart-large) from [BART](https://huggingface.co/transformers/model_doc/bart.html)) model currently achieves the following scores:

|            | BLEU  | METEOR | TER  | MoverScore  | BERTScore  | BLEURT |
| -----      | ----- | ------ | ---- | ----------- | ---------- | ------ |
| BART       | 37.06 | 0.36   | 0.57 | 0.44        | 0.92       | 0.22   |

This task has an active leaderboard which can be found [here](https://github.com/Yale-LILY/dart#leaderboard) and ranks models based on the above metrics while also reporting.

### Languages

The dataset is in english (en).

## Dataset Structure

### Data Instances

Here is an example from the dataset:

```
{'annotations': {'source': ['WikiTableQuestions_mturk'],
  'text': ['First Clearing\tbased on Callicoon, New York and location at On NYS 52 1 Mi. Youngsville']},
 'subtree_was_extended': False,
 'tripleset': [['First Clearing', 'LOCATION', 'On NYS 52 1 Mi. Youngsville'],
  ['On NYS 52 1 Mi. Youngsville', 'CITY_OR_TOWN', 'Callicoon, New York']]}
```

It contains one annotation where the textual description is 'First Clearing\tbased on Callicoon, New York and location at On NYS 52 1 Mi. Youngsville'. The RDF triplets considered to generate this description are in tripleset and are formatted as subject, predicate, object.

### Data Fields

The different fields are:

- `annotations`:
  - `text`: list of text descriptions of the triplets
  - `source`: list of sources of the RDF triplets (WikiTable, e2e, etc.)
- `subtree_was_extended`: boolean, if the subtree condidered during the dataset construction was extended. Sometimes this field is missing, and therefore set to `None`
- `tripleset`: RDF triplets as a list of triplets of strings (subject, predicate, object)

### Data Splits

There are three splits, train, validation and test:

|                  | Tain    | Valid | Test |
| -----            | ------- | ----- | ---- |
| N. Examples      | 30526   | 2768  | 6959 |

## Dataset Creation

### Curation Rationale

Automatically generating textual descriptions from structured data inputs is crucial to improving the accessibility of knowledge bases to lay users.

### Source Data

DART comes from existing datasets that cover a variety of different domains while allowing to build a tree ontology and form RDF triple sets as semantic representations. The datasets used are WikiTableQuestions, WikiSQL, WebNLG and Cleaned E2E.

#### Initial Data Collection and Normalization

DART is constructed using multiple complementary methods: (1) human annotation on open-domain Wikipedia tables
from WikiTableQuestions (Pasupat and Liang, 2015) and WikiSQL (Zhong et al., 2017), (2) automatic conversion of questions in WikiSQL to declarative sentences, and (3) incorporation of existing datasets including WebNLG 2017 (Gardent et al., 2017a,b; Shimorina and Gardent, 2018) and Cleaned E2E (Novikova et al., 2017b; Dušek et al., 2018, 2019)

#### Who are the source language producers?

[More Information Needed]

### Annotations

DART is constructed using multiple complementary methods: (1) human annotation on open-domain Wikipedia tables
from WikiTableQuestions (Pasupat and Liang, 2015) and WikiSQL (Zhong et al., 2017), (2) automatic conversion of questions in WikiSQL to declarative sentences, and (3) incorporation of existing datasets including WebNLG 2017 (Gardent et al., 2017a,b; Shimorina and Gardent, 2018) and Cleaned E2E (Novikova et al., 2017b; Dušek et al., 2018, 2019)

#### Annotation process

The two stage annotation process for constructing tripleset sentence pairs is based on a tree-structured ontology of each table.
First, internal skilled annotators denote the parent column for each column header.
Then, a larger number of annotators provide a sentential description of an automatically-chosen subset of table cells in a row.

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

Under MIT license (see [here](https://github.com/Yale-LILY/dart/blob/master/LICENSE))

### Citation Information

```
@article{radev2020dart,
  title={DART: Open-Domain Structured Data Record to Text Generation},
  author={Dragomir Radev and Rui Zhang and Amrit Rau and Abhinand Sivaprasad and Chiachun Hsieh and Nazneen Fatema Rajani and Xiangru Tang and Aadit Vyas and Neha Verma and Pranav Krishna and Yangxiaokang Liu and Nadia Irwanto and Jessica Pan and Faiaz Rahman and Ahmad Zaidi and Murori Mutuma and Yasin Tarabar and Ankit Gupta and Tao Yu and Yi Chern Tan and Xi Victoria Lin and Caiming Xiong and Richard Socher},
  journal={arXiv preprint arXiv:2007.02871},
  year={2020}
```
