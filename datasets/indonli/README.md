---
pretty_name: IndoNLI
annotations_creators:
- expert-generated
- crowdsourced
language_creators:
- expert-generated
language:
- id
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- natural-language-inference
paperswithcode_id: indonli
---

# Dataset Card for IndoNLI

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

- **Repository:** [GitHub](https://github.com/ir-nlp-csui/indonli)
- **Paper:** [EMNLP 2021](https://aclanthology.org/2021.emnlp-main.821/)
- **Point of Contact:** [GitHub](https://github.com/ir-nlp-csui/indonli)

### Dataset Summary

IndoNLI is the first human-elicited Natural Language Inference (NLI) dataset for Indonesian. 
IndoNLI is annotated by both crowd workers and experts. The expert-annotated data is used exclusively as a test set. It is designed to provide a challenging test-bed for Indonesian NLI by explicitly incorporating various linguistic phenomena such as numerical reasoning, structural changes, idioms, or temporal and spatial reasoning.

### Supported Tasks and Leaderboards

- Natural Language Inference for Indonesian

### Languages

Indonesian

## Dataset Structure

### Data Instances

An example of `train` looks as follows.

```
{
  "premise": "Keindahan alam yang terdapat di Gunung Batu Jonggol ini dapat Anda manfaatkan sebagai objek fotografi yang cantik.", 
  "hypothesis": "Keindahan alam tidak dapat difoto.", 
  "label": 2
}
```
### Data Fields

The data fields are:
- `premise`: a `string` feature
- `hypothesis`: a `string` feature
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

### Data Splits

The data is split across `train`, `valid`, `test_lay`, and `test_expert`. 

`test_expert` is written by expert annotators, whereas the rest are written by lay annotators.

|   split   | # examples |
|----------|-------:|
|train|   10330|
|valid|   2197|
|test_lay|   2201|
|test_expert|   2984|

A small subset of `test_expert` is used as a diasnostic tool. For more info, please visit https://github.com/ir-nlp-csui/indonli



## Dataset Creation

### Curation Rationale

Indonesian NLP is considered under-resourced. Up until now, there is no publicly available human-annotated NLI dataset for Indonesian.

### Source Data

#### Initial Data Collection and Normalization

The premise were collected from Indonesian Wikipedia and from other public Indonesian dataset: Indonesian PUD and GSD treebanks provided by the [Universal Dependencies 2.5](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3105) and [IndoSum](https://github.com/kata-ai/indosum)

The hypothesis were written by annotators.

#### Who are the source language producers?

The data was produced by humans.

### Annotations

#### Annotation process

We start by writing the hypothesis, given the premise and the target label. Then, we ask 2 different independent annotators to predict the label, given the premise and hypothesis. If all 3 (the original hypothesis + 2 independent annotators) agree with the label, then the annotation process ends for that sample. Otherwise, we incrementally ask additional annotator until  3 annotators agree with the label. If there's no majority concensus after 5 annotations, the sample is removed.

#### Who are the annotators?

Lay annotators were computer science students, and expert annotators were NLP scientists with 7+ years research experience in NLP. All annotators are native speakers.
Additionally, expert annotators were explicitly instructed to provide challenging examples by incorporating various linguistic phenomena such as numerical reasoning, structural changes, idioms, or temporal and spatial reasoning. Annotators were compensated based on hourly rate.

### Personal and Sensitive Information

There might be some personal information coming from Wikipedia and news, especially the information of famous/important people.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

INDONLI is created using premise sentences taken from Wikipedia and news. These data sources may contain some bias.

### Other Known Limitations

No other known limitations

## Additional Information

### Dataset Curators

This dataset is the result of the collaborative work of Indonesian researchers from the University of Indonesia, kata.ai, New York University, Fondazione Bruno Kessler, and the University of St Andrews.


### Licensing Information

CC-BY-SA 4.0.

Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

Please contact authors for any information on the dataset.

### Citation Information

```
@inproceedings{mahendra-etal-2021-indonli,
    title = "{I}ndo{NLI}: A Natural Language Inference Dataset for {I}ndonesian",
    author = "Mahendra, Rahmad and Aji, Alham Fikri and Louvan, Samuel and Rahman, Fahrurrozi and Vania, Clara",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.821",
    pages = "10511--10527",
}
```

### Contributions

Thanks to [@afaji](https://github.com/afaji) for adding this dataset.
