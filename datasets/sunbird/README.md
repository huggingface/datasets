---
YAML tags:
- copy-paste the tags obtained with the tagging app: https://github.com/huggingface/datasets-tagging
---

# Dataset Card for Sunbird AI Parallel Text MT Dataset

## Table of Contents
- [Dataset Card for Sunbird](#dataset-card-for-sunbird)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** sunbird.ai
- **Repository:** https://github.com/SunbirdAI/ug-language-parallel-text-dataset
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** sunbird.ai

### Dataset Summary

This is Multi-way parallel text corpus of 5 key Ugandan languages intended for the task of machine translation


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

en-lug - English to Luganda
en-run - English to Runyankore
en-ach - English to Acholi
en-teo - English to Itesot
en-lgg - English to Lugbara

## Dataset Structure

For luganda;

DatasetDict({
    test: Dataset({
        features: ['translation'],
        num_rows: 4126
    })
    train: Dataset({
        features: ['translation'],
        num_rows: 16754
    })
    validation: Dataset({
        features: ['translation'],
        num_rows: 4126
    })
})

### Data Instances

{'translation': {'en': 'The president will support the club where they are lacking.',
  'lug': 'Pulezidenti ajja kuyamba ttiimu we zitubidde.'}}

### Data Fields

`src_tag`: string text in source language <br>
`tgt_tag`: string translation of source language in target language

### Data Splits

The dataset is split into training, validation, and test portions. Data was prepared by randomly sampled up to 5000 sentence pairs per language pair for training and up to 3000 each for test and 2000 for validation.

- train - 5000
- test - 3000
- val - 2000

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

Thanks to [@sunbirdai](https://github.com/sunbirdai) for adding this dataset.
