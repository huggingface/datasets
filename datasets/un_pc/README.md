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
- multilingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: united-nations-parallel-corpus
pretty_name: United Nations Parallel Corpus
configs:
- ar-en
- ar-es
- ar-fr
- ar-ru
- ar-zh
- en-es
- en-fr
- en-ru
- en-zh
- es-fr
- es-ru
- es-zh
- fr-ru
- fr-zh
- ru-zh
dataset_info:
- config_name: ar-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - en
  splits:
  - name: train
    num_bytes: 8039689939
    num_examples: 20044478
  download_size: 2025106743
  dataset_size: 8039689939
- config_name: ar-es
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - es
  splits:
  - name: train
    num_bytes: 8715754848
    num_examples: 20532014
  download_size: 2167791297
  dataset_size: 8715754848
- config_name: ar-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - fr
  splits:
  - name: train
    num_bytes: 8897848038
    num_examples: 20281645
  download_size: 2188765415
  dataset_size: 8897848038
- config_name: ar-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - ru
  splits:
  - name: train
    num_bytes: 11395923083
    num_examples: 20571334
  download_size: 2476562835
  dataset_size: 11395923083
- config_name: ar-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - zh
  splits:
  - name: train
    num_bytes: 6447658008
    num_examples: 17306056
  download_size: 1738869755
  dataset_size: 6447658008
- config_name: en-es
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - es
  splits:
  - name: train
    num_bytes: 8241635322
    num_examples: 25227004
  download_size: 2300411698
  dataset_size: 8241635322
- config_name: en-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fr
  splits:
  - name: train
    num_bytes: 9718522775
    num_examples: 30340652
  download_size: 2657208676
  dataset_size: 9718522775
- config_name: en-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ru
  splits:
  - name: train
    num_bytes: 11156164691
    num_examples: 25173398
  download_size: 2589707636
  dataset_size: 11156164691
- config_name: en-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - zh
  splits:
  - name: train
    num_bytes: 4988812558
    num_examples: 17451549
  download_size: 1535707641
  dataset_size: 4988812558
- config_name: es-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - fr
  splits:
  - name: train
    num_bytes: 9230891207
    num_examples: 25887160
  download_size: 2492342915
  dataset_size: 9230891207
- config_name: es-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - ru
  splits:
  - name: train
    num_bytes: 10789780134
    num_examples: 22294106
  download_size: 2487664520
  dataset_size: 10789780134
- config_name: es-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - zh
  splits:
  - name: train
    num_bytes: 5475365986
    num_examples: 17599223
  download_size: 1639717723
  dataset_size: 5475365986
- config_name: fr-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ru
  splits:
  - name: train
    num_bytes: 12099669711
    num_examples: 25219973
  download_size: 2762585269
  dataset_size: 12099669711
- config_name: fr-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - zh
  splits:
  - name: train
    num_bytes: 5679222134
    num_examples: 17521170
  download_size: 1668823634
  dataset_size: 5679222134
- config_name: ru-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ru
        - zh
  splits:
  - name: train
    num_bytes: 7905443441
    num_examples: 17920922
  download_size: 1934425373
  dataset_size: 7905443441
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

- **Homepage:**[UNPC](http://opus.nlpl.eu/UNPC.php)
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

This parallel corpus consists of manually translated UN documents from the last 25 years (1990 to 2014) \
for the six official UN languages, Arabic, Chinese, English, French, Russian, and Spanish.
6 languages, 15 bitexts

### Supported Tasks and Leaderboards

The underlying task is machine translation.

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

```
@inproceedings{ziemski-etal-2016-united,
    title = "The {U}nited {N}ations Parallel Corpus v1.0",
    author = "Ziemski, Micha{\\l}  and
      Junczys-Dowmunt, Marcin  and
      Pouliquen, Bruno",
    booktitle = "Proceedings of the Tenth International Conference on Language Resources and Evaluation ({LREC}'16)",
    month = may,
    year = "2016",
    address = "Portoro{\v{z}}, Slovenia",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L16-1561",
    pages = "3530--3534",
    abstract = "This paper describes the creation process and statistics of the official United Nations Parallel Corpus, the first parallel corpus composed from United Nations documents published by the original data creator. The parallel corpus presented consists of manually translated UN documents from the last 25 years (1990 to 2014) for the six official UN languages, Arabic, Chinese, English, French, Russian, and Spanish. The corpus is freely available for download under a liberal license. Apart from the pairwise aligned documents, a fully aligned subcorpus for the six official UN languages is distributed. We provide baseline BLEU scores of our Moses-based SMT systems trained with the full data of language pairs involving English and for all possible translation directions of the six-way subcorpus.",
}
```
### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.