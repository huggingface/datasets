---
annotations_creators:
- expert-generated
language:
- en
language_creators:
- expert-generated
license:
- unknown
multilinguality:
- monolingual
pretty_name: Text Retrieval Conference Question Answering
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
paperswithcode_id: trecqa
---

# Dataset Card for "trec"

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

- **Homepage:** [https://cogcomp.seas.upenn.edu/Data/QA/QC/](https://cogcomp.seas.upenn.edu/Data/QA/QC/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.34 MB
- **Size of the generated dataset:** 0.39 MB
- **Total amount of disk used:** 0.74 MB

### Dataset Summary

The Text REtrieval Conference (TREC) Question Classification dataset contains 5500 labeled questions in training set and another 500 for test set.

The dataset has 6 coarse class labels and 50 fine class labels. Average length of each sentence is 10, vocabulary size of 8700.

Data are collected from four sources: 4,500 English questions published by USC (Hovy et al., 2001), about 500 manually constructed questions for a few rare classes, 894 TREC 8 and TREC 9 questions, and also 500 questions from TREC 10 which serves as the test set. These questions were manually labeled.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

The language in this dataset is English (`en`).

## Dataset Structure

### Data Instances

- **Size of downloaded dataset files:** 0.34 MB
- **Size of the generated dataset:** 0.39 MB
- **Total amount of disk used:** 0.74 MB

An example of 'train' looks as follows.
```
{
  'text': 'How did serfdom develop in and then leave Russia ?',
  'coarse_label': 2,
  'fine_label': 26
}
```

### Data Fields

The data fields are the same among all splits.

- `text` (`str`): Text of the question.
- `coarse_label` (`ClassLabel`): Coarse class label. Possible values are:
  - 'ABBR' (0): Abbreviation.
  - 'ENTY' (1): Entity.
  - 'DESC' (2): Description and abstract concept.
  - 'HUM' (3): Human being.
  - 'LOC' (4): Location.
  - 'NUM' (5): Numeric value.
- `fine_label` (`ClassLabel`): Fine class label. Possible values are:
  - ABBREVIATION:
    - 'ABBR:abb' (0): Abbreviation.
    - 'ABBR:exp' (1): Expression abbreviated.
  - ENTITY:
    - 'ENTY:animal' (2): Animal.
    - 'ENTY:body' (3): Organ of body.
    - 'ENTY:color' (4): Color.
    - 'ENTY:cremat' (5): Invention, book and other creative piece.
    - 'ENTY:currency' (6): Currency name.
    - 'ENTY:dismed' (7): Disease and medicine.
    - 'ENTY:event' (8): Event.
    - 'ENTY:food' (9): Food.
    - 'ENTY:instru' (10): Musical instrument.
    - 'ENTY:lang' (11): Language.
    - 'ENTY:letter' (12): Letter like a-z.
    - 'ENTY:other' (13): Other entity.
    - 'ENTY:plant' (14): Plant.
    - 'ENTY:product' (15): Product.
    - 'ENTY:religion' (16): Religion.
    - 'ENTY:sport' (17): Sport.
    - 'ENTY:substance' (18): Element and substance.
    - 'ENTY:symbol' (19): Symbols and sign.
    - 'ENTY:techmeth' (20): Techniques and method.
    - 'ENTY:termeq' (21): Equivalent term.
    - 'ENTY:veh' (22): Vehicle.
    - 'ENTY:word' (23): Word with a special property.
  - DESCRIPTION:
    - 'DESC:def' (24): Definition of something.
    - 'DESC:desc' (25): Description of something.
    - 'DESC:manner' (26): Manner of an action.
    - 'DESC:reason' (27): Reason.
  - HUMAN:
    - 'HUM:gr' (28): Group or organization of persons
    - 'HUM:ind' (29): Individual.
    - 'HUM:title' (30): Title of a person.
    - 'HUM:desc' (31): Description of a person.
  - LOCATION:
    - 'LOC:city' (32): City.
    - 'LOC:country' (33): Country.
    - 'LOC:mount' (34): Mountain.
    - 'LOC:other' (35): Other location.
    - 'LOC:state' (36): State.
  - NUMERIC:
    - 'NUM:code' (37): Postcode or other code.
    - 'NUM:count' (38): Number of something.
    - 'NUM:date' (39): Date.
    - 'NUM:dist' (40): Distance, linear measure.
    - 'NUM:money' (41): Price.
    - 'NUM:ord' (42): Order, rank.
    - 'NUM:other' (43): Other number.
    - 'NUM:period' (44): Lasting time of something
    - 'NUM:perc' (45): Percent, fraction.
    - 'NUM:speed' (46): Speed.
    - 'NUM:temp' (47): Temperature.
    - 'NUM:volsize' (48): Size, area and volume.
    - 'NUM:weight' (49): Weight.


### Data Splits

| name    | train | test |
|---------|------:|-----:|
| default |  5452 |  500 |

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@inproceedings{li-roth-2002-learning,
    title = "Learning Question Classifiers",
    author = "Li, Xin  and
      Roth, Dan",
    booktitle = "{COLING} 2002: The 19th International Conference on Computational Linguistics",
    year = "2002",
    url = "https://www.aclweb.org/anthology/C02-1150",
}
@inproceedings{hovy-etal-2001-toward,
    title = "Toward Semantics-Based Answer Pinpointing",
    author = "Hovy, Eduard  and
      Gerber, Laurie  and
      Hermjakob, Ulf  and
      Lin, Chin-Yew  and
      Ravichandran, Deepak",
    booktitle = "Proceedings of the First International Conference on Human Language Technology Research",
    year = "2001",
    url = "https://www.aclweb.org/anthology/H01-1069",
}
```


### Contributions

Thanks to [@lhoestq](https://github.com/lhoestq), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
