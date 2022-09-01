---
language:
- en
paperswithcode_id: doqa
pretty_name: DoQA
---

# Dataset Card for "doqa"

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

- **Homepage:** [https://github.com/RevanthRameshkumar/CRD3](https://github.com/RevanthRameshkumar/CRD3)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 12.01 MB
- **Size of the generated dataset:** 16.88 MB
- **Total amount of disk used:** 28.88 MB

### Dataset Summary

DoQA is a dataset for accessing Domain Specific FAQs via conversational QA that contains 2,437 information-seeking question/answer dialogues
(10,917 questions in total) on three different domains: cooking, travel and movies. Note that we include in the generic concept of FAQs also
Community Question Answering sites, as well as corporate information in intranets which is maintained in textual form similar to FAQs, often
referred to as internal “knowledge bases”.

These dialogues are created by crowd workers that play the following two roles: the user who asks questions about a given topic posted in Stack
Exchange (https://stackexchange.com/), and the domain expert who replies to the questions by selecting a short span of text from the long textual
reply in the original post. The expert can rephrase the selected span, in order to make it look more natural. The dataset covers unanswerable
questions and some relevant dialogue acts.

DoQA enables the development and evaluation of conversational QA systems that help users access the knowledge buried in domain specific FAQs.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### cooking

- **Size of downloaded dataset files:** 4.00 MB
- **Size of the generated dataset:** 10.79 MB
- **Total amount of disk used:** 14.79 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [852],
        "text": ["CANNOTANSWER"]
    },
    "background": "\"So, over mixing batter forms gluten, which in turn hardens the cake. Fine.The problem is that I don't want lumps in the cakes, ...",
    "context": "\"Milk won't help you - it's mostly water, and gluten develops from flour (more accurately, specific proteins in flour) and water...",
    "followup": "n",
    "id": "C_64ce44d5f14347f488eb04b50387f022_q#2",
    "orig_answer": {
        "answer_start": [852],
        "text": ["CANNOTANSWER"]
    },
    "question": "Ok. What can I add to make it more softer and avoid hardening?",
    "title": "What to add to the batter of the cake to avoid hardening when the gluten formation can't be avoided?",
    "yesno": "x"
}
```

#### movies

- **Size of downloaded dataset files:** 4.00 MB
- **Size of the generated dataset:** 3.02 MB
- **Total amount of disk used:** 7.02 MB

An example of 'test' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [852],
        "text": ["CANNOTANSWER"]
    },
    "background": "\"So, over mixing batter forms gluten, which in turn hardens the cake. Fine.The problem is that I don't want lumps in the cakes, ...",
    "context": "\"Milk won't help you - it's mostly water, and gluten develops from flour (more accurately, specific proteins in flour) and water...",
    "followup": "n",
    "id": "C_64ce44d5f14347f488eb04b50387f022_q#2",
    "orig_answer": {
        "answer_start": [852],
        "text": ["CANNOTANSWER"]
    },
    "question": "Ok. What can I add to make it more softer and avoid hardening?",
    "title": "What to add to the batter of the cake to avoid hardening when the gluten formation can't be avoided?",
    "yesno": "x"
}
```

#### travel

- **Size of downloaded dataset files:** 4.00 MB
- **Size of the generated dataset:** 3.07 MB
- **Total amount of disk used:** 7.07 MB

An example of 'test' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [852],
        "text": ["CANNOTANSWER"]
    },
    "background": "\"So, over mixing batter forms gluten, which in turn hardens the cake. Fine.The problem is that I don't want lumps in the cakes, ...",
    "context": "\"Milk won't help you - it's mostly water, and gluten develops from flour (more accurately, specific proteins in flour) and water...",
    "followup": "n",
    "id": "C_64ce44d5f14347f488eb04b50387f022_q#2",
    "orig_answer": {
        "answer_start": [852],
        "text": ["CANNOTANSWER"]
    },
    "question": "Ok. What can I add to make it more softer and avoid hardening?",
    "title": "What to add to the batter of the cake to avoid hardening when the gluten formation can't be avoided?",
    "yesno": "x"
}
```

### Data Fields

The data fields are the same among all splits.

#### cooking
- `title`: a `string` feature.
- `background`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `id`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.
- `followup`: a `string` feature.
- `yesno`: a `string` feature.
- `orig_answer`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### movies
- `title`: a `string` feature.
- `background`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `id`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.
- `followup`: a `string` feature.
- `yesno`: a `string` feature.
- `orig_answer`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

#### travel
- `title`: a `string` feature.
- `background`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `id`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.
- `followup`: a `string` feature.
- `yesno`: a `string` feature.
- `orig_answer`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

### Data Splits

#### cooking

|       |train|validation|test|
|-------|----:|---------:|---:|
|cooking| 4612|       911|1797|

#### movies

|      |test|
|------|---:|
|movies|1884|

#### travel

|      |test|
|------|---:|
|travel|1713|

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

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```

@misc{campos2020doqa,
    title={DoQA -- Accessing Domain-Specific FAQs via Conversational QA},
    author={Jon Ander Campos and Arantxa Otegi and Aitor Soroa and Jan Deriu and Mark Cieliebak and Eneko Agirre},
    year={2020},
    eprint={2005.01328},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```


### Contributions

Thanks to [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
