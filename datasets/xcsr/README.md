---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- machine-generated
language:
- en
- zh
- de
- es
- fr
- it
- ja
- nl
- pl
- pt
- ru
- ar
- vi
- hi
- sw
- ur
license:
- mit
multilinguality:
- multilingual
pretty_name: X-CSR
size_categories:
- 1K<n<10K
source_datasets:
- extended|codah
- extended|commonsense_qa
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
---

# Dataset Card for X-CSR

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

- **Homepage:** https://inklab.usc.edu//XCSR/
- **Repository:** https://github.com/INK-USC/XCSR
- **Paper:** https://arxiv.org/abs/2106.06937
- **Leaderboard:** https://inklab.usc.edu//XCSR/leaderboard
- **Point of Contact:** https://yuchenlin.xyz/

### Dataset Summary

To evaluate multi-lingual language models (ML-LMs) for commonsense reasoning in a cross-lingual zero-shot transfer setting (X-CSR), i.e., training in English and test in other languages, we create two benchmark datasets, namely X-CSQA and X-CODAH. Specifically, we automatically translate the original CSQA and CODAH datasets, which only have English versions, to 15 other languages, forming development and test sets for studying X-CSR. As our goal is to evaluate different ML-LMs in a unified evaluation protocol for X-CSR, we argue that such translated examples, although might contain noise, can serve as a starting benchmark for us to obtain meaningful analysis, before more human-translated datasets will be available in the future.


### Supported Tasks and Leaderboards

https://inklab.usc.edu//XCSR/leaderboard

### Languages

The total 16 languages for X-CSR: {en, zh, de, es, fr, it, jap, nl, pl, pt, ru, ar, vi, hi, sw, ur}.


## Dataset Structure

### Data Instances

An example of the X-CSQA dataset:
```
{
  "id": "be1920f7ba5454ad",  # an id shared by all languages
  "lang": "en", # one of the 16 language codes.
  "question": { 
    "stem": "What will happen to your knowledge with more learning?",   # question text
    "choices": [
      {"label": "A",  "text": "headaches" },
      {"label": "B",  "text": "bigger brain" },
      {"label": "C",  "text": "education" },
      {"label": "D",  "text": "growth" },
      {"label": "E",  "text": "knowing more" }
    ] },
  "answerKey": "D"    # hidden for test data.
}
```

An example of the X-CODAH dataset:
```
{
  "id": "b8eeef4a823fcd4b",   # an id shared by all languages
  "lang": "en", # one of the 16 language codes.
  "question_tag": "o",  # one of 6 question types
  "question": {
    "stem": " ", # always a blank as a dummy question
    "choices": [
      {"label": "A",
        "text": "Jennifer loves her school very much, she plans to drop every courses."},
      {"label": "B",
        "text": "Jennifer loves her school very much, she is never absent even when she's sick."},
      {"label": "C",
        "text": "Jennifer loves her school very much, she wants to get a part-time job."},
      {"label": "D",
        "text": "Jennifer loves her school very much, she quits school happily."}
    ]
  },
  "answerKey": "B"  # hidden for test data.
}
```

### Data Fields

  - id: an id shared by all languages
  - lang: one of the 16 language codes.
  - question_tag: one of 6 question types
  - stem: always a blank as a dummy question
  - choices: a list of answers, each answer has: 
    - label: a string answer identifier for each answer
    - text: the answer text

### Data Splits

- X-CSQA: There are 8,888 examples for training in English, 1,000 for development in each language, and 1,074 examples for testing in each language.
- X-CODAH: There are 8,476 examples for training in English, 300 for development in each language, and 1,000 examples for testing in each language. 

## Dataset Creation

### Curation Rationale

To evaluate multi-lingual language models (ML-LMs) for commonsense reasoning in a cross-lingual zero-shot transfer setting (X-CSR), i.e., training in English and test in other languages, we create two benchmark datasets, namely X-CSQA and X-CODAH. 

The details of the dataset construction, especially the translation procedures, can be found in section A of the appendix of the [paper](https://inklab.usc.edu//XCSR/XCSR_paper.pdf).

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
# X-CSR
@inproceedings{lin-etal-2021-xcsr,
    title = "Common Sense Beyond English: Evaluating and Improving Multilingual Language Models for Commonsense Reasoning",
    author = "Lin, Bill Yuchen and Lee, Seyeon and Qiao, Xiaoyang and Ren, Xiang",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL-IJCNLP 2021)",
    year = "2021",
    note={to appear}
}

# CSQA
@inproceedings{Talmor2019commonsenseqaaq,
    address = {Minneapolis, Minnesota},
    author = {Talmor, Alon  and Herzig, Jonathan  and Lourie, Nicholas and Berant, Jonathan},
    booktitle = {Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)},
    doi = {10.18653/v1/N19-1421},
    pages = {4149--4158},
    publisher = {Association for Computational Linguistics},
    title = {CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge},
    url = {https://www.aclweb.org/anthology/N19-1421},
    year = {2019}
}

# CODAH
@inproceedings{Chen2019CODAHAA,
    address = {Minneapolis, USA},
    author = {Chen, Michael  and D{'}Arcy, Mike  and Liu, Alisa  and Fernandez, Jared  and Downey, Doug},
    booktitle = {Proceedings of the 3rd Workshop on Evaluating Vector Space Representations for {NLP}},
    doi = {10.18653/v1/W19-2008},
    pages = {63--69},
    publisher = {Association for Computational Linguistics},
    title = {CODAH: An Adversarially-Authored Question Answering Dataset for Common Sense},
    url = {https://www.aclweb.org/anthology/W19-2008},
    year = {2019}
}
```

### Contributions

Thanks to [Bill Yuchen Lin](https://yuchenlin.xyz/), [Seyeon Lee](https://seyeon-lee.github.io/), [Xiaoyang Qiao](https://www.linkedin.com/in/xiaoyang-qiao/), [Xiang Ren](http://www-bcf.usc.edu/~xiangren/) for adding this dataset.