---
annotations_creators:
- found
language_creators:
- found
languages:
- fr
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
---

# Dataset Card for OrangeSum

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

- **Repository:** [OrangeSum repository](https://github.com/Tixierae/OrangeSum)
- **Paper:** [BARThez: a Skilled Pretrained French Sequence-to-Sequence Model](https://arxiv.org/abs/2010.12321)	
- **Point of Contact:** [Antoine J.-P. Tixier](Antoine.Tixier-1@colorado.edu)

### Dataset Summary

The OrangeSum dataset was inspired by the XSum dataset. It was created by scraping the "Orange Actu" website: https://actu.orange.fr/. Orange S.A. is a large French multinational telecommunications corporation, with 266M customers worldwide. Scraped pages cover almost a decade from Feb 2011 to Sep 2020. They belong to five main categories: France, world, politics, automotive, and society. The society category is itself divided into 8 subcategories: health, environment, people, culture, media, high-tech, unsual ("insolite" in French), and miscellaneous.

Each article featured a single-sentence title as well as a very brief abstract, both professionally written by the author of the article. These two fields were extracted from each page, thus creating two summarization tasks: OrangeSum Title and OrangeSum Abstract.

### Supported Tasks and Leaderboards

**Tasks:** OrangeSum Title and OrangeSum Abstract.

To this day, there is no Leaderboard for this dataset.

### Languages

The text in the dataset is in French.

## Dataset Structure

### Data Instances

A data instance consists of a news article  and a summary. The summary can be a short abstract or a title depending on the configuration.

Example:

**Document:** Le temps sera pluvieux sur huit départements de la France ces prochaines heures : outre les trois départements bretons placés en vigilance orange jeudi matin, cinq autres départements du sud du Massif Central ont été à leur tour placés en alerte orange pluie et inondation. Il s'agit de l'Aveyron, du Cantal, du Gard, de la Lozère, et de la Haute-Loire. Sur l'ensemble de l'épisode, les cumuls de pluies attendus en Bretagne sont compris entre 40 et 60 mm en 24 heures et peuvent atteindre localement les 70 mm en 24 heures.Par la suite, la dégradation qui va se mettre en place cette nuit sur le Languedoc et le sud du Massif Central va donner sur l'Aveyron une première salve intense de pluie. Des cumuls entre 70 et 100 mm voir 120 mm localement sont attendus sur une durée de 24 heures. Sur le relief des Cévennes on attend de 150 à 200 mm, voire 250 mm très ponctuellement sur l'ouest du Gard et l'est de la Lozère. Cet épisode va s'estomper dans la soirée avec le décalage des orages vers les régions plus au nord. Un aspect orageux se mêlera à ces précipitations, avec de la grêle possible, des rafales de vent et une forte activité électrique.

**Abstract:** Outre les trois départements bretons, cinq autres départements du centre de la France ont été placés en vigilance orange pluie-inondation.

**Title:** Pluie-inondations : 8 départements en alerte orange.

### Data Fields

`text`: the document to be summarized. \
`summary`: the summary of the source document.

### Data Splits

The data is split into a training, validation and test in both configuration.

|          | Tain   | Valid | Test |
| -----    | ------ | ----- | ---- |
| Abstract | 21400  |  1500 | 1500 |
| Title    | 30658  |  1500 | 1500 |

## Dataset Creation

### Curation Rationale

The goal here was to create a French equivalent of the recently introduced [XSum](https://github.com/EdinburghNLP/XSum/tree/master/XSum-Dataset) dataset. Unlike the historical summarization datasets, CNN, DailyMail, and NY Times, which favor extractive strategies, XSum, as well as OrangeSum require the models to display a high degree of abstractivity to perform well. The summaries in OrangeSum are not catchy headlines, but rather capture the gist of the articles.

### Source Data

#### Initial Data Collection and Normalization

Each article features a single-sentence title as well as a very brief abstract. Extracting these two fields from each news article page, creates two summarization tasks: OrangeSum Title and OrangeSum Abstract. As a post-processing step, all empty articles and those whose summaries were shorter than 5 words were removed. For OrangeSum Abstract, the top 10% articles in terms of proportion of novel unigrams in the abstracts were removed, as it was observed that such abstracts tend to be introductions rather than real abstracts. This corresponded to a threshold of 57% novel unigrams. For both OrangeSum Title and OrangeSum Abstract, 1500 pairs for testing and 1500 for validation are set aside, and all the remaining ones are used for training.

#### Who are the source language producers?

The authors of the artiles.

### Annotations

#### Annotation process

The smmaries are professionally written by the author of the articles.

#### Who are the annotators?

The authors of the artiles.

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

The dataset was initially created by Antoine J.-P. Tixier.

### Licensing Information

[More Information Needed]

### Citation Information

```
@article{eddine2020barthez,
  title={BARThez: a Skilled Pretrained French Sequence-to-Sequence Model},
  author={Eddine, Moussa Kamal and Tixier, Antoine J-P and Vazirgiannis, Michalis},
  journal={arXiv preprint arXiv:2010.12321},
  year={2020}
}
```
