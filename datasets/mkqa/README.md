---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- ar
- da
- de
- en
- es
- fi
- fr
- he
- hu
- it
- ja
- km
- ko
- ms
- nl
- 'no'
- pl
- pt
- ru
- sv
- th
- tr
- vi
- zh
license:
- cc-by-3.0
multilinguality:
- multilingual
- translation
size_categories:
- 10K<n<100K
source_datasets:
- extended|natural_questions
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: mkqa
pretty_name: Multilingual Knowledge Questions and Answers
dataset_info:
  features:
  - name: example_id
    dtype: string
  - name: queries
    struct:
    - name: ar
      dtype: string
    - name: da
      dtype: string
    - name: de
      dtype: string
    - name: en
      dtype: string
    - name: es
      dtype: string
    - name: fi
      dtype: string
    - name: fr
      dtype: string
    - name: he
      dtype: string
    - name: hu
      dtype: string
    - name: it
      dtype: string
    - name: ja
      dtype: string
    - name: ko
      dtype: string
    - name: km
      dtype: string
    - name: ms
      dtype: string
    - name: nl
      dtype: string
    - name: 'no'
      dtype: string
    - name: pl
      dtype: string
    - name: pt
      dtype: string
    - name: ru
      dtype: string
    - name: sv
      dtype: string
    - name: th
      dtype: string
    - name: tr
      dtype: string
    - name: vi
      dtype: string
    - name: zh_cn
      dtype: string
    - name: zh_hk
      dtype: string
    - name: zh_tw
      dtype: string
  - name: query
    dtype: string
  - name: answers
    struct:
    - name: ar
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: da
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: de
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: en
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: es
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: fi
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: fr
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: he
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: hu
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: it
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: ja
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: ko
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: km
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: ms
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: nl
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: 'no'
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: pl
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: pt
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: ru
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: sv
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: th
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: tr
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: vi
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: zh_cn
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: zh_hk
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
    - name: zh_tw
      list:
      - name: type
        dtype:
          class_label:
            names:
              0: entity
              1: long_answer
              2: unanswerable
              3: date
              4: number
              5: number_with_unit
              6: short_phrase
              7: binary
      - name: entity
        dtype: string
      - name: text
        dtype: string
      - name: aliases
        list: string
  config_name: mkqa
  splits:
  - name: train
    num_bytes: 36005650
    num_examples: 10000
  download_size: 11903948
  dataset_size: 36005650
---

# Dataset Card for MKQA: Multilingual Knowledge Questions & Answers

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

- [**Homepage:**](https://github.com/apple/ml-mkqa/)
- [**Paper:**](https://arxiv.org/abs/2007.15207)

### Dataset Summary

MKQA contains 10,000 queries sampled from the [Google Natural Questions dataset](https://github.com/google-research-datasets/natural-questions).  

For each query we collect new passage-independent answers. 
These queries and answers are then human translated into 25 Non-English languages.

### Supported Tasks and Leaderboards

`question-answering`

### Languages

| Language code | Language name |
|---------------|---------------|
| `ar`     | `Arabic`                    |
| `da`     | `Danish`                    |
| `de`     | `German`                    |
| `en`     | `English`                   |
| `es`     | `Spanish`                   |
| `fi`     | `Finnish`                   |
| `fr`     | `French`                    |
| `he`     | `Hebrew`                    |
| `hu`     | `Hungarian`                 |
| `it`     | `Italian`                   |
| `ja`     | `Japanese`                  |
| `ko`     | `Korean`                    |
| `km`     | `Khmer`                    |
| `ms`     | `Malay`                     |
| `nl`     | `Dutch`                     |
| `no`     | `Norwegian`                 |
| `pl`     | `Polish`                    |
| `pt`     | `Portuguese`                |
| `ru`     | `Russian`                   |
| `sv`     | `Swedish`                   |
| `th`     | `Thai`                      |
| `tr`     | `Turkish`                   |
| `vi`     | `Vietnamese`                |
| `zh_cn`     | `Chinese (Simplified)`   |
| `zh_hk`     | `Chinese (Hong kong)`    |
| `zh_tw`     | `Chinese (Traditional)`  |

## Dataset Structure

### Data Instances

An example from the data set looks as follows:

```
{
 'example_id': 563260143484355911,
 'queries': {
  'en': "who sings i hear you knocking but you can't come in",
  'ru': "кто поет i hear you knocking but you can't come in",
  'ja': '「 I hear you knocking」は誰が歌っていますか',
  'zh_cn': "《i hear you knocking but you can't come in》是谁演唱的",
  ...
 },
 'query': "who sings i hear you knocking but you can't come in",
 'answers': {'en': [{'type': 'entity',
    'entity': 'Q545186',
    'text': 'Dave Edmunds',
    'aliases': []}],
  'ru': [{'type': 'entity',
    'entity': 'Q545186',
    'text': 'Эдмундс, Дэйв',
    'aliases': ['Эдмундс', 'Дэйв Эдмундс', 'Эдмундс Дэйв', 'Dave Edmunds']}],
  'ja': [{'type': 'entity',
    'entity': 'Q545186',
    'text': 'デイヴ・エドモンズ',
    'aliases': ['デーブ・エドモンズ', 'デイブ・エドモンズ']}],
  'zh_cn': [{'type': 'entity', 'text': '戴维·埃德蒙兹 ', 'entity': 'Q545186'}],
  ...
  },
}

```

### Data Fields

Each example in the dataset contains the unique Natural Questions `example_id`, the original English `query`, and then `queries` and `answers` in 26 languages.
Each answer is labelled with an answer type. The breakdown is:

| Answer Type | Occurrence |
|---------------|---------------|
| `entity`               | `4221`             |
| `long_answer`          | `1815`             |
| `unanswerable`         | `1427`             |
| `date`                 | `1174`             |
| `number`               | `485`              |
| `number_with_unit`     | `394`              |
| `short_phrase`         | `346`              |
| `binary`               | `138`              |
  
For each language, there can be more than one acceptable textual answer, in order to capture a variety of possible valid answers. 

Detailed explanation of fields taken from [here](https://github.com/apple/ml-mkqa/#dataset)

when `entity` field is not available it is set to an empty string ''.
when `aliases` field is not available it is set to an empty list [].

### Data Splits

- Train: 10000

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[Google Natural Questions dataset](https://github.com/google-research-datasets/natural-questions)

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

[CC BY-SA 3.0](https://github.com/apple/ml-mkqa#license)

### Citation Information
```
@misc{mkqa,
    title = {MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering},
    author = {Shayne Longpre and Yi Lu and Joachim Daiber},
    year = {2020},
    URL = {https://arxiv.org/pdf/2007.15207.pdf}
}
```

### Contributions

Thanks to [@cceyda](https://github.com/cceyda) for adding this dataset.