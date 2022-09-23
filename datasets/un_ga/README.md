---
annotations_creators:
- found
language_creators:
- found
language:
- ar
- en
- es
- fr
- ru
- zh
license:
- unknown
multilinguality:
- translation
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: UnGa
configs:
- ar-to-en
- ar-to-es
- ar-to-fr
- ar-to-ru
- ar-to-zh
- en-to-es
- en-to-fr
- en-to-ru
- en-to-zh
- es-to-fr
- es-to-ru
- es-to-zh
- fr-to-ru
- fr-to-zh
- ru-to-zh
dataset_info:
- config_name: ar_to_en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - en
  splits:
  - name: train
    num_bytes: 53122872
    num_examples: 74067
  download_size: 10584906
  dataset_size: 53122872
- config_name: ar_to_es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - es
  splits:
  - name: train
    num_bytes: 55728711
    num_examples: 74067
  download_size: 11084275
  dataset_size: 55728711
- config_name: ar_to_fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - fr
  splits:
  - name: train
    num_bytes: 55930898
    num_examples: 74067
  download_size: 11248563
  dataset_size: 55930898
- config_name: ar_to_ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - ru
  splits:
  - name: train
    num_bytes: 72657721
    num_examples: 74067
  download_size: 12852834
  dataset_size: 72657721
- config_name: ar_to_zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - zh
  splits:
  - name: train
    num_bytes: 48217675
    num_examples: 74067
  download_size: 10254078
  dataset_size: 48217675
- config_name: en_to_es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - es
  splits:
  - name: train
    num_bytes: 45358866
    num_examples: 74067
  download_size: 9850684
  dataset_size: 45358866
- config_name: en_to_fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fr
  splits:
  - name: train
    num_bytes: 45561053
    num_examples: 74067
  download_size: 10014972
  dataset_size: 45561053
- config_name: en_to_ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ru
  splits:
  - name: train
    num_bytes: 62287876
    num_examples: 74067
  download_size: 11619243
  dataset_size: 62287876
- config_name: en_to_zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - zh
  splits:
  - name: train
    num_bytes: 37847830
    num_examples: 74067
  download_size: 9020487
  dataset_size: 37847830
- config_name: es_to_fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - fr
  splits:
  - name: train
    num_bytes: 48166892
    num_examples: 74067
  download_size: 10514341
  dataset_size: 48166892
- config_name: es_to_ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - ru
  splits:
  - name: train
    num_bytes: 64893715
    num_examples: 74067
  download_size: 12118612
  dataset_size: 64893715
- config_name: es_to_zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - zh
  splits:
  - name: train
    num_bytes: 40453669
    num_examples: 74067
  download_size: 9519856
  dataset_size: 40453669
- config_name: fr_to_ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ru
  splits:
  - name: train
    num_bytes: 65095902
    num_examples: 74067
  download_size: 12282900
  dataset_size: 65095902
- config_name: fr_to_zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - zh
  splits:
  - name: train
    num_bytes: 40655856
    num_examples: 74067
  download_size: 9684144
  dataset_size: 40655856
- config_name: ru_to_zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ru
        - zh
  splits:
  - name: train
    num_bytes: 57382679
    num_examples: 74067
  download_size: 11288415
  dataset_size: 57382679
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

- **Homepage:** http://opus.nlpl.eu/UN.php
- **Repository:**
- **Paper:** https://www.researchgate.net/publication/228579662_United_nations_general_assembly_resolutions_A_six-language_parallel_corpus
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary
This is a collection of translated documents from the United Nations originally compiled into a translation memory by Alexandre Rafalovitch, Robert Dale (see http://uncorpora.org).


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

@inproceedings{title = "United Nations General Assembly Resolutions: a six-language parallel corpus",
abstract = "In this paper we describe a six-ways parallel public-domain corpus consisting of 2100 United Nations General Assembly Resolutions with translations in the six official languages of the United Nations, with an average of around 3 million tokens per language. The corpus is available in a preprocessed, formatting-normalized TMX format with paragraphs aligned across multiple languages. We describe the background to the corpus and its content, the process of its construction, and some of its interesting properties.",
author = "Alexandre Rafalovitch and Robert Dale",
year = "2009",
language = "English",
booktitle = "MT Summit XII proceedings",
publisher = "International Association of Machine Translation",
}
### Contributions

Thanks to [@param087](https://github.com/param087) for adding this dataset.