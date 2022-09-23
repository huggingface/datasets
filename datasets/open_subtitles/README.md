---
annotations_creators:
- found
language_creators:
- found
language:
- af
- ar
- bg
- bn
- br
- bs
- ca
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fr
- gl
- he
- hi
- hr
- hu
- hy
- id
- is
- it
- ja
- ka
- kk
- ko
- lt
- lv
- mk
- ml
- ms
- nl
- 'no'
- pl
- pt
- ro
- ru
- si
- sk
- sl
- sq
- sr
- sv
- ta
- te
- th
- tl
- tr
- uk
- ur
- vi
- zh
language_bcp47:
- pt-BR
- ze-EN
- ze-ZH
- zh-CN
- zh-TW
license:
- unknown
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
- 1M<n<10M
- n<1K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: opensubtitles
pretty_name: OpenSubtitles
configs:
- bn-is
- bs-eo
- da-ru
- en-hi
- fr-hy
dataset_info:
- config_name: bs-eo
  features:
  - name: id
    dtype: string
  - name: meta
    struct:
    - name: year
      dtype: uint32
    - name: imdbId
      dtype: uint32
    - name: subtitleId
      struct:
      - name: bs
        dtype: uint32
      - name: eo
        dtype: uint32
    - name: sentenceIds
      struct:
      - name: bs
        sequence: uint32
      - name: eo
        sequence: uint32
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - eo
  splits:
  - name: train
    num_bytes: 1204266
    num_examples: 10989
  download_size: 333050
  dataset_size: 1204266
- config_name: fr-hy
  features:
  - name: id
    dtype: string
  - name: meta
    struct:
    - name: year
      dtype: uint32
    - name: imdbId
      dtype: uint32
    - name: subtitleId
      struct:
      - name: fr
        dtype: uint32
      - name: hy
        dtype: uint32
    - name: sentenceIds
      struct:
      - name: fr
        sequence: uint32
      - name: hy
        sequence: uint32
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - hy
  splits:
  - name: train
    num_bytes: 132450
    num_examples: 668
  download_size: 41861
  dataset_size: 132450
- config_name: da-ru
  features:
  - name: id
    dtype: string
  - name: meta
    struct:
    - name: year
      dtype: uint32
    - name: imdbId
      dtype: uint32
    - name: subtitleId
      struct:
      - name: da
        dtype: uint32
      - name: ru
        dtype: uint32
    - name: sentenceIds
      struct:
      - name: da
        sequence: uint32
      - name: ru
        sequence: uint32
  - name: translation
    dtype:
      translation:
        languages:
        - da
        - ru
  splits:
  - name: train
    num_bytes: 1082649105
    num_examples: 7543012
  download_size: 267995167
  dataset_size: 1082649105
- config_name: en-hi
  features:
  - name: id
    dtype: string
  - name: meta
    struct:
    - name: year
      dtype: uint32
    - name: imdbId
      dtype: uint32
    - name: subtitleId
      struct:
      - name: en
        dtype: uint32
      - name: hi
        dtype: uint32
    - name: sentenceIds
      struct:
      - name: en
        sequence: uint32
      - name: hi
        sequence: uint32
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hi
  splits:
  - name: train
    num_bytes: 13845544
    num_examples: 93016
  download_size: 2967295
  dataset_size: 13845544
- config_name: bn-is
  features:
  - name: id
    dtype: string
  - name: meta
    struct:
    - name: year
      dtype: uint32
    - name: imdbId
      dtype: uint32
    - name: subtitleId
      struct:
      - name: bn
        dtype: uint32
      - name: is
        dtype: uint32
    - name: sentenceIds
      struct:
      - name: bn
        sequence: uint32
      - name: is
        sequence: uint32
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - is
  splits:
  - name: train
    num_bytes: 6371251
    num_examples: 38272
  download_size: 1411625
  dataset_size: 6371251
---

# Dataset Card for OpenSubtitles

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

- **Homepage:** http://opus.nlpl.eu/OpenSubtitles.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2016/pdf/62_Paper.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

To load a language pair which isn't part of the config, all you need to do is specify the language code as pairs.
You can find the valid pairs in Homepage section of Dataset Description: http://opus.nlpl.eu/OpenSubtitles.php
E.g.

`dataset = load_dataset("open_subtitles", lang1="fi", lang2="hi")`


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The languages in the dataset are:
- af
- ar
- bg
- bn
- br
- bs
- ca
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fr
- gl
- he
- hi
- hr
- hu
- hy
- id
- is
- it
- ja
- ka
- kk
- ko
- lt
- lv
- mk
- ml
- ms
- nl
- no
- pl
- pt
- pt_br: Portuguese (Brazil) (pt-BR)
- ro
- ru
- si
- sk
- sl
- sq
- sr
- sv
- ta
- te
- th
- tl
- tr
- uk
- ur
- vi
- ze_en: English constituent of Bilingual Chinese-English (subtitles displaying two languages at once, one per line)
- ze_zh: Chinese constituent of Bilingual Chinese-English (subtitles displaying two languages at once, one per line)
- zh_cn: Simplified Chinese (zh-CN, `zh-Hans`)
- zh_tw: Traditional Chinese (zh-TW, `zh-Hant`)

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