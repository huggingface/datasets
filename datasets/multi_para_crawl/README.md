---
annotations_creators:
- found
language_creators:
- found
language:
- bg
- ca
- cs
- da
- de
- el
- es
- et
- eu
- fi
- fr
- ga
- gl
- ha
- hr
- hu
- ig
- is
- it
- km
- lt
- lv
- mt
- my
- nb
- ne
- nl
- nn
- pl
- ps
- pt
- ro
- ru
- si
- sk
- sl
- so
- sv
- sw
- tl
license:
- cc0-1.0
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
pretty_name: MultiParaCrawl
dataset_info:
- config_name: cs-is
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - is
  splits:
  - name: train
    num_bytes: 148967967
    num_examples: 691006
  download_size: 61609317
  dataset_size: 148967967
- config_name: ga-sk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ga
        - sk
  splits:
  - name: train
    num_bytes: 92802332
    num_examples: 390327
  download_size: 39574554
  dataset_size: 92802332
- config_name: lv-mt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - lv
        - mt
  splits:
  - name: train
    num_bytes: 116533998
    num_examples: 464160
  download_size: 49770574
  dataset_size: 116533998
- config_name: nb-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - nb
        - ru
  splits:
  - name: train
    num_bytes: 116899303
    num_examples: 399050
  download_size: 40932849
  dataset_size: 116899303
- config_name: de-tl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - tl
  splits:
  - name: train
    num_bytes: 30880849
    num_examples: 98156
  download_size: 12116471
  dataset_size: 30880849
---

# Dataset Card for MultiParaCrawl

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

- **Homepage:** http://opus.nlpl.eu/MultiParaCrawl.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/MultiParaCrawl.php
E.g.

`dataset = load_dataset("multi_para_crawl", lang1="en", lang2="nl")`

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