---
annotations_creators:
- found
language_creators:
- found
languages:
- zh
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: liveqa
---

# Dataset Card for LiveQA

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

- **Homepage:** [Github](https://github.com/PKU-TANGENT/LiveQA)
- **Repository:** [Github](https://github.com/PKU-TANGENT/LiveQA)
- **Paper:** [Liu et al., 2020](https://www.aclweb.org/anthology/2020.ccl-1.98.pdf)
- **Leaderboard:** N/A
- **Point of Contact:** Qianying Liu

### Dataset Summary
The LiveQA dataset is a Chinese question-answering resource constructed from playby-play live broadcasts. It contains 117k multiple-choice questions written by human commentators for over 1,670 NBA games, which are collected from the Chinese Hupu website.

### Supported Tasks and Leaderboards
Question Answering. 

[More Information Needed]

### Languages
Chinese. 

## Dataset Structure

### Data Instances
Each instance represents a timeline (i.e., a game) with an identifier. The passages field comprise an array of text or question segments. In the following truncated example, user comments about the game is followed by a question about which team will be the first to reach 60 points. 
```python
{
  
    'id': 1,
    'passages': [
      {
        "is_question": False,
        "text": "'我希望两位球员都能做到！！",
        "candidate1": "",
        "candidate2": "",
        "answer": "",
      },
      {
        "is_question": False,
        "text": "新年给我们送上精彩比赛！",
        "candidate1": "",
        "candidate2": "",
        "answer": "",
      },
      {
        "is_question": True,
        "text": "先达到60分？",
        "candidate1": "火箭",
        "candidate2": "勇士",
        "answer": "勇士",
      },
      {
        "is_question": False,
        "text": "自己急停跳投！！！",
        "candidate1": "",
        "candidate2": "",
        "answer": "",
      }
    ]
}
```

### Data Fields
- id: identifier for the game
- passages: collection of text/question segments
- text: real-time text comment or binary question related to the context
- candidate1/2: one of the two answer options to the question
- answer: correct answer to the question in text

### Data Splits
There is no predefined split in this dataset. 

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

[More Information Needed]

### Citation Information
This resource is developed by [Liu et al., 2020](https://www.aclweb.org/anthology/2020.ccl-1.98.pdf).
```
@inproceedings{qianying-etal-2020-liveqa,
    title = "{L}ive{QA}: A Question Answering Dataset over Sports Live",
    author = "Qianying, Liu  and
      Sicong, Jiang  and
      Yizhong, Wang  and
      Sujian, Li",
    booktitle = "Proceedings of the 19th Chinese National Conference on Computational Linguistics",
    month = oct,
    year = "2020",
    address = "Haikou, China",
    publisher = "Chinese Information Processing Society of China",
    url = "https://www.aclweb.org/anthology/2020.ccl-1.98",
    pages = "1057--1067"
}
```

### Contributions

Thanks to [@j-chim](https://github.com/j-chim) for adding this dataset.