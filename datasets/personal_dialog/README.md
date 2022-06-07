---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- zh
licenses:
- other-weibo
multilinguality:
- monolingual
paperswithcode_id: personaldialog
pretty_name: "PersonalDialog"
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- conversational
task_ids:
- dialogue-generation
---

# Dataset Card for PersonalDialog

## Table of Contents
- [Dataset Card for PersonalDialog](#dataset-card-for-personaldialog)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://www.zhengyinhe.com/datasets/
- **Repository:** https://github.com/silverriver/PersonalDilaog
- **Paper:** https://arxiv.org/abs/1901.09672

### Dataset Summary

The PersonalDialog dataset is a large-scale multi-turn Chinese dialogue dataset containing various traits from a large number of speakers.
We are releasing about 5M sessions of carefully filtered dialogues.
Each utterance in PersonalDialog is associated with a speaker marked with traits like Gender, Location, Interest Tags.

### Supported Tasks and Leaderboards

- dialogue-generation: The dataset can be used to train a model for generating dialogue responses.
- response-retrieval: The dataset can be used to train a reranker model that can be used to implement a retrieval-based dialogue model.

### Languages

PersonalDialog is in Chinese

PersonalDialog中的对话是中文的

## Dataset Structure

### Data Instances

`train` split:

```json
{
  "dialog": ["那么 晚", "加班 了 刚 到 家 呀 ！", "吃饭 了 么", "吃 过 了 ！"], 
  "profile": [
    { 
      "tag": ["间歇性神经病", "爱笑的疯子", "他们说我犀利", "爱做梦", "自由", "旅游", "学生", "双子座", "好性格"], 
      "loc": "福建 厦门", "gender": "male"
    }, {
      "tag": ["设计师", "健康养生", "热爱生活", "善良", "宅", "音樂", "时尚"], 
      "loc": "山东 济南", "gender": "male"
      }
  ], 
  "uid": [0, 1, 0, 1],
}
```

`dev` and `test` split:

```json
{
  "dialog": ["没 人性 啊 ！", "可以 来 组织 啊", "来 上海 陪姐 打 ？"], 
  "profile": [
    {"tag": [""], "loc": "上海 浦东新区", "gender": "female"}, 
    {"tag": ["嘉庚", "keele", "leicester", "UK", "泉州五中"], "loc": "福建 泉州", "gender": "male"},
  ], 
  "uid": [0, 1, 0],
  "responder_profile": {"tag": ["嘉庚", "keele", "leicester", "UK", "泉州五中"], "loc": "福建 泉州", "gender": "male"}, 
  "golden_response": "吴经理 派车来 小 泉州 接 么 ？", 
  "is_biased": true,
}
```

### Data Fields

- `dialog` (list of strings): List of utterances consisting of a dialogue.
- `profile` (list of dicts): List of profiles associated with each speaker.
- `tag` (list of strings): List of tags associated with each speaker.
- `loc` (string): Location of each speaker.
- `gender` (string): Gender of each speaker.
- `uid` (list of int): Speaker id for each utterance in the dialogue.
- `responder_profile` (dict): Profile of the responder. (Only available in `dev` and `test` split)
- `golden_response` (str): Response of the responder. (Only available in `dev` and `test` split)
- `id_biased` (bool): Whether the dialogue is guranteed to be persona related or not. (Only available in `dev` and `test` split)

### Data Splits


|train|valid|test|
|---:|---:|---:|
|5,438,165 | 10,521 | 10,523 |


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

other-weibo

This dataset is collected from Weibo.
You can refer to the [detailed policy](https://weibo.com/signup/v5/privacy) required to use this dataset.
Please restrict the usage of this dataset to non-commerical purposes.

### Citation Information

```bibtex
@article{zheng2019personalized,
  title   = {Personalized dialogue generation with diversified traits},
  author  = {Zheng, Yinhe and Chen, Guanyi and Huang, Minlie and Liu, Song and Zhu, Xuan},
  journal = {arXiv preprint arXiv:1901.09672},
  year    = {2019}
}

@inproceedings{zheng2020pre,
  title     = {A pre-training based personalized dialogue generation model with persona-sparse data},
  author    = {Zheng, Yinhe and Zhang, Rongsheng and Huang, Minlie and Mao, Xiaoxi},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {34},
  number    = {05},
  pages     = {9693--9700},
  year      = {2020}
}
```

### Contributions

Thanks to [Yinhe Zheng](https://github.com/silverriver) for adding this dataset.
