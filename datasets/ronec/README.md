---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
- found
languages:
- ro
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: ronec
pretty_name: RONEC
---

# Dataset Card for RONEC

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

- **Homepage:** https://github.com/dumitrescustefan/ronec
- **Repository:** https://github.com/dumitrescustefan/ronec
- **Paper:** https://arxiv.org/abs/1909.01247
- **Leaderboard:** https://lirobenchmark.github.io/
- **Point of Contact:** [Stefan](dumitrescu.stefan@gmail.com) and [Andrei-Marius](avram.andreimarius@gmail.com)

### Dataset Summary

RONEC, at version 2.0, holds 12330 sentences with over 0.5M tokens, annotated with 15 classes, to a total of 80.283 distinctly annotated entities.

The corpus has the following classes and distribution in the train/valid/test splits:

| Classes      	| Total  	    | Train  	|         	| Valid  	|         	| Test   	|         	|
|-------------	|:------:	    |:------:	|:-------:	|:------:	|:-------:	|:------:	|:-------:	|
|            	| #     	    | #     	| %     	| # 	    | % 	    | #     	| %     	|
| PERSON      	|  **26130** 	| 19167  	|  73.35  	|  2733  	|  10.46  	|  4230  	|  16.19  	|
| GPE         	|  **11103** 	|  8193  	|  73.79  	|  1182  	|  10.65  	|  1728  	|   15.56 	|
| LOC         	|  **2467**  	|  1824  	|  73.94  	|  270   	|  10.94  	|  373   	|  15.12  	|
| ORG         	|  **7880**  	|  5688  	|  72.18  	|   880  	|  11.17  	|  1312  	|  16.65  	|
| LANGUAGE    	|   **467**  	|   342  	|  73.23  	|   52   	|  11.13  	|   73   	|  15.63  	|
| NAT_REL_POL 	|  **4970**  	|  3673  	|  73.90  	|   516  	|  10.38  	|   781  	|  15.71  	|
| DATETIME    	|  **9614**  	|  6960  	|  72.39  	|  1029  	|   10.7  	|  1625  	|   16.9  	|
| PERIOD      	|  **1188**  	|   862  	|  72.56  	|   129  	|  10.86  	|   197  	|  16.58  	|
| QUANTITY    	|  **1588**  	|  1161  	|  73.11  	|   181  	|   11.4  	|   246  	|  15.49  	|
| MONEY       	|  **1424**  	|  1041  	|  73.10  	|   159  	|  11.17  	|   224  	|  15.73  	|
| NUMERIC     	|  **7735**  	|  5734  	|  74.13  	|   814  	|  10.52  	|  1187  	|  15.35  	|
| ORDINAL     	|  **1893**  	|  1377  	|   72.74 	|   212  	|   11.2  	|   304  	|  16.06  	|
| FACILITY    	|  **1126**  	|   840  	|   74.6  	|   113  	|  10.04  	|   173  	|  15.36  	|
| WORK_OF_ART 	|  **1596**  	|  1157  	|  72.49  	|   176  	|  11.03  	|   263  	|  16.48  	|
| EVENT       	|  **1102**  	|   826  	|  74.95  	|   107  	|   9.71  	|   169  	|  15.34  	|


### Supported Tasks and Leaderboards

The corpus is meant to train Named Entity Recognition models for the Romanian language. 

Please see the leaderboard here : [https://lirobenchmark.github.io/](https://lirobenchmark.github.io/) 

### Languages

RONEC is in Romanian (`ro`)

## Dataset Structure

### Data Instances

The dataset is a list of instances. For example, an instance looks like:

```json
{
  "id": 10454,
  "tokens": ["Pentru", "a", "vizita", "locația", "care", "va", "fi", "pusă", "la", "dispoziția", "reprezentanților", "consiliilor", "județene", ",", "o", "delegație", "a", "U.N.C.J.R.", ",", "din", "care", "a", "făcut", "parte", "și", "dl", "Constantin", "Ostaficiuc", ",", "președintele", "C.J.T.", ",", "a", "fost", "prezentă", "la", "Bruxelles", ",", "între", "1-3", "martie", "."], 
  "ner_tags": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-PERSON", "O", "O", "O", "O", "O", "O", "B-ORG", "O", "O", "O", "O", "O", "O", "O", "B-PERSON", "I-PERSON", "I-PERSON", "I-PERSON", "I-PERSON", "B-ORG", "O", "O", "O", "O", "O", "B-GPE", "O", "B-PERIOD", "I-PERIOD", "I-PERIOD", "O"], 
  "ner_ids": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 5, 0, 19, 20, 20, 0], 
  "space_after": [true, true, true, true, true, true, true, true, true, true, true, true, false, true, true, true, true, false, true, true, true, true, true, true, true, true, true, false, true, true, false, true, true, true, true, true, false, true, true, true, false, false]
}
```

### Data Fields

The fields of each examples are:

- ``tokens`` are the words of the sentence.
- ``ner_tags`` are the string tags assigned to each token, following the BIO2 format. For example, the span ``"între", "1-3", "martie"`` has three tokens, but is a single class ``PERIOD``, marked as ``"B-PERIOD", "I-PERIOD", "I-PERIOD"``. 
- ``ner_ids`` are the integer encoding of each tag, to be compatible with the standard and to be quickly used for model training. Note that each ``B``-starting tag is odd, and each ``I``-starting tag is even.
- ``space_after`` is used to help if there is a need to detokenize the dataset. A ``true`` value means that there is a space after the token on that respective position. 

### Data Splits

The dataset is split in train: 9000 sentences, dev: 1330 sentence and test: 2000 sentences. 

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

*The corpus data source represents sentences that are free of copyright, taken from older datasets like the freely available SEETimes and more recent datasources like the Romanian Wikipedia or the Common Crawl.*

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

The corpus was annotated with the following classes: 

1. PERSON - proper nouns, including common nouns or pronouns if they refer to a person. (e.g. 'sister') 
2. GPE - geo political entity, like a city or a country; has to have a governance form
3. LOC - location, like a sea, continent, region, road, address, etc.
4. ORG - organization
5. LANGUAGE - language (e.g. Romanian, French, etc.)
6. NAT_REL_POL - national, religious or political organizations
7. DATETIME - a time and date in any format, including references to time (e.g. 'yesterday')
8. PERIOD - a period that is precisely bounded by two date times
9. QUANTITY - a quantity that is not numerical; it has a unit of measure 
10. MONEY - a monetary value, numeric or otherwise
11. NUMERIC - a simple numeric value, represented as digits or words
12. ORDINAL - an ordinal value like 'first', 'third', etc.
13. FACILITY - a named place that is easily recognizable 
14. WORK_OF_ART - a work of art like a named TV show, painting, etc.
15. EVENT - a named recognizable or periodic major event 

#### Annotation process

The corpus was annotated by 3 language experts, and was cross-checked for annotation consistency. The annotation took several months to complete, but the result is a high quality dataset.  

#### Who are the annotators?

Stefan Dumitrescu (lead). 

### Personal and Sensitive Information

All the source data is already freely downloadable and usable online, so there are no privacy concerns. 

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

MIT License

### Citation Information

```bibtex
@article{dumitrescu2019introducing,
  title={Introducing RONEC--the Romanian Named Entity Corpus},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei-Marius},
  journal={arXiv preprint arXiv:1909.01247},
  year={2019}
}
```

### Contributions

Thanks to [@iliemihai](https://github.com/iliemihai) for adding v1.0 of the dataset.
