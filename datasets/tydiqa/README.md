---
pretty_name: TyDi QA
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- ar
- bn
- en
- fi
- id
- ja
- ko
- ru
- sw
- te
- th
license:
- apache-2.0
multilinguality:
- multilingual
size_categories:
- unknown
source_datasets:
- extended|wikipedia
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: tydi-qa
---

# Dataset Card for "tydiqa"

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

- **Homepage:** [https://github.com/google-research-datasets/tydiqa](https://github.com/google-research-datasets/tydiqa)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3726.74 MB
- **Size of the generated dataset:** 5812.92 MB
- **Total amount of disk used:** 9539.67 MB

### Dataset Summary

TyDi QA is a question answering dataset covering 11 typologically diverse languages with 204K question-answer pairs.
The languages of TyDi QA are diverse with regard to their typology -- the set of linguistic features that each language
expresses -- such that we expect models performing well on this set to generalize across a large number of the languages
in the world. It contains language phenomena that would not be found in English-only corpora. To provide a realistic
information-seeking task and avoid priming effects, questions are written by people who want to know the answer, but
don’t know the answer yet, (unlike SQuAD and its descendents) and the data is collected directly in each language without
the use of translation (unlike MLQA and XQuAD).

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### primary_task

- **Size of downloaded dataset files:** 1863.37 MB
- **Size of the generated dataset:** 5757.59 MB
- **Total amount of disk used:** 7620.96 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "annotations": {
        "minimal_answers_end_byte": [-1, -1, -1],
        "minimal_answers_start_byte": [-1, -1, -1],
        "passage_answer_candidate_index": [-1, -1, -1],
        "yes_no_answer": ["NONE", "NONE", "NONE"]
    },
    "document_plaintext": "\"\\nรองศาสตราจารย์[1] หม่อมราชวงศ์สุขุมพันธุ์ บริพัตร  (22 กันยายน 2495 -) ผู้ว่าราชการกรุงเทพมหานครคนที่ 15 อดีตรองหัวหน้าพรรคปร...",
    "document_title": "หม่อมราชวงศ์สุขุมพันธุ์ บริพัตร",
    "document_url": "\"https://th.wikipedia.org/wiki/%E0%B8%AB%E0%B8%A1%E0%B9%88%E0%B8%AD%E0%B8%A1%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%A7%E0%B8%87%E0%B8%...",
    "language": "thai",
    "passage_answer_candidates": "{\"plaintext_end_byte\": [494, 1779, 2931, 3904, 4506, 5588, 6383, 7122, 8224, 9375, 10473, 12563, 15134, 17765, 19863, 21902, 229...",
    "question_text": "\"หม่อมราชวงศ์สุขุมพันธุ์ บริพัตร เรียนจบจากที่ไหน ?\"..."
}
```

#### secondary_task

- **Size of downloaded dataset files:** 1863.37 MB
- **Size of the generated dataset:** 55.34 MB
- **Total amount of disk used:** 1918.71 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [394],
        "text": ["بطولتين"]
    },
    "context": "\"أقيمت البطولة 21 مرة، شارك في النهائيات 78 دولة، وعدد الفرق التي فازت بالبطولة حتى الآن 8 فرق، ويعد المنتخب البرازيلي الأكثر تت...",
    "id": "arabic-2387335860751143628-1",
    "question": "\"كم عدد مرات فوز الأوروغواي ببطولة كاس العالم لكرو القدم؟\"...",
    "title": "قائمة نهائيات كأس العالم"
}
```

### Data Fields

The data fields are the same among all splits.

#### primary_task
- `passage_answer_candidates`: a dictionary feature containing:
  - `plaintext_start_byte`: a `int32` feature.
  - `plaintext_end_byte`: a `int32` feature.
- `question_text`: a `string` feature.
- `document_title`: a `string` feature.
- `language`: a `string` feature.
- `annotations`: a dictionary feature containing:
  - `passage_answer_candidate_index`: a `int32` feature.
  - `minimal_answers_start_byte`: a `int32` feature.
  - `minimal_answers_end_byte`: a `int32` feature.
  - `yes_no_answer`: a `string` feature.
- `document_plaintext`: a `string` feature.
- `document_url`: a `string` feature.

#### secondary_task
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

### Data Splits

| name           |  train | validation |
| -------------- | -----: | ---------: |
| primary_task   | 166916 |      18670 |
| secondary_task |  49881 |       5077 |

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@article{tydiqa,
title   = {TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages},
author  = {Jonathan H. Clark and Eunsol Choi and Michael Collins and Dan Garrette and Tom Kwiatkowski and Vitaly Nikolaev and Jennimaria Palomaki}
year    = {2020},
journal = {Transactions of the Association for Computational Linguistics}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@albertvillanova](https://github.com/albertvillanova), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.