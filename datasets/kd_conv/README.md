---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- crowdsourced
language:
- zh
license:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- dialogue-modeling
paperswithcode_id: kdconv
pretty_name: Knowledge-driven Conversation
dataset_info:
- config_name: travel_dialogues
  features:
  - name: messages
    sequence:
    - name: message
      dtype: string
    - name: attrs
      sequence:
      - name: attrname
        dtype: string
      - name: attrvalue
        dtype: string
      - name: name
        dtype: string
  - name: name
    dtype: string
  - name: domain
    dtype: string
  splits:
  - name: test
    num_bytes: 793883
    num_examples: 150
  - name: train
    num_bytes: 3241550
    num_examples: 1200
  - name: validation
    num_bytes: 617177
    num_examples: 150
  download_size: 11037768
  dataset_size: 4652610
- config_name: travel_knowledge_base
  features:
  - name: head_entity
    dtype: string
  - name: kb_triplets
    sequence:
      sequence: string
  - name: domain
    dtype: string
  splits:
  - name: train
    num_bytes: 1517024
    num_examples: 1154
  download_size: 11037768
  dataset_size: 1517024
- config_name: music_dialogues
  features:
  - name: messages
    sequence:
    - name: message
      dtype: string
    - name: attrs
      sequence:
      - name: attrname
        dtype: string
      - name: attrvalue
        dtype: string
      - name: name
        dtype: string
  - name: name
    dtype: string
  - name: domain
    dtype: string
  splits:
  - name: test
    num_bytes: 801012
    num_examples: 150
  - name: train
    num_bytes: 3006192
    num_examples: 1200
  - name: validation
    num_bytes: 633905
    num_examples: 150
  download_size: 11037768
  dataset_size: 4441109
- config_name: music_knowledge_base
  features:
  - name: head_entity
    dtype: string
  - name: kb_triplets
    sequence:
      sequence: string
  - name: domain
    dtype: string
  splits:
  - name: train
    num_bytes: 5980643
    num_examples: 4441
  download_size: 11037768
  dataset_size: 5980643
- config_name: film_dialogues
  features:
  - name: messages
    sequence:
    - name: message
      dtype: string
    - name: attrs
      sequence:
      - name: attrname
        dtype: string
      - name: attrvalue
        dtype: string
      - name: name
        dtype: string
  - name: name
    dtype: string
  - name: domain
    dtype: string
  splits:
  - name: test
    num_bytes: 956995
    num_examples: 150
  - name: train
    num_bytes: 4867659
    num_examples: 1200
  - name: validation
    num_bytes: 884232
    num_examples: 150
  download_size: 11037768
  dataset_size: 6708886
- config_name: film_knowledge_base
  features:
  - name: head_entity
    dtype: string
  - name: kb_triplets
    sequence:
      sequence: string
  - name: domain
    dtype: string
  splits:
  - name: train
    num_bytes: 10500882
    num_examples: 8090
  download_size: 11037768
  dataset_size: 10500882
- config_name: all_dialogues
  features:
  - name: messages
    sequence:
    - name: message
      dtype: string
    - name: attrs
      sequence:
      - name: attrname
        dtype: string
      - name: attrvalue
        dtype: string
      - name: name
        dtype: string
  - name: name
    dtype: string
  - name: domain
    dtype: string
  splits:
  - name: test
    num_bytes: 2551802
    num_examples: 450
  - name: train
    num_bytes: 11115313
    num_examples: 3600
  - name: validation
    num_bytes: 2135226
    num_examples: 450
  download_size: 11037768
  dataset_size: 15802341
- config_name: all_knowledge_base
  features:
  - name: head_entity
    dtype: string
  - name: kb_triplets
    sequence:
      sequence: string
  - name: domain
    dtype: string
  splits:
  - name: train
    num_bytes: 17998529
    num_examples: 13685
  download_size: 11037768
  dataset_size: 17998529
---

# Dataset Card for KdConv

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

