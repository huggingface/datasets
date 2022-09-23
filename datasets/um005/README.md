---
annotations_creators:
- no-annotation
language_creators:
- other
language:
- en
- ur
license:
- unknown
multilinguality:
- multilingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: umc005-english-urdu
pretty_name: UMC005 English-Urdu
dataset_info:
- config_name: bible
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ur
        - en
  splits:
  - name: test
    num_bytes: 104678
    num_examples: 257
  - name: train
    num_bytes: 2350730
    num_examples: 7400
  - name: validation
    num_bytes: 113476
    num_examples: 300
  download_size: 3683565
  dataset_size: 2568884
- config_name: quran
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ur
        - en
  splits:
  - name: test
    num_bytes: 44413
    num_examples: 200
  - name: train
    num_bytes: 2929711
    num_examples: 6000
  - name: validation
    num_bytes: 43499
    num_examples: 214
  download_size: 3683565
  dataset_size: 3017623
- config_name: all
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ur
        - en
  splits:
  - name: test
    num_bytes: 149079
    num_examples: 457
  - name: train
    num_bytes: 5280441
    num_examples: 13400
  - name: validation
    num_bytes: 156963
    num_examples: 514
  download_size: 3683565
  dataset_size: 5586483
---

# Dataset Card for UMC005 English-Urdu

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

- **Homepage:** http://ufal.ms.mff.cuni.cz/umc/005-en-ur/
- **Repository:** None
- **Paper:** https://www.researchgate.net/publication/268008206_Word-Order_Issues_in_English-to-Urdu_Statistical_Machine_Translation
- **Leaderboard:** [If the dataset supports an active leaderboard, add link here]()
- **Point of Contact:** Bushra Jawaid and Daniel Zeman

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