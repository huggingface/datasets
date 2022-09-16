---
annotations_creators:
- other
language_creators:
- other
language:
- zh
license:
- mit
multilinguality:
- monolingual
paperswithcode_id: lccc
pretty_name: "LCCC: Large-scale Cleaned Chinese Conversation corpus"
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- conversational
task_ids:
- dialogue-generation
---

# Dataset Card for LCCC

## Table of Contents
- [Dataset Card for LCCC](#dataset-card-for-lccc)
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

- **Repository:** https://github.com/thu-coai/CDial-GPT
- **Paper:** https://arxiv.org/abs/2008.03946

### Dataset Summary

LCCC: Large-scale Cleaned Chinese Conversation corpus (LCCC) is a large Chinese dialogue corpus originate from Chinese social medias. A rigorous data cleaning pipeline is designed to ensure the quality of the corpus. This pipeline involves a set of rules and several classifier-based filters. Noises such as offensive or sensitive words, special symbols, emojis, grammatically incorrect sentences, and incoherent conversations are filtered.

LCCC是一套来自于中文社交媒体的对话数据，我们设计了一套严格的数据过滤流程来确保该数据集中对话数据的质量。 这一数据过滤流程中包括一系列手工规则以及若干基于机器学习算法所构建的分类器。 我们所过滤掉的噪声包括：脏字脏词、特殊字符、颜表情、语法不通的语句、上下文不相关的对话等。

### Supported Tasks and Leaderboards

- dialogue-generation: The dataset can be used to train a model for generating dialogue responses.
- response-retrieval: The dataset can be used to train a reranker model that can be used to implement a retrieval-based dialogue model.

### Languages

LCCC is in Chinese

LCCC中的对话是中文的

## Dataset Structure

### Data Instances

```json
{
    "dialog": ["火锅 我 在 重庆 成都 吃 了 七八 顿 火锅", "哈哈哈哈 ！ 那 我 的 嘴巴 可能 要 烂掉 ！", "不会 的 就是 好 油腻"]
}
```

### Data Fields

- `dialog` (list of strings): List of utterances consisting of a dialogue.

### Data Splits

We do not provide the offical split for LCCC-large.
But we provide a split for LCCC-base:

|train|valid|test|
|---:|---:|---:|
|6,820,506 | 20,000 | 10,000|

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

MIT License

Copyright (c) 2020 lemon234071

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Citation Information

```bibtex
@inproceedings{wang2020chinese,
  title={A Large-Scale Chinese Short-Text Conversation Dataset},
  author={Wang, Yida and Ke, Pei and Zheng, Yinhe and Huang, Kaili and Jiang, Yong and Zhu, Xiaoyan and Huang, Minlie},
  booktitle={NLPCC},
  year={2020},
  url={https://arxiv.org/abs/2008.03946}
}
```

### Contributions

Thanks to [Yinhe Zheng](https://github.com/silverriver) for adding this dataset.
