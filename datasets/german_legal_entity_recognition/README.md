---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- de
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: legal-documents-entity-recognition
pretty_name: Legal Documents Entity Recognition
dataset_info:
- config_name: bag
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
- config_name: bfh
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
- config_name: bgh
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
- config_name: bpatg
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
- config_name: bsg
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
- config_name: bverfg
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
- config_name: bverwg
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
- config_name: all
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-AN
          1: B-EUN
          2: B-GRT
          3: B-GS
          4: B-INN
          5: B-LD
          6: B-LDS
          7: B-LIT
          8: B-MRK
          9: B-ORG
          10: B-PER
          11: B-RR
          12: B-RS
          13: B-ST
          14: B-STR
          15: B-UN
          16: B-VO
          17: B-VS
          18: B-VT
          19: I-AN
          20: I-EUN
          21: I-GRT
          22: I-GS
          23: I-INN
          24: I-LD
          25: I-LDS
          26: I-LIT
          27: I-MRK
          28: I-ORG
          29: I-PER
          30: I-RR
          31: I-RS
          32: I-ST
          33: I-STR
          34: I-UN
          35: I-VO
          36: I-VS
          37: I-VT
          38: O
  splits:
  - name: train
  download_size: 4392913
  dataset_size: 0
---

# Dataset Card for Legal Documents Entity Recognition

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

- **Homepage:** https://github.com/elenanereiss/Legal-Entity-Recognition
- **Repository:** None
- **Paper:** https://link.springer.com/chapter/10.1007/978-3-030-33220-4_20
- **Leaderboard:** [If the dataset supports an active leaderboard, add link here]()
- **Point of Contact:** Georg Rehm (georg.rehm@dfki.de)

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]
## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

[More Information Needed]
### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.