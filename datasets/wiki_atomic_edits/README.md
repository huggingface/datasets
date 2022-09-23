---
annotations_creators:
- found
language_creators:
- found
language:
- de
- en
- es
- fr
- it
- ja
- ru
- zh
license:
- cc-by-sa-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
- 10M<n<100M
- 1M<n<10M
source_datasets:
- original
task_categories:
- summarization
task_ids: []
paperswithcode_id: wikiatomicedits
pretty_name: WikiAtomicEdits
configs:
- chinese_deletions
- chinese_insertions
- english_deletions
- english_insertions
- french_deletions
- french_insertions
- german_deletions
- german_insertions
- italian_deletions
- italian_insertions
- japanese_deletions
- japanese_insertions
- russian_deletions
- russian_insertions
- spanish_deletions
- spanish_insertions
dataset_info:
- config_name: german_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 1072443082
    num_examples: 3343403
  download_size: 274280387
  dataset_size: 1072443082
- config_name: german_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 624070402
    num_examples: 1994329
  download_size: 160133549
  dataset_size: 624070402
- config_name: english_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 4258411914
    num_examples: 13737796
  download_size: 1090652177
  dataset_size: 4258411914
- config_name: english_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 2865754626
    num_examples: 9352389
  download_size: 736560902
  dataset_size: 2865754626
- config_name: spanish_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 481145004
    num_examples: 1380934
  download_size: 118837934
  dataset_size: 481145004
- config_name: spanish_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 317253196
    num_examples: 908276
  download_size: 78485695
  dataset_size: 317253196
- config_name: french_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 651525210
    num_examples: 2038305
  download_size: 160442894
  dataset_size: 651525210
- config_name: french_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 626323354
    num_examples: 2060242
  download_size: 155263358
  dataset_size: 626323354
- config_name: italian_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 372950256
    num_examples: 1078814
  download_size: 92302006
  dataset_size: 372950256
- config_name: italian_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 198598618
    num_examples: 583316
  download_size: 49048596
  dataset_size: 198598618
- config_name: japanese_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 765754162
    num_examples: 2249527
  download_size: 185766012
  dataset_size: 765754162
- config_name: japanese_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 459683880
    num_examples: 1352162
  download_size: 110513593
  dataset_size: 459683880
- config_name: russian_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 790822192
    num_examples: 1471638
  download_size: 152985812
  dataset_size: 790822192
- config_name: russian_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 514750186
    num_examples: 960976
  download_size: 100033230
  dataset_size: 514750186
- config_name: chinese_insertions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 233367646
    num_examples: 746509
  download_size: 66124094
  dataset_size: 233367646
- config_name: chinese_deletions
  features:
  - name: id
    dtype: int32
  - name: base_sentence
    dtype: string
  - name: phrase
    dtype: string
  - name: edited_sentence
    dtype: string
  splits:
  - name: train
    num_bytes: 144269112
    num_examples: 467271
  download_size: 40898651
  dataset_size: 144269112
---

# Dataset Card for WikiAtomicEdits

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

- **Homepage:** None
- **Repository:** https://github.com/google-research-datasets/wiki-atomic-edits
- **Paper:** https://www.aclweb.org/anthology/D18-1028/
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The languages in the dataset are:
- de
- en
- es
- fr
- it
- jp: Japanese (`ja`)
- ru
- zh

## Dataset Structure

### Data Instances

Here are some examples of questions and facts:


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