---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- xh
licenses:
- other-Creative Commons Attribution 2.5 South Africa License
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
---

# Dataset Card for [Dataset Name]

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

- **Homepage:**  [IsiXhosa Ner Corpus Homepage](https://repo.sadilar.org/handle/20.500.12185/312)
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [Martin Puttkammer](mailto:Martin.Puttkammer@nwu.ac.za)


### Dataset Summary

The isiXhosa Ner Corpus is a Xhosa dataset developed by [The Centre for Text Technology (CTexT), North-West University, South Africa](http://humanities.nwu.ac.za/ctext). The data is based on documents from the South African goverment domain and crawled from gov.za websites. It was created to support NER task for Xhosa language. The dataset uses CoNLL shared task annotation standards.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language supported is Xhosa.

## Dataset Structure

### Data Instances

A data point consists of sentences seperated by empty line and tab-seperated tokens and tags. 
{'id': '0',
 'ner_tags': [7, 8, 5, 6, 0],
 'tokens': ['Injongo', 'ye-website', 'yaseMzantsi', 'Afrika', 'kukuvelisa']
}

### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

The NER tags correspond to this list:
```
"OUT", "B-PERS", "I-PERS", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC",
```
The NER tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any non-initial word. There are four types of phrases: person names (PER), organizations (ORG), locations (LOC) and miscellaneous names (MISC). (OUT) is used for tokens not considered part of any named entity.

### Data Splits

The data was not split.

## Dataset Creation

### Curation Rationale

The data was created to help introduce resources to new language - Xhosa.

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The data is based on South African government domain and was crawled from gov.za websites.

[More Information Needed]
#### Who are the source language producers?

The data was produced by writers of South African government websites - gov.za

[More Information Needed]
### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

The data was annotated during the NCHLT text resource development project.

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

The annotated data sets were developed by the Centre for Text Technology (CTexT, North-West University, South Africa).

See: [more information](http://www.nwu.ac.za/ctext)

### Licensing Information

The data is under the [Creative Commons Attribution 2.5 South Africa License](http://creativecommons.org/licenses/by/2.5/za/legalcode)

### Citation Information

```
@inproceedings{isixhosa_ner_corpus,
  author    = {	K. Podile and
              Roald Eiselen},
  title     = {NCHLT isiXhosa Named Entity Annotated Corpus},
  booktitle = {Eiselen, R. 2016. Government domain named entity recognition for South African languages. Proceedings of the 10th      Language Resource and Evaluation Conference, Portorož, Slovenia.},
  year      = {2016},
  url       = {https://repo.sadilar.org/handle/20.500.12185/312},
}
```
