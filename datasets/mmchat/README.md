---
annotations_creators:
- other
language_creators:
- other
languages:
- zh
licenses:
- mit
multilinguality:
- monolingual
paperswithcode_id: mmchat-multi-modal-chat-dataset-on-social
pretty_name: "MMChat: Multi-Modal Chat Dataset on Social Media"
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- conversational
task_ids:
- dialogue-generation
---

# Dataset Card for MMChat

## Table of Contents
- [Dataset Card for MMChat](#dataset-card-for-mmchat)
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
- **Repository:** https://github.com/silverriver/MMChat
- **Paper:** https://arxiv.org/abs/2108.07154

### Dataset Summary

MMChat is a large-scale dialogue dataset that contains image-grounded dialogues in Chinese. Each dialogue in MMChat is associated with one or more images (maximum 9 images per dialogue). We design various strategies to ensure the quality of the dialogues in MMChat.

MMChat comes with 4 different versions: 

- `mmchat`: The MMChat dataset used in our paper.
- `mmchat_hf`: Contains human annotation on 100K sessions of dialogues. 
- `mmchat_raw`: Raw dialogues used to construct MMChat.
  `mmchat_lccc_filtered`: Raw dialogues filtered using the LCCC dataset.

If you what to use high quality multi-modal dialogues that are closed related to the given images, I suggest you to use the `mmchat_hf` version.
If you only care about the quality of dialogue texts, I suggest you to use the `mmchat_lccc_filtered` version.

### Supported Tasks and Leaderboards

- dialogue-generation: The dataset can be used to train a model for generating dialogue responses.
- response-retrieval: The dataset can be used to train a reranker model that can be used to implement a retrieval-based dialogue model.

### Languages

MMChat is in Chinese

MMChat中的对话是中文的

## Dataset Structure

### Data Instances

Several versions of MMChat are available. For `mmchat`, `mmchat_raw`, `mmchat_lccc_filtered`, the following instance applies:

```json
{
  "dialog": ["你只拍出了你十分之一的美", "你的头像竟然换了，奥"],
  "weibo_content": "分享图片",
  "imgs": ["https://wx4.sinaimg.cn/mw2048/d716a6e2ly1fmug2w2l9qj21o02yox6p.jpg"]
}
```

For `mmchat_hf`, the following instance applies:

```json
{
  "dialog": ["白百合", "啊？", "有点像", "还好吧哈哈哈牙像", "有男盆友没呢", "还没", "和你说话呢。没回我"],
  "weibo_content": "补一张昨天礼仪的照片",
  "imgs": ["https://ww2.sinaimg.cn/mw2048/005Co9wdjw1eyoz7ib9n5j307w0bu3z5.jpg"],
  "labels": {
    "image_qualified": true, 
    "dialog_qualified": true, 
    "dialog_image_related": true
  }
}
```

### Data Fields

- `dialog` (list of strings): List of utterances consisting of a dialogue.
- `weibo_content` (string): Weibo content of the dialogue.
- `imgs` (list of strings): List of URLs of images.
- `labels` (dict): Human-annotated labels of the dialogue.
- `image_qualified` (bool): Whether the image is of high quality.
- `dialog_qualified` (bool): Whether the dialogue is of high quality.
- `dialog_image_related` (bool): Whether the dialogue is related to the image.

### Data Splits

For `mmchat`, we provide the following splits:

|train|valid|test|
|---:|---:|---:|
|115,842 | 4,000 | 1,000 |

For other versions, we do not provide the offical split.
More stastics are listed here:

| `mmchat`                   | Count   |
|--------------------------------------|--------:|
| Sessions                             | 120.84 K |
| Sessions with more than 4 utterances |  17.32 K |
| Utterances                           | 314.13 K |
| Images                               |  198.82 K |
| Avg. utterance per session           |  2.599 |
| Avg. image per session               |  2.791 |
| Avg. character per utterance         |  8.521 |

| `mmchat_hf`                     | Count   |
|--------------------------------------|--------:|
| Sessions                             | 19.90 K |
| Sessions with more than 4 utterances | 8.91 K |
| Totally annotated sessions           | 100.01 K |
| Utterances                           | 81.06 K |
| Images                               | 52.66K |
| Avg. utterance per session           | 4.07 |
| Avg. image per session               | 2.70 |
| Avg. character per utterance         | 11.93 |

| `mmchat_raw`                     | Count    |
|--------------------------------------|---------:|
| Sessions                             | 4.257 M  |
| Sessions with more than 4 utterances | 2.304 M  |
| Utterances                           | 18.590 M |
| Images                               | 4.874 M  |
| Avg. utterance per session           | 4.367    |
| Avg. image per session               | 1.670    |
| Avg. character per utterance         | 14.104   |

| `mmchat_lccc_filtered`                     | Count   |
|--------------------------------------|--------:|
| Sessions                             | 492.6 K |
| Sessions with more than 4 utterances | 208.8 K |
| Utterances                           | 1.986 M |
| Images                               | 1.066 M |
| Avg. utterance per session           | 4.031   |
| Avg. image per session               | 2.514   |
| Avg. character per utterance         | 11.336  |

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

Copyright (c) 2020 silver

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

```
@inproceedings{zheng2022MMChat,
  author    = {Zheng, Yinhe and Chen, Guanyi and Liu, Xin and Sun, Jian},
  title     = {MMChat: Multi-Modal Chat Dataset on Social Media},
  booktitle = {Proceedings of The 13th Language Resources and Evaluation Conference},
  year      = {2022},
  publisher = {European Language Resources Association},
}

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
