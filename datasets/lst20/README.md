---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- th
licenses:
- other-aiforthai
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
- part-of-speech-tagging
- structure-prediction-other-clause-segmentation
- structure-prediction-other-sentence-segmentation
- structure-prediction-other-word-segmentation
paperswithcode_id: null
pretty_name: LST20
---

# Dataset Card for LST20

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

- **Homepage:** https://aiforthai.in.th/
- **Repository:**
- **Paper:** 
- **Leaderboard:**
- **Point of Contact:** [email](thepchai@nectec.or.th)

### Dataset Summary

LST20 Corpus is a dataset for Thai language processing developed by National Electronics and Computer Technology Center (NECTEC), Thailand.
It offers five layers of linguistic annotation: word boundaries, POS tagging, named entities, clause boundaries, and sentence boundaries.
At a large scale, it consists of 3,164,002 words, 288,020 named entities, 248,181 clauses, and 74,180 sentences, while it is annotated with
16 distinct POS tags. All 3,745 documents are also annotated with one of 15 news genres. Regarding its sheer size, this dataset is
considered large enough for developing joint neural models for NLP.
Manually download at https://aiforthai.in.th/corpus.php
See `LST20 Annotation Guideline.pdf` and `LST20 Brief Specification.pdf` within the downloaded `AIFORTHAI-LST20Corpus.tar.gz` for more details.

### Supported Tasks and Leaderboards

- POS tagging
- NER tagging
- clause segmentation
- sentence segmentation
- word tokenization

### Languages

Thai

## Dataset Structure

### Data Instances

```
{'clause_tags': [1, 2, 2, 2, 2, 2, 2, 2, 3], 'fname': 'T11964.txt', 'id': '0', 'ner_tags': [8, 0, 0, 0, 0, 0, 0, 0, 25], 'pos_tags': [0, 0, 0, 1, 0, 8, 8, 8, 0], 'tokens': ['ธรรมนูญ', 'แชมป์', 'สิงห์คลาสสิก', 'กวาด', 'รางวัล', 'แสน', 'สี่', 'หมื่น', 'บาท']}
{'clause_tags': [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3], 'fname': 'T11964.txt', 'id': '1', 'ner_tags': [8, 18, 28, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 15, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6], 'pos_tags': [0, 2, 0, 2, 1, 1, 2, 8, 2, 10, 2, 8, 2, 1, 0, 1, 0, 4, 7, 1, 0, 2, 8, 2, 10, 1, 10, 4, 2, 8, 2, 4, 0, 4, 0, 2, 8, 2, 10, 2, 8], 'tokens': ['ธรรมนูญ', '_', 'ศรีโรจน์', '_', 'เก็บ', 'เพิ่ม', '_', '4', '_', 'อันเดอร์พาร์', '_', '68', '_', 'เข้า', 'ป้าย', 'รับ', 'แชมป์', 'ใน', 'การ', 'เล่น', 'อาชีพ', '_', '19', '_', 'ปี', 'เป็น', 'ครั้ง', 'ที่', '_', '8', '_', 'ใน', 'ชีวิต', 'ด้วย', 'สกอร์', '_', '18', '_', 'อันเดอร์พาร์', '_', '270']}
```

### Data Fields

- `id`: nth sentence in each set, starting at 0
- `fname`: text file from which the sentence comes from
- `tokens`: word tokens
- `pos_tags`: POS tags
- `ner_tags`: NER tags
- `clause_tags`: clause tags

### Data Splits

|                      | train     | eval        | test        | all       |
|----------------------|-----------|-------------|-------------|-----------|
| words                | 2,714,848 | 240,891     | 207,295     | 3,163,034 |
| named entities       | 246,529   | 23,176      | 18,315      | 288,020   |
| clauses              | 214,645   | 17,486      | 16,050      | 246,181   |
| sentences            | 63,310    | 5,620       | 5,250       | 74,180    |
| distinct words       | 42,091    | (oov) 2,595 | (oov) 2,006 | 46,692    |
| breaking spaces※     | 63,310    | 5,620       | 5,250       | 74,180    |
| non-breaking spaces※※| 402,380   | 39,920      | 32,204      | 475,504   |

※ Breaking space = space that is used as a sentence boundary marker
※※ Non-breaking space = space that is not used as a sentence boundary marker

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Respective authors of the news articles

### Annotations

#### Annotation process

Detailed annotation guideline can be found in `LST20 Annotation Guideline.pdf`.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

All texts are from public news. No personal and sensitive information is expected to be included.

## Considerations for Using the Data

### Social Impact of Dataset

- Large-scale Thai NER & POS tagging, clause & sentence segmentatation, word tokenization

### Discussion of Biases

- All 3,745 texts are from news domain:
  - politics: 841
  - crime and accident: 592
  - economics: 512
  - entertainment: 472
  - sports: 402
  - international: 279
  - science, technology and education: 216
  - health: 92
  - general: 75
  - royal: 54
  - disaster: 52
  - development: 45
  - environment: 40
  - culture: 40
  - weather forecast: 33
- Word tokenization is done accoding to Inter­BEST 2009 Guideline.


### Other Known Limitations

- Some NER tags do not correspond with given labels (`B`, `I`, and so on)

## Additional Information

### Dataset Curators

[NECTEC](https://www.nectec.or.th/en/)

### Licensing Information

1. Non-commercial use, research, and open source

Any non-commercial use of the dataset for research and open-sourced projects is encouraged and free of charge. Please cite our technical report for reference.

If you want to perpetuate your models trained on our dataset and share them to the research community in Thailand, please send your models, code, and APIs to the AI for Thai Project. Please contact Dr. Thepchai Supnithi via thepchai@nectec.or.th for more information.

Note that modification and redistribution of the dataset by any means are strictly prohibited unless authorized by the corpus authors.

2. Commercial use

In any commercial use of the dataset, there are two options.

- Option 1 (in kind): Contributing a dataset of 50,000 words completely annotated with our annotation scheme within 1 year. Your data will also be shared and recognized as a dataset co-creator in the research community in Thailand.

- Option 2 (in cash): Purchasing a lifetime license for the entire dataset is required. The purchased rights of use cover only this dataset.

In both options, please contact Dr. Thepchai Supnithi via thepchai@nectec.or.th for more information.

### Citation Information

```
@article{boonkwan2020annotation,
  title={The Annotation Guideline of LST20 Corpus},
  author={Boonkwan, Prachya and Luantangsrisuk, Vorapon and Phaholphinyo, Sitthaa and Kriengket, Kanyanat and Leenoi, Dhanon and Phrombut, Charun and Boriboon, Monthika and Kosawat, Krit and Supnithi, Thepchai},
  journal={arXiv preprint arXiv:2008.05055},
  year={2020}
}
```

### Contributions

Thanks to [@cstorm125](https://github.com/cstorm125) for adding this dataset.