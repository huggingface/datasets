---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- ar
- de
- el
- en
- es
- hi
- ru
- th
- tr
- vi
- zh
license:
- cc-by-sa-4.0
multilinguality:
- multilingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|squad
- extended|xquad
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: xquad-r
pretty_name: LAReQA
configs:
- ar
- de
- el
- en
- es
- hi
- ru
- th
- tr
- vi
- zh
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

- **Homepage:** [LAReQA](https://github.com/google-research-datasets/lareqa)
- **Repository:** [XQuAD-R](https://github.com/google-research-datasets/lareqa)
- **Paper:** [LAReQA: Language-agnostic answer retrieval from a multilingual pool](https://arxiv.org/pdf/2004.05484.pdf)
- **Point of Contact:** [Noah Constant](mailto:nconstant@google.com)


### Dataset Summary
 
XQuAD-R is a retrieval version of the XQuAD dataset (a cross-lingual extractive
QA dataset). Like XQuAD, XQUAD-R is an 11-way parallel dataset,  where each
question appears in 11 different languages and has 11 parallel correct answers
across the languages.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset can be found with the following languages:
* Arabic: `xquad-r/ar.json`
* German: `xquad-r/de.json`
* Greek: `xquad-r/el.json`
* English: `xquad-r/en.json`
* Spanish: `xquad-r/es.json`
* Hindi: `xquad-r/hi.json`
* Russian: `xquad-r/ru.json`
* Thai: `xquad-r/th.json`
* Turkish: `xquad-r/tr.json`
* Vietnamese: `xquad-r/vi.json`
* Chinese: `xquad-r/zh.json`

## Dataset Structure

[More Information Needed]

### Data Instances

An example from `en` config:
```
{'id': '56beb4343aeaaa14008c925b',
 'context': "The Panthers defense gave up just 308 points, ranking sixth in the league, while also leading the NFL in interceptions with 24 and boasting four Pro Bowl selections. Pro Bowl defensive tackle Kawann Short led the team in sacks with 11, while also forcing three fumbles and recovering two. Fellow lineman Mario Addison added 6½ sacks. The Panthers line also featured veteran defensive end Jared Allen, a 5-time pro bowler who was the NFL's active career sack leader with 136, along with defensive end Kony Ealy, who had 5 sacks in just 9 starts. Behind them, two of the Panthers three starting linebackers were also selected to play in the Pro Bowl: Thomas Davis and Luke Kuechly. Davis compiled 5½ sacks, four forced fumbles, and four interceptions, while Kuechly led the team in tackles (118) forced two fumbles, and intercepted four passes of his own. Carolina's secondary featured Pro Bowl safety Kurt Coleman, who led the team with a career high seven interceptions, while also racking up 88 tackles and Pro Bowl cornerback Josh Norman, who developed into a shutdown corner during the season and had four interceptions, two of which were returned for touchdowns.",
 'question': 'How many points did the Panthers defense surrender?',
 'answers': {'text': ['308'], 'answer_start': [34]}}
```

### Data Fields

- `id` (`str`): Unique ID for the context-question pair.
- `context` (`str`): Context for the question.
- `question` (`str`): Question.
- `answers` (`dict`): Answers with the following keys:
  - `text` (`list` of `str`): Texts of the answers.
  - `answer_start` (`list` of `int`): Start positions for every answer text.

### Data Splits

The number of questions and candidate sentences for each language for XQuAD-R is shown in the table below:

|     | XQuAD-R   |            |
|-----|-----------|------------|
|     | questions | candidates |
| ar |      1190 |       1222 |
| de |      1190 |       1276 |
| el |      1190 |       1234 |
| en |      1190 |       1180 |
| es |      1190 |       1215 |
| hi |      1190 |       1244 |
| ru |      1190 |       1219 |
| th |      1190 |        852 |
| tr |      1190 |       1167 |
| vi |      1190 |       1209 |
| zh |      1190 |       1196 |

## Dataset Creation

[More Information Needed]

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

[More Information Needed]

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

[More Information Needed]

### Dataset Curators

The dataset was initially created by Uma Roy, Noah Constant, Rami Al-Rfou, Aditya Barua, Aaron Phillips and Yinfei Yang, during work done at Google Research.

### Licensing Information

XQuAD-R is distributed under the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/legalcode).

### Citation Information

```
@article{roy2020lareqa,
  title={LAReQA: Language-agnostic answer retrieval from a multilingual pool},
  author={Roy, Uma and Constant, Noah and Al-Rfou, Rami and Barua, Aditya and Phillips, Aaron and Yang, Yinfei},
  journal={arXiv preprint arXiv:2004.05484},
  year={2020}
}
```

### Contributions

Thanks to [@manandey](https://github.com/manandey) for adding this dataset.
