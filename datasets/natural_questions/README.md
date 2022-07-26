---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-sa-3.0
multilinguality:
- monolingual
pretty_name: Natural Questions
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: natural-questions
---

# Dataset Card for Natural Questions

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

- **Homepage:** [https://ai.google.com/research/NaturalQuestions/dataset](https://ai.google.com/research/NaturalQuestions/dataset)
- **Repository:** [https://github.com/google-research-datasets/natural-questions](https://github.com/google-research-datasets/natural-questions)
- **Paper:** [https://research.google/pubs/pub47761/](https://research.google/pubs/pub47761/)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 42981.34 MB
- **Size of the generated dataset:** 95175.86 MB
- **Total amount of disk used:** 138157.19 MB

### Dataset Summary

The NQ corpus contains questions from real users, and it requires QA systems to
read and comprehend an entire Wikipedia article that may or may not contain the
answer to the question. The inclusion of real user questions, and the
requirement that solutions should read an entire page to find the answer, cause
NQ to be a more realistic and challenging task than prior QA datasets.

### Supported Tasks and Leaderboards

[https://ai.google.com/research/NaturalQuestions](https://ai.google.com/research/NaturalQuestions)

### Languages

en

## Dataset Structure

### Data Instances

- **Size of downloaded dataset files:** 42981.34 MB
- **Size of the generated dataset:** 95175.86 MB
- **Total amount of disk used:** 138157.19 MB

An example of 'train' looks as follows. This is a toy example.
```
{
  "id": "797803103760793766",
  "document": {
    "title": "Google",
    "url": "http://www.wikipedia.org/Google",
    "html": "<html><body><h1>Google Inc.</h1><p>Google was founded in 1998 By:<ul><li>Larry</li><li>Sergey</li></ul></p></body></html>",
    "tokens":[
      {"token": "<h1>", "start_byte": 12, "end_byte": 16, "is_html": True},
      {"token": "Google", "start_byte": 16, "end_byte": 22, "is_html": False},
      {"token": "inc", "start_byte": 23, "end_byte": 26, "is_html": False},
      {"token": ".", "start_byte": 26, "end_byte": 27, "is_html": False},
      {"token": "</h1>", "start_byte": 27, "end_byte": 32, "is_html": True},
      {"token": "<p>", "start_byte": 32, "end_byte": 35, "is_html": True},
      {"token": "Google", "start_byte": 35, "end_byte": 41, "is_html": False},
      {"token": "was", "start_byte": 42, "end_byte": 45, "is_html": False},
      {"token": "founded", "start_byte": 46, "end_byte": 53, "is_html": False},
      {"token": "in", "start_byte": 54, "end_byte": 56, "is_html": False},
      {"token": "1998", "start_byte": 57, "end_byte": 61, "is_html": False},
      {"token": "by", "start_byte": 62, "end_byte": 64, "is_html": False},
      {"token": ":", "start_byte": 64, "end_byte": 65, "is_html": False},
      {"token": "<ul>", "start_byte": 65, "end_byte": 69, "is_html": True},
      {"token": "<li>", "start_byte": 69, "end_byte": 73, "is_html": True},
      {"token": "Larry", "start_byte": 73, "end_byte": 78, "is_html": False},
      {"token": "</li>", "start_byte": 78, "end_byte": 83, "is_html": True},
      {"token": "<li>", "start_byte": 83, "end_byte": 87, "is_html": True},
      {"token": "Sergey", "start_byte": 87, "end_byte": 92, "is_html": False},
      {"token": "</li>", "start_byte": 92, "end_byte": 97, "is_html": True},
      {"token": "</ul>", "start_byte": 97, "end_byte": 102, "is_html": True},
      {"token": "</p>", "start_byte": 102, "end_byte": 106, "is_html": True}
    ],
  },
  "question" :{
    "text": "who founded google",
    "tokens": ["who", "founded", "google"]
  },
  "long_answer_candidates": [
    {"start_byte": 32, "end_byte": 106, "start_token": 5, "end_token": 22, "top_level": True},
    {"start_byte": 65, "end_byte": 102, "start_token": 13, "end_token": 21, "top_level": False},
    {"start_byte": 69, "end_byte": 83, "start_token": 14, "end_token": 17, "top_level": False},
    {"start_byte": 83, "end_byte": 92, "start_token": 17, "end_token": 20 , "top_level": False}
  ],
  "annotations": [{
    "id": "6782080525527814293",
    "long_answer": {"start_byte": 32, "end_byte": 106, "start_token": 5, "end_token": 22, "candidate_index": 0},
    "short_answers": [
      {"start_byte": 73, "end_byte": 78, "start_token": 15, "end_token": 16, "text": "Larry"},
      {"start_byte": 87, "end_byte": 92, "start_token": 18, "end_token": 19, "text": "Sergey"}
    ],
    "yes_no_answer": -1
  }]
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `id`: a `string` feature.
- `document` a dictionary feature containing:
  - `title`: a `string` feature.
  - `url`: a `string` feature.
  - `html`: a `string` feature.
  - `tokens`: a dictionary feature containing:
    - `token`: a `string` feature.
    - `is_html`: a `bool` feature.
    - `start_byte`: a `int64` feature.
    - `end_byte`: a `int64` feature.
- `question`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `tokens`: a `list` of `string` features.
- `long_answer_candidates`: a dictionary feature containing:
  - `start_token`: a `int64` feature.
  - `end_token`: a `int64` feature.
  - `start_byte`: a `int64` feature.
  - `end_byte`: a `int64` feature.
  - `top_level`: a `bool` feature.
- `annotations`: a dictionary feature containing:
  - `id`: a `string` feature.
  - `long_answers`: a dictionary feature containing:
    - `start_token`: a `int64` feature.
    - `end_token`: a `int64` feature.
    - `start_byte`: a `int64` feature.
    - `end_byte`: a `int64` feature.
    - `candidate_index`: a `int64` feature.
  - `short_answers`: a dictionary feature containing:
    - `start_token`: a `int64` feature.
    - `end_token`: a `int64` feature.
    - `start_byte`: a `int64` feature.
    - `end_byte`: a `int64` feature.
    - `text`: a `string` feature.
  - `yes_no_answer`: a classification label, with possible values including `NO` (0), `YES` (1).

### Data Splits

| name    |  train | validation |
|---------|-------:|-----------:|
| default | 307373 |       7830 |
| dev     |    N/A |       7830 |

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

[Creative Commons Attribution-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/).

### Citation Information

```

@article{47761,
title	= {Natural Questions: a Benchmark for Question Answering Research},
author	= {Tom Kwiatkowski and Jennimaria Palomaki and Olivia Redfield and Michael Collins and Ankur Parikh and Chris Alberti and Danielle Epstein and Illia Polosukhin and Matthew Kelcey and Jacob Devlin and Kenton Lee and Kristina N. Toutanova and Llion Jones and Ming-Wei Chang and Andrew Dai and Jakob Uszkoreit and Quoc Le and Slav Petrov},
year	= {2019},
journal	= {Transactions of the Association of Computational Linguistics}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
