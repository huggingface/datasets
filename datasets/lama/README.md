---
annotations_creators:
- crowdsourced
- expert-generated
- machine-generated
language_creators:
- crowdsourced
- expert-generated
- machine-generated
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets:
- extended|conceptnet5
- extended|squad
task_categories:
- text-retrieval
- text-scoring
task_ids:
- fact-checking-retrieval
- text-scoring-other-probing
---

# Dataset Card for LAMA: LAnguage Model Analysis - a dataset for probing and analyzing the factual and commonsense knowledge contained in pretrained language models.

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

- **Homepage:**
https://github.com/facebookresearch/LAMA
- **Repository:**
https://github.com/facebookresearch/LAMA
- **Paper:**
@inproceedings{petroni2019language,
  title={Language Models as Knowledge Bases?},
  author={F. Petroni, T. Rockt{\"{a}}schel, A. H. Miller, P. Lewis, A. Bakhtin, Y. Wu and S. Riedel},
  booktitle={In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP), 2019},
  year={2019}
}

@inproceedings{petroni2020how,
  title={How Context Affects Language Models' Factual Predictions},
  author={Fabio Petroni and Patrick Lewis and Aleksandra Piktus and Tim Rockt{\"a}schel and Yuxiang Wu and Alexander H. Miller and Sebastian Riedel},
  booktitle={Automated Knowledge Base Construction},
  year={2020},
  url={https://openreview.net/forum?id=025X0zPfn}
}

### Dataset Summary

This dataset provides the data for LAMA. The dataset include a subset
of Google_RE
(https://code.google.com/archive/p/relation-extraction-corpus/), TRex
(subset of wikidata triples), Conceptnet
(https://github.com/commonsense/conceptnet5/wiki) and Squad. There are
configs for each of "google_re", "trex", "conceptnet" and "squad",
respectively.

The dataset includes some cleanup, and addition of a masked sentence
and assocaited answers for the [MASK] token. The accuracy in
predicting the [MASK] token shows how well the language model knows
facts and common sense information. The [MASK] tokens are only for the
"object" slots.

This version of the dataset includes "negated" sentences as well as
the masked sentence. Also, certain of the config includes "template"
and "template_negated" fields of the form "[X] some text [Y]", where
[X] and [Y] are the subject and object slots respectively of certain
relations.

See the paper for more details.  For more information, also see:
https://github.com/facebookresearch/LAMA

### Languages
en

## Dataset Structure

### Data Instances


The trex config has the following fields:


``
{
	'uuid': ...,
	'obj_uri': ...,
	'obj_label': ...,
	'sub_uri': ...,
	'sub_label': ...,
	'predicate_id': ...,
	'sub_surface': ...
	'obj_surface': ...
	'masked_sentence': ...
	'template': ...
	'template_negated': ...
	'label': ...
	'description': ...
	'type': ...
}
``

The conceptnet config has the following fields:


``
{
	'uuid': ...,
	'sub': ...,
	'obj': ...,
	'pred': ...,
	'obj_label': ...,
	'masked_sentence': ...,
	'negated': ...
}
``

The squad config has the following fields:


``
{
	'id': ...,
	'sub_label': ...,
	'obj_label': ...,
	'negated': ...,
	'masked_sentence': ...,
}
``

The google_re config has the following fields:


``
{
	'pred': ...,
	'sub': ...,
	'obj': ...,
	'evidences': ...,
	'judgments': ...,
	'sub_q': ...,
	'sub_label': ...
	'sub_aliases': ...
	'obj_w': ...
	'obj_label': ...
	'obj_aliases': ...
	'uuid': ...
	'masked_sentence': ...
	'template': ...
	'template_negated': ...
}
``

### Data Fields

The trex config has the following fields:
* uuid: the id
* obj_uri: a uri for the object slot
* obj_label: a label for the object slot
* sub_uri: a uri for the subject slot
* sub_label: a label for the subject slot
* predicate_id: the predicate/relationship
* sub_surface: the surface text for the subject
* obj_surface: The surface text for the object. This is the word that should be predicted by the [MASK] token.
* masked_sentence: The masked sentence used to probe, with the object word replaced with [MASK]
* template: A pattern of text for extracting the relationship, object and subject of the form "[X] some text [Y]", where [X] and [Y] are the subject and object slots respectively. 
* template_negated: Same as above, except the [Y] is not the object.
* label: the label for the relationship/predicate
* description': a description of the relationship/predicate
* type: a type id for the relationship/predicate

The conceptnet config has the following fields:
* uuid: the id
* sub: the subject
* obj: the object to be predicted.
* pred: the predicate/relationship
* obj_label: the object label
* masked_sentence: The masked sentence used to probe, with the object word replaced with [MASK]
* negated: same as above, except [MASK] should predict something that is not the object word.


The squad config has the following fields:
* id: the id
* sub_label: the subject label
* obj_label: the object label that is being predicted
* masked_sentence: The masked sentence used to probe, with the object word replaced with [MASK]
* negated: same as above, except [MASK] should predict something that is not the object word.


The google_re config has the following fields:

* uuid: the id
* pred: the predicate
* sub: the subject
* obj: the object
* evidences: flattened json string that provides evidence for predicate. parse this json string to get more 'snippet' information.
* judgments: data about judgments
* sub_q: unknown
* sub_label: label for the subject
* sub_aliases: unknown
* obj_w: unknown
* obj_label: label for the object
* obj_aliases: unknown
* masked_sentence: The masked sentence used to probe, with the object word replaced with [MASK]
* template: A pattern of text for extracting the relationship, object and subject of the form "[X] some text [Y]", where [X] and [Y] are the subject and object slots respectively. 
* template_negated: Same as above, except the [Y] is not the object.


### Data Splits

There are no data splits.

## Dataset Creation

### Curation Rationale

This dataset was gathered and created to probe what language models understand.

### Source Data

#### Initial Data Collection and Normalization

See the reaserch paper and website for more detail. The dataset was
created gathered from various other datasets with cleanups for probing.


#### Who are the source language producers?

The LAMA authors and the original authors of the various configs.

### Annotations

#### Annotation process

Human annotations under the original datasets (conceptnet), and various machine annotations.

#### Who are the annotators?

Human annotations and machine annotations.

### Personal and Sensitive Information

Unkown, but likely names of famous people.

## Considerations for Using the Data

### Social Impact of Dataset

The goal for the work is to probe the understanding of language models.

### Discussion of Biases

Since the data is from human annotators, there is likely to be baises. 

### Other Known Limitations

The original documentation for the datafields are limited.

## Additional Information

### Dataset Curators

The authors of LAMA at Facebook and the authors of the original datasets.

### Licensing Information

The Creative Commons Attribution-Noncommercial 4.0 International License. see https://github.com/facebookresearch/LAMA/blob/master/LICENSE

### Citation Information

@inproceedings{petroni2019language,
  title={Language Models as Knowledge Bases?},
  author={F. Petroni, T. Rockt{\"{a}}schel, A. H. Miller, P. Lewis, A. Bakhtin, Y. Wu and S. Riedel},
  booktitle={In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP), 2019},
  year={2019}
}

@inproceedings{petroni2020how,
  title={How Context Affects Language Models' Factual Predictions},
  author={Fabio Petroni and Patrick Lewis and Aleksandra Piktus and Tim Rockt{\"a}schel and Yuxiang Wu and Alexander H. Miller and Sebastian Riedel},
  booktitle={Automated Knowledge Base Construction},
  year={2020},
  url={https://openreview.net/forum?id=025X0zPfn}
}


