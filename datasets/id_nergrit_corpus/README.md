---
pretty_name: Nergrit Corpus
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- id
license:
- other
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: nergrit-corpus
dataset_info:
- config_name: ner
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-CRD
          1: B-DAT
          2: B-EVT
          3: B-FAC
          4: B-GPE
          5: B-LAN
          6: B-LAW
          7: B-LOC
          8: B-MON
          9: B-NOR
          10: B-ORD
          11: B-ORG
          12: B-PER
          13: B-PRC
          14: B-PRD
          15: B-QTY
          16: B-REG
          17: B-TIM
          18: B-WOA
          19: I-CRD
          20: I-DAT
          21: I-EVT
          22: I-FAC
          23: I-GPE
          24: I-LAN
          25: I-LAW
          26: I-LOC
          27: I-MON
          28: I-NOR
          29: I-ORD
          30: I-ORG
          31: I-PER
          32: I-PRC
          33: I-PRD
          34: I-QTY
          35: I-REG
          36: I-TIM
          37: I-WOA
          38: O
  splits:
  - name: test
    num_bytes: 1135577
    num_examples: 2399
  - name: train
    num_bytes: 5428411
    num_examples: 12532
  - name: validation
    num_bytes: 1086437
    num_examples: 2521
  download_size: 14988232
  dataset_size: 7650425
- config_name: sentiment
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-NEG
          1: B-NET
          2: B-POS
          3: I-NEG
          4: I-NET
          5: I-POS
          6: O
  splits:
  - name: test
    num_bytes: 1097517
    num_examples: 2317
  - name: train
    num_bytes: 3167972
    num_examples: 7485
  - name: validation
    num_bytes: 337679
    num_examples: 782
  download_size: 14988232
  dataset_size: 4603168
- config_name: statement
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-BREL
          1: B-FREL
          2: B-STAT
          3: B-WHO
          4: I-BREL
          5: I-FREL
          6: I-STAT
          7: I-WHO
          8: O
  splits:
  - name: test
    num_bytes: 182553
    num_examples: 335
  - name: train
    num_bytes: 1469081
    num_examples: 2405
  - name: validation
    num_bytes: 105119
    num_examples: 176
  download_size: 14988232
  dataset_size: 1756753
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [PT Gria Inovasi Teknologi](https://grit.id/)
- **Repository:** [Nergrit Corpus](https://github.com/grit-id/nergrit-corpus)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [Taufiqur Rohman](mailto:taufiq@grit.id)

### Dataset Summary

Nergrit Corpus is a dataset collection of Indonesian Named Entity Recognition, Statement Extraction, 
and Sentiment Analysis developed by [PT Gria Inovasi Teknologi (GRIT)](https://grit.id/). 

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Indonesian

## Dataset Structure

A data point consists of sentences seperated by empty line and tab-seperated tokens and tags. 
```
{'id': '0',
 'tokens': ['Gubernur', 'Bank', 'Indonesia', 'menggelar', 'konferensi', 'pers'],
 'ner_tags': [9, 28, 28, 38, 38, 38],
}
```
### Data Instances

[More Information Needed]

### Data Fields
- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

#### Named Entity Recognition
The ner_tags correspond to this list:
```
"B-CRD", "B-DAT", "B-EVT", "B-FAC", "B-GPE", "B-LAN", "B-LAW", "B-LOC", "B-MON", "B-NOR", 
"B-ORD", "B-ORG", "B-PER", "B-PRC", "B-PRD", "B-QTY", "B-REG", "B-TIM", "B-WOA",
"I-CRD", "I-DAT", "I-EVT", "I-FAC", "I-GPE", "I-LAN", "I-LAW", "I-LOC", "I-MON", "I-NOR",
"I-ORD", "I-ORG", "I-PER", "I-PRC", "I-PRD", "I-QTY", "I-REG", "I-TIM", "I-WOA", "O",
```
The ner_tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any 
non-initial word. The dataset contains 19 following entities
```
    'CRD': Cardinal
    'DAT': Date
    'EVT': Event
    'FAC': Facility
    'GPE': Geopolitical Entity
    'LAW': Law Entity (such as Undang-Undang)
    'LOC': Location
    'MON': Money
    'NOR': Political Organization
    'ORD': Ordinal
    'ORG': Organization
    'PER': Person
    'PRC': Percent
    'PRD': Product
    'QTY': Quantity
    'REG': Religion
    'TIM': Time
    'WOA': Work of Art
    'LAN': Language
```
#### Sentiment Analysis
The ner_tags correspond to this list:
```
"B-NEG", "B-NET", "B-POS",
"I-NEG", "I-NET", "I-POS",
"O",
```

#### Statement Extraction
The ner_tags correspond to this list:
```
"B-BREL", "B-FREL", "B-STAT", "B-WHO",
"I-BREL", "I-FREL", "I-STAT", "I-WHO", 
"O"
```
The ner_tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any 
non-initial word.

### Data Splits

The dataset is splitted in to train, validation and test sets.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?
The annotators are listed in the
[Nergrit Corpus repository](https://github.com/grit-id/nergrit-corpus)

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

[More Information Needed]

### Contributions

Thanks to [@cahya-wirawan](https://github.com/cahya-wirawan) for adding this dataset.