---
annotations_creators:
- found
language_creators:
- found
language:
- am
- ar
- az
- bg
- bn
- bs
- cs
- de
- dv
- en
- es
- fa
- fr
- ha
- hi
- id
- it
- ja
- ko
- ku
- ml
- ms
- nl
- 'no'
- pl
- pt
- ro
- ru
- sd
- so
- sq
- sv
- sw
- ta
- tg
- th
- tr
- tt
- ug
- ur
- uz
- zh
license:
- unknown
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: tanzil
dataset_info:
- config_name: bg-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - en
  splits:
  - name: train
    num_bytes: 34473016
    num_examples: 135477
  download_size: 9305292
  dataset_size: 34473016
- config_name: bn-hi
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - hi
  splits:
  - name: train
    num_bytes: 18869103
    num_examples: 24942
  download_size: 3542740
  dataset_size: 18869103
- config_name: fa-sv
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fa
        - sv
  splits:
  - name: train
    num_bytes: 29281634
    num_examples: 68601
  download_size: 8550826
  dataset_size: 29281634
- config_name: ru-zh
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
    num_bytes: 59736143
    num_examples: 99779
  download_size: 16214659
  dataset_size: 59736143
- config_name: en-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tr
  splits:
  - name: train
    num_bytes: 255891913
    num_examples: 1189967
  download_size: 82954694
  dataset_size: 255891913
---

# Dataset Card for tanzil

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

- **Homepage:** http://opus.nlpl.eu/Tanzil.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary


To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/Tanzil.php
E.g.

`dataset = load_dataset("tanzil", lang1="en", lang2="ru")`


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

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