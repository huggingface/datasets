---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-meaning-representtion-to-text
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

- **Homepage:** [homepage](http://www.macs.hw.ac.uk/InteractionLab/E2E/)
- **Repository:** [repository](https://github.com/tuetschek/e2e-dataset/)
- **Paper:** [paper](https://arxiv.org/abs/1706.09254)
- **Leaderboard:** [leaderboard](http://www.macs.hw.ac.uk/InteractionLab/E2E/)


### Dataset Summary

The E2E dataset is used for training end-to-end, data-driven natural language generation systems in the restaurant domain, which is ten times bigger than existing, frequently used datasets in this area.
The E2E dataset poses new challenges:
(1) its human reference texts show more lexical richness and syntactic variation, including discourse phenomena;
(2) generating from this set requires content selection. As such, learning from this dataset promises more natural, varied and less template-like system utterances.

E2E is released in the following paper where you can find more details and baseline results:
https://arxiv.org/abs/1706.09254

### Supported Tasks and Leaderboards

- `conditional-text-generation-other-meaning-representtion-to-text`: The dataset can be used to train a model to generate descriptions in the restaurant domain from meaning representations, which consists in taking as input some data about a restaurant and generate a sentence in natural language that presents the different aspects of the data about the restaurant.. Success on this task is typically measured by achieving a *high* [BLEU](https://huggingface.co/metrics/bleu), [NIST](https://huggingface.co/metrics/nist), [METEOR](https://huggingface.co/metrics/meteor), [Rouge-L](https://huggingface.co/metrics/rouge), [CIDEr](https://huggingface.co/metrics/cider). The TGen model (Dusek and Jurcıcek, 2016a) was used a baseline, had the following scores:

|          | BLEU	  | NIST   | METEOR | ROUGE_L | CIDEr  |
| -------- | ------ | ------ | ------ | ------- | ------ |
| BASELINE | 0.6593 |	8.6094 | 0.4483 | 0.6850  | 2.2338 |


This task has an inactive leaderboard which can be found [here](http://www.macs.hw.ac.uk/InteractionLab/E2E/) and ranks models based on the metrics above.

### Languages

The dataset is in english (en).

## Dataset Structure

### Data Instances

Example of one instance:

```
{'human_reference': 'The Vaults pub near Café Adriatic has a 5 star rating.  Prices start at £30.',
 'meaning_representation': 'name[The Vaults], eatType[pub], priceRange[more than £30], customer rating[5 out of 5], near[Café Adriatic]'}
```


### Data Fields

- `human_reference`: string, the text is natural language that describes the different characteristics in the meaning representation
- `meaning_representation`: list of slots and values to generate a description from

Each MR consists of 3–8 attributes (slots), such as name, food or area, and their values.

### Data Splits

The dataset is split into training, validation and testing sets (in a 76.5-8.5-15 ratio), keeping a similar distribution of MR and reference text lengths and ensuring that MRs in different sets are distinct.

|                            | Tain   | Valid | Test |
| -----                      | ------ | ----- | ---- |
| N. Instances               | 42061  | 4672  | 4693 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

The data was collected using the CrowdFlower platform and quality-controlled following Novikova et al. (2016).

#### Who are the source language producers?

[More Information Needed]

### Annotations

Following Novikova et al. (2016), the E2E data was collected using pictures as stimuli, which was shown to elicit significantly more natural, more informative, and better phrased human references than textual MRs.

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

[More Information Needed]

### Citation Information

```
@article{dusek.etal2020:csl,
  title = {Evaluating the {{State}}-of-the-{{Art}} of {{End}}-to-{{End Natural Language Generation}}: {{The E2E NLG Challenge}}},
  author = {Du{\v{s}}ek, Ond\v{r}ej and Novikova, Jekaterina and Rieser, Verena},
  year = {2020},
  month = jan,
  volume = {59},
  pages = {123--156},
  doi = {10.1016/j.csl.2019.06.009},
  archivePrefix = {arXiv},
  eprint = {1901.11528},
  eprinttype = {arxiv},
  journal = {Computer Speech \& Language}
```
