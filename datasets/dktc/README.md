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
- text-classification
task_ids:
- multi-label-classification
pretty_name: Dataset of Korean Threatening Conversations
---

# Dataset Card for Dataset of Korean Threatening Conversations

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

- **Homepage:** 
- **Repository:** [GitHub](https://github.com/tunib-ai/DKTC)
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

It is a Korean dataset that classifies threatening conversation data into four threat situations.  

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Korean

## Dataset Structure

### Data Instances

Here is an example from the dataset:
```
{'class': 0,
'text': '이 약이 뭔 거 같아? \n뭔데요.?\n뭐긴 뭐야 네 엄마 저승길 보내주는 약이지.\n네? 그게 무슨.\n네 엄마 지금 저 빌딩에 있지? 그리고 저 빌딩에선 시음회가 열리고 있고.\n그게.무슨.\n이미 인력은 다 배치해놨어. 저 음료를 마시면 네 엄마는.\n아 안 돼!!\n네 엄마 살리고 싶으면 내가 시키는 대로 해.\n멈춰요 알겠으니까 그만하라고!!\n내가 시키는 대로 해!!\n알겠다고요!!! 제발 그만'}
```

### Data Fields

The dataset has two fields:
- **class**: the classification label of the text: threat (0), extortion (1), workspace (2) or etc (3)
- **text**: text content as a string

### Data Splits

- The train spit has 3950 samples, divided into several classes:
  - threat (0): 896
  - extortion (1): 981
  - workspace (2): 979
  - etc (3): 1,094

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

CC-BY-NC-SA 4.0 License.

### Citation Information

```bibtex
@misc{DKTC
  author       = {Cho, Soyoung and Ha, Sangchun and Ryu, Myeonghyeon and
                  Keum, Bitna and Park, Kyubyong},
  title        = {DKTC, Dataset of Korean Threatening Conversations},
  howpublished = {https://github.com/tunib-ai/DKTC},
  year         = {2022},
}
```

### Contributions
Thanks to [@sooftware](https://github.com/sooftware) for adding this dataset.