---
annotations_creators:
- no-annotation
language_creators:
- wikipedia
languages:
- fr
licenses:
- CC BY-NC-SA 3.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- closed-domain-qa
---

# Dataset Card for FQuAD

## Table of Contents
- [Tasks Supported](#tasks-supported)
- [Purpose](#purpose)
- [Languages](#languages)
- [People Involved](#who-iswas-involved-in-the-dataset-use-and-creation)
- [Data Characteristics](#data-characteristics)
- [Dataset Structure](#dataset-structure)
- [Known Limitations](#known-limitations)
- [Licensing information](#licensing-information)

## Tasks supported:
### Task categorization / tags

SQuAD-like question answering in French.

## Purpose

Developped to provide a SQuAD equivalent in the French language. Questions are original and based on high quality Wikipedia articles.

## Languages 
### Per language:

The BCP-47 code for French is fr.

## Who is/was involved in the dataset use and creation?
### Who are the dataset curators?

The FQuAD dataset was created by Illuin technology. 

### Who are the language producers (who wrote the text / created the base content)?

The text used for the contexts are from the curated list of French High-Quality Wikipedia [articles](https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Article_de_qualit%C3%A9).

### Who are the annotators?

Annotations (spans and questions) are written by students of the CentraleSupélec school of engineering.

## Data characteristics

The texts are movie reviews written by members of the [Allociné.fr](https://www.allocine.fr/) community for various films. The reviews were written between 2006 and 2020. Further information on the kinds of films included in the dataset has not been documented.

### How was the data collected?

Wikipedia articles were scraped and Illuin used an internally-developped tool to help annotators ask questions and indicate the answer spans.

### Normalization information

Format is similar to SQuAD. Question type are further described in the FQuAD publication [publication](https://arxiv.org/abs/2002.06071).

### Annotation process

Annotators were given paragraph sized contexts and asked to generate 4/5 non-trivial questions about information in the context.

## Dataset Structure
### Splits, features, and labels

The FQuAD dataset has 3 splits: _train_, _validation_, and _test_. The _test_ split is however not released publicly at the moment. The splits contain disjoint sets of articles. The following table contains stats about each split. 
Dataset Split | Number of Articles in Split | Number of paragraphs in split | Number of questions in split
--------------|------------------------------|--------------------------|-------------------------
Train | 117 | 4921 | 20731
Validation | 768 | 51.0% | 3188
Test | 10 | 532 | 2189


### Structure

FQuAD has the same structure as the SQuAD dataset. 

### Suggested metrics / models:

[camembert-large-fquad](https://huggingface.co/illuin/camembert-large-fquad) achieves 91.5 F1 and 82.0 % exact match accuracy on the test set.

## Known Limitations
### Known social biases

The social biases of this dataset have not yet been investigated.

### Other known limitations

The limitations of the FQuAD dataset have not yet been investigated.

## Licensing information

The FQuAD dataset is licensed under the [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/fr/) license.

