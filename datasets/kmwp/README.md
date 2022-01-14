---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- ko
licenses:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-math-word-problem
pretty_name: KMWP (Korean Math Word Problems)
---

# Dataset Card for KMWP

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** https://github.com/tunib-ai/KMWP
- **Repository:** https://github.com/tunib-ai/KMWP
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** contact@tunib.ai

### Dataset Summary

A dataset in which Python codes corresponding to math problems and solutions in Korean are paired. It consists of 8 types, see https://github.com/tunib-ai/KMWP for more information.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Korean

## Dataset Structure

### Data Instances

{'class': 1,
 'problem': '한 변의 길이가 24cm인 정육각형과 둘레가 같은 정팔각형이 있습니다. 이 정팔각형의 한 변의 길이는 몇 cm인지 구하시오.',
 'code': 'a = 3.2\nb = 0.4\ny = int(a / b)\nprint(y)',
 'answer': '8'}

### Data Fields

{'class': Value(dtype='string', id=None),
 'problem': Value(dtype='string', id=None),
 'code': Value(dtype='string', id=None),
 'answer': Value(dtype='string', id=None)}

### Data Splits

- Train
  - class 1: 1000
  - class 2: 30
  - class 3: 200
  - class 4: 24
  - class 5: 20
  - class 6: 15
  - class 7: 20
  - class 8: 80

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information
```
@misc{KMWP
  author       = {Keum, Bitna and Ryu, Myeonghyeon and Ham, Yoseph and Seo, Minsuh and 
                  Jo, Heechang and Kim, Hangyeol and Park, Kyubyong},
  title        = {KMWP, Korean Math Word Problems},
  howpublished = {\url{https://github.com/tunib-ai/KMWP}},
  year         = {2022},
}
```

[Needs More Information]