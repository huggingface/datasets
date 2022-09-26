---
annotations_creators:
- crowdsourced
language:
- en
language_creators:
- found
license:
- other
multilinguality:
- monolingual
pretty_name: "CoQA: Conversational Question Answering Challenge"
size_categories:
- 1K<n<10K
source_datasets:
- extended|race
- extended|cnn_dailymail
- extended|wikipedia
- extended|other
task_categories:
- question-answering
task_ids:
- extractive-qa
- question-answering-other-conversational-qa
paperswithcode_id: coqa
---

# Dataset Card for "coqa"

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

- **Homepage:** [https://stanfordnlp.github.io/coqa/](https://stanfordnlp.github.io/coqa/)
- **Repository:** https://github.com/stanfordnlp/coqa-baselines
- **Paper:** [CoQA: A Conversational Question Answering Challenge](https://arxiv.org/abs/1808.07042)
- **Point of Contact:** [Google Group](https://groups.google.com/forum/#!forum/coqa), [Siva Reddy](mailto:siva.reddy@mila.quebec), [Danqi Chen](mailto:danqic@cs.princeton.edu)
- **Size of downloaded dataset files:** 55.40 MB
- **Size of the generated dataset:** 18.35 MB
- **Total amount of disk used:** 73.75 MB

### Dataset Summary

CoQA is a large-scale dataset for building Conversational Question Answering systems.

Our dataset contains 127k questions with answers, obtained from 8k conversations about text passages from seven diverse domains. The questions are conversational, and the answers are free-form text with their corresponding evidence highlighted in the passage.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 55.40 MB
- **Size of the generated dataset:** 18.35 MB
- **Total amount of disk used:** 73.75 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answers": "{\"answer_end\": [179, 494, 511, 545, 879, 1127, 1128, 94, 150, 412, 1009, 1046, 643, -1, 764, 724, 125, 1384, 881, 910], \"answer_...",
    "questions": "[\"When was the Vat formally opened?\", \"what is the library for?\", \"for what subjects?\", \"and?\", \"what was started in 2014?\", \"ho...",
    "source": "wikipedia",
    "story": "\"The Vatican Apostolic Library (), more commonly called the Vatican Library or simply the Vat, is the library of the Holy See, l..."
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `source`: a `string` feature.
- `story`: a `string` feature.
- `questions`: a `list` of `string` features.
- `answers`: a dictionary feature containing:
  - `input_text`: a `string` feature.
  - `answer_start`: a `int32` feature.
  - `answer_end`: a `int32` feature.

### Data Splits

| name  |train|validation|
|-------|----:|---------:|
|default| 7199|       500|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

CoQA contains passages from seven domains. We make five of these public under the following licenses:
- Literature and Wikipedia passages are shared under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
- Children's stories are collected from [MCTest](https://www.microsoft.com/en-us/research/publication/mctest-challenge-dataset-open-domain-machine-comprehension-text/) which comes with [MSR-LA](https://github.com/mcobzarenco/mctest/blob/master/data/MCTest/LICENSE.pdf) license.
- Middle/High school exam passages are collected from [RACE](https://arxiv.org/abs/1704.04683) which comes with its [own](http://www.cs.cmu.edu/~glai1/data/race/) license.
- News passages are collected from the [DeepMind CNN dataset](https://arxiv.org/abs/1506.03340) which comes with [Apache](https://github.com/deepmind/rc-data/blob/master/LICENSE) license. 

### Citation Information

```
@article{reddy-etal-2019-coqa,
    title = "{C}o{QA}: A Conversational Question Answering Challenge",
    author = "Reddy, Siva  and
      Chen, Danqi  and
      Manning, Christopher D.",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "7",
    year = "2019",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/Q19-1016",
    doi = "10.1162/tacl_a_00266",
    pages = "249--266",
}
```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@ojasaar](https://github.com/ojasaar), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
