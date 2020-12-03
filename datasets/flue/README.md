---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- crowdsourced
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
- text-classification
task_ids:
- PAWS-X:
  - intent-classification
- XNLI:
  - semantic-similarity-classification
- CLS:
  - sentiment-classification
- WSD-V:
  - text-classification-other-Word Sense Disambiguation for Verbs
---

# Dataset Card for FLUE

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Text Classification (CLS)](#text-classification-(cls))
    - [Data Instances](#data-instances)
    - [Data Fields](#data-instances)
    - [Data Splits](#data-instances)
  - [Paraphrasing (PAWS-X)](#paraphrasing-(paws-x))
    - [Data Instances](#data-instances)
    - [Data Fields](#data-instances)
    - [Data Splits](#data-instances)
  - [Natural Language Inference (XNLI)](#natural-language-inference-(xnli))
    - [Data Instances](#data-instances)
    - [Data Fields](#data-instances)
    - [Data Splits](#data-instances)
  - [Word Sense Disambiguation for Verbs (WSD-V)](#word-sense-disambiguation-for-verbs-(wsd-v))
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

- **Homepage:** [homepage](https://github.com/getalp/Flaubert/tree/master/flue)
- **Repository:**[github](https://github.com/getalp/Flaubert/tree/master/flue)
- **Paper:**[paper](https://arxiv.org/abs/1912.05372)
- **Leaderboard:**[leaderboard](https://github.com/getalp/Flaubert/tree/master/flue/leaderboard)
- **Point of Contact:**[Hang Le](thi-phuong-hang.le@univ-grenoble-alpes.fr)

### Dataset Summary

FLUE is an evaluation setup for French NLP systems similar to the popular GLUE benchmark. The goal is to enable further reproducible experiments in the future and to share models and progress on the French language. The tasks and data are obtained from existing works, please refer to our Flaubert paper for a complete list of references.

### Supported Tasks and Leaderboards

The supported tasks are: Text Classification, Paraphrasing, Natural Language Inference, Constituency Parsing, Dependency Parsing, Verb Sense Disambiguation and Noun Sense Disambiguation

### Languages

The datasets are all in French.

## Dataset Structure

### Text Classification (CLS)

This is a binary classification task. It consists in classifying Amazon reviews for three product categories: books, DVD, and music. Each sample contains a review text and the associated rating from 1 to 5 stars. Reviews rated above 3 is labeled as positive, and those rated less than 3 is labeled as negative.

#### Data Instances

An instance looks like:

```
{
    'idx': 1,
    'label': 0,
    'text': 'Bilan plus que mitigé pour cet album fourre-tout qui mêle quelques bonnes idées (les parodies d\'oeuvres d\'art) et des scènetes qui ne font que faire écho paresseusement aux précédents albums. Uderzo n\'a pas pris de risque pour cet album, mais, au vu des précédents, on se dit que c\'est peut-être un moindre mal ... L\'album semble n\'avoir été fait que pour permettre à Uderzo de rappeler avec une insistance suspecte qu\'il est bien l\'un des créateurs d\'Astérix (comme lorsqu\'il se met en scène lui même dans la BD) et de traiter ses critiques d\' "imbéciles" dans une préface un rien aigrie signée "Astérix". Préface dans laquelle Uderzo feint de croire que ce qu\'on lui reproche est d\'avoir fait survivre Asterix à la disparition de Goscinny (reproche naturellement démenti par la fidélité des lecteurs - démonstration imparable !). On aurait tant aimé qu\'Uderzo accepte de s\'entourer d\'un scénariste compétent et respectueux de l\'esprit Goscinnien (cela doit se trouver !) et nous propose des albums plus ambitieux ...'
}
```

#### Data Fields

The dataset is composed of two fields:
- **text**: the field that represents the text to classify.
- **label**: the sentiment represented by the text, here **positive** or **negative**.

#### Data Splits

The train and test sets are balanced, including around 1k positive and 1k negative reviews for a total of 2k reviews in each dataset. We take the French portion to create the binary text classification task in FLUE and report the accuracy on the test set.

### Paraphrasing (PAWS-X)

The task consists in identifying whether the two sentences in a pair are semantically equivalent or not.

#### Data Instances

An instance looks like:

```
{
    'idx': 1,
    'label': 0,
    'sentence1': "À Paris, en octobre 1560, il rencontra secrètement l'ambassadeur d'Angleterre, Nicolas Throckmorton, lui demandant un passeport pour retourner en Angleterre en passant par l'Écosse.",
    'sentence2': "En octobre 1560, il rencontra secrètement l'ambassadeur d'Angleterre, Nicolas Throckmorton, à Paris, et lui demanda un passeport pour retourner en Écosse par l'Angleterre."
}
```

#### Data Fields

The dataset is compososed of three fields:
- **sentence1**: The first sentence of an example
- **sentence2**: The second sentence of an example
- **lalel**: **0** if the two sentences are not paraphrasing each other, **1** otherwise.

#### Data Splits

The train set includes 49.4k examples, the dev and test sets each comprises nearly 2k examples. We take the related datasets for French to perform the paraphrasing task and report the accuracy on the test set.

### Natural Language Inference (XNLI)

The Natural Language Inference (NLI) task, also known as recognizing textual entailment (RTE), is to determine whether a premise entails, contradicts or neither entails nor contradicts a hypothesis. We take the French part of the XNLI corpus to form the development and test sets for the NLI task in FLUE.

#### Data Instances

An instance looks like:

```
{
    'idx': 1,
    'label': 2,
    'hypo': 'Le produit et la géographie sont ce qui fait travailler la crème de la crème .',
    'premise': "L' écrémage conceptuel de la crème a deux dimensions fondamentales : le produit et la géographie ."
}
```

#### Data Fields

The dataset is composed of three fields:
- **premise**: Premise sentence.
- **hypo**: Hypothesis sentence.
- **label**: **contradiction** if the two sentences are contradictory, **entailment** if the two sentences entails, **neutral** if they neither entails or contradict each other.

#### Data Splits

The train set includes 392.7k examples, the dev and test sets comprises 2.5k and 5k examples respectively. We take the related datasets for French to perform the NLI task and report the accuracy on the test set.

### Word Sense Disambiguation for Verbs (WSD-V)

The FrenchSemEval (FSE) dataset aims to evaluate the Word Sense Disambiguation for Verbs task for the French language. Extracted from Wiktionary.

#### Data Instances

An instance looks like:

```
{
    'idx': 'd000.s001',
    'sentence': ['"', 'Ce', 'ne', 'fut', 'pas', 'une', 'révolution', '2.0', ',', 'ce', 'fut', 'une', 'révolution', 'de', 'rue', '.'],
    'fine_pos_tags': [27, 26, 18, 13, 18, 0, 6, 22, 27, 26, 13, 0, 6, 4, 6, 27],
    'lemmas': ['"', 'ce', 'ne', 'être', 'pas', 'un', 'révolution', '2.0', ',', 'ce', 'être', 'un', 'révolution', 'de', 'rue', '.'],
    'pos_tags': [13, 11, 14, 0, 14, 9, 15, 4, 13, 11, 0, 9, 15, 7, 15, 13],
    'disambiguate_labels': ['__ws_1_2.0__adj__1'],
    'disambiguate_tokens_ids': [7],
}
```

#### Data Fields

The dataset is composed of six fields:
- **sentence**: The sentence to process split in tokens.
- **pos_tags**: The corresponding POS tags for each tokens.
- **lemmas**: The corresponding lemma for each tokens.
- **fine_pos_tags**: Fined (more specific) POS tags for each tokens.
- **disambiguate_tokens_ids**: The ID of the token in the sentence to disambiguate.
- **disambiguate_labels**: The label in the form of **sentenceID __ws_sentence-number_token__pos__number-of-time-the-token-appeared-across-all-the-sentences** (i.e. **d000.s404.t000 __ws_2_agir__verb__1**). 

#### Data Splits

The train set includes 269821 examples, the test set includes 3121 examples.

## Considerations for Using the Data

### Social Impact of Dataset

The goal is to enable further reproducible experiments in the future and to share models and progress on the French language.

## Additional Information

### Licensing Information

The licenses are:
- The licensing status of the data, especially the news source text, is unknown for CLS
- *The dataset may be freely used for any purpose, although acknowledgement of Google LLC ("Google") as the data source would be appreciated. The dataset is provided "AS IS" without any warranty, express or implied. Google disclaims all liability for any damages, direct or indirect, resulting from the use of the dataset.* for PAWS-X
- CC BY-NC 4.0 for XNLI
- The licensing status of the data, especially the news source text, is unknown for Verb Sense Disambiguation 

### Citation Information

```
@misc{le2019flaubert,
    title={FlauBERT: Unsupervised Language Model Pre-training for French},
    author={Hang Le and Loïc Vial and Jibril Frej and Vincent Segonne and Maximin Coavoux and Benjamin Lecouteux and Alexandre Allauzen and Benoît Crabbé and Laurent Besacier and Didier Schwab},
    year={2019},
    eprint={1912.05372},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```