- **Repository:** [Github](https://github.com/thu-coai/KdConv)
- **Paper:** [{K}d{C}onv: A {C}hinese Multi-domain Dialogue Dataset Towards Multi-turn Knowledge-driven Conversation](https://www.aclweb.org/anthology/2020.acl-main.635.pdf)

### Dataset Summary

KdConv is a Chinese multi-domain Knowledge-driven Conversionsation dataset, grounding the topics in multi-turn 
conversations to knowledge graphs. KdConv contains 4.5K conversations from three domains (film, music, and travel), 
and 86K utterances with an average turn number of 19.0. These conversations contain in-depth discussions on related 
topics and natural transition between multiple topics, while the corpus can also used for exploration of transfer 
learning and domain adaptation.

### Supported Tasks and Leaderboards

This dataset can be leveraged for dialogue modelling tasks involving multi-turn and Knowledge base setup.

### Languages

This dataset has only Chinese Language.

## Dataset Structure

### Data Instances

Each data instance is a multi-turn conversation between 2 people with annotated knowledge base data used while talking
, e.g.:
```
{
  "messages": [
    {
      "message": "对《我喜欢上你时的内心活动》这首歌有了解吗？"
    },
    {
      "attrs": [
        {
          "attrname": "Information",
          "attrvalue": "《我喜欢上你时的内心活动》是由韩寒填词，陈光荣作曲，陈绮贞演唱的歌曲，作为电影《喜欢你》的主题曲于2017年4月10日首发。2018年，该曲先后提名第37届香港电影金像奖最佳原创电影歌曲奖、第7届阿比鹿音乐奖流行单曲奖。",
          "name": "我喜欢上你时的内心活动"
        }
      ],
      "message": "有些了解，是电影《喜欢你》的主题曲。"
    },
    ...
    {
      "attrs": [
        {
          "attrname": "代表作品",
          "attrvalue": "旅行的意义",
          "name": "陈绮贞"
        },
        {
          "attrname": "代表作品",
          "attrvalue": "时间的歌",
          "name": "陈绮贞"
        }
      ],
      "message": "我还知道《旅行的意义》与《时间的歌》，都算是她的代表作。"
    },
    {
      "message": "好，有时间我找出来听听。"
    }
  ],
  "name": "我喜欢上你时的内心活动"
}
```

The corresponding entries in Knowledge base is a dictionary with list of knowledge base triplets (head entity
, relationship, tail entity), e.g.:
```
"忽然之间": [
  [
    "忽然之间",
    "Information",
    "《忽然之间》是歌手 莫文蔚演唱的歌曲，由 周耀辉， 李卓雄填词， 林健华谱曲，收录在莫文蔚1999年发行专辑《 就是莫文蔚》里。"
  ],
  [
    "忽然之间",
    "谱曲",
    "林健华"
  ]
  ...
]
``` 

### Data Fields

Conversation data fields:
- `name`: the starting topic (entity) of the conversation
- `domain`: the domain this sample belongs to. Categorical value among `{travel, film, music}`
- `messages`:  list of all the turns in the dialogue. For each turn:
    - `message`: the utterance
    - `attrs`: list of knowledge graph triplets referred by the utterance. For each triplet:
        - `name`: the head entity
        - `attrname`: the relation
        - `attrvalue`: the tail entity

Knowledge Base data fields:
- `head_entity`: the head entity
- `kb_triplets`: list of corresponding triplets
- `domain`: the domain this sample belongs to. Categorical value among `{travel, film, music}`

### Data Splits

The conversation dataset is split into a `train`, `validation`, and `test` split with the following sizes:

|        | train | validation | test |
|--------|------:|-----------:|-----:|
| travel |  1200 |       1200 | 1200 |
| film   |  1200 |        150 |  150 |
| music  |  1200 |        150 |  150 |
| all    |  3600 |        450 |  450 |

The Knowledge base dataset is having only train split with following sizes:

|        | train |
|--------|------:|
| travel |  1154 | 
| film   |  8090 | 
| music  |  4441 | 
| all    | 13685 | 

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

Apache License 2.0

### Citation Information
```
@inproceedings{zhou-etal-2020-kdconv,
    title = "{K}d{C}onv: A {C}hinese Multi-domain Dialogue Dataset Towards Multi-turn Knowledge-driven Conversation",
    author = "Zhou, Hao  and
      Zheng, Chujie  and
      Huang, Kaili  and
      Huang, Minlie  and
      Zhu, Xiaoyan",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.635",
    doi = "10.18653/v1/2020.acl-main.635",
    pages = "7098--7108",
}
```
### Contributions

Thanks to [@pacman100](https://github.com/pacman100) for adding this dataset.