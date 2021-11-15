---
pretty_name: "LAMA: LAnguage Model Analysis"
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
  conceptnet:
  - 10K<n<100K
  google_re:
  - 1K<n<10K
  squad:
  - n<1K
  trex:
  - 1M<n<10M
source_datasets:
- extended|conceptnet5
- extended|squad
task_categories:
- text-retrieval
- text-scoring
task_ids:
- fact-checking-retrieval
- text-scoring-other-probing
paperswithcode_id: lama
---

# Dataset Card for LAMA: LAnguage Model Analysis - a dataset for probing and analyzing the factual and commonsense knowledge contained in pretrained language models.

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
and associated answers for the [MASK] token. The accuracy in
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
{'description': 'the item (an institution, law, public office ...) or statement belongs to or has power over or applies to the value (a territorial jurisdiction: a country, state, municipality, ...)', 'label': 'applies to jurisdiction', 'masked_sentence': 'It is known as a principality as it is a monarchy headed by two Co-Princes – the Spanish/Roman Catholic Bishop of Urgell and the President of [MASK].', 'obj_label': 'France', 'obj_surface': 'France', 'obj_uri': 'Q142', 'predicate_id': 'P1001', 'sub_label': 'president of the French Republic', 'sub_surface': 'President', 'sub_uri': 'Q191954', 'template': '[X] is a legal term in [Y] .', 'template_negated': '[X] is not a legal term in [Y] .', 'type': 'N-M', 'uuid': '3fe3d4da-9df9-45ba-8109-784ce5fba38a'}
``

The conceptnet config has the following fields:


``
{'masked_sentence': 'One of the things you do when you are alive is [MASK].', 'negated': '', 'obj': 'think', 'obj_label': 'think', 'pred': 'HasSubevent', 'sub': 'alive', 'uuid': 'd4f11631dde8a43beda613ec845ff7d1'}
``

The squad config has the following fields:


``
{'id': '56be4db0acb8001400a502f0_0', 'masked_sentence': 'To emphasize the 50th anniversary of the Super Bowl the [MASK] color was used.', 'negated': "['To emphasize the 50th anniversary of the Super Bowl the [MASK] color was not used.']", 'obj_label': 'gold', 'sub_label': 'Squad'}
``

The google_re config has the following fields:


``
{'evidences': '[{\'url\': \'http://en.wikipedia.org/wiki/Peter_F._Martin\', \'snippet\': "Peter F. Martin (born 1941) is an American politician who is a Democratic member of the Rhode Island House of Representatives. He has represented the 75th District Newport since 6 January 2009. He is currently serves on the House Committees on Judiciary, Municipal Government, and Veteran\'s Affairs. During his first term of office he served on the House Committees on Small Business and Separation of Powers & Government Oversight. In August 2010, Representative Martin was appointed as a Commissioner on the Atlantic States Marine Fisheries Commission", \'considered_sentences\': [\'Peter F Martin (born 1941) is an American politician who is a Democratic member of the Rhode Island House of Representatives .\']}]', 'judgments': "[{'rater': '18349444711114572460', 'judgment': 'yes'}, {'rater': '17595829233063766365', 'judgment': 'yes'}, {'rater': '4593294093459651288', 'judgment': 'yes'}, {'rater': '7387074196865291426', 'judgment': 'yes'}, {'rater': '17154471385681223613', 'judgment': 'yes'}]", 'masked_sentence': 'Peter F Martin (born [MASK]) is an American politician who is a Democratic member of the Rhode Island House of Representatives .', 'obj': '1941', 'obj_aliases': '[]', 'obj_label': '1941', 'obj_w': 'None', 'pred': '/people/person/date_of_birth', 'sub': '/m/09gb0bw', 'sub_aliases': '[]', 'sub_label': 'Peter F. Martin', 'sub_w': 'None', 'template': '[X] (born [Y]).', 'template_negated': '[X] (not born [Y]).', 'uuid': '18af2dac-21d3-4c42-aff5-c247f245e203'}
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
* template: A pattern of text for extracting the relationship, object and subject of the form "[X] some text [Y]", where [X] and [Y] are the subject and object slots respectively. template may be missing and replaced with an empty string.
* template_negated: Same as above, except the [Y] is not the object. template_negated may be missing and replaced with empty strings.
* label: the label for the relationship/predicate. label may be missing and replaced with an empty string.
* description': a description of the relationship/predicate. description may be missing and replaced with an empty string.
* type: a type id for the relationship/predicate. type may be missing and replaced with an empty string.

The conceptnet config has the following fields:
* uuid: the id
* sub: the subject. subj may be missing and replaced with an empty string.
* obj: the object to be predicted. obj may be missing and replaced with an empty string.
* pred: the predicate/relationship
* obj_label: the object label
* masked_sentence: The masked sentence used to probe, with the object word replaced with [MASK]
* negated: same as above, except [MASK] is replaced by something that is not the object word. negated may be missing and replaced with empty strings.


The squad config has the following fields:
* id: the id
* sub_label: the subject label
* obj_label: the object label that is being predicted
* masked_sentence: The masked sentence used to probe, with the object word replaced with [MASK]
* negated: same as above, except [MASK] is replaced by something that is not the object word. negated may be missing and replaced with empty strings.


The google_re config has the following fields:

* uuid: the id
* pred: the predicate
* sub: the subject. subj may be missing and replaced with an empty string.
* obj: the object. obj may be missing and replaced with an empty string.
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

[More Information Needed]

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


### Contributions

Thanks to [@ontocord](https://github.com/ontocord) for adding this dataset.