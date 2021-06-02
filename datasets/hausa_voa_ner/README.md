---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- ha
licenses:
- cc-by-4.0
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
paperswithcode_id: null
---

# Dataset Card for Hausa VOA NER Corpus

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

- **Homepage:** https://www.aclweb.org/anthology/2020.emnlp-main.204/
- **Repository:** [Hausa VOA NER](https://github.com/uds-lsv/transfer-distant-transformer-african/tree/master/data/hausa_ner)
- **Paper:** https://www.aclweb.org/anthology/2020.emnlp-main.204/
- **Leaderboard:**
- **Point of Contact:** [David Adelani](mailto:didelani@lsv.uni-saarland.de)

### Dataset Summary
The Hausa VOA NER is a named entity recognition (NER) dataset for Hausa language based on the [VOA Hausa news](https://www.voahausa.com/) corpus. 
### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language supported is Hausa.

## Dataset Structure

### Data Instances

A data point consists of sentences seperated by empty line and tab-seperated tokens and tags. 
{'id': '0',
 'ner_tags': [B-PER, 0, 0, B-LOC, 0],
 'tokens': ['Trump', 'ya', 'ce', 'Rasha', 'ma']
}

### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

The NER tags correspond to this list:
```
"O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-DATE", "I-DATE",
```
The NER tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any non-initial word. There are four types of phrases: person names (PER), organizations (ORG), locations (LOC) and dates & times (DATE). (O) is used for tokens not considered part of any named entity.

### Data Splits

Training (1,014 sentences), validation (145 sentences) and test split (291 sentences)

## Dataset Creation

### Curation Rationale

The data was created to help introduce resources to new language - Hausa.

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The dataset is based on the news domain and was crawled from [VOA Hausa news](https://www.voahausa.com/).


[More Information Needed]

#### Who are the source language producers?

The dataset was collected from VOA Hausa news. Most of the texts used in creating the Hausa VOA NER are news stories from Nigeria, Niger Republic, United States, and other parts of the world.

[More Information Needed]

### Annotations
Named entity recognition annotation
#### Annotation process

[More Information Needed]

#### Who are the annotators?

The data was annotated by Jesujoba Alabi and David Adelani for the paper: 
[Transfer Learning and Distant Supervision for Multilingual Transformer Models: A Study on African Languages](https://www.aclweb.org/anthology/2020.emnlp-main.204/).

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

The annotated data sets were developed by students of Saarland University, Saarbrücken, Germany .


### Licensing Information

The data is under the [Creative Commons Attribution 4.0 ](https://creativecommons.org/licenses/by/4.0/)

### Citation Information
```
@inproceedings{hedderich-etal-2020-transfer,
    title = "Transfer Learning and Distant Supervision for Multilingual Transformer Models: A Study on {A}frican Languages",
    author = "Hedderich, Michael A.  and
      Adelani, David  and
      Zhu, Dawei  and
      Alabi, Jesujoba  and
      Markus, Udia  and
      Klakow, Dietrich",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.204",
    doi = "10.18653/v1/2020.emnlp-main.204",
    pages = "2580--2591",
}
```
### Contributions

Thanks to [@dadelani](https://github.com/dadelani) for adding this dataset